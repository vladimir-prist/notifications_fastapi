from pydantic.v1 import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
from pydantic import ValidationError

load_dotenv()


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    database_url_sqlalchemy: str = os.getenv("DATABASE_URL_SQLALCHEMY")
    EMAIL_HOST: str = os.getenv("EMAIL_HOST")
    EMAIL_PORT: int = os.getenv("EMAIL_PORT")
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    print("Ошибка инициализации настроек. Проверьте файл .env или переменные окружения:")
    print(e)
    exit(1)


engine = create_async_engine(settings.database_url_sqlalchemy, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db
