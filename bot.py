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

    dp.message.register(start.command_start, Command(commands=["start"]))
    dp.callback_query.register(options.callback_handler)

    # from aiogram.types import ContentType
    # dp.message.register(handle_text, lambda message: message.content_type == ContentType.TEXT)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await register_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
