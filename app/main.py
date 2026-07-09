from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.config import BOT_TOKEN
from app.database.database import database
from app.handlers.start import start
from app.handlers.help import help_command
from app.handlers.chat import chat


async def post_init(application: Application):
    await database.initialize()
    print("✅ Database initialized")


def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat,
        )
    )

    print("🚀 FIMA AI started")

    app.run_polling()


if __name__ == "__main__":
    main()
