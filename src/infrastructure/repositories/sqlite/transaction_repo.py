from src.domain.repositories.transaction_use_case import ITransactionRepository
from src.domain.entities.transaction import TransactionEntity
from src.utils.mappers.transaction_mapper import db_to_domain, domain_to_db


class TransactionSQLiteRepositoryImpl(ITransactionRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def add(self, transaction: TransactionEntity) -> TransactionEntity:
        async with self.session_factory() as session:
            db_transation = domain_to_db(transaction)
            session.add(db_transation)
            await session.commit()
            await session.refresh(db_transation)
            return db_to_domain(db_transation)
