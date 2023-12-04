# modules/embed_module.py
from discord.ext import commands
from discord import Embed, ButtonStyle
from discord.ui import Button, View

class EmbedCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sendembed")
    async def send_embed(self, ctx):
        embed = Embed(title="Test", description="Test", color=0x00ff00)

        embed.set_image(url="https://starwalk.space/gallery/images/what-is-space/1920x1080.jpg")
        # Создание кнопок
        view = View()
        view.add_item(Button(label="Button 1", style=ButtonStyle.primary))
        view.add_item(Button(label="Button 2", style=ButtonStyle.secondary))

        # Отправка сообщения с embed и кнопками
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(EmbedCommands(bot))
