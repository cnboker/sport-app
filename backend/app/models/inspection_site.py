from typing import Any, Optional
from sqlmodel import SQLModel, Field
from geoalchemy2 import Geometry
from sqlalchemy import Column

class InspectionSite(SQLModel, table=True):
    __tablename__ = "inspection_site" # 显式指定表名
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # 添加 srid=4326 (经纬度标准)，这在地理计算中非常重要
    area: Any = Field(sa_column=Column(Geometry("POLYGON", srid=4326)))