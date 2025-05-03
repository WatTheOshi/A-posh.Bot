import json
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import time
import humanfriendly
from datetime import datetime, timezone, timedelta
from cap_game import setup


intents = discord.Intents.default()
intents.members = True

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


# --- Модули, импорт других файлов ---
import answers
import actions
import modcom
import helpcom
import cap_game

# Передаем бота в модули
answers.setup(bot)
actions.setup(bot)
modcom.setup(bot)
helpcom.setup(bot)
cap_game.setup(bot)

load_dotenv()
test_mode = False  # Режим тестирования (без реальных действий)


# --- События бота ---
@bot.event
async def on_ready():
    """Вызывается при запуске бота."""
    print("Я готова к приказам! >~<")


# --- Запуск бота ---
bot.run(os.getenv("BOT_TOKEN"))