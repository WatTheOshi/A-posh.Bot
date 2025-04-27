import json
from datetime import datetime, timedelta
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

# Made by Oshi with love for Aposh and all people who like her

print("Текущая директория:", os.getcwd())

bot = commands.Bot(command_prefix="&", help_command=None, intents=discord.Intents.all())

load_dotenv()

test_mode = False

@bot.event
async def on_ready():
    print("Я готова к приказам! >~<")

@bot.command(name="Aposh")
async def Aposh(ctx):
    await ctx.send(f"Привет, **{ctx.author.display_name}**! Меня зовут **Апош**, меня прислали на помощь! \n"
                   "Если нужна помощь, просто напиши **&help** и я расскажу, что я умею! \n")

last_response_time = None
cooldown_seconds = 13

@bot.event
async def on_message(message):
    global last_response_time 

    if message.author.bot:
        return

    message_content = message.content.lower()

    now = datetime.utcnow()
    if last_response_time is not None:
        if (now - last_response_time).total_seconds() < cooldown_seconds:
            return

    
    love_questions = [
        "кого ты любишь",
        "кто твой создатель",
        "кого ты считаешь важным",
        "кем ты дорожишь",
        "кого ты обожаешь",
        "кто твой любимый человек",
        "кто твой любимый",
        "кто твой любимый человек в этом мире",
        "с кем бы ты хотела бы провести время",
        "с кем бы ты хотела провести время",
        "с кем бы ты хотела",
        "кто для тебя важен",
    ]

    love_answers = [
        "Созданные вручную, но самые искренние чувства от и для @wattheoshi! 💖",
        "Моё сердце принадлежит моему создателю! ✨",
        "Только мой создатель, @wattheoshi, может заглядывать в меня так глубоко, как вам и не снилось! ˶˃⤙˂˶ ",
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

    
    calls = ["апош", "апошка", "апоша", "апошенька", "апошечка", "апошась", "aposh", "апошка?", "апош?"]
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



@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="Чему я обучена?",
        description="Вот что я умею делать пока что: ",
        color=discord.Color.blue()
    )
    embed.add_field(name="&Aposh", value="Просто приветствую вас!", inline=False)
    embed.add_field(name="&help", value="Вы наблюдаете результат команды!", inline=False)
    embed.add_field(name="&ban @user [причина]", value="Ух, страшный бан!", inline=False)
    embed.add_field(name="&kick @user [причина]", value="Выметаю негодяев из нашего поместья!", inline=False)
    embed.add_field(name="&clear [количество]", value="Чищу мусор и привожу канал в порядок без последних лишних сообщений!", inline=False)
    await ctx.send(embed=embed)

@bot.command() 
@commands.has_permissions(administrator=True) 
async def clear(ctx, amount: int):
    if amount < 1:
        await ctx.send("Количество сообщений должно быть больше 0.")
        return
    else:
        await ctx.channel.purge(limit=amount+1)
        await ctx.channel.send(f"Подметаю аж {amount} сообщений...")

@bot.command() 
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason="Зажал"):
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

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason="Зажал"):
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

bot.run(os.getenv("BOT_TOKEN"))
