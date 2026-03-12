from fastapi import FastAPI
from app.api.v1.api import api_router  # 导入聚合后的路由
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="巡查管理系统")
# 定义允许访问的源
# 在开发环境下，可以直接写 ["*"]，或者指定你的前端地址
origins = [
    "http://localhost:10086",
    "http://127.0.0.1:10086",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # 允许跨域的源列表
    allow_credentials=True,            # 允许携带 Cookie
    allow_methods=["*"],               # 允许所有的请求方法 (GET, POST, 等)
    allow_headers=["*"],               # 允许所有的请求头
)
# 将所有的路由挂载到 /api/v1 路径下
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to My Sport App API"}

# 启动脚本
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)