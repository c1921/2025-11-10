from enum import Enum


class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class ActionType(str, Enum):
    """行动类型枚举"""
    REST = "rest"        # 休息
    LUMBERING = "lumbering"  # 伐木
    MINING = "mining"    # 采石
    GATHERING = "gathering"  # 采集浆果
    FARMING = "farming"  # 种植
    EAT = "eat"          # 进食
    ENTERTAINMENT = "entertainment"  # 娱乐
    IDLE = "idle"        # 空闲

