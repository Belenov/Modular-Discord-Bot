import os

from discord.ext import commands

from loggers import action_logger, logger

ALLOWED_ROLE_IDS = [885561160001257593, 1167753949546299433, 1167847850969939969]
FORBIDDEN_CHARS = [
    "@",
    "/",
    '"',
    "'",
    ";",
    "<",
    ">",
    "{",
    "}",
    "[",
    "]",
    "|",
    "&",
    "^",
    "%",
    "$",
    "#",
    "!",
    "\\",
    ":",
    "*",
    "?",
    "`",
    "~",
    "=",
    "+",
]


def is_allowed_role(ctx):
    return any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)


def contains_forbidden_chars(name):
    return any(char in name for char in FORBIDDEN_CHARS)


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "I'ma whitelist module!"

    @commands.command()
    @commands.check(is_allowed_role)
    async def whitelist(ctx, action, *, name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "whitelist.txt")
        action = action.lower()

        # Отладочное сообщение
        logger.info(f"Работаем с файлом: {file_path}")
        logger.info(f"Действие: {action}, пользователь: {name}")

        if contains_forbidden_chars(name):
            await ctx.send(
                "Недопустимые символы в имени. Пожалуйста, используйте другое имя."
            )
            return

        with open(file_path, "r") as f:
            lines = f.readlines()

        if action == "add":
            if name + "\n" in lines:
                await ctx.send(f"{name} уже есть в списке!")
                return
            with open(file_path, "a") as f:
                f.write(name + "\n")
            await ctx.send(f"{name} было отправлено на опыты!")
            action_logger.warning(f"{ctx.author} добавил {name}")

        elif action == "remove":
            if name + "\n" not in lines:
                await ctx.send(f"{name} нет в списке!")
                return
            with open(file_path, "w") as f:
                for line in lines:
                    if line.strip("\n") != name:
                        f.write(line)
            await ctx.send(f"{name} было отправлено в чистилище!")
            action_logger.warning(f"{ctx.author} удалил {name}")

        else:
            await ctx.send(f"Неизвестное действие: {action}")

    @whitelist.error
    async def whitelist_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Недостаточно прав для использования этой команды!")
        else:
            await ctx.send("Произошла ошибка!")


async def setup(bot):
    await bot.add_cog(Whitelist(bot))
