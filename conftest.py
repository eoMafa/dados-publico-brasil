import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from database import Base
import cache_model

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/dados_brasil_test"

engine_teste = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
SessionTeste = async_sessionmaker(engine_teste, expire_on_commit=False)


@pytest_asyncio.fixture
async def db_session():
    async with engine_teste.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionTeste() as session:
        yield session

    async with engine_teste.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)