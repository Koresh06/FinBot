from dataclasses import dataclass

from src.domain.entities.transaction import TransactionEntity
from src.domain.entities.user import UserEntity
from src.domain.repositories.transaction_repo_interface import ITransactionRepository
from src.domain.repositories.user_repo_intarface import IUserRepository
from src.application.services.transactions.interface import ITransactionService


@dataclass
class TransactionServiceImpl(ITransactionService):

    transaction_repo: ITransactionRepository
    user_repo: IUserRepository

    async def add_transaction(self, user: UserEntity, transaction: TransactionEntity) -> TransactionEntity:
        await self.user_repo.update(user_update=user)
        return await self.transaction_repo.add(transaction)
