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


last_response_time = None
cooldown_seconds = 13  # Задержка между ответами (в секундах)

def setup(bot):
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
            if call in message_content.split() or f" {call} " in f" {message_content} ":
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