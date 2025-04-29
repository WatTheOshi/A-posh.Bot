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


# --- Команды взаимодействия ---
def setup(bot):
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

