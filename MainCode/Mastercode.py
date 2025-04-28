import json
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import time
from datetime import datetime, timezone, timedelta

# --- Конфигурация бота ---
bot = commands.Bot(
    command_prefix="&",
    help_command=None,
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="My creator >~<"
    ),
    intents=discord.Intents.all()
)

load_dotenv()
test_mode = False  # Режим тестирования (без реальных действий)

# --- Вспомогательные функции ---
def parse_time(time_str: str) -> int:
    """
    Конвертирует строку времени (например, '5m', '2h') в секунды.
    Поддерживаемые единицы: s (секунды), m (минуты), h (часы), d (дни).
    """
    units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }

    try:
        unit = time_str[-1]
        if unit not in units:
            return None
        amount = int(time_str[:-1])
        return amount * units[unit]
    except (ValueError, IndexError):
        return None

def load_mutes():
    """Загружает данные о мутах из JSON-файла."""
    if not os.path.exists('mutes.json'):
        return {}
    with open('mutes.json', 'r') as f:
        return json.load(f)

def save_mutes(mutes):
    """Сохраняет данные о мутах в JSON-файл."""
    with open('mutes.json', 'w') as f:
        json.dump(mutes, f, indent=4)

# --- События бота ---
@bot.event
async def on_ready():
    """Вызывается при запуске бота."""
    print("Я готова к приказам! >~<")
    mutes = load_mutes()

    # Восстановление тайм-аутов после перезапуска
    for user_id, data in mutes.items():
        guild = bot.get_guild(data["guild_id"])
        if guild is None:
            continue

        member = guild.get_member(int(user_id))
        if member is None:
            continue

        remaining = data["end_time"] - int(time.time())
        if remaining <= 0:
            try:
                await member.timeout(until=None, reason="Авторазмут после офлайна бота.")
            except Exception:
                pass
            continue

        bot.loop.create_task(unmute_later(member, remaining))

async def unmute_later(member, delay):
    """Снимает мут через указанное время."""
    await asyncio.sleep(delay)
    try:
        await member.timeout(until=None, reason="Авторазмут после окончания времени.")
    except Exception:
        pass

    mutes = load_mutes()
    mutes.pop(str(member.id), None)
    save_mutes(mutes)

# --- Обработка сообщений ---
last_response_time = None
cooldown_seconds = 13  # Задержка между ответами (в секундах)

@bot.event
async def on_message(message):
    """Обрабатывает все сообщения в чате."""
    global last_response_time

    if message.author.bot:
        return

    message_content = message.content.lower()
    now = datetime.now(timezone.utc)

    # Проверка задержки между ответами
    if last_response_time is not None:
        if (now - last_response_time).total_seconds() < cooldown_seconds:
            return

    # Ответы на вопросы о любви
    love_questions = [
        "кого ты любишь", "кто твой создатель", "кого ты считаешь важным",
        "кем ты дорожишь", "кого ты обожаешь", "кто твой любимый человек",
        "кто твой любимый", "кто твой любимый человек в этом мире",
        "с кем бы ты хотела бы провести время", "с кем бы ты хотела провести время",
        "с кем бы ты хотела", "кто для тебя важен",
    ]

    love_answers = [
        "Созданные вручную, но самые искренние чувства от и для @wattheoshi! 💖",
        "Моё сердце принадлежит моему создателю! ✨",
        "Только мой создатель, @wattheoshi, может заглядывать в меня так глубоко, как вам и не снилось! ˶˃⤙˂˶",
        "Я создана для **него**... ну и для вас тоже! 🌸",
        "Я без ума от Оши! 🎀"
    ]

    if bot.user in message.mentions:
        for question in love_questions:
            if question in message_content:
                async with message.channel.typing():
                    await asyncio.sleep(random.uniform(0.5, 2.0))
                    await message.channel.send(random.choice(love_answers))
                    last_response_time = now
                return

    # Ответы на обращения к боту
    calls = [
        "апош", "апошка", "апоша", "апошенька", "апошечка", "апошась",
        "aposh", "апошка?", "апош?", "апоши", "апошу"
    ]

    for call in calls:
        if f" {call} " in f" {message_content} ":
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(0.5, 2.0))
                responses = [
                    "Ой, ой, кто меня звал? >~<",
                    "Я тут, я тут! Что-то нужно? :3",
                    "https://tenor.com/lZuHcGbo7eh.gif",
                    "Я всегда здесь! Слежу! :eye:",
                    "Я отвлеклась! :anger:",
                    "Да-да!",
                    "Я услышала своё имя!",
                    "Может, мне показалось? :thinking:",
                    "print('Я тут!')",
                    "command = ban.user.user-said(bot.name)... Да ладно, я пошутила ))",
                ]
                await message.channel.send(random.choice(responses))
                last_response_time = now
            return

    await bot.process_commands(message)

