import discord
from discord.ext import commands
import json
import requests


# --- Команды утилиты ---
def setup(bot):
    @bot.command(name="ping")
    async def ping(ctx):
        """Проверяет задержку бота."""
        latency = round(bot.latency * 1000)  # Переводим в миллисекунды
        await ctx.send(f"Понг! Задержка: {latency} мс")

    @bot.command(name="userinfo")
    async def userinfo(ctx, member: discord.Member = None):
        """Показывает информацию о пользователе."""
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"Информация о {member.name}", color=discord.Color.light_grey())
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Создан", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Присоединился", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @bot.command(name="serverinfo")
    async def serverinfo(ctx):
        """Показывает информацию о сервере."""
        guild = ctx.guild
        embed = discord.Embed(title=f'Информация о поместьи "{guild.name}"', color=discord.Color.dark_magenta())
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Основан в", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Сколько жильцов", value=guild.member_count)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
        await ctx.send(embed=embed)

    @bot.command(name="giverole")
    @commands.has_permissions(manage_roles=True)
    async def giverole(ctx, role: discord.Role, member: discord.Member):
        """Выдает роль указанному пользователю."""
        if role in member.roles:
            await ctx.send(f"{member.mention} уже имеет роль {role.name}!")
            return
        if discord.Forbidden:
            await ctx.send("Такая как я не может выдавать подобные роли...")
            return
        await ctx.send(f"Ролью {role.name} награждено {member.mention}!")
        await member.add_roles(role)

    @bot.command(name="rmrole")
    @commands.has_permissions(manage_roles=True)
    async def removerole(ctx, role: discord.Role, member: discord.Member):
        """Удаляет роль у указанного пользователя."""
        if role not in member.roles:
            await ctx.send(f"{member.mention} не имеет роль {role.name}!")
            return
        if discord.Forbidden:
            await ctx.send("Такая как я не может отнимать подобные роли...")
            return
        await member.remove_roles(role)
        await ctx.send(f"Роль {role.name} отобрана у {member.mention}!")

    @bot.command(name="welcome")
    @commands.has_permissions(administrator=True)
    async def welcome(ctx, channel: discord.TextChannel = None):
        """Устанавливает канал для приветственных сообщений."""
        if channel is None:
            await ctx.send("Пожалуйста, укажите канал для приветствий.")
            return
        # Сохраняем канал в контексте или базе данных
        async def welcome(ctx, channel: discord.TextChannel):
            config = await load_json(CONFIG_FILE)
            cfg = config.get(str(ctx.guild.id), {})
            cfg['welcome_channel'] = channel.id
            config[str(ctx.guild.id)] = cfg
            await save_json(CONFIG_FILE, config)
        # Здесь можно добавить логику сохранения канала
        await ctx.send(f"Канал для приветствий установлен: {channel.mention}")

    @bot.command(name="dicten")
    async def dicten(ctx, word):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        response = requests.get(url)

        if response.status_code != 200:
            await ctx.send("❌ У меня не получилось найти такое слово...")
            return

        data = response.json()

        try:
            # Берём первое значение, первую часть речи и определение
            meaning = data[0]["meanings"][0]
            part_of_speech = meaning["partOfSpeech"]
            definition = meaning["definitions"][0]["definition"]
            example = meaning["definitions"][0].get("example", "Не нашлось")

            embed = discord.Embed(
                title=f":open_book: И так, **{word.capitalize()}**",
                color=discord.Color.light_embed()
            )
            embed.add_field(name=":jigsaw: Часть речи: ", value=part_of_speech, inline=False)
            embed.add_field(name=":point_up: Определение: ", value=definition, inline=False)
            embed.add_field(name=":cocktail: Пример: ", value=example, inline=False)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("⚠️ Что-то пошло не так при разборе ответа API.")