from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://root:123@localhost:5433/meu_banco"
    DBBaseModel: ClassVar = declarative_base()
    # Create by secrets
    JWT_SECRET: str = "R8Q7NzJ0c-TkG-7wMIVWelUQDFHckH1tm0BUObOr738"
    ALGORITH: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive: bool = True


settings: Settings = Settings()
