import discord
from discord.ext import commands
import json


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