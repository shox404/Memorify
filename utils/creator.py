from aiogram.types import InlineKeyboardButton, Message, BotCommand
from lang.function import use_text
from bot import bot


def inline_btn(value, msg):
    """Inline button creator"""
    return InlineKeyboardButton(text=use_text(value, msg), callback_data=value)


async def set_commands(msg: Message):
    commands = [
        BotCommand(command="start", description=use_text("start", msg)),
        BotCommand(command="set_reminder", description=use_text("set_reminder", msg)),
    ]
    await bot.set_my_commands(commands)


async def create_table_if_not_exists(conn, table_name, schema):
    """Create a table if it does not already exist."""

    await conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});")
