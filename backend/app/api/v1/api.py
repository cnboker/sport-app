from fastapi import APIRouter
from app.api.v1.endpoints import users
from backend.app.api.v1.endpoints import communities, streets, venues  # 导入刚才写的 users 模块

api_router = APIRouter()

# 注册用户模块，并给它加一个前缀
api_router.include_router(users.router, prefix="/users", tags=["用户管理"]) 
api_router.include_router(streets.router, prefix="/streets", tags=["基础数据-街道"])
api_router.include_router(communities.router, prefix="/communities", tags=["基础数据-社区"])
api_router.include_router(venues.router, prefix="/venues", tags=["场地管理"])