from enum import Enum

class UserRole(str, Enum):
    CITIZEN = "CITIZEN"           # 群众
    INSPECTOR = "INSPECTOR"       # 巡查人员
    MAINTAINER = "MAINTAINER"     # 维修人员
    ADMIN = "ADMIN"               # 管理员
    CLIENT_ADMIN = "CLIENT_ADMIN" # 甲方管理员