from typing import cast
from aiogram import Dispatcher

from src.presentation.bot.middlewares.container import ContainerMiddleware
from src.presentation.bot.middlewares.db_session import DbSessionMiddleware
from src.application.containers.container import Container


def setup_middlewares(
    dp: Dispatcher,
    container: Container,
):
    db_type: str = container.db_type()

    if db_type in ("sqlite", "postgres"):
        from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

        sessionmaker_provider = cast(
            async_sessionmaker[AsyncSession],
            {
                "sqlite": container.sqlite_sessionmaker,
                "postgres": container.postgres_sessionmaker,
            }[db_type]
        )

        dp.update.outer_middleware(DbSessionMiddleware(sessionmaker=sessionmaker_provider))

    dp.update.middleware(ContainerMiddleware(container=container))
