import discord
from discord.ext import commands, tasks
import json
import os
from datetime import timedelta

# -------------------- Configuration --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_PATH, 'config.json')
ACTIVITY_FILE = os.path.join(DATA_PATH, 'activity_log.json')
INVENTORY_FILE = os.path.join(DATA_PATH, 'inventory_log.json')
INACTIVITY_NOTIFY_FILE = os.path.join(DATA_PATH, 'inactive_notified.json')

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

    # -------------------- Background Tasks --------------------
    @tasks.loop(seconds=CHECK_INTERVAL)
    async def check_inactivity():
        activity = await load_json(ACTIVITY_FILE)
        notified = await load_json(INACTIVITY_NOTIFY_FILE)
        config = await load_json(CONFIG_FILE)

        now_ts = discord.utils.utcnow().timestamp()

        for guild in bot.guilds:
            chan_id = config.get(str(guild.id), {}).get('notify_channel')
            channel = guild.get_channel(chan_id) if chan_id else guild.system_channel

            for member in guild.members:
                if member.bot:
                    continue
                last_ts = activity.get(str(member.id), 0)
                if now_ts - last_ts >= INACTIVITY_THRESHOLD:
                    if str(member.id) not in notified:
                        if channel:
                            await channel.send(
                                f'⚠️ {member.mention} стал уязвим для краж! Он не проявлял активности в течение 48 часов.'
                            )
                        notified[str(member.id)] = True

        await save_json(INACTIVITY_NOTIFY_FILE, notified)


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
        cap_name = f"Пробка {ctx.author.name}-{ctx.author.id}"
        # Проверяем, есть ли любая пробка этого пользователя в любом инвентаре
        has_cap = any(
            any(item.endswith(f"-{ctx.author.id}") for item in items)
            for items in inventory.values()
        )
        if has_cap:
            await ctx.send(f'{ctx.author.mention}, такая пробка есть уже!')
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


    @bot.command(name='steal')
    async def steal(ctx, target: discord.Member, *, cap_tag: str):
        """Перемещает пробку с target на автора команды по короткому тэгу"""
        inventory = await load_json(INVENTORY_FILE)
        activity = await load_json(ACTIVITY_FILE)
        
        thief_id = str(ctx.author.id)
        target_id = str(target.id)
        
        # Проверка активности жертвы
        last_active = activity.get(target_id, 0)
        now_ts = discord.utils.utcnow().timestamp()
        if now_ts - last_active < INACTIVITY_THRESHOLD:
            await ctx.send(f'{ctx.author.mention}, хранилище {target.display_name} ещё под надзором, воровать нельзя!')
            return
        
        # Проверка, что вор ещё не имеет пробку от жертвы
        if any(item.endswith(f"-{ctx.author.id}") for item in inventory.get(thief_id, [])):
            await ctx.send(f'{ctx.author.mention}, у тебя она уже есть!')
            return
        
        # Поиск пробки у жертвы
        target_items = inventory.get(target_id, [])
        full_name = None
        for item in target_items:
            if item.startswith(f"Пробка {cap_tag}-"):
                full_name = item
                break
        if not full_name:
            await ctx.send(f'{ctx.author.mention}, у пользователя {target.mention} нет такой пробки `{cap_tag}`.')
            return
        
        # Перемещение
        target_items.remove(full_name)
        inventory[target_id] = target_items
        thief_items = inventory.get(thief_id, [])
        thief_items.append(full_name)
        inventory[thief_id] = thief_items
        await save_json(INVENTORY_FILE, inventory)

        await ctx.send(f'{ctx.author.mention} успешно стырил **{full_name}** у {target.mention}!')



    return bot
