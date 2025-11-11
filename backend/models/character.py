from enum import Enum


class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class Character:
    """角色类"""
    def __init__(self, name: str, gender: Gender):
        self.name = name
        self.gender = gender
        # 状态值（0-100）
        self.fatigue = 0  # 疲劳度，0=精力充沛，100=极度疲劳
        self.hunger = 0   # 饥饿度，0=饱腹，100=极度饥饿
        self.mood = 100   # 心情，0=极度糟糕，100=极好

    def update_status(self):
        """每小时更新状态"""
        # 疲劳度增加
        self.fatigue = min(100, self.fatigue + 2)
        # 饥饿度增加
        self.hunger = min(100, self.hunger + 3)
        # 心情降低
        self.mood = max(0, self.mood - 1)

        # 如果饥饿或疲劳过高，心情额外降低
        if self.hunger > 70:
            self.mood = max(0, self.mood - 2)
        if self.fatigue > 70:
            self.mood = max(0, self.mood - 2)

    def get_status_dict(self) -> dict:
        """获取角色状态数据"""
        return {
            "name": self.name,
            "gender": self.gender.value,
            "fatigue": round(self.fatigue, 1),
            "hunger": round(self.hunger, 1),
            "mood": round(self.mood, 1),
            "status_text": self._get_status_text()
        }

    def _get_status_text(self) -> str:
        """获取状态描述"""
        status_parts = []

        if self.fatigue < 30:
            status_parts.append("精力充沛")
        elif self.fatigue < 60:
            status_parts.append("有些疲惫")
        else:
            status_parts.append("非常疲劳")

        if self.hunger < 30:
            status_parts.append("不饿")
        elif self.hunger < 60:
            status_parts.append("有点饿")
        else:
            status_parts.append("很饿")

        if self.mood > 70:
            status_parts.append("心情愉快")
        elif self.mood > 40:
            status_parts.append("心情一般")
        else:
            status_parts.append("心情低落")

        return "、".join(status_parts)
