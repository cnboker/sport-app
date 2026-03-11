from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select, col, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.venue import Venue, Community, Street  # 确保路径正确
from app.api.deps import get_session

router = APIRouter()

# --- 1. 创建 (Create) ---
@router.post("/", response_model=Venue, status_code=status.HTTP_201_CREATED)
async def create_venue(venue: Venue, session: AsyncSession = Depends(get_session)):
    # 校验：检查所属社区是否存在
    community = await session.get(Community, venue.community_id)
    if not community:
        raise HTTPException(status_code=400, detail="指定的社区 ID 不存在")
    
    # 校验：检查所属街道是否存在
    street = await session.get(Street, venue.street_id)
    if not street:
        raise HTTPException(status_code=400, detail="指定的街道 ID 不存在")

    session.add(venue)
    await session.commit()
    await session.refresh(venue)
    return venue

# --- 2. 列表、搜索与筛选 (Index/List) ---
@router.get("/", response_model=List[Venue])
async def read_venues(
    skip: int = 0,
    limit: int = 100,
    street_id: Optional[int] = None,    # 按街道筛选
    community_id: Optional[int] = None, # 按社区筛选
    search: Optional[str] = None,       # 按名称模糊搜索
    session: AsyncSession = Depends(get_session)
):
    statement = select(Venue)
    
    if street_id:
        statement = statement.where(Venue.street_id == street_id)
    if community_id:
        statement = statement.where(Venue.community_id == community_id)
    if search:
        statement = statement.where(col(Venue.name).contains(search))
    
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()

# --- 3. 获取单个详细信息 (Read One) ---
@router.get("/{venue_id}", response_model=Venue)
async def read_venue(venue_id: int, session: AsyncSession = Depends(get_session)):
    venue = await session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="场地不存在")
    return venue

# --- 4. 更新 (Update) ---
@router.patch("/{venue_id}", response_model=Venue)
async def update_venue(
    venue_id: int, 
    update_data: dict, 
    session: AsyncSession = Depends(get_session)
):
    db_venue = await session.get(Venue, venue_id)
    if not db_venue:
        raise HTTPException(status_code=404, detail="场地不存在")
    
    # 如果更新了社区或街道 ID，执行校验
    if "community_id" in update_data:
        if not await session.get(Community, update_data["community_id"]):
            raise HTTPException(status_code=400, detail="更新的社区 ID 不存在")
    if "street_id" in update_data:
        if not await session.get(Street, update_data["street_id"]):
            raise HTTPException(status_code=400, detail="更新的街道 ID 不存在")

    for key, value in update_data.items():
        if hasattr(db_venue, key):
            setattr(db_venue, key, value)
            
    session.add(db_venue)
    await session.commit()
    await session.refresh(db_venue)
    return db_venue

# --- 5. 删除 (Delete) ---
@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(venue_id: int, session: AsyncSession = Depends(get_session)):
    db_venue = await session.get(Venue, venue_id)
    if not db_venue:
        raise HTTPException(status_code=404, detail="场地不存在")
    
    await session.delete(db_venue)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)