from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

DATABASE_URL = settings.DATABASE_URL_asyncpg

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
