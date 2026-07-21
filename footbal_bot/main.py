import asyncio

from telegram.ext import ApplicationBuilder

from config import BOT_TOKEN, logger
from services.data_manager import DataManager

from handlers import (
    start_handler,
    help_handler,
    scores_handler,
    fixtures_handler,
    update_handler,
)


async def main():

    logger.info("Bot başlatılıyor...")

    data_manager = DataManager()
    await data_manager.initialize()

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(start_handler())
    app.add_handler(help_handler())
    app.add_handler(scores_handler(data_manager))
    app.add_handler(fixtures_handler(data_manager))
    app.add_handler(update_handler(data_manager))

    logger.info("Bot çalışıyor...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())