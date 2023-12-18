from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "I'ma hello cog!"

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Working!")


async def setup(bot):
    await bot.add_cog(Hello(bot))
