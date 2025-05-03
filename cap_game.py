import discord
from discord.ext import commands, tasks
import json
import os
from datetime import timedelta

# -------------------- Configuration --------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_PATH, 'config.json')
ACTIVITY_FILE = os.path.join(DATA_PATH, 'activity_log.json')
INVENTORY_FILE = os.path.join(DATA_PATH, 'inventory_log.json')

CHECK_INTERVAL = 60 * 60         # Проверка раз в час
INACTIVITY_THRESHOLD = 48 * 3600 # 48 часов в секундах


def ensure_data_dir(path=DATA_PATH):
    os.makedirs(path, exist_ok=True)

async def load_json(path):
    ensure_data_dir(os.path.dirname(path))
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

async def save_json(path, data):
    ensure_data_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def setup(bot: commands.Bot):
    # -------------------- Events --------------------
    @bot.event
    async def on_ready():
        print(f'Бот {bot.user} готов к работе!')
        ensure_data_dir()
        if not os.path.isfile(INVENTORY_FILE):
            await save_json(INVENTORY_FILE, {})
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
        config = await load_json(CONFIG_FILE)
        for guild in bot.guilds:
            chan_id = config.get(str(guild.id), {}).get('notify_channel')
            channel = guild.get_channel(chan_id) if chan_id else guild.system_channel
            for member in guild.members:
                last_ts = activity.get(str(member.id), 0)
                if now_ts - last_ts >= INACTIVITY_THRESHOLD:
                    if channel:
                        await channel.send(f'@everyone \n{member.mention} не следит за пробками уже как 48 часов! Их могут своровать!')
                    activity[str(member.id)] = now_ts
        await save_json(ACTIVITY_FILE, activity)

    # -------------------- Commands --------------------
    @bot.command(name='setnotify')
    @commands.has_permissions(administrator=True)
    async def setnotify(ctx, channel: discord.TextChannel):
        config = await load_json(CONFIG_FILE)
        cfg = config.get(str(ctx.guild.id), {})
        cfg['notify_channel'] = channel.id
        config[str(ctx.guild.id)] = cfg
        await save_json(CONFIG_FILE, config)
        await ctx.send(f'Канал уведомлений установлен: {channel.mention}')

    @bot.command(name='acquire')
    async def acquire(ctx):
        """Выдает пользователю его стартовую пробку, если она ещё не получена."""
        # Загружаем весь инвентарь
        inventory = await load_json(INVENTORY_FILE)
        uid = str(ctx.author.id)
        # Генерируем имя пробки
        cap_name = f"Пробка @{ctx.author.name}-{ctx.author.id}"
        # Проверяем, есть ли любая пробка этого пользователя в любом инвентаре
        has_cap = any(
            any(item.endswith(f"-{ctx.author.id}") for item in items)
            for items in inventory.values()
        )
        if has_cap:
            await ctx.send(f'{ctx.author.mention}, у тебя уже есть твоя пробка!')
            return
        # Выдаём пробку
        user_items = inventory.get(uid, [])
        user_items.append(cap_name)
        inventory[uid] = user_items
        await save_json(INVENTORY_FILE, inventory)
        await ctx.send(f'{ctx.author.mention}, ты получил свою пробку: **{cap_name}**!')

        
    @bot.command(name='stash')
    async def stash(ctx, target: discord.Member = None):
        user = target or ctx.author
        inventory = await load_json(INVENTORY_FILE)
        items = inventory.get(str(user.id), [])
        embed = discord.Embed(title=f'Хранилище {user.display_name}', color=discord.Color.light_grey())
        if items:
            for itm in items:
                embed.add_field(name=itm, value=':petri_dish:', inline=False)
        else:
            embed.description = 'Тут ничего нету...'
        await ctx.send(embed=embed)

    return bot
