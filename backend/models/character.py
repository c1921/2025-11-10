from enum import Enum


class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class ActionType(str, Enum):
    """行动类型枚举"""
    REST = "rest"        # 休息
    WORK = "work"        # 劳动
    EAT = "eat"          # 进食
    ENTERTAINMENT = "entertainment"  # 娱乐
    IDLE = "idle"        # 空闲


class Character:
    """角色类"""
    def __init__(self, name: str, gender: Gender):
        self.name = name
        self.gender = gender
        # 状态值（0-100）
        self.fatigue = 100  # 疲劳度，100=精力充沛，0=极度疲劳
        self.hunger = 100   # 饥饿度，100=饱腹，0=极度饥饿
        self.mood = 100     # 心情，100=极好，0=极度糟糕
        # 行动相关
        self.current_action: ActionType = ActionType.IDLE  # 当前行动
        self.action_duration = 0  # 行动持续时间（小时）

    def update_status(self):
        """每小时更新状态"""
        # 执行当前行动的效果
        self._apply_action_effects()

        # 自然状态变化（没有行动时的自然降低）
        if self.current_action == ActionType.IDLE:
            self.fatigue = max(0, self.fatigue - 2)  # 疲劳度自然降低（没有休息恢复得慢）
            self.hunger = max(0, self.hunger - 3)     # 饥饿度自然降低
            self.mood = max(0, self.mood - 1)         # 心情自然降低

        # 如果饥饿或疲劳过低，心情额外降低
        if self.hunger < 30:
            self.mood = max(0, self.mood - 2)
        if self.fatigue < 30:
            self.mood = max(0, self.mood - 2)

        # 行动持续时间增加
        if self.current_action != ActionType.IDLE:
            self.action_duration += 1

    def _apply_action_effects(self):
        """应用行动效果"""
        if self.current_action == ActionType.REST:
            # 休息恢复疲劳
            self.fatigue = min(100, self.fatigue + 10)
            self.hunger = max(0, self.hunger - 1)  # 休息时也会饿

        elif self.current_action == ActionType.EAT:
            # 进食恢复饥饿
            self.hunger = min(100, self.hunger + 100)
            self.fatigue = max(0, self.fatigue - 1)  # 进食会消耗一点精力

        elif self.current_action == ActionType.ENTERTAINMENT:
            # 娱乐恢复心情
            self.mood = min(100, self.mood + 8)
            self.fatigue = max(0, self.fatigue - 2)  # 娱乐会消耗精力
            self.hunger = max(0, self.hunger - 2)    # 娱乐会消耗饥饿

        elif self.current_action == ActionType.WORK:
            # 劳动消耗疲劳和饥饿，但不直接影响心情
            self.fatigue = max(0, self.fatigue - 5)
            self.hunger = max(0, self.hunger - 4)

    def assign_action(self, action: ActionType):
        """分配行动"""
        self.current_action = action
        self.action_duration = 0

    def auto_assign_action(self):
        """根据角色状态自动分配行动"""
        # 优先级：饥饿 > 疲劳 > 心情

        # 如果当前正在休息，持续到疲劳值90以上再切换
        if self.current_action == ActionType.REST and self.fatigue < 90:
            return  # 继续休息，不切换状态
        
        # 如果饥饿度低于40，去进食
        if self.hunger < 40:
            self.assign_action(ActionType.EAT)
        # 如果疲劳度低于40，去休息
        elif self.fatigue < 40:
            self.assign_action(ActionType.REST)
        # 如果心情低于50，去娱乐
        elif self.mood < 50:
            self.assign_action(ActionType.ENTERTAINMENT)
        # 如果状态都还不错，可以劳动
        elif self.fatigue > 60 and self.hunger > 60:
            self.assign_action(ActionType.WORK)
        # 否则空闲
        else:
            self.assign_action(ActionType.IDLE)

    def get_status_dict(self) -> dict:
        """获取角色状态数据"""
        return {
            "name": self.name,
            "gender": self.gender.value,
            "fatigue": round(self.fatigue, 1),
            "hunger": round(self.hunger, 1),
            "mood": round(self.mood, 1),
            "current_action": self.current_action.value,
            "action_duration": self.action_duration,
            "status_text": self._get_status_text()
        }

    def _get_status_text(self) -> str:
        """获取状态描述"""
        status_parts = []

        # 疲劳度（100=精力充沛，0=极度疲劳）
        if self.fatigue > 70:
            status_parts.append("精力充沛")
        elif self.fatigue > 40:
            status_parts.append("有些疲惫")
        else:
            status_parts.append("非常疲劳")

        # 饥饿度（100=饱腹，0=极度饥饿）
        if self.hunger > 70:
            status_parts.append("不饿")
        elif self.hunger > 40:
            status_parts.append("有点饿")
        else:
            status_parts.append("很饿")

        # 心情（100=极好，0=极度糟糕）
        if self.mood > 70:
            status_parts.append("心情愉快")
        elif self.mood > 40:
            status_parts.append("心情一般")
        else:
            status_parts.append("心情低落")

        return "、".join(status_parts)
