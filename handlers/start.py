from aiogram.types import InlineKeyboardMarkup, Message
from lang.function import use_text
from utils.creator import inline_btn, set_commands
from database.functions.user import insert_user_data


async def command_start(msg: Message):
    user = msg.from_user

    await msg.answer(use_text("welcome", msg))

    await set_commands(msg)

    user_id = user.id
    username = user.username or "NoUsername"

    user_data = {"id": user_id, "username": username, "first_name": user.first_name}

    await insert_user_data(user_data)

    board = InlineKeyboardMarkup(
        inline_keyboard=[
            [inline_btn("save_reminder", msg)],
        ]
    )

    await msg.answer(use_text("choose_option", msg), reply_markup=board)