# --- Команды взаимодействия ---
@bot.command(name="hug")
async def hug(ctx, member: discord.Member):
    """Обнимает указанного пользователя."""
    if member == ctx.author:
        await ctx.send("Оу, тебе одиноко?(")
        return
    if member == bot.user:
        await ctx.send("Ааа, меня хотят обнять! >~<")
        return
    await ctx.send(f":smile: \n{ctx.author.mention} обнимает {member.mention}!")

@bot.command(name="pat")
async def pat(ctx, member: discord.Member):
    """Гладит указанного пользователя."""
    if member == ctx.author:
        await ctx.send("Оу, тебе плохо?(")
        return
    if member == bot.user:
        await ctx.send("_мурычет_")
        return
    await ctx.send(f":heart_eyes: \n{ctx.author.mention} гладит {member.mention}!")

@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member):
    """Целует указанного пользователя (с особым ответом для создателя)."""
    special_user_id = 773282996324270141  # ID создателя

    if member == ctx.author:
        await ctx.send("Боюсь, это достаточно странно...")
        return
    if member == bot.user:
        if ctx.author.id == special_user_id:
            await ctx.send("𖦹 ´﹏` 𖦹 \n_**BLUSH!**_ \n_**KISS!**_ \n_**HUG!**_")
        else:
            await ctx.send("_**DODGE!**_ \nС тобой я уж воздержусь!")
        return
    await ctx.send(f":flushed: \n{ctx.author.mention} целует {member.mention}!")

@bot.command(name="hit")
async def hit(ctx, member: discord.Member):
    """Бьёт указанного пользователя (с особым ответом для создателя)."""
    special_user_id = 773282996324270141  # ID создателя

    if member == ctx.author:
        await ctx.send("Бедолага, пожалуйста, не надо...")
        return
    if member == bot.user:
        if ctx.author.id == special_user_id:
            await ctx.send("Дурак!! \n_**PARRY!**_ \n_**DODGE!**_ \n_**BITE!**_ \nЯ прощая тебя. Но не испытывай моё терпение!")
        else:
            await ctx.send("_**BYPASS!**_ \n_**GUARD!**_ \n_**OFFER A CUP OF TEA!**_")
        return
    await ctx.send(f":angry: \n{ctx.author.mention} бьёт {member.mention}!")

@bot.command(name="dodge")
async def dodge(ctx):
    """Уклоняется от предыдущего действия."""
    channel = ctx.channel
    async for message in channel.history(limit=5):
        if message.author != ctx.author:
            if message.content.startswith("&kiss"):
                await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уворачивается от поцелуя!")
                return
            elif message.content.startswith("&hit"):
                await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уворачивается от удара!")
                return
            elif message.content.startswith("&hug"):
                await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уворачивается от объятий!")
                return
            elif message.content.startswith("&pat"):
                await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уворачивается от поглаживания!")
                return
            elif message.content.startswith("&dodge"):
                await ctx.send("https://tenor.com/bVA8m.gif")
                return
    await ctx.send("За последнее время не от чего уклоняться...")

@bot.command(name="rape")
async def rape(ctx, member: discord.Member):
    await ctx.send(f"еблан?")
    return

