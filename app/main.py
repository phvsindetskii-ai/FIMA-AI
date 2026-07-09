from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import BOT_TOKEN
from app.handlers.start import router as start_router
from app.handlers.chat import router as chat_router
from app.handlers.help import router as help_router
from app.database.database import database

import asyncio


async def main():

    await database.initialize()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(chat_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
