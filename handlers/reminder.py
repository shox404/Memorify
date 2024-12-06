import uuid
import time
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from database.functions.reminder import set_reminder_data, schedule_reminder
from aiogram.types import ContentType, CallbackQuery, Message
from lang.function import use_text

user_data = {}


async def set_reminder(msg: CallbackQuery):
    user_id = msg.from_user.id
    user_data[user_id] = {"step": "waiting_for_task"}
    task_prompt = use_text("task_prompt", msg)
    await msg.answer(f"<b>{task_prompt}</b>")


async def handle_task_description(message: Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_task":
        task_text = message.text
        user_data[user_id]["task"] = task_text
        user_data[user_id]["step"] = "waiting_for_time"
        time_prompt = use_text("time_prompt", message)
        await message.answer(f"<b>{time_prompt}</b>")


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


async def register_reminder_command(dp: Dispatcher):
    dp.message.register(set_reminder, Command(commands=["set_reminder"]))
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
