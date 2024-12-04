from lang.function import use_text
from aiogram.types import CallbackQuery
from options.save_data import save_data


async def callback_handler(cb_query: CallbackQuery):
    callback_data = cb_query.data

    await cb_query.answer()

    if callback_data == "save_data":
        await save_data(cb_query)
    else:
        response_text = use_text("option_not_recognized", {"user_id": cb_query.from_user.id})
        await cb_query.message.answer(response_text)

