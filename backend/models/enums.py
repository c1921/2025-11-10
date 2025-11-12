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


class TraitType(str, Enum):
    """特质类型枚举"""
    STRONG = "strong"                    # 强壮：劳动时疲劳消耗减少30%
    EFFICIENT_SLEEPER = "efficient_sleeper"  # 高效睡眠：休息时疲劳恢复提升50%
    GOOD_APPETITE = "good_appetite"      # 好胃口：进食时饥饿恢复提升30%
    CHEERFUL = "cheerful"                # 开朗：娱乐时心情恢复提升40%
    QUICK_LEARNER = "quick_learner"      # 手巧：劳动产出进度提升25%
    RESILIENT = "resilient"              # 坚韧：所有负面状态降低速度减少20%
    GOURMAND = "gourmand"                # 美食家：进食时额外恢复3点心情
    WORKAHOLIC = "workaholic"            # 工作狂：劳动时心情降低速度减少50%
