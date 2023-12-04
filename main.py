# Стандартные библиотеки
import json
import logging
import os
import sys
import asyncio
# Сторонние библиотеки
import discord
from discord.ext import commands
import importlib
import colorama
from colorama import Fore, Style




print(sys.path)
logging.basicConfig(level=logging.INFO)
colorama.init(autoreset=True)

# Load the config file and retrieve the token
with open(f'C:[your_path]/python3/config/config.json') as config_file:
    config = json.load(config_file)
token = config["Token"]


# Устанавливаем параметры намерений (intents) для бота
intents = discord.Intents.all()
intents.message_content = True
intents.messages = True

# Create an instance of a bot
bot = commands.Bot(command_prefix='!', intents=intents)

async def load():
    module_state = load_module_state()
    for filename in os.listdir('./modules'):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            if module_state.get(module_name) != 'unloaded':
                try:
                    await bot.load_extension(f'modules.{module_name}')
                    print(Fore.BLUE + Style.BRIGHT + '[modules]' + Style.RESET_ALL + f' Modules {module_name} working')
                except Exception as e:
                    print(Fore.RED + '[modules]' + Style.RESET_ALL + f' Not working {module_name}: {e}')


def load_module_state():
    try:
        with open('./config/module_state.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_module_state(state):
    with open('./config/module_state.json', 'w') as file:
        json.dump(state, file)

@bot.event
async def on_ready():
    print(Fore.GREEN + Style.BRIGHT + f'Logged in as {bot.user.name} (ID: {bot.user.id})')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.command(name='reload')
@commands.is_owner()
async def reload(ctx, extension):
    if os.path.isfile(f'./modules/{extension}.py'):
        try:
            await bot.unload_extension(f'modules.{extension}')
            await bot.load_extension(f'modules.{extension}')
            await ctx.send(f'Модуль {extension} был перезагружен.')
        except Exception as e:
            await ctx.send(f'Ошибка при перезагрузке модуля: {e}')

@bot.command(name='load')
@commands.is_owner()
async def loads(ctx, extension):
    if os.path.isfile(f'./modules/{extension}.py'):
        try:
            await bot.load_extension(f'modules.{extension}')
            await ctx.send(f'Модуль {extension} загружен.')
        except Exception as e:
            await ctx.send(f'Ошибка при загрузке модуля: {e}')
    else:
        await ctx.send(f'Модуль {extension} не найден.')
    state = load_module_state()
    state[extension] = 'loaded'
    save_module_state(state)

@bot.command(name='unload')
@commands.is_owner()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f'modules.{extension}')
        await ctx.send(f'Модуль {extension} выгружен.')
    except Exception as e:
        await ctx.send(f'Ошибка при выгрузке модуля: {e}')
    state = load_module_state()
    state[extension] = 'unloaded'
    save_module_state(state)




async def main():
    await load()
    await bot.start(token)

asyncio.run(main())
