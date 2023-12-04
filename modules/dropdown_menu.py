import discord
from discord.ext import commands

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Test 1', description='Test 1'),
            discord.SelectOption(label='Test 2', description='Test 2'),
            discord.SelectOption(label='Test 3', description='Test 3'),
        ]
        super().__init__(placeholder='Choose an option...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You selected: {self.values[0]}')

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class DropdownMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def menu(self, ctx):
        embed = discord.Embed(title="Test 5", description="Test 5")
        await ctx.send(embed=embed, view=DropdownView())

async def setup(bot):
    await bot.add_cog(DropdownMenuCog(bot))