from datetime import datetime
from typing import Optional, Any
from sqlmodel import SQLModel, Field, Column

class Maintenance(SQLModel, table=True):
    __tablename__ = "maintenance"

    id: Optional[int] = Field(default=None, primary_key=True)
    inspection_id: int = Field(foreign_key="inspection.id", title="关联巡查单ID")
    venue_id: int = Field(foreign_key="venue.id", title="关联场地ID")
    
    # 维修流程
    maintainer_name: Optional[str] = Field(default=None, title="维修人员姓名")
    issue_type: str = Field(title="故障类型") # 如：器械断裂、地面破损
    maintenance_status: str = Field(default="pending", title="维修状态") # pending, repairing, completed
    
    # 结果记录
    action_taken: Optional[str] = Field(default=None, title="维修措施")
    thumb_photo: Optional[str] = Field(default=None, title="缩微图片")
    completion_photo1: Optional[str] = Field(default=None, title="维修后照片")
    completion_photo2: Optional[str] = Field(default=None, title="维修后照片")
    completion_photo3: Optional[str] = Field(default=None, title="维修后照片")
    completion_photo4: Optional[str] = Field(default=None, title="维修后照片")
    create_at: datetime = Field(default_factory=datetime.now,title="维修单创建时间")
    reported_at: datetime = Field(default_factory=datetime.now, title="报修时间")
    finished_at: Optional[datetime] = Field(default=None, title="完成时间")