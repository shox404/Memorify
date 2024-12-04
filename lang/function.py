from lang.data import translations
from aiogram.types import Message

def use_text(type, message: Message):
    language = message.from_user.language_code
    return translations[type][language]