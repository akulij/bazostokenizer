from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, session
from sqlalchemy.orm import sessionmaker
import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select, Field

async_engine = create_async_engine(
        # "mysql+aiomysql://akulijdev:rerfhtre@178.32.58.161:3306/yeezydirect?charset=utf8mb4",
        "sqlite+aiosqlite:///:memory:",
        echo=True,
        future=True
)
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

session: AsyncSession = async_session()


async def close_db_connection():
    session.close()

async def migrate():
   async with async_engine.begin() as conn:
       await conn.run_sync(SQLModel.metadata.create_all)
