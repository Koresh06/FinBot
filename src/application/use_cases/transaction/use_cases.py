from dataclasses import dataclass

from src.application.uow.interfase import AbstractUnitOfWork
from src.domain.entities.transaction import TransactionEntity
from src.application.services.transactions.interface import ITransactionService
from src.application.services.users.interface import IUserService
from src.application.use_cases.intarface import UseCaseOneEntity


@dataclass
class AddTransactionDefaultUseCase(UseCaseOneEntity[TransactionEntity]):
    transac_service: ITransactionService
    user_service: IUserService
    uow: AbstractUnitOfWork

    async def execute(self, tg_id: int, data: dict) -> None:
        async with self.uow:
            user = await self.user_service.get_user_by_tg_id(tg_id)
            if user is None:
                raise ValueError(f"Пользователь с tg_id={tg_id} не найден")

            transaction = TransactionEntity(
                user_id=user.id,
                category_id=data["category"],
                amount=data["total_sum"],
                type=data["type"],
                comment=data["comment"],
            )
            await self.transac_service.add_transaction(user, transaction)
        
