# import uuid
# import time
# from aiogram import types, Bot
# from database.functions.reminder import set_reminder_data, schedule_reminder
# from lang.function import use_text

# user_data = {}


# async def set_reminder(cb_query: types.CallbackQuery):
#     user_id = cb_query.from_user.id
#     user_data[user_id] = {"step": "waiting_for_task"}
#     text = use_text("reminder_task_description", cb_query)
#     await cb_query.message.answer(f"<b>{text}</b>")


# async def handle_task_description(message: types.Message):
#     user_id = message.from_user.id
#     if user_id in user_data and user_data[user_id].get("step") == "waiting_for_task":
#         task_text = message.text
#         user_data[user_id]["task"] = task_text
#         user_data[user_id]["step"] = "waiting_for_time"
#         text = use_text("reminder_time_prompt", message)
#         await message.answer(f"<b>{text}</b>")


# async def handle_time(message: types.Message, bot: Bot):
#     user_id = message.from_user.id
#     if user_id in user_data and user_data[user_id].get("step") == "waiting_for_time":
#         reminder_time_str = message.text
#         try:
#             reminder_time = time.mktime(
#                 time.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
#             )

#             user_data[user_id]["time"] = reminder_time
#             user_data[user_id]["step"] = "completed"
#             text = use_text("reminder_set_message", message)
#             await message.answer(
#                 f"<b>{text.format(reminder_time_str=reminder_time_str)}</b>"
#             )

#             reminder_data = {
#                 "id": str(uuid.uuid4()),
#                 "task": user_data[user_id]["task"],
#                 "reminder_time": user_data[user_id]["time"],
#                 "user_id": user_id,
#             }

#             await set_reminder_data(reminder_data)
#             await schedule_reminder(reminder_data, bot, message)
#             user_data.pop(user_id, None)
#         except ValueError:
#             text = use_text("invalid_time_format", message)
#             await message.answer(f"<b>{text}</b>")

import uuid
import time
from aiogram import types, Bot
from database.functions.reminder import set_reminder_data, schedule_reminder
from lang.function import use_text

user_data = {}
taskMsg = None
timeMsg = None


async def set_reminder(cb_query: types.CallbackQuery):
    user_id = cb_query.from_user.id
    user_data[user_id] = {"step": "waiting_for_task"}
    text = use_text("reminder_task_description", cb_query)
    global taskMsg
    taskMsg = await cb_query.message.answer(f"<b>{text}</b>")


async def handle_task_description(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_task":
        task_text = message.text
        user_data[user_id]["task"] = task_text
        if taskMsg:
            try:
                await taskMsg.delete()
                await message.delete()
            except Exception as e:
                print("Error deleting message!")
        user_data[user_id]["step"] = "waiting_for_time"
        text = use_text("reminder_time_prompt", message)
        global timeMsg
        timeMsg = await message.answer(f"<b>{text}</b>")


async def handle_time(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_time":
        reminder_time_str = message.text
        if timeMsg:
            try:
                await timeMsg.delete()
                await message.delete()
            except Exception as e:
                print("Error deleting message!")
        try:
            reminder_time = time.mktime(
                time.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
            )

            user_data[user_id]["time"] = reminder_time
            user_data[user_id]["step"] = "completed"
            text = use_text("reminder_set_message", message)
            await message.answer(
                f"<b>{text.format(reminder_time_str=reminder_time_str)}</b>"
            )

            reminder_data = {
                "id": str(uuid.uuid4()),
                "task": user_data[user_id]["task"],
                "reminder_time": user_data[user_id]["time"],
                "user_id": user_id,
            }

            await set_reminder_data(reminder_data)
            await schedule_reminder(reminder_data, bot, message)
            user_data.pop(user_id, None)
        except ValueError:
            text = use_text("invalid_time_format", message)
            await message.answer(f"<b>{text}</b>")
