from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:mysecret@localhost/mysport"
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建异步 Session 工厂
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)