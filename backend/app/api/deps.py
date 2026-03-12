from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

# 1. 数据库配置 (使用 asyncpg 异步驱动)
DATABASE_URL = "postgresql+asyncpg://postgres:mysecret@localhost/mysport"
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. 依赖项：获取异步 Session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session   