from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.application.services.categories.category_service import CategoryServiceImpl
from src.application.use_cases.transaction_use_cases import AddTransactionDefaultUseCase
from src.core.config import settings
from src.infrastructure.database.session.postgresql import PostgresSQLDatabaseHelper
from src.infrastructure.database.session.sqlite import SQLiteDatabaseHelper
from src.infrastructure.repositories.memory.category_repo import (
    CategoryMemoryRepositoryImpl,
)
from src.infrastructure.repositories.memory.transaction_repo import (
    TransactionMemoryRepositoryImpl,
)
from src.infrastructure.repositories.memory.user_repo import UserMemoryRepositoryImpl
from src.application.services.users.user_service import UserServiceImpl
from src.infrastructure.repositories.sqlite.category_repo import (
    CategorySQLiteRepositoryImpl,
)
from src.infrastructure.repositories.sqlite.transaction_repo import (
    TransactionSQLiteRepositoryImpl,
)
from src.infrastructure.repositories.sqlite.user_repo import UserSQLiteRepositoryImpl
from src.application.services.transactions.transaction_service import TransactionServiceImpl

from src.application.use_cases.user_use_cases import (
    RegisterUserUseCase,
    UpdateUserSettingsUseCase,
    GetUserByTgIdUseCase,
    SetUserMonthlyBudgetUseCase,
)
from src.application.use_cases.category_use_cases import (
    CreateCategoryUserUseCase,
    GetCategoriesOfUserUseCase,
)


def get_sqlite_sessionmaker(helper: SQLiteDatabaseHelper) -> async_sessionmaker[AsyncSession]:
    return helper.get_sessionmaker()

def get_postgres_sessionmaker(helper: PostgresSQLDatabaseHelper) -> async_sessionmaker[AsyncSession]:
    return helper.get_sessionmaker()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_type = providers.Object(settings.db.db_type)

    sqlite_helper = providers.Singleton(SQLiteDatabaseHelper)
    postgres_helper = providers.Singleton(PostgresSQLDatabaseHelper)

    sqlite_sessionmaker = providers.Callable(
        get_sqlite_sessionmaker,
        sqlite_helper,
    )
    postgres_sessionmaker = providers.Callable(
        get_postgres_sessionmaker,
        postgres_helper,
    )

    # --- Repositories ---
    user_repo = providers.Selector(
        db_type,
        memory=providers.Factory(UserMemoryRepositoryImpl),
        sqlite=providers.Factory(
            UserSQLiteRepositoryImpl,
            session_factory=sqlite_sessionmaker,
        ),
        postgres=providers.Factory(
            # UserPostgresRepositoryImpl,
            session_factory=postgres_sessionmaker,
        ),
    )
    category_repo = providers.Selector(
        db_type,
        memory=providers.Factory(CategoryMemoryRepositoryImpl),
        sqlite=providers.Factory(
            CategorySQLiteRepositoryImpl,
            session_factory=sqlite_sessionmaker,
        ),
        postgres=providers.Factory(
            # CategoryPostgresRepositoryImpl,
            session_factory=postgres_sessionmaker,
        ),
    )

    transaction_repo = providers.Selector(
        db_type,
        memory=providers.Factory(TransactionMemoryRepositoryImpl),
        sqlite=providers.Factory(
            TransactionSQLiteRepositoryImpl, session_factory=sqlite_sessionmaker
        ),
        postgres=providers.Factory(
            # TransactionPostgresRepositoryImpl,
            session_factory=postgres_sessionmaker,
        ),
    )

    # --- Services ---
    user_service = providers.Singleton(
        UserServiceImpl,
        repository=user_repo,
    )
    category_service = providers.Singleton(
        CategoryServiceImpl,
        category_repo=category_repo,
    )
    transac_service = providers.Singleton(
        TransactionServiceImpl,
        transaction_repo=transaction_repo,
    )

    # --- User use cases ---
    register_user_uc = providers.Factory(
        RegisterUserUseCase,
        user_service=user_service,
        category_service=category_service,
    )
    get_user_uc = providers.Factory(
        GetUserByTgIdUseCase,
        service=user_service,
    )
    update_user_stgs_uc = providers.Factory(
        UpdateUserSettingsUseCase,
        service=user_service,
    )
    set_budget_user_uc = providers.Factory(
        SetUserMonthlyBudgetUseCase,
        service=user_service,
    )

    # --- Category use cases ---
    get_categories_uc = providers.Factory(
        GetCategoriesOfUserUseCase,
        category_service=category_service,
        user_service=user_service,
    )
    create_category_uc = providers.Factory(
        CreateCategoryUserUseCase,
        category_service=category_service,
        user_service=user_service,
    )

    # --- Transaction use cases ---
    add_transac_uv = providers.Factory(
        AddTransactionDefaultUseCase,
        transac_service=transac_service,
        user_service=user_service,
    )


container = Container()
