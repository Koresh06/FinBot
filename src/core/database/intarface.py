from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker


from contextlib import AbstractAsyncContextManager

class IDatabase(ABC):
    @abstractmethod
    def get_engine(self) -> AsyncEngine:
        ...

    @abstractmethod
    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        ...

    @abstractmethod
    def get_session(self) -> AbstractAsyncContextManager[AsyncSession]:
        ...
