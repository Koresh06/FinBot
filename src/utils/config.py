from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseModel):
    host: str = "localhost"
    port: int = 8050

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class PostgresSQLConfig(BaseModel):
    name: str
    password: str
    user: str
    host: str
    port: int
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class SQLiteConfig(BaseModel):
    name: str
    path: str
    echo: bool = False
    in_memory: bool = False

    @property
    def url(self) -> str:
        if self.in_memory:
            return "sqlite+aiosqlite:///:memory:"
        return f"sqlite+aiosqlite:///{self.path}/{self.name}.db"


class RedisConfig(BaseModel):
    host: str
    port: int = 6379
    db: int = 0
    password: str | None = None

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class MongoConfig(BaseModel):
    host: str
    port: int = 27017
    db_name: str
    username: str | None = None
    password: str | None = None

    @property
    def url(self) -> str:
        credentials = f"{self.username}:{self.password}@" if self.username and self.password else ""
        return f"mongodb://{credentials}{self.host}:{self.port}/{self.db_name}"


class DatabaseConfig(BaseModel):
    db_type: str = "memory"  # Тип БД: postgres, sqlite, redis, mongo
    postgres: PostgresSQLConfig | None = None
    sqlite: SQLiteConfig | None = None
    redis: RedisConfig | None = None
    mongo: MongoConfig | None = None

    @property
    def connection_url(self) -> str:
        if self.db_type == "postgres" and self.postgres:
            return self.postgres.url
        elif self.db_type == "sqlite" and self.sqlite:
            return self.sqlite.url
        elif self.db_type == "redis" and self.redis:
            return str(self.redis.url)
        elif self.db_type == "mongo" and self.mongo:
            return str(self.mongo.url)
        elif self.db_type == "memory":
            return "memory://"
        else:
            raise ValueError(f"Unsupported db_type: {self.db_type}")



class TgBot(BaseModel):
    token: str = "token"


class GeminiApiKey(BaseModel):
    gemeni_api_key: str = "gemeni_api_key"
    model: str = "model"
    proxy: str = "proxy"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.dist", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    api_client: ApiConfig = ApiConfig()
    db: DatabaseConfig = DatabaseConfig()
    bot: TgBot = TgBot()
    ai: GeminiApiKey = GeminiApiKey()


settings = Settings()
