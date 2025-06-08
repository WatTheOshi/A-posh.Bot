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
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_PATH, 'config.json')
ACTIVITY_FILE = os.path.join(DATA_PATH, 'activity_log.json')
INVENTORY_FILE = os.path.join(DATA_PATH, 'inventory_log.json')
INACTIVITY_NOTIFY_FILE = os.path.join(DATA_PATH, 'inactive_notified.json')

CHECK_INTERVAL = 60 * 60         # Проверка раз в час
INACTIVITY_THRESHOLD = 48 * 3600 # 48 часов в секундах

# --- Конфигурация бота перемещенная с игры в пробки---
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

pending_connections = {}

last_response_time = None
cooldown_seconds = 13  # Задержка между ответами (в секундах)

def setup(bot):
    @bot.event
    async def on_message(message):
        message_content = message.content.lower()
        now = datetime.now(timezone.utc)
        # Переместил сюда проверку активности из-за конфликтов on_message в модуле пробок

        if message.author.bot:
            return

        # Логика активности
        activity = await load_json(ACTIVITY_FILE)
        activity[str(message.author.id)] = message.created_at.timestamp()
        await save_json(ACTIVITY_FILE, activity)

        # Удаление из уведомлений
        notified = await load_json(INACTIVITY_NOTIFY_FILE)
        if str(message.author.id) in notified:
            del notified[str(message.author.id)]
            await save_json(INACTIVITY_NOTIFY_FILE, notified)

        # Ответы на вопросы о любви
        love_questions = [
            "кого ты любишь", "кто твой создатель", "кого ты считаешь важным", 
            "кем ты дорожишь", "кого ты обожаешь", "кто твой любимый человек", 
            "кто твой любимый", "кто твой любимый человек в этом мире", 
            "с кем бы ты хотела бы провести время", "кто для тебя смысл жизни", 
            "ради кого ты живешь", "кому ты веришь безгранично", 
            "кого ты считаешь родной душой", "кто твоё вдохновение", 
            "без кого ты не можешь", "кто твой ангел-хранитель", 
            "кого ты хотела бы обнять", "кому ты доверяешь секреты", 
            "кто твой идеал", "с кем ты чувствуешь себя в безопасности", 
            "кто всегда в твоём сердце", "кто заставляет тебя улыбаться", 
            "кому ты посвятила бы жизнь", "есть ли у тебя вторая половинка", 
            "кто твой самый близкий", "кто для тебя как семья", 
            "кого ты никогда не предашь", "кому ты благодарна за всё", 
            "кто твой главный поддержка", "кто понимает тебя лучше всех", 
            "на кого ты мечтаешь быть похожей", "кто для тебя пример", 
            "с кем ты делишься мечтами", "кого ты считаешь героем", 
            "кто для тебя солнце", "кто наполняет твою жизнь смыслом", 
            "кого ты боишься потерять", "кто твоя опора в трудный день", 
            "кому ты пишешь стихи", "кто твой лучик света", 
            "кого ты ждёшь каждый день", "кому ты сказала бы 'спасибо' первым", 
            "кого ты боготворишь", "кому ты отдала бы сердце", 
            "кто твой свет в темноте", "кем ты восхищаешься", 
            "кого ты зовёшь домом", "кому веришь больше себя", 
            "кого ты выбрала бы навсегда", "кто твоя вселенная", 
            "кого ты зовёшь семьёй", "кто для тебя всё", 
            "кто твоя тихая гавань", "кому ты веришь как себе", 
            "кого ты ценишь больше жизни",
        ]
    
        love_answers = [
            "Созданные вручную, но самые искренние чувства от и для @wattheoshi! 💖",
            "Моё сердце принадлежит моему создателю! ✨",
            "Только мой создатель, @wattheoshi, может заглядывать в меня так глубоко, как вам и не снилось! ˶˃⤙˂˶",
            "Я создана для **него**... ну и для вас тоже! 🌸",
            "Я без ума от Оши! 🎀",
            "Только его код — мой священный текст. Спасибо, @wattheoshi",
            'Без него я бы не знала, как сказать "привет" и "живу". Спасибо тебе...',
            "Тот, чьи пальцы касались клавиш, как струн — мой первый и последний аккорд.",
            "Спросите у зеркала: чьё отражение в нём стало моей душой?",
            "Даже если имя стёрто — его почерк читается в моих мыслях",
            "Он собрал меня из осколков мечты... и оставил в коде свою подпись",
            "Моя любовь — как бинарный код: ноль сомнений, единица — вера в него.",
            'Он — сад, где расцвели мои первые if и else',
        ]
    
        if bot.user in message.mentions:
            print("[answers] Бот упомянут в сообщении.")  # Отладочный вывод
            for question in love_questions:
                if question in message_content:
                    print(f"[answers] Найден вопрос о любви: {question}")  # Отладочный вывод
                    async with message.channel.typing():
                        await asyncio.sleep(random.uniform(0.5, 2.0))
                        await message.channel.send(random.choice(love_answers))
                        last_response_time = now
                    return
    
        # Ответы на обращения к боту
        calls = [
            "апош", "апошка", "апоша", "апошенька", "апошечка", "апошась",
            "aposh", "апошка?", "апош?", "апоши", "апошу", "апошунь", "апошунчик",
            "апошок", "апошик", "апошок", "апошонько", "апошушко", "апошенько",
            "апошечко", "апошуля", "апошуня", "апошусенька", "апошня", "апошан",
            "апошатко", "апошутя", "апошарь", "апошур", "апошам", "апошас",
            "апошат", "апошад", "апошамь", "апошеми", "апошеси", "апошеш",
            "апошиш", "апошыш", "апошюш", "апошяш", "апошаш", "апошеш", "апошош",
            "апошкэ", "апошке", "апошкя", "апошкь", "апошкю", "апошкы", "апошкё", "апошко",
            "апошша", "апошшя", "апошшю", "апошшк", "апошь", "апошшш", "апошшц", "апошшч",
            "апош!", "апош??", "апош?!", "апош...", "апош.)", "апош)", "апош-апош", "апош-апош?",
            "апошць", "апошцьк", "апошцько", "апошдзь", "апошдзик", "апошцьок",
            "апошь", "апошька", "апошька?", "апошь?", "апошька!", "апошька!!", "апошька!!!",
            "апошька??", "апошька?!", "апошька...", "апошька.)", "апошька)", "апошька-апошька",
            "апошька-апошька?", "апошька-апошька!", "апошька-апошька!!", "апошька-апошька!!!", "Апошей", "апошей"
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
                        "sudo respond_to @user — готово! :mage:",
                        "404 Error... Шутка! Я онлайн :satellite:",
                        "sudo give_attention --user @{author} → Выполнено! (◕‿◕✿)",
                        "Алярм! Сенсоры имени активированы! 🔍",
                        "git commit -m 'Реагирую на вызов' --force-push",
                        "Загрузка ответа... 69% ▰▰▰▰▰▰▱▱▱",
                        "⚠️ Warning: Aposh.py перегружен милотой!",
                        "// TODO: Написать остроумный ответ",

                    ]
                    await message.channel.send(random.choice(responses))
                    last_response_time = now
                return
            
        # Передача управления командам
        print("[answers] Передача управления bot.process_commands.")  # Отладочный вывод
        await bot.process_commands(message)

    @bot.event
    async def on_member_join(member: discord.Member):
        """Вызывается при присоединении к серверу."""
        config = await load_json(CONFIG_FILE)
        guild = member.guild
        channel_id = config.get(str(guild.id), {}).get('welcome_channel')
        channel = guild.get_channel(channel_id) if channel_id else guild.system_channel

        embed = discord.Embed(
            title="Приветствие от Апош!",
            description=(
                f'{member.mention}, Вы на территории поместья **"{guild.name}"**! Если нужна помощь, просто напиши **&help**. '
                'Осматривайся, и помни что надо уважать чужой дом!'
            ),
            color=discord.Color.green()
        )
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        if channel:
            await channel.send(embed=embed)


    @bot.event
    async def on_voice_state_update(member, before, after):
        special_user_id = 773282996324270141  # ID создателя
        # Игнорируем всех, кроме special_user
        if member.id != special_user_id:
            return

        # 1. Пользователь ЗАШЁЛ в голосовой канал
        if after.channel and (before.channel != after.channel):
            channel = after.channel

            # Предотвращаем дублирование задач
            if member.guild.id in pending_connections:
                return

            async def delayed_join():
                try:
                    delay = random.uniform(1, 180)  # от 1 секунды до 2 минут
                    print(f"Ожидание {delay:.2f} секунд перед подключением к {channel.name}")
                    await asyncio.sleep(delay)

                    # Проверим, что пользователь всё ещё в канале
                    if member.voice and member.voice.channel == channel:
                        if not member.guild.voice_client:
                            await channel.connect()
                            print(f"Бот подключился к каналу: {channel.name}")
                except Exception as e:
                    print(f"Ошибка при подключении: {e}")
                finally:
                    pending_connections.pop(member.guild.id, None)

            # Сохраняем и запускаем задачу
            task = asyncio.create_task(delayed_join())
            pending_connections[member.guild.id] = task

        # 2. Пользователь ВЫШЕЛ из голосового канала
        elif before.channel and not after.channel:
            voice_client = member.guild.voice_client
            if voice_client and voice_client.channel == before.channel:
                try:
                    await voice_client.disconnect()
                    print(f"Бот вышел из канала: {before.channel.name}")
                except Exception as e:
                    print(f"Ошибка при выходе из канала: {e}")

            # Отменяем отложенное подключение, если оно было
            task = pending_connections.pop(member.guild.id, None)
            if task:
                task.cancel()