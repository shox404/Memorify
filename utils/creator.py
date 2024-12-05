from aiogram.types import InlineKeyboardButton, Message, BotCommand
from lang.function import use_text
from bot import bot


def inline_btn(value, msg):
    return InlineKeyboardButton(text=use_text(value, msg), callback_data=value)


async def set_commands(msg: Message):
    commands = [
        BotCommand(command="start", description=use_text("start", msg)),
        BotCommand(command="save_reminder", description=use_text("save_reminder", msg)),
    ]
    await bot.set_my_commands(commands)


async def create_table_if_not_exists(conn, table_name, schema):
    """
    Create a table if it does not already exist.
    Args:
        conn: Database connection object.
        table_name (str): Name of the table.
        schema (str): SQL schema definition for the table.
    """
    await conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});")
