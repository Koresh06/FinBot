import copy
from src.application.uow.interfase import AbstractUnitOfWork
from src.domain.repositories.category_repo_interface import ICategoryRepository
from src.domain.repositories.transaction_repo_interface import ITransactionRepository
from src.domain.repositories.user_repo_intarface import IUserRepository


class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        user_repository: IUserRepository,
        category_repository: ICategoryRepository,
        transaction_repository: ITransactionRepository,
    ):
        self._user_repository = user_repository
        self._category_repository = category_repository
        self._transaction_repository = transaction_repository
        self._committed = False

        self._snapshot = {}

    @property
    def user_repository(self) -> IUserRepository:
        return self._user_repository

    @property
    def category_repository(self) -> ICategoryRepository:
        return self._category_repository

    @property
    def transaction_repository(self) -> ITransactionRepository:
        return self._transaction_repository

    async def __aenter__(self) -> "InMemoryUnitOfWork":
        self._snapshot['users'] = self._user_repository.snapshot()
        self._snapshot['categories'] = self._category_repository.snapshot()
        self._snapshot['transactions'] = self._transaction_repository.snapshot()
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
        self._snapshot.clear()