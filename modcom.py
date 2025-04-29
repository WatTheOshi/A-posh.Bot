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


# --- Модераторские команды ---
def setup(bot):
    @bot.command(aliases=['mute', 'мут', 'мьют', 'timemute'])
    @commands.has_permissions(administrator=True)
    async def timeout(ctx, member: discord.Member = None, time=None, *, reason=None):
        author = ctx.author
        if member is not None:
            if time is not None:
                try:
                    t = humanfriendly.parse_timespan(time)
                    await member.timeout(timedelta(seconds=t), reason=reason)
                    embed = discord.Embed(
                        title='Успешно замучен',
                        description=f'**{member.mention}** заткнулся на **{time}**\n\n**По причине: `{reason}`**',
                        colour=discord.Colour.from_rgb(0, 189, 0)
                    )
                    await ctx.send(embed=embed)
                except Exception as e:
                    await ctx.send(f"Произошла ошибка: {e}")
            else:
                embed = discord.Embed(
                    title='Блять, не всё так просто',
                    description=f'{author.mention}, укажите время замута.',
                    colour=discord.Colour.from_rgb(171, 0, 0)
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Блять, не всё так просто',
                description=f'{author.mention}, укажите кого нужно замутить.',
                colour=discord.Colour.from_rgb(171, 0, 0)
            )
            await ctx.send(embed=embed)


    @bot.command(aliases=['unmute', 'размут', 'анмьют'])
    @commands.has_permissions(administrator=True)
    async def untimeout(ctx, member: discord.Member = None, *, reason=None):
        author = ctx.author
        if member is not None:
            try:
                await member.timeout(None, reason=reason)
                embed = discord.Embed(
                    title='Успешно размучен',
                    description=f'**{member.mention}** снова может гавкать!\n\n**По причине: `{reason}`**',
                    colour=discord.Colour.from_rgb(0, 189, 0)
                )
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"Произошла ошибка: {e}")
        else:
            embed = discord.Embed(
                title='Блять, не всё так просто',
                description=f'{author.mention}, укажите кого нужно размутить.',
                colour=discord.Colour.from_rgb(171, 0, 0)
            )
            await ctx.send(embed=embed)


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

