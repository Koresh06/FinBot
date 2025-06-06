from src.domain.entities.transaction import TransactionEntity
from src.domain.services.transaction_service import ITransactionService
from src.domain.services.user_service_intarface import IUserService
from src.domain.use_case.base_use_case import BaseUseCase
from src.domain.use_case.intarface import UseCaseOneEntity


class AddTransactionDefaultUseCase(UseCaseOneEntity[TransactionEntity], BaseUseCase):
    def __init__(
        self,
        transac_service: ITransactionService,
        user_service: IUserService,
    ):
        self.transac_service = transac_service
        self.user_service = user_service

    async def execute(self, tg_id: int, data: dict) -> None:
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
        await self.transac_service.add_transaction(transaction)
        
        
