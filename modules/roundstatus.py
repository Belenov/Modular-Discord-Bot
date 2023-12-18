import datetime
import time

import discord
from discord.ext import commands, tasks

from byond_topic import queryStatus
from loggers import logger


class Roundstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Checks for round continuity on server."
        self.channel_alert = 1186264416304500736
        self.channel_id = 1186264489750954034
        self.last_gamestate = -1337
        self.init = False

    def cog_unload(self):
        self.round_checker.cancel()

    @tasks.loop(seconds=35.0)
    async def round_checker(self):
        try:
            responseData = await queryStatus("127.0.0.1", 65556)
            logger.info(responseData)
        except ConnectionRefusedError as ref_ex:
            logger.info("Сервер выключен.")
            return
        except Exception as ex:
            logger.warning(ex, type(ex))
            return
        current_time = int(responseData["round_duration"][0])
        current_gamestate = int(responseData["gamestate"][0])
        if self.init and (current_gamestate == self.last_gamestate):
            # result = requests.get(
            #     "https://g.tenor.com/v2/search?q=ss13&key=AIzaSyDbkTHFgMmXeEB1U1JPFqycpHw2HujFUhA&limit=20"
            # )
            # img = result.json()["results"][random.randint(0, 19)]["media_formats"][
            #     "gif"
            # ]["url"]
            # bot.custom_embed.set_image(url=img)
            self.bot.custom_embed.clear_fields()
            self.bot.custom_embed.add_field(
                name="Количество игроков",
                value=responseData["players"][0] + " игрок(ов)",
            )
            self.bot.custom_embed.add_field(
                name="Время раунда",
                value=time.strftime("%H:%M", time.gmtime(current_time)),
            )
            if hasattr(self.bot, "custom_embed_message"):
                await self.bot.custom_embed_message.edit(embed=self.bot.custom_embed)
        elif current_gamestate == 0 or not self.init:
            if hasattr(self.bot, "custom_embed"):
                self.bot.custom_embed.clear_fields()
                self.bot.custom_embed.add_field(
                    name="Раунд завершён",
                    value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                if hasattr(self.bot, "custom_embed_message"):
                    await self.bot.custom_embed_message.edit(
                        embed=self.bot.custom_embed
                    )
            self.bot.custom_embed = discord.Embed(
                title=f'Статус раунда #{responseData["round_id"][0]}',
                color=0xFFFF00,
            )
            if self.channel_id:
                self.bot.custom_embed_message = await self.channel_id.send(
                    embed=self.bot.custom_embed
                )
            if self.channel_alert:
                await self.channel_alert.send(
                    f'<@&938048041208905728> Новый раунд на карте {responseData["map_name"][0]}'
                )

            self.last_gamestate = current_gamestate
            self.init = True

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel_alert = self.bot.get_channel(self.channel_alert)
        self.channel_id = self.bot.get_channel(self.channel_id)
        self.round_checker.start()


async def setup(bot):
    await bot.add_cog(Roundstatus(bot))
