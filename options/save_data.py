import uuid
from aiogram import types
from aiogram.types import CallbackQuery
from database.functions.data import save_simple_data

user_data = {}


async def save_data(cb_query: CallbackQuery):
    """
    Starts the data-saving process via callback query.
    Guides the user to upload an image.
    """
    user_id = cb_query.from_user.id
    user_data[user_id] = {"step": "waiting_for_image"}
    await cb_query.message.answer("Please upload an image to start the process.")


async def handle_image(message: types.Message):
    """
    Handles image uploads from the user.
    """
    user_id = message.from_user.id

    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_image":
        if message.photo:
            photo = message.photo[-1]
            file_id = photo.file_id

            user_data[user_id]["image"] = file_id
            user_data[user_id]["step"] = "waiting_for_text"

            await message.answer("Image received! Now, please send the text data.")
        else:
            await message.answer("Invalid input. Please upload an image.")
    else:
        await message.answer(
            "Please start the process again using the callback button."
        )


async def handle_text(message: types.Message):
    """
    Handles text input after the image has been uploaded.
    """
    user_id = message.from_user.id

    if user_id in user_data and user_data[user_id].get("step") == "waiting_for_text":
        text = message.text

        data_to_save = {
            "id": str(uuid.uuid4()),
            "image": user_data[user_id]["image"],
            "text": text,
        }

        try:
            await save_simple_data(data_to_save)
            await message.answer("Thank you! Your data has been saved successfully.")
        except Exception as e:
            await message.answer(f"An error occurred while saving your data: {e}")
            raise

        user_data.pop(user_id, None)
    else:
        await message.answer(
            "Unexpected input. Please start the process again using the callback button."
        )
