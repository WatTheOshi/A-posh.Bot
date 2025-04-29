import discord
from discord.ext import commands


# --- Команда помощи ---
def setup(bot):
    @bot.command(name="help")
    async def help(ctx):
        """Отправляет embed с доступными командами."""
        embed = discord.Embed(
            title="Чему я обучена?",
            description="Вот что я умею делать пока что:",
            color=discord.Color.blue()
        )
        embed.add_field(name="&Aposh", value="Просто приветствую вас!", inline=False)
        embed.add_field(name="&help", value="Вы наблюдаете результат команды!", inline=False)
        embed.add_field(name="&ban @user [причина]", value="Ух, страшный бан!", inline=False)
        embed.add_field(name="&kick @user [причина]", value="Выметаю негодяев из нашего поместья!", inline=False)
        embed.add_field(name="&clear [количество]", value="Чищу мусор и привожу канал в порядок без последних лишних сообщений!", inline=False)
        await ctx.send(embed=embed)
    
    
    @bot.command(name="Aposh")
    async def Aposh(ctx):
        await ctx.send(f"Привет, **{ctx.author.display_name}**! Меня зовут **Апош**, меня прислали на помощь! \n"
                       "Если нужна помощь, просто напиши **&help** и я расскажу, что я умею! \n")

