from dataclasses import dataclass, field

from src.application.uow.interfase import AbstractUnitOfWork
from src.domain.repositories.category_repo_interface import ICategoryRepository
from src.domain.repositories.transaction_repo_interface import ITransactionRepository
from src.domain.repositories.user_repo_intarface import IUserRepository
from src.domain.repositories.monthly_balance_interface import IMonthlyBalanceRepository


@dataclass(kw_only=True)
class InMemoryUnitOfWork(AbstractUnitOfWork):
    _user_repository: IUserRepository = field(repr=False)
    _category_repository: ICategoryRepository = field(repr=False)
    _transaction_repository: ITransactionRepository = field(repr=False)
    _monthly_balance_repository: IMonthlyBalanceRepository = field(repr=False)

    _snapshot: dict = field(default_factory=dict, init=False)
    _committed: bool = field(default=False, init=False)

    @property
    def user_repository(self) -> IUserRepository:
        return self._user_repository

    @property
    def category_repository(self) -> ICategoryRepository:
        return self._category_repository

    @property
    def transaction_repository(self) -> ITransactionRepository:
        return self._transaction_repository
    
    @property
    def monthly_balance_repository(self) -> IMonthlyBalanceRepository:
        return self._monthly_balance_repository

    async def __aenter__(self) -> "InMemoryUnitOfWork":
        self._snapshot['users'] = self._user_repository.snapshot()
        self._snapshot['categories'] = self._category_repository.snapshot()
        self._snapshot['transactions'] = self._transaction_repository.snapshot()
        self._snapshot['monthly_balance'] = self._monthly_balance_repository.snapshot()
        return self

    async def __aexit__(self, exc_type, exc_val, traceback) -> bool:
        if exc_type:
            await self.rollback()
            return False
        await self.commit()
        return True

    async def commit(self):
        self._committed = True
        self._snapshot.clear()

    async def rollback(self):
        self._user_repository.restore(self._snapshot['users'])
        self._category_repository.restore(self._snapshot['categories'])
        self._transaction_repository.restore(self._snapshot['transactions'])
        self._monthly_balance_repository.restore(self._snapshot['monthly_balance'])
        self._snapshot.clear()
