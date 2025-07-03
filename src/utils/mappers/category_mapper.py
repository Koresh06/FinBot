from dataclasses import asdict
from src.domain.entities.category import CategoryEntity
from src.infrastructure.database.models.category import CategoryModel


def domain_to_db(category: CategoryEntity) -> CategoryModel:
    return CategoryModel(**asdict(category))

def db_to_domain(category: CategoryModel) -> CategoryEntity:
    return CategoryEntity(**category.model_dump())

