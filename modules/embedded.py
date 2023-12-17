# modules/embed_module.py
from discord import ButtonStyle, Embed
from discord.ext import commands
from discord.ui import Button, View


class Embedded(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "I'ma embedded cog!"

    @commands.command(name="sendembed")
    async def send_embed(self, ctx):
        embed = Embed(title="Test", description="Test", color=0x00FF00)
        embed.set_image(
            url="https://starwalk.space/gallery/images/what-is-space/1920x1080.jpg"
        )
        view = View()
        view.add_item(Button(label="Button 1", style=ButtonStyle.primary))
        view.add_item(Button(label="Button 2", style=ButtonStyle.secondary))
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Embedded(bot))
