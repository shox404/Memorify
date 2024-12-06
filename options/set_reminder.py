import uuid
import time
from aiogram import types, Bot
from database.functions.reminder import set_reminder_data, schedule_reminder
from lang.function import use_text

user_data = {}


async def handle_time(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_time":
        reminder_time_str = message.text
        try:
            reminder_time = time.mktime(
                time.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
            )

            user_data[user_id]["time"] = reminder_time
            user_data[user_id]["step"] = "completed"
            reminder_time_str = time.strftime(
                "%Y-%m-%d %H:%M", time.localtime(reminder_time)
            )

            reminder_message = use_text("reminder_set", message).format(
                time=reminder_time_str
            )
            await message.answer(f"<b>{reminder_message}</b>")

            reminder_data = {
                "id": str(uuid.uuid4()),
                "task": user_data[user_id]["task"],
                "reminder_time": user_data[user_id]["time"],
                "user_id": user_id,
            }

            await set_reminder_data(reminder_data)
            await schedule_reminder(reminder_data, bot)
            user_data.pop(user_id, None)
        except ValueError:
            invalid_time_message = use_text("invalid_time_format", message)
            await message.answer(f"<b>{invalid_time_message}</b>")
