from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class Venue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 基础信息
    management_unit: str = Field(title="管理单位")
    owner_unit: str = Field(title="场地产权单位")
    floor_type: str = Field(title="地面类型")
    address: str = Field(title="详细地址")
    # 联系方式
    contact_name: str = Field(title="联系人")
    contact_phone: str = Field(title="联系人电话")
    # 场地属性
    warranty_period: str = Field(title="保质时间")
    area_size: str = Field(title="场地面积")
    inspection_detail: str = Field(title="巡查情况")
    venue_type: str = Field(title="场地类型")
    # 设备信息
    equipment_type: str = Field(title="设备种类")
    equipment_brand: str = Field(title="设施品牌")
    venue_count: int = Field(default=1, title="场地数量")
    equipment_count: int = Field(default=0, title="设备数量")
    # 时间与媒体
    install_date: date = Field(title="安装时间")
    photo1: Optional[str] = Field(default=None, title="照片1 URL")
    photo2: Optional[str] = Field(default=None, title="照片2 URL")
    photo3: Optional[str] = Field(default=None, title="照片3 URL")
     # 建立与街道表的关联
    community_id: int = Field(foreign_key="community.id", title="所属社区ID")
    