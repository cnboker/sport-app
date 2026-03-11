from fastapi import FastAPI
from app.api.v1.api import api_router  # 导入聚合后的路由



app = FastAPI(title="巡查管理系统")

# 将所有的路由挂载到 /api/v1 路径下
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to My Sport App API"}




# 启动脚本
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)