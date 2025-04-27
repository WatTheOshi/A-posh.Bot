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
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    responses = [
        "Ой, ой, кто меня звал? >~<",
        "Я тут, я тут! Что-то нужно? :3",
        "https://tenor.com/lZuHcGbo7eh.gif",
        "Я всегда здесь! Слежу! :eye:",
        "Я отвлеклась! :anger:"
    ]
    for content in message.content.lower().split():
        for call in ["апош", "апошка", "апоша", "апошенька", "апошечка", "апошась", "aposh", "a posh"]:
            if call in content:
                await message.channel.send(random.choice(responses))
                break
    await bot.process_commands(message)

                                       
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
