import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
from options.save_data import register_saver

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"), default=None)
dp = Dispatcher()


async def register_handlers():
    from handlers import start

    dp.message.register(start.command_start, Command(commands=["start"]))

    from handlers import options

    dp.callback_query.register(options.callback_handler)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await register_handlers()
    register_saver(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
