from typing import Any, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import SQLModel, Field, select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Contains, ST_GeomFromText
from typing import List
from sqlalchemy import Column
# 1. 数据库配置 (使用 asyncpg 异步驱动)
DATABASE_URL = "postgresql+asyncpg://postgres:mysecret@localhost/mysport"
engine = create_async_engine(DATABASE_URL, echo=True)

# 2. 依赖项：获取异步 Session
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

# 3. 定义地理模型 (SQLModel)
class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # 存储多边形范围 (SRID 4326 为全球经纬度标准)
    boundary: Any = Field(sa_column=Column(Geometry("POLYGON", srid=4326)))

app = FastAPI(title="巡查管理系统")

# 4. 接口示例：判定人员是否在场地内
@app.get("/check-location/")
async def check_location(
    lng: float, 
    lat: float, 
    session: AsyncSession = Depends(get_session)
):
    """
    输入经纬度，返回该人员所在的场地列表
    """
    # 构造 PostGIS 点坐标：ST_SetSRID(ST_MakePoint(经度, 纬度), 4326)
    point = f"SRID=4326;POINT({lng} {lat})"
    
    # 核心 SQL：查询哪个 Site 的 boundary 包含当前的 point
    statement = select(Site).where(
        func.ST_Contains(Site.boundary, ST_GeomFromText(point))
    )
    
    result = await session.execute(statement)
    sites = result.scalars().all()
    
    if not sites:
        return {"status": "outside", "message": "不在任何巡查区域内"}
    
    return {
        "status": "inside",
        "sites": [site.name for site in sites]
    }

# 启动脚本
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)