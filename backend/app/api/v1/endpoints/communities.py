from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.venue import Community, Street  # 确保路径正确
from app.api.deps import get_session

router = APIRouter()

# --- 1. 创建 (Create) ---
@router.post("/", response_model=Community, status_code=status.HTTP_201_CREATED)
async def create_community(community: Community, session: AsyncSession = Depends(get_session)):
    # 核心校验：检查所属街道是否存在
    street = await session.get(Street, community.street_id)
    if not street:
        raise HTTPException(status_code=400, detail="所属街道不存在，请检查 street_id")
    
    # 检查同街道下社区名是否重复（可选）
    statement = select(Community).where(
        Community.name == community.name, 
        Community.street_id == community.street_id
    )
    result = await session.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该街道下已存在同名社区")
    
    session.add(community)
    await session.commit()
    await session.refresh(community)
    return community

# --- 2. 列表与搜索 (Index/List) ---
@router.get("/", response_model=List[Community])
async def read_communities(
    skip: int = 0,
    limit: int = 100,
    street_id: Optional[int] = None, # 支持按街道筛选
    name: Optional[str] = None,      # 支持按名称搜索
    session: AsyncSession = Depends(get_session)
):
    statement = select(Community)
    if street_id:
        statement = statement.where(Community.street_id == street_id)
    if name:
        statement = statement.where(col(Community.name).contains(name))
    
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

# --- 3. 更新 (Update) ---
@router.patch("/{community_id}", response_model=Community)
async def update_community(
    community_id: int, 
    update_data: dict, 
    session: AsyncSession = Depends(get_session)
):
    db_community = await session.get(Community, community_id)
    if not db_community:
        raise HTTPException(status_code=404, detail="社区不存在")
    
    # 如果修改了 street_id，需要再次校验
    if "street_id" in update_data:
        street = await session.get(Street, update_data["street_id"])
        if not street:
            raise HTTPException(status_code=400, detail="更新的 street_id 不存在")

    for key, value in update_data.items():
        if hasattr(db_community, key):
            setattr(db_community, key, value)
            
    session.add(db_community)
    await session.commit()
    await session.refresh(db_community)
    return db_community

# --- 4. 删除 (Delete) ---
@router.delete("/{community_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_community(community_id: int, session: AsyncSession = Depends(get_session)):
    db_community = await session.get(Community, community_id)
    if not db_community:
        raise HTTPException(status_code=404, detail="社区不存在")
    
    await session.delete(db_community)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)