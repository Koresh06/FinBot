from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy import AsyncAdaptedQueuePool

from src.utils.database.intarface import IDatabase
from src.utils.config import settings


class PostgresSQLDatabaseHelper(IDatabase):
    def __init__(self):
        self.engine = self.get_engine()
        self.sessionmaker = self.get_sessionmaker()

    def get_engine(self) -> AsyncEngine:
        return create_async_engine(
            url=settings.db.connection_url,
            query_cache_size=1200,
            poolclass=AsyncAdaptedQueuePool,
            pool_recycle=1800,
            pool_pre_ping=True,
            future=True,
            echo=False,
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
