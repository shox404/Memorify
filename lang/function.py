from lang.data import translations
from aiogram.types import Message


def use_text(type, message: Message):
    """Fetch the translation based on the user's language."""
 
    language = message.from_user.language_code
    return translations[type][language]
