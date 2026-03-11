from datetime import datetime
from typing import Optional, Any
from sqlmodel import SQLModel, Field, Column
from geoalchemy2 import Geometry

#巡查单
class Inspection(SQLModel, table=True):
    __tablename__ = "inspection"

    id: Optional[int] = Field(default=None, primary_key=True)
    venue_id: int = Field(foreign_key="venue.id", title="所属场地ID")
    inspector_id: int = Field(title="巡查人员ID") # 关联你的用户表
    
    # 地理信息：巡查时的实时坐标点，用于核实是否在场
    current_location: Any = Field(sa_column=Column(Geometry("POINT", srid=4326)))
    
    # 业务字段
    status: int = Field(default="normal", title="设备状态") # normal: 正常, damaged: 损坏
    description: Optional[str] = Field(default=None, title="巡查备注")
    photo_url1: Optional[str] = Field(default=None, title="巡查现场照")
    photo_url2: Optional[str] = Field(default=None, title="巡查现场照")
    photo_url3: Optional[str] = Field(default=None, title="巡查现场照")
    photo_url4: Optional[str] = Field(default=None, title="巡查现场照")
    
    created_at: datetime = Field(default_factory=datetime.now, title="巡查单创建日期")
    inspection_time: datetime = Field(default_factory=datetime.now, title="巡查时间")