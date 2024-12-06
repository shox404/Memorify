import uuid
import time
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from database.functions.reminder import save_reminder_data, schedule_reminder
from aiogram.types import ContentType, CallbackQuery, Message

user_data = {}


async def set_reminder(msg: CallbackQuery):
    user_id = msg.from_user.id
    user_data[user_id] = {"step": "waiting_for_task"}
    await msg.answer("Please describe your task or reminder.")


async def handle_task_description(message: Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_task":
        task_text = message.text
        user_data[user_id]["task"] = task_text
        user_data[user_id]["step"] = "waiting_for_time"
        await message.answer(
            "Now, please send the time you want to be reminded (in the format 'YYYY-MM-DD HH:MM')."
        )


async def handle_time(message: Message, bot: Bot):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_time":
        reminder_time_str = message.text
        try:
            reminder_time = time.mktime(
                time.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
            )

            user_data[user_id]["time"] = reminder_time
            user_data[user_id]["step"] = "completed"
            await message.answer(
                f"Your reminder for '{user_data[user_id]['task']}' is set for {reminder_time_str}."
            )

            reminder_data = {
                "id": str(uuid.uuid4()),
                "task": user_data[user_id]["task"],
                "reminder_time": user_data[user_id]["time"],
                "user_id": user_id,
            }

            await save_reminder_data(reminder_data)
            await schedule_reminder(reminder_data, bot)
            user_data.pop(user_id, None)
        except ValueError:
            await message.answer("Invalid time format. Please use 'YYYY-MM-DD HH:MM'.")


async def register_reminder_command(dp: Dispatcher):
    dp.message.register(set_reminder, Command(commands=["save_reminder"]))
    dp.message.register(
        handle_task_description,
        lambda message: message.content_type == ContentType.TEXT
        and "step" in user_data.get(message.from_user.id, {})
        and user_data[message.from_user.id]["step"] == "waiting_for_task",
    )
    dp.message.register(
        handle_time,
        lambda message: message.content_type == ContentType.TEXT
        and "step" in user_data.get(message.from_user.id, {})
        and user_data[message.from_user.id]["step"] == "waiting_for_time",
    )
