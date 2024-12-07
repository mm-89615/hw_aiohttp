import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.models.base import Base

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
