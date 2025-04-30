import discord
from discord.ext import commands
from discord.ui import View, Button

# --- Тематические блоки ---
help_sections = [
    {
        "title": "Функциональные команды",
        "commands": [
            ("**&help**", "Вы наблюдаете результат команды!"),
            ("**&Aposh**", "Просто приветствую вас!"),
            ("**&ban @user [причина]**", "Ух, страшный бан!"),
            ("**&kick @user [причина]**", "Выметаю негодяев из нашего поместья!"),
            ("**&mute @user [время] [причина]**", "Заткнись, я не хочу тебя слышать!"),
            ("**&unmute @user**", "Ладно, можешь печатать..."),
            ("**&mutes**", "Последние список из 10 наказанных в нашем поместье"),
            ("**&clear [количество]**", "Чищу мусор и привожу канал в порядок без последних лишних сообщений!"),
        ]
    },
    {
        "title": "Взаимодействие с пользователями",
        "commands": [
            ("**&bnuysteal** и **bnuyreturn**", "Украсть и вернуть bnuy!"),
            ("**&hug @user**", "Обними своего приятеля!"),
            ("**&pat @user**", 'Погладь своего "котенка"!'),
            ("**&kiss @user**", "Целуй тех кто считаешь что заслужил!"),
            ("**&hit @user**", "Ударь негодяев!"),
            ("**&dolove @user**", "Что-то более серьезное, чем просто поцелуй!"),
            ("**&dodge**", "Попытка избежать того что написано выше!"),
        ]
    },
    {
        "title": "Особенности и пассивные реакции",
        "commands": [
            ("**Кто-то сказал моё имя?**", "Я слышу если вы обо мне говорите!"),
            ("**Вопросы!**", "Придется ответить на некоторые спецефичные вопросы... Если спросить меня через упомянание..."),
        ]
    }
]


# --- Создание embed по номеру раздела ---
def create_help_embed(section_index: int):
    section = help_sections[section_index]
    embed = discord.Embed(
        title=f"Чему я обучена — {section['title']}",
        color=discord.Color.light_gray(),
    )
    embed.set_author(
        name="Апош!",
        url="https://github.com/WatTheOshi/A-posh.Bot/",
        icon_url="https://cdn.britannica.com/62/236062-050-CD53AE96/Ampersand-symbol.jpg",
    )

    for name, desc in section["commands"]:
        embed.add_field(name=name, value=desc, inline=False)

    embed.set_footer(text=f"Страница {section_index + 1} из {len(help_sections)}")
    return embed


# --- View с кнопками для тем ---
class HelpView(View):
    def __init__(self, author_id):
        super().__init__(timeout=60)
        self.page = 0
        self.author_id = author_id
        self.max_pages = len(help_sections) - 1

    @discord.ui.button(label="⬅️ Назад", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Ты не вызывал это меню~", ephemeral=True)
            return

        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=create_help_embed(self.page), view=self)

    @discord.ui.button(label="➡️ Далее", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Это не твоё меню, дорогуша", ephemeral=True)
            return

        if self.page < self.max_pages:
            self.page += 1
            await interaction.response.edit_message(embed=create_help_embed(self.page), view=self)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


# --- Команды ---
def setup(bot):
    @bot.command(name="help")
    async def help(ctx):
        """Отправляет embed с доступными командами, разделёнными по категориям."""
        view = HelpView(author_id=ctx.author.id)
        embed = create_help_embed(view.page)
        await ctx.send(embed=embed, view=view)

    @bot.command(name="Aposh")
    async def Aposh(ctx):
        await ctx.send(f"Привет, **{ctx.author.display_name}**! Меня зовут **Апош**, меня прислали на помощь! \n"
                       "Если нужна помощь, просто напиши **&help** и я расскажу, что я умею! \n")
