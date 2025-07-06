import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.application.containers.modules import MODULES
from src.utils.config import settings
from src.application.containers.container import container
from src.presentation.bot import get_all_dialogs, get_routers
from src.presentation.bot.middlewares.setup import setup_middlewares
from src.utils.logging import setup_logging


logger = logging.getLogger(__name__)

async def start_bot():
    bot: Bot = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp: Dispatcher = Dispatcher()
    
    commands = [
        BotCommand(command="/start", description="Старт бота"),
        BotCommand(command="/add", description="Добавить транзакцию"),
        BotCommand(command="/profile", description="Мой профиль"),
    ]
    await bot.set_my_commands(commands)

    container.wire(modules=MODULES)
    
    setup_middlewares(dp=dp, container=container)

    dp.include_routers(*get_routers())
    dp.include_routers(*get_all_dialogs())
    
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




async def main():
    setup_logging()

    await start_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot has been stopped")