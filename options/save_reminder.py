import uuid
import time
from aiogram import types
from database.functions.reminder import save_reminder_data, schedule_reminder

user_data = {}


async def save_reminder(cb_query: types.CallbackQuery):
    user_id = cb_query.from_user.id
    user_data[user_id] = {"step": "waiting_for_task"}
    await cb_query.message.answer("Please describe your task or reminder.")


async def handle_task_description(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_task":
        task_text = message.text
        user_data[user_id]["task"] = task_text
        user_data[user_id]["step"] = "waiting_for_time"
        await message.answer(
            "Now, please send the time you want to be reminded (in the format 'YYYY-MM-DD HH:MM')."
        )


# async def handle_time(message: types.Message):
#     user_id = message.from_user.id
#     if user_id in user_data and user_data[user_id].get("step") == "waiting_for_time":
#         reminder_time_str = message.text
#         try:
#             reminder_time = time.mktime(
#                 time.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
#             )

#             user_data[user_id]["time"] = reminder_time
#             user_data[user_id]["step"] = "completed"
#             await message.answer(
#                 f"Your reminder for '{user_data[user_id]['task']}' is set for {reminder_time_str}."
#             )

#             reminder_data = {
#                 "id": str(uuid.uuid4()),
#                 "task": user_data[user_id]["task"],
#                 "reminder_time": user_data[user_id]["time"],
#             }

#             await save_reminder_data(reminder_data)
#             await schedule_reminder(reminder_data)
#             user_data.pop(user_id, None)
#         except ValueError:
#             await message.answer("Invalid time format. Please use 'YYYY-MM-DD HH:MM'.")
from aiogram import Bot 
async def handle_time(message: types.Message,bot:Bot):
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
                "user_id": user_id,  # Add the user ID
            }

            await save_reminder_data(reminder_data)
            await schedule_reminder(reminder_data,bot)
            user_data.pop(user_id, None)
        except ValueError:
            await message.answer("Invalid time format. Please use 'YYYY-MM-DD HH:MM'.")
