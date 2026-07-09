from aiogram import Router
from aiogram.types import Message

from ИИ.gemini import ask_gemini

router = Router()


@router.message()
async def chat(message: Message):
    try:
        response = await ask_gemini(message.text)
        await message.answer(response)
    except Exception:
        await message.answer("❌ Произошла ошибка. Попробуй позже.")