# --- Модераторские команды ---
@bot.command(name="mute")
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time_str: str, *, reason: str = "Причина не указана"):
    """Выдаёт тайм-аут пользователю на указанное время."""
    try:
        seconds = parse_time(time_str)
        if seconds is None or seconds <= 0:
            await ctx.send("Некорректное время! Используй формат типа '5m', '2h', '1d'.")
            return

        mutes = load_mutes()
        end_time = int(time.time()) + seconds
        until_time = datetime.now(timezone.utc) + timedelta(seconds=seconds)

        mutes[str(member.id)] = {
            "end_time": end_time,
            "guild_id": ctx.guild.id,
            "reason": reason
        }
        save_mutes(mutes)

        if test_mode:
            await ctx.send(f"Я бы выдала {member.mention} таймаут на {time_str}. Причина: {reason}. Но я тренируюсь...")
        else:
            await member.edit(timeout=until_time, reason=reason)
            await ctx.send(f"{member.mention} отправлен в жоски мут на {time_str}! Причина: {reason}")

    except discord.Forbidden:
        await ctx.send("У подчиненной Оши не достаточно прав...")
    except discord.HTTPException:
        await ctx.send("Не получается... Блять, не получается таймаут выдать...")

@bot.command(name="clear")
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    """Удаляет указанное количество сообщений."""
    if amount < 1:
        await ctx.send("Количество сообщений должно быть больше 0.")
        return
    else:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f"Подметаю аж {amount} сообщений...")

@bot.command(name="ban")
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="Зажал"):
    """Банит указанного пользователя."""
    try:
        if test_mode:
            await ctx.send(f"Я бы забанила {member.mention} за: {reason} но тренируюсь...")
        else:
            await member.ban(reason=reason)

            embed = discord.Embed(
                title="Одним из апостолов было решено!",
                description=f"{member.mention} люто забанен и отъебанен!",
                color=discord.Color.red()
            )
            embed.add_field(name="По причине сверх уважительной", value=reason, inline=False)
            embed.set_footer(text="Апошка следит за вами, ребята...")
            await ctx.send(embed=embed)
            await ctx.send("https://tenor.com/pEAz7Zo8ljh.gif")

    except discord.Forbidden:
        await ctx.send("У подчиненной Оши не достаточно прав...")
    except discord.HTTPException:
        await ctx.send("Не получается... Да бля, не получается...")

@bot.command(name="kick")
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Зажал"):
    """Кикает указанного пользователя."""
    try:
        if test_mode:
            await ctx.send(f"Я бы изгнала {member.mention} за: {reason} но тренируюсь...")
        else:
            await member.kick(reason=reason)

            embed = discord.Embed(
                title="Одним из апостолов было решено!",
                description=f"{member.mention} отправился нахуй!",
                color=discord.Color.red()
            )
            embed.add_field(name="По причине уважительной", value=reason, inline=False)
            embed.set_footer(text="Апош следит за вами, ребята...")
            await ctx.send(embed=embed)
            await ctx.send("https://tenor.com/pEAz7Zo8ljh.gif")

    except discord.Forbidden:
        await ctx.send("У подчиненной Оши не достаточно прав...")
    except discord.HTTPException:
        await ctx.send("Не получается... Пиздец, не получается...")

# --- Команда помощи ---
@bot.command(name="help")
async def help(ctx):
    """Отправляет embed с доступными командами."""
    embed = discord.Embed(
        title="Чему я обучена?",
        description="Вот что я умею делать пока что:",
        color=discord.Color.blue()
    )
    embed.add_field(name="&Aposh", value="Просто приветствую вас!", inline=False)
    embed.add_field(name="&help", value="Вы наблюдаете результат команды!", inline=False)
    embed.add_field(name="&ban @user [причина]", value="Ух, страшный бан!", inline=False)
    embed.add_field(name="&kick @user [причина]", value="Выметаю негодяев из нашего поместья!", inline=False)
    embed.add_field(name="&clear [количество]", value="Чищу мусор и привожу канал в порядок без последних лишних сообщений!", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="Aposh")
async def Aposh(ctx):
    await ctx.send(f"Привет, **{ctx.author.display_name}**! Меня зовут **Апош**, меня прислали на помощь! \n"
                   "Если нужна помощь, просто напиши **&help** и я расскажу, что я умею! \n")

# --- Запуск бота ---
bot.run(os.getenv("BOT_TOKEN"))