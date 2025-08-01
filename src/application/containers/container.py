from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.application.services.categories.category_service import CategoryServiceImpl
from src.application.services.monthly_balance.monthly_balance_service import MonthlyBalanceServiceImpl
from src.application.use_cases.monthly_balance.use_cases import GetMonthlyBalanceUseCase
from src.application.use_cases.transaction.use_cases import AddTransactionUseCase
from src.infrastructure.repositories.memory.monthly_balance_repo import MonthlyBalanceMemoryRepositoryImpl
from src.application.uow.uow import InMemoryUnitOfWork
from src.utils.config import settings
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
from src.application.services.transactions.transaction_service import (
    TransactionServiceImpl,
)

from src.application.use_cases.user.use_cases import (
    RegisterUserUseCase,
    # UpdateUserSettingsUseCase,
    GetUserByTgIdUseCase,
    # SetUserMonthlyBudgetUseCase,
)
from src.application.use_cases.category.use_cases import (
    CreateCategoryUserUseCase,
    GetAllGetegoriesUserUseCase,
    GetCategoriesOfUserUseCase,
)


def get_sqlite_sessionmaker(
    helper: SQLiteDatabaseHelper,
) -> async_sessionmaker[AsyncSession]:
    return helper.get_sessionmaker()


def get_postgres_sessionmaker(
    helper: PostgresSQLDatabaseHelper,
) -> async_sessionmaker[AsyncSession]:
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
        memory=providers.Singleton(UserMemoryRepositoryImpl),
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
        memory=providers.Singleton(CategoryMemoryRepositoryImpl),
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
        memory=providers.Singleton(TransactionMemoryRepositoryImpl),
        sqlite=providers.Factory(
            TransactionSQLiteRepositoryImpl, session_factory=sqlite_sessionmaker
        ),
        postgres=providers.Factory(
            # TransactionPostgresRepositoryImpl,
            session_factory=postgres_sessionmaker,
        ),
    )
    
    monthly_balance_repo = providers.Selector(
        db_type,
        memory=providers.Singleton(MonthlyBalanceMemoryRepositoryImpl),
    )

    # --- UoW ---
    in_memory_uow = providers.Factory(
        InMemoryUnitOfWork,
        _user_repository=user_repo,
        _category_repository=category_repo,
        _transaction_repository=transaction_repo,
        _monthly_balance_repository=monthly_balance_repo,
    )

    # --- Services ---
    user_service = providers.Singleton(
        UserServiceImpl,
        user_repo=user_repo,
    )
    category_service = providers.Singleton(
        CategoryServiceImpl,
        category_repo=category_repo,
    )
    transac_service = providers.Singleton(
        TransactionServiceImpl,
        transaction_repo=transaction_repo,
        monthly_balance_repo=monthly_balance_repo
    )
    monthly_balance_service = providers.Singleton(
        MonthlyBalanceServiceImpl,
        monthly_balance_repo=monthly_balance_repo,
    )

    # --- User use cases ---
    register_user_uc = providers.Factory(
        RegisterUserUseCase,
        user_service=user_service,
        category_service=category_service,
        # uow=in_memory_uow,
    )
    get_user_uc = providers.Factory(
        GetUserByTgIdUseCase,
        user_service=user_service,
        # uow=in_memory_uow,
    )
    # update_user_stgs_uc = providers.Factory(
    #     UpdateUserSettingsUseCase,
    #     user_service=user_service,
    # )
    # set_budget_user_uc = providers.Factory(
    #     SetUserMonthlyBudgetUseCase,
    #     user_service=user_service,
    # )

    # --- Category use cases ---
    get_categories_uc = providers.Factory(
        GetCategoriesOfUserUseCase,
        category_service=category_service,
        user_service=user_service,
        # uow=in_memory_uow,
    )
    create_category_uc = providers.Factory(
        CreateCategoryUserUseCase,
        category_service=category_service,
        user_service=user_service,
        # uow=in_memory_uow,
    )
    get_all_categories_uc = providers.Factory(
        GetAllGetegoriesUserUseCase,
        category_service=category_service,
    )

    # --- Transaction use cases ---
    add_transaction_uc = providers.Factory(
        AddTransactionUseCase,
        transac_service=transac_service,
        monthly_balance_service=monthly_balance_service,
        uow=in_memory_uow,
    )

    # --- MonthlyBalance use cases ---
    get_monthly_balance_uc = providers.Factory(
        GetMonthlyBalanceUseCase,
        monthly_balance_service=monthly_balance_service,
    )


container = Container()
