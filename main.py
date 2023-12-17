# Стандартные библиотеки
import asyncio
import yaml
import logging
import os

import colorama

# Сторонние библиотеки
import discord
from colorama import Fore, Style
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
colorama.init(autoreset=True)
logger = logging.getLogger(__name__)
CONFIG_PATH = os.getenv("DISORD_CONFIG_PATH", "./settings/config.yaml")
# Load the config file and retrieve the token
with open(CONFIG_PATH) as config_file:
    CONFIG = yaml.safe_load(config_file)
token = CONFIG["token"]


# Устанавливаем параметры намерений (intents) для бота
intents = discord.Intents.all()
intents.message_content = True
intents.messages = True
intents.members = True

# Create an instance of a bot
bot = commands.Bot(command_prefix="!", intents=intents)


async def load():
    module_states = load_module_state()
    if not module_states:
        # Если нет файла модулей то первый раз нужно его сделать
        module_states = {}
    module_descriptions = {}
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            if not module_states.get(module_name):
                # Все модули загружаются по умолчанию
                module_states[module_name] = "loaded"
                # Дампим состояние всех модулей после загрузки каждого
                save_module_state(module_states)
            if module_states.get(module_name, "loaded") != "unloaded":
                try:
                    await bot.load_extension(f"modules.{module_name}")
                    # Сделаем обработку созданного кога
                    cogi = bot.get_cog(module_name.capitalize())
                    # Сохраним его описание в файл из кода
                    module_descriptions[module_name] = cogi.description
                    logger.info(
                        Fore.BLUE
                        + Style.BRIGHT
                        + "[modules]"
                        + Style.RESET_ALL
                        + f" Modules {module_name} working"
                    )
                except Exception as e:
                    logger.info(
                        Fore.RED
                        + "[modules]"
                        + Style.RESET_ALL
                        + f" Not working {module_name}: {e}"
                    )
    save_module_descriptions(module_descriptions)


def load_module_state():
    with open("./settings/module_state.yaml", "a+") as file:
        return yaml.safe_load(file)


def save_module_state(state):
    with open("./settings/module_state.yaml", "w+") as file:
        yaml.dump(state, file)


def save_module_descriptions(module_descriptions):
    file_path = "./settings/module_descriptions.yaml"
    with open(file_path, "w+") as f:
        yaml.dump(module_descriptions, f)


@bot.event
async def on_ready():
    logger.info(
        Fore.GREEN + Style.BRIGHT + f"Logged in as {bot.user.name} (ID: {bot.user.id})"
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx, extension):
    if os.path.isfile(f"./modules/{extension}.py"):
        try:
            await bot.unload_extension(f"modules.{extension}")
            await bot.load_extension(f"modules.{extension}")
            await ctx.send(f"Модуль {extension} был перезагружен.")
        except Exception as e:
            await ctx.send(f"Ошибка при перезагрузке модуля: {e}")


@bot.command(name="load")
@commands.is_owner()
async def loads(ctx, extension):
    if os.path.isfile(f"./modules/{extension}.py"):
        try:
            await bot.load_extension(f"modules.{extension}")
            await ctx.send(f"Модуль {extension} загружен.")
        except Exception as e:
            await ctx.send(f"Ошибка при загрузке модуля: {e}")
    else:
        await ctx.send(f"Модуль {extension} не найден.")
    state = load_module_state()
    state[extension] = "loaded"
    save_module_state(state)


@bot.command(name="unload")
@commands.is_owner()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f"modules.{extension}")
        await ctx.send(f"Модуль {extension} выгружен.")
    except Exception as e:
        await ctx.send(f"Ошибка при выгрузке модуля: {e}")
    state = load_module_state()
    state[extension] = "unloaded"
    save_module_state(state)


async def main():
    await load()
    await bot.start(token)


asyncio.run(main())
