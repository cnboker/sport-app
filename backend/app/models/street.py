from typing import Optional
from sqlmodel import SQLModel, Field

class Street(SQLModel, table=True):
    __tablename__ = "street"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(title="街道名称", index=True) # 增加索引方便搜索
    contact_name: str = Field(title="联系人")
    contact_phone: str = Field(title="联系电话")
    region: str = Field(title="区域") # 例如：西湖区、滨江区等