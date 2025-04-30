import discord
from discord.ext import commands, tasks
import json
import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configuration
DATA_PATH = './data'
ACTIVITY_FILE = f'{DATA_PATH}/activity_log.json'
INVENTORY_FILE = f'{DATA_PATH}/inventory_log.json'
CHECK_INTERVAL = 60 * 60  # Проверка раз в час
INACTIVITY_THRESHOLD = 48 * 3600  # 48 часов в секундах

def setup(bot):
# -------------------- Utilities --------------------
    def ensure_data_dir():
        os.makedirs(DATA_PATH, exist_ok=True)
    
    async def load_json(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    async def save_json(path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    async def get_notification_channel(guild):
        config = await load_json(CONFIG_FILE)
        chan_id = config.get(str(guild.id), {}).get('notify_channel')
        if chan_id:
            return guild.get_channel(chan_id)
        return guild.system_channel or guild.text_channels[0]
    
    async def set_notification_channel(guild, channel_id):
        config = await load_json(CONFIG_FILE)
        cfg = config.get(str(guild.id), {})
        cfg['notify_channel'] = channel_id
        config[str(guild.id)] = cfg
        await save_json(CONFIG_FILE, config)
    
    async def ensure_personal_roles():
        inventory = await load_json(INVENTORY_FILE)
        for guild in bot.guilds:
            for member in guild.members:
                if member.bot:
                    continue
                role_name = f"Пробка {member.name}"
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    role = await guild.create_role(name=role_name)
                if role not in member.roles:
                    await member.add_roles(role)
                items = inventory.get(str(member.id), [])
                if role_name not in items:
                    items.append(role_name)
                    inventory[str(member.id)] = items
        await save_json(INVENTORY_FILE, inventory)
    
    # -------------------- Events --------------------
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')
        ensure_data_dir()
        await ensure_personal_roles()
        check_inactivity.start()
    
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        activity = await load_json(ACTIVITY_FILE)
        activity[str(message.author.id)] = message.created_at.timestamp()
        await save_json(ACTIVITY_FILE, activity)
        await bot.process_commands(message)
    
    # -------------------- Background Tasks --------------------
    @tasks.loop(seconds=CHECK_INTERVAL)
    async def check_inactivity():
        activity = await load_json(ACTIVITY_FILE)
        now_ts = discord.utils.utcnow().timestamp()
        for guild in bot.guilds:
            channel = await get_notification_channel(guild)
            for member in guild.members:
                last_ts = activity.get(str(member.id), 0)
                if now_ts - last_ts >= INACTIVITY_THRESHOLD:
                    await channel.send(f'{member.mention} не активен более 48 часов! Защита снята.')
                    activity[str(member.id)] = now_ts
        await save_json(ACTIVITY_FILE, activity)
    
    # -------------------- Commands --------------------
    @bot.command(name='setnotify')
    @commands.has_permissions(administrator=True)
    async def setnotify(ctx, channel: discord.TextChannel):
        """
        Устанавливает канал для уведомлений о снятии защиты от кражи.
        Usage: &setnotify #канал
        """
        await set_notification_channel(ctx.guild, channel.id)
        await ctx.send(f'Канал для уведомлений установлен: {channel.mention}')
    
    @bot.command(name='steal')
    async def steal(ctx, target: discord.Member, *, item_name: str):
        """
        Кража предмета у неактивного пользователя.
        Usage: &steal @user "Пробка username"
        """
        # Проверяем неактивность цели
        activity = await load_json(ACTIVITY_FILE)
        last_ts = activity.get(str(target.id), 0)
        now_ts = discord.utils.utcnow().timestamp()
        if now_ts - last_ts < INACTIVITY_THRESHOLD:
            await ctx.send(f'{target.mention} ещё под защитой от кражи.')
            return
        # Проверяем наличие предмета в инвентаре
        inventory = await load_json(INVENTORY_FILE)
        target_items = inventory.get(str(target.id), [])
        if item_name not in target_items:
            await ctx.send(f'{target.mention} не имеет "{item_name}"')
            return
        # Переносим предмет
        target_items.remove(item_name)
        inventory[str(target.id)] = target_items
        user_items = inventory.get(str(ctx.author.id), [])
        user_items.append(item_name)
        inventory[str(ctx.author.id)] = user_items
        await save_json(INVENTORY_FILE, inventory)
        # Управление ролями
        role = discord.utils.get(ctx.guild.roles, name=item_name)
        if role:
            await target.remove_roles(role)
            await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.mention} успешно украл "{item_name}" у {target.mention}!')
    
    @bot.command(name='stash')
    async def stash(ctx, target: discord.Member=None):
        """
        Показывает инвентарь пользователя в виде embed.
        Usage: &stash [@user]
        """
        user = target or ctx.author
        inventory = await load_json(INVENTORY_FILE)
        items = inventory.get(str(user.id), [])
        embed = discord.Embed(title=f'Инвентарь {user.display_name}', color=discord.Color.blue())
        if items:
            for itm in items:
                embed.add_field(name=itm, value='📦', inline=False)
        else:
            embed.description = 'Пусто'
        await ctx.send(embed=embed)