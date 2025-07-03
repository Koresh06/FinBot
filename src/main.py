import logging
import asyncio

from src.presentation.bot.bot import start_bot
from src.utils.logging import setup_logging


logger = logging.getLogger(__name__)


async def main():
    setup_logging()

    await start_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot has been stopped")