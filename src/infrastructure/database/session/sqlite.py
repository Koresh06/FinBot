from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from typing import AsyncGenerator

from src.utils.database.intarface import IDatabase
from src.utils.config import settings


class SQLiteDatabaseHelper(IDatabase):
    def __init__(self):
        self.engine = self.get_engine()
        self.sessionmaker = self.get_sessionmaker()

    def get_engine(self) -> AsyncEngine:
        return create_async_engine(
            url=settings.db.connection_url,
            echo=settings.db.sqlite.echo if settings.db.sqlite else False,
        )

    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.sessionmaker() as session:
            yield session
