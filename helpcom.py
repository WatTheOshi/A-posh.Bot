import discord
from discord.ext import commands


# --- Команда помощи ---
def setup(bot):
    @bot.command(name="help")
    async def help(ctx):
        """Отправляет embed с доступными командами."""
        embed = discord.Embed(
            title="Чему я обучена?",
            color=discord.Color.light_gray(),
        )

        embed.set_author(
            name="Апош!",
            url="https://github.com/WatTheOshi/A-posh.Bot/",
            icon_url="https://cdn.britannica.com/62/236062-050-CD53AE96/Ampersand-symbol.jpg", 
        )

        # Функциональные команды :
        embed.add_field(name="_**Функциональные команды :**_", value="", inline=False)
        embed.add_field(name="**&help**", value="Вы наблюдаете результат команды!", inline=False)
        embed.add_field(name="**&Aposh**", value="Просто приветствую вас!", inline=False)
        embed.add_field(name="**&ban @user [причина]**", value="Ух, страшный бан!", inline=False)
        embed.add_field(name="**&kick @user [причина]**", value="Выметаю негодяев из нашего поместья!", inline=False)
        embed.add_field(name="**&mute @user [время] [причина]**", value="Заткнись, я не хочу тебя слышать!", inline=False)
        embed.add_field(name="**&unmute @user**", value="Ладно, можешь печатать...", inline=False)
        embed.add_field(name="**&clear [количество]**", value="Чищу мусор и привожу канал в порядок без последних лишних сообщений!", inline=False)
        # Взаимодействие с пользователями :
        embed.add_field(name="_**Взаимодействие с пользователями :**_", value="", inline=False)
        embed.add_field(name="**&hug @user**", value="Обними своего приятеля!", inline=False)
        embed.add_field(name="**&pat @user**", value='Погладь своего "котенка"!', inline=False)
        embed.add_field(name="**&kiss @user**", value="Целуй тех кто считаешь что заслужил!", inline=False)
        embed.add_field(name="**&hit @user**", value="Ударь негодяев!", inline=False)
        embed.add_field(name="**&dodge**", value="Попытка избежать того что написано выше!", inline=False)
        # В добавок, есть особенности :
        embed.add_field(name="_**В добавок, есть особенности :**_", value="", inline=False)
        embed.add_field(name="**Кто-то сказал моё имя?**", value="Я слышу если вы обо мне говорите!", inline=False)
        embed.add_field(name="Вопросы!", value="Придется ответить на некоторые спецефичные вопросы... Если спросить меня через упомянание...", inline=False)
        await ctx.send(embed=embed)
    
    
    @bot.command(name="Aposh")
    async def Aposh(ctx):
        await ctx.send(f"Привет, **{ctx.author.display_name}**! Меня зовут **Апош**, меня прислали на помощь! \n"
                       "Если нужна помощь, просто напиши **&help** и я расскажу, что я умею! \n")

