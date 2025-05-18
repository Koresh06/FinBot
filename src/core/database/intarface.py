from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from typing import AsyncGenerator


class IDatabase(ABC):
    @abstractmethod
    def get_engine(self) -> AsyncEngine:
        pass

    @abstractmethod
    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        pass

    @abstractmethod
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        pass
