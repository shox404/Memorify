import time
import asyncio
from database.config import get_db_connection
from utils.creator import create_table_if_not_exists
from aiogram import Bot


async def set_reminder_data(data):
    db = await get_db_connection()

    await create_table_if_not_exists(
        db,
        "reminders",
        """
        id UUID PRIMARY KEY,
        task TEXT NOT NULL,
        reminder_time TIMESTAMP NOT NULL,
        user_id BIGINT NOT NULL
        """,
    )

    await db.execute(
        """
        INSERT INTO reminders (id, task, reminder_time, user_id)
        VALUES ($1, $2, to_timestamp($3), $4)
        """,
        data["id"],
        data["task"],
        data["reminder_time"],
        data["user_id"],
    )
    await db.close()


async def schedule_reminder(reminder_data, bot: Bot):
    reminder_id = reminder_data["id"]
    reminder_time = reminder_data["reminder_time"]

    delay = max(0, reminder_time - time.time())
    await asyncio.sleep(delay)
    await notify_user(reminder_id, reminder_data, bot)


async def get_user_id_by_reminder(reminder_id):
    """Fetch the user_id associated with a specific reminder from the database."""

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


async def notify_user(reminder_id, reminder, bot: Bot):
    try:
        user_id = await get_user_id_by_reminder(reminder_id)
        if user_id:
            reminder_text = (
                f"<b>🌟 Hey! It's time to: {reminder['task']}</b>\n"
                f"<b>🔔 Set for: {time.strftime('%Y-%m-%d %H:%M', time.localtime(reminder['reminder_time']))}</b>"
            )
            await bot.send_message(user_id, reminder_text, parse_mode="HTML")
    except Exception as e:
        print(f"Error notifying user: {e}")
