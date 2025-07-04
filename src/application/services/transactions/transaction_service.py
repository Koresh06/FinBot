from dataclasses import dataclass

from src.domain.entities.transaction import TransactionEntity
from src.domain.entities.user import UserEntity
from src.domain.repositories.transaction_repo_interface import ITransactionRepository
from src.domain.repositories.user_repo_intarface import IUserRepository
from src.application.services.transactions.interface import ITransactionService
from src.domain.value_objects.operetion_type_enum import OperationType


@dataclass
class TransactionServiceImpl(ITransactionService):

    transaction_repo: ITransactionRepository
    user_repo: IUserRepository

    async def add_transaction(self,user: UserEntity, transaction: TransactionEntity) -> TransactionEntity:
        if transaction.type == OperationType.expense:
            user.decrease_balance(transaction.amount)
        else:
            user.increase_balance(transaction.amount)
            
        await self.user_repo.update(user_update=user)
        return await self.transaction_repo.add(transaction)
