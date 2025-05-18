from dataclasses import asdict
from src.domain.entities.transaction import TransactionEntity
from src.infrastructure.database.models.transaction import TransactionModel



def db_to_domain(transaction: TransactionModel) -> TransactionEntity:
    return TransactionEntity(**transaction.model_dump())

def domain_to_db(transaction: TransactionEntity) -> TransactionModel:
    return TransactionModel(**asdict(transaction))

