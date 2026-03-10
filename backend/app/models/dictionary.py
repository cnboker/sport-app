# PostgreSQL 配合 SQLModel
from sqlmodel import SQLModel, Field

class Dictionary(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    dict_code: str = Field(index=True)  # 例如: "FAULT_LIST"
    item_key: str
    item_value: str
    sort_order: int = 0
    is_system: bool = False