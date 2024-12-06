import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), default=None)
dp = Dispatcher()


async def register_handlers():
    from handlers import start, options
    from aiogram.types import ContentType
    from options.save_reminder import handle_time, handle_task_description, user_data
    from handlers.reminder import register_reminder_command

    # dp.message.register(
    #     reminder.command_set_reminder, Command(commands=["save_reminder"])
    # )

    await register_reminder_command(dp)
    dp.message.register(start.command_start, Command(commands=["start"]))
    dp.callback_query.register(options.callback_handler)

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


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await register_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
