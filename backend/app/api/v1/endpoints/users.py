from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from sqlmodel import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User  # 确保路径正确
from app.api.deps import get_session
# 导入之前定义的加密工具函数 (假设在 app.core.security 中)
from app.core.security import hash_password, verify_password, create_access_token 

router = APIRouter()

# response_model 使用 List[User] 来返回用户列表
@router.get("/", response_model=List[User])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    """
    获取所有用户信息
    """
    # 执行查询语句
    statement = select(User)
    result = await session.execute(statement)
    
    # 获取所有的 scalar 结果
    users = result.scalars().all()
    
    return users

# --- 1. 创建用户 (注册) ---
@router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    # 检查手机号是否已存在
    statement = select(User).where(User.phone == user.phone)
    result = await session.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该手机号已被注册")
    
    # 关键：对明文密码进行加密后再存入数据库
    user.password = hash_password(user.password)
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# --- 2. 登录逻辑 ---
@router.post("/token")
async def login(
    id: str = Form(...),           # 显式声明从表单获取
    password: str = Form(...),     # 显式声明从表单获取
    session: AsyncSession = Depends(get_session)
):
    print('login->id={id},password={password}')
    # 查找用户
    statement = select(User).where(
    or_(
            User.full_name == id, 
            User.phone == id
        )
    )
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    # 验证账号存在且密码匹配
    if not user or not verify_password(password, user.password):
        # 实际开发中可以增加 login_retry_count 计数逻辑
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="手机号或密码错误"
        )
    
    if user.is_disabled:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    # 重置失败次数 (如果之前有计数)
    user.login_retry_count = 0
    await session.commit()

    # 生成 JWT Token
    token = create_access_token({"sub": user.phone, "role": user.role})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user": {
            "name": user.full_name,
            "role": user.role
        }
    }

# --- 3. 分配角色 (修改角色) ---
@router.patch("/{user_id}/role")
async def assign_role(
    user_id: int, 
    new_role: str, 
    session: AsyncSession = Depends(get_session)
):
    """
    修改用户角色。在实际生产中，此接口应配合权限校验，仅限 ADMIN 调用。
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到该人员")
    
    user.role = new_role
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"msg": f"用户 {user.full_name} 的角色已更新为 {new_role}"}


# --- 4. 禁用/启用用户 (软删除/状态管理) ---
@router.patch("/{user_id}/status")
async def toggle_user_status(
    user_id: int, 
    is_disabled: bool, 
    session: AsyncSession = Depends(get_session)
):
    """
    禁用或启用用户账号：
    - is_disabled: true (停用) / false (启用)
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到该人员")
    
    user.is_disabled = is_disabled
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    status_msg = "已停用" if is_disabled else "已启用"
    return {"msg": f"用户 {user.full_name} {status_msg}"}

# --- 5. 删除用户 (物理删除) ---
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(get_session)
):
    """
    从数据库中物理删除用户。
    注意：在有业务关联（如已存在巡查单）的情况下，建议使用上面的禁用接口而非删除。
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="找不到该人员")
    
    await session.delete(user)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)