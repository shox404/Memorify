from lang.function import use_text
from aiogram.types import CallbackQuery
from options.set_reminder import set_reminder


async def callback_handler(cb_query: CallbackQuery):
    callback_data = cb_query.data

    await cb_query.answer()

    if callback_data == "set_reminder":
        await set_reminder(cb_query)
    else:
        response_text = use_text("option_not_recognized", cb_query)
        await cb_query.message.answer(response_text)
