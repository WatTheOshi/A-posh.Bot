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
special_user_id = 773282996324270141  # ID создателя


# --- Команды взаимодействия ---
def setup(bot):
    # Убедимся, что здесь нет `on_message`, чтобы избежать конфликта
    pass

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
                elif message.content.startswith("&dolove"):
                    await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уклоняется от неожиданных действий!")
                    return
                elif message.content.startswith("&feed"):
                    await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уклоняется от еды!")
                    return
                elif message.content.startswith("&bonk"):
                    await ctx.send(f"_**DODGE!**_ \n{ctx.author.mention} уклоняется от бонка!")
                    return
                elif message.content.startswith("&dodge"):
                    await ctx.send("https://tenor.com/bVA8m.gif")
                    return
        await ctx.send("За последнее время не от чего уклоняться...")
    
    
    @bot.command(name="dolove") # хз я чето кринжанул но меня попросили
    async def dolove(ctx, member: discord.Member):
        """Слишком близкие взаимодействия пользователей (с особым ответом для создателя)."""
        special_user_id = 773282996324270141  # ID создателя
    
        if member == ctx.author:
            await ctx.send("Эээ... ну, классика, да?...")
            return
        if member == bot.user:
            if ctx.author.id == special_user_id:
                await ctx.send("https://tenor.com/bR7LV.gif")
            else:
                await ctx.send("_**DODGE!**_\nДа как ты обращаешься со мной?!")
                await ctx.send("&hit {ctx.author.mention}")
            return
        
        interactions = [
            "нежно прижимается к", 
            "страстно шепчет что-то на ухо", 
            "пытается флиртовать с", 
            "притягивает к себе",
            "ласково смотрит на",
        ]
        choice = random.choice(interactions)

        await ctx.send(f":heartpulse: \n{ctx.author.mention} {choice} {member.mention}!")


    @bot.command(name="stand")
    async def stand(ctx):
        """Присылает гифку со стендами из Джоджо"""
        await ctx.send("https://tenor.com/bCwYG.gif")

    @bot.command(name="bnuysteal")
    async def bnuysteal(ctx):
        """Присылает гифку с кражей кролика"""
        await ctx.send("https://tenor.com/bV8kF.gif")

    @bot.command(name="bnuyreturn")
    async def bnuyreturn(ctx):
        """Присылает гифку с возвращением кролика"""
        await ctx.send("https://tenor.com/rZ6HCDf6wU8.gif")


    @bot.command(name="rape")
    async def rape(ctx, member: discord.Member):
        await ctx.send(f"бывают же ебланы... не смей такое писать, {ctx.author.mention}!")
        return

    @bot.command(name="feed")
    async def feed(ctx, member: discord.Member):
            """feeding user"""
            if member == ctx.author:
                await ctx.send("Видимо кто-то решил обедать?")
                return
            if member == bot.user:
                await ctx.send("//°o°//")
                return
            await ctx.send(f":watermelon: \n{ctx.author.mention} кормит {member.mention}!")

    @bot.command(name="bonk")
    async def bonk(ctx, member: discord.Member):
            """bonk user"""
            if member == ctx.author:
                await ctx.send("Ээ, ну, это странно... Не стоит так делать!")
                return
            if member == bot.user:
                await ctx.send("***DODGE!*** \nНеа! Меня нельзя!")
                return
            await ctx.send(f":heart_eyes: \n{ctx.author.mention} стукнул {member.mention} по макушке!")

    @bot.command(name="summon")
    async def summon(ctx, member: discord.Member):
            """tries to summon user"""
            if member == ctx.author:
                await ctx.send("Ты патаешься кого-то запутать?")
                return
            if member == bot.user:
                await ctx.send("*шепчет сзади* А я всегда тут~")
                return
            await ctx.send(f":heart_eyes: \n{ctx.author.mention} колдует призыв {member.mention}!")
            await asyncio.sleep(2)
            await ctx.send(f":sparkler: {member.mention} :sparkler:")

    @bot.command(name="glitch")
    async def glitch(ctx):
        """Присылает гифку с глитчем"""
        await ctx.send("https://tenor.com/bZw7b.gif")

    @bot.command(name="pair")
    async def pair(ctx, doveOne: discord.Member, doveTwo: discord.Member):
        """Pair percentage between members"""

        if doveOne == doveTwo:
            await ctx.send("Это ведь один и тот же человек? Наверное, должно быть 100%... Хотя, кто знает? :thinking:")
            return

        # Исправленное условие
        elif (
            (doveOne == bot.user and doveTwo.id == special_user_id) or
            (doveTwo == bot.user and doveOne.id == special_user_id)
        ):
            await ctx.send("~~76%~~ :pen_fountain: \n_**BLUSH!**_ \n**999%** :pen_fountain: \n_**KISS!**_")
            return

        else: 
            def digit_sum(user_id):
                return sum(int(digit) for digit in str(user_id))

            sum_one = digit_sum(doveOne.id)
            sum_two = digit_sum(doveTwo.id)

            total = sum_one + sum_two
            percentage = (total % 101)

            await ctx.send(f":revolving_hearts: Совместимость между {doveOne.display_name} и {doveTwo.display_name}: {percentage}%")


