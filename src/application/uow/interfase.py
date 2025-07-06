from abc import ABC, abstractmethod

from src.domain.repositories.transaction_repo_interface import ITransactionRepository
from src.domain.repositories.category_repo_interface import ICategoryRepository
from src.domain.repositories.user_repo_intarface import IUserRepository
from src.domain.repositories.monthly_balance_interface import IMonthlyBalanceRepository


class AbstractUnitOfWork(ABC):

    @property
    @abstractmethod
    def user_repository(self) -> IUserRepository:
        pass

    @property
    @abstractmethod
    def category_repository(self) -> ICategoryRepository:
        pass

    @property
    @abstractmethod
    def transaction_repository(self) -> ITransactionRepository:
        pass

    @property
    @abstractmethod
    def monthly_balance_repository(self) -> IMonthlyBalanceRepository:
        pass
      
    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, traceback) -> bool:
        pass