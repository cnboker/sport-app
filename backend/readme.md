### 初始化项目,Alembic 需要配置为异步模式才能与 asyncpg 协同工作
alembic init -t async migrations


# 生成记录脚本
alembic revision --autogenerate -m "create_initial_tables"

# 同步到数据库
alembic upgrade head
# 强制同步版本号（推荐）
alembic stamp head
### 启动 FastAPI
uvicorn main:app --reload

### sql cmd
```bash
sudo docker exec -it 1da4714b7ed7 psql -U postgres -d mysport
# 查看所有数据库
\l 
# 查看当前数据库下的所有表
\dt
# 切换到 mysport 数据库
\c mysport
#在 psql 提示符下，输入 \d 加上表名：
\d dictionary
```
