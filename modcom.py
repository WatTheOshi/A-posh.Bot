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


LOG_FILE = "mute_logs.json"

def log_timeout_action(user, moderator, reason, duration_seconds, action="mute"):
    log_entry = {
        "user_id": user.id,
        "username": str(user),
        "moderator_id": moderator.id,
        "moderator_name": str(moderator),
        "reason": reason,
        "duration_seconds": duration_seconds,
        "timestamp": datetime.utcnow().isoformat(),
        "action": action
    }

    # Создаём файл если его нет
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    # лог
    with open(LOG_FILE, "r+", encoding="utf-8") as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()



test_mode = False

# --- Модераторские команды ---
def setup(bot):
     # Убедимся, что здесь нет `on_message`, чтобы избежать конфликта
    pass

    @bot.command(aliases=['mute', 'мут', 'мьют', 'timemute'])
    @commands.has_permissions(administrator=True)
    async def timeout(ctx, member: discord.Member = None, time=None, *, reason=None):
        author = ctx.author
        if member is not None:
            if time is not None:
                try:
                    t = humanfriendly.parse_timespan(time)
                    await member.timeout(timedelta(seconds=t), reason=reason)

                    log_timeout_action(
                    user=member,
                    moderator=ctx.author,
                    reason=reason,
                    duration_seconds=int(t),
                    action="mute"
                )


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

                log_timeout_action(
                user=member,
                moderator=ctx.author,
                reason=reason,
                duration_seconds=0,
                action="unmute"
                )


                embed = discord.Embed(
                    title='Успешно размучен',
                    description=f'**{member.mention}** снова может гавкать!\n\n**По причине: `{reason}`**',
                    colour=discord.Colour.from_rgb(0, 189, 0)
                )
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"Эхх, не получилось!")
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

    @bot.command(aliases=['mutes', 'муты', 'mutelog'])
    @commands.has_permissions(administrator=True)
    async def show_mutes(ctx):
        """Показывает последние 10 мутов."""
        try:
            if not os.path.exists(LOG_FILE):
                await ctx.send("Картотека пустая...")
                return

            with open(LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Фильтруем только муты
            mutes = [entry for entry in data if entry["action"] == "mute"]

            if not mutes:
                await ctx.send("Пока никого не мутила... Ау?")
                return

            # Берём последние 10
            last_mutes = mutes[-10:][::-1]  # свежие сверху

            embed = discord.Embed(
                title="🔇 Последние жертвы",
                color=discord.Color.light_grey()
            )

            for entry in last_mutes:
                user_name = entry["username"]
                reason = entry.get("reason", "Не указана")
                duration = humanfriendly.format_timespan(entry["duration_seconds"])
                time_str = entry["timestamp"].replace("T", " ").split(".")[0] + " UTC"

                embed.add_field(
                    name=user_name,
                    value=f"⏱ `{duration}` | 📝 `{reason}`\n🕒 `{time_str}`",
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Произошла ошибка при чтении логов: {e}")

    @bot.command(name="voice")
    async def voice(ctx, amountUsers: int):
        """Создаёт приватный голосовой канал в той же категории, где был пользователь."""
        # Проверяем, что пользователь в голосовом канале
        if ctx.author.voice and ctx.author.voice.channel:
            guild = ctx.guild
            author = ctx.author
            old_channel = ctx.author.voice.channel
            category = old_channel.category  # Получаем категорию текущего голосового канала

            # Создаём канал
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False),
                author: discord.PermissionOverwrite(connect=True, manage_channels=True)
            }
            channel = await guild.create_voice_channel(
                name=f"& Собрание {author.name}",
                user_limit=amountUsers,
                overwrites=overwrites,
                category=category,  # Указываем категорию
                reason="Приватное собрание"
            )

            await ctx.send("Приватное собрание организовано!")
            # Перемещаем пользователя в новый канал
            await author.move_to(channel)

            # Функция для удаления канала, если он пуст
            async def delete_when_empty(channel):
                while True:
                    await asyncio.sleep(1)
                    ch = guild.get_channel(channel.id)
                    if ch is None:
                        break
                    if len(ch.members) == 0:
                        await ctx.send(f"Собрание {author.name} окончилось...")
                        await ch.delete(reason="Приватный канал опустел")
                        break

            # Запускаем задачу на удаление
            ctx.bot.loop.create_task(delete_when_empty(channel))
        else:
            await ctx.send("Сначала зайдите в любой голосовой канал!")

