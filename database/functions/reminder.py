import asyncpg
import time
from database.config import get_db_connection
from utils.creator import create_table_if_not_exists

async def save_reminder_data(data):
    conn = await get_db_connection()

    await conn.execute(
        """DROP TABLE IF EXISTS reminders"""
    )
    await create_table_if_not_exists(
        conn,
        "reminders",
        """
        id UUID PRIMARY KEY,
        task TEXT NOT NULL,
        reminder_time TIMESTAMP NOT NULL,
        user_id BIGINT NOT NULL
        """
    )

    # Insert reminder data into the table
    await conn.execute(
        """
        INSERT INTO reminders (id, task, reminder_time, user_id)
        VALUES ($1, $2, to_timestamp($3), $4)
        """,
        data["id"],
        data["task"],
        data["reminder_time"],
        data["user_id"],  # Insert the user ID
    )
    await conn.close()

# async def save_reminder_data(data):
#     conn = await get_db_connection()

#     await create_table_if_not_exists(
#         conn,
#         "reminders",
#         """
#         id UUID PRIMARY KEY,
#         task TEXT NOT NULL,
#         reminder_time TIMESTAMP NOT NULL
#         """
#     )

#     # Insert reminder data into the table
#     await conn.execute(
#         """
#         INSERT INTO reminders (id, task, reminder_time)
#         VALUES ($1, $2, to_timestamp($3))
#         """,
#         data["id"],
#         data["task"],
#         data["reminder_time"]
#     )
#     await conn.close()

# async def schedule_reminder(data):
#     """
#     Schedule a reminder to notify the user at the specified reminder_time.
#     """
#     current_time = time.time()
#     time_to_wait = data["reminder_time"] - current_time

#     print(time_to_wait)

#     if time_to_wait > 0:
#         await notify_user(data["id"], data["task"])
#     else:
#         print("Reminder time is in the past.")

from aiogram import Bot
import asyncio

async def schedule_reminder(reminder_data, bot: Bot):
    reminder_id = reminder_data["id"]
    task = reminder_data["task"]
    reminder_time = reminder_data["reminder_time"]

    delay = max(0, reminder_time - time.time())
    await asyncio.sleep(delay)
    await notify_user(reminder_id, task, bot)

# async def notify_user(reminder_id, task):
#     """
#     Notify the user about the reminder.

#     Args:
#         reminder_id (str): The unique ID of the reminder.
#         task (str): The task or message to remind the user about.
#     """
#     conn = await get_db_connection()

#     try:
#         # Retrieve the user's chat ID based on the reminder ID
#         reminder_data = await conn.fetchrow(
#             """
#             SELECT users.id AS user_id
#             FROM reminders
#             JOIN users ON reminders.user_id = users.id
#             WHERE reminders.id = $1
#             """,
#             reminder_id,
#         )

#         if not reminder_data:
#             print(f"Reminder with ID {reminder_id} not found.")
#             return

#         user_id = reminder_data["user_id"]

#         # Send a notification to the user
#         await Bot.get_current().send_message(user_id, f"Reminder: {task}")

#         print(f"Notification sent to user {user_id}: {task}")
#     except Exception as e:
#         print(f"Error notifying user: {e}")
#     finally:
#         await conn.close()
from database.config import get_db_connection

async def get_user_id_by_reminder(reminder_id):
    """
    Fetch the user_id associated with a specific reminder from the database.
    Args:
        reminder_id (str): The ID of the reminder.
    Returns:
        int: The user ID associated with the reminder or None if not found.
    """
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow(
            """
            SELECT user_id
            FROM reminders
            WHERE id = $1
            """,
            reminder_id,
        )
        return result["user_id"] if result else None
    finally:
        await conn.close()


async def notify_user(reminder_id, task, bot: Bot):
    try:
        # Logic to get the user ID and send a notification
        user_id = await get_user_id_by_reminder(reminder_id)  # Replace with actual logic
        if user_id:
            await bot.send_message(user_id, f"Reminder: {task}")
    except Exception as e:
        print(f"Error notifying user: {e}")
