from typing import Optional
from sqlmodel import SQLModel, Field

class Community(SQLModel, table=True):
    __tablename__ = "community"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(title="社区名称", index=True)
    contact_name: str = Field(title="联系人")
    contact_phone: str = Field(title="联系电话")
    address: str = Field(title="地址")
    
    # 建立与街道表的关联
    street_id: int = Field(foreign_key="street.id", title="所属街道ID")