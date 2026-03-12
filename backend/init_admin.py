import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session,engine
from app.models.user import User
from app.core.security import hash_password


async def create_admin_direct():
    # 1. 获取异步 Session 工厂
    # 注意：在脚本中我们跳过 FastAPI 的 Depends 逻辑，直接手动管理 session
    async with AsyncSession(engine) as session:
        async with session.begin():
            # 2. 检查管理员是否已存在
            from sqlalchemy import select
            existing_admin = await session.execute(select(User).where(User.full_name == "admin"))
            if existing_admin.scalar_one_or_none():
                print("管理员帐号 admin 已存在，无需创建。")
                return

            # 3. 创建新管理员对象
            # 提示：务必对密码进行 Hash 加密，不要存明文 111111
            admin_user = User(
                full_name="admin",
                phone="18938919024", # 随便填个格式正确的手机号
                password=hash_password("111111"), # 假设你有这个函数
                role="管理员"         # 方便你后续做权限控制
            )

            session.add(admin_user)
            # 4. 提交到数据库
            await session.commit()
            print("管理员帐号 admin (密码: 111111) 创建成功！")

if __name__ == "__main__":
    asyncio.run(create_admin_direct())