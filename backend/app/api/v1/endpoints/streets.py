from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.street import Street  # 假设 Street 模型在 venue.py 中
from app.api.deps import get_session

router = APIRouter()

# --- 1. 创建 (Create) ---
@router.post("/", response_model=Street, status_code=status.HTTP_201_CREATED)
async def create_street(street: Street, session: AsyncSession = Depends(get_session)):
    # 检查重名（可选）
    statement = select(Street).where(Street.name == street.name)
    result = await session.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该街道名称已存在")
    
    session.add(street)
    await session.commit()
    await session.refresh(street)
    return street

# --- 2. 列表与搜索 (Index/List) ---
@router.get("/", response_model=List[Street])
async def read_streets(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    statement = select(Street)
    if name:
        statement = statement.where(col(Street.name).contains(name))
    
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

# --- 3. 更新 (Update) ---
@router.patch("/{street_id}", response_model=Street)
async def update_street(
    street_id: int, 
    street_data: dict, # 接收部分更新字段
    session: AsyncSession = Depends(get_session)
):
    db_street = await session.get(Street, street_id)
    if not db_street:
        raise HTTPException(status_code=404, detail="街道不存在")
    
    # 循环更新传入的字段
    for key, value in street_data.items():
        if hasattr(db_street, key):
            setattr(db_street, key, value)
            
    session.add(db_street)
    await session.commit()
    await session.refresh(db_street)
    return db_street

# --- 4. 删除 (Delete) ---
@router.delete("/{street_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_street(street_id: int, session: AsyncSession = Depends(get_session)):
    db_street = await session.get(Street, street_id)
    if not db_street:
        raise HTTPException(status_code=404, detail="街道不存在")
    
    # 注意：如果街道下有关联的社区，建议先检查是否存在关联
    await session.delete(db_street)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)