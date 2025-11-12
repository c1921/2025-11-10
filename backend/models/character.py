"""角色模块 - 核心角色类"""
import uuid
from typing import TYPE_CHECKING, List
from .enums import Gender, ActionType, TraitType

if TYPE_CHECKING:
    from .item import Inventory


class Character:
    """角色类 - 负责角色基础属性和状态管理"""
    
    def __init__(self, name: str, gender: Gender, inventory_slots: int = 20, age_years: int = 25, age_days: int = 0, traits: List[TraitType] = None):
        self.id = str(uuid.uuid4())  # 生成唯一UUID
        self.name = name
        self.gender = gender
        # 年龄系统
        self.age_years = age_years  # 年龄（岁）
        self.age_days = age_days    # 年龄的天数部分（0-364）
        # 特质系统
        self.traits: List[TraitType] = traits if traits is not None else []
        # 状态值（0-100）
        self.fatigue = 100  # 疲劳度，100=精力充沛，0=极度疲劳
        self.hunger = 100   # 饥饿度，100=饱腹，0=极度饥饿
        self.mood = 100     # 心情，100=极好，0=极度糟糕
        # 行动相关
        self.current_action: ActionType = ActionType.REST  # 当前行动（初始为休息）
        self.action_duration = 0  # 行动持续时间（小时）
        # 劳动进度计数器（每种工作类型独立记录）
        self.work_progress = {
            ActionType.LUMBERING: 0,
            ActionType.MINING: 0,
            ActionType.GATHERING: 0,
            ActionType.FARMING: 0
        }
        # 背包系统
        from .item import Inventory
        self.inventory: Inventory = Inventory(max_slots=inventory_slots)
        # 物品字典引用（用于劳动产出）
        self.all_items_ref = None

    def update_status(self):
        """每小时更新状态"""
        from .action_system import ActionSystem
        from .trait_system import TraitSystem
        
        # 执行当前行动的效果
        ActionSystem.apply_action_effects(self)

        # 移除了 IDLE 空闲状态，角色总是在做事情

        # 如果饥饿或疲劳过低，心情额外降低 - 应用坚韧特质
        if self.hunger < 30:
            base_mood_penalty = -2
            mood_penalty = TraitSystem.apply_mood_change(self, base_mood_penalty, is_consumption=True)
            self.mood = max(0, self.mood + mood_penalty)
        if self.fatigue < 30:
            base_mood_penalty = -2
            mood_penalty = TraitSystem.apply_mood_change(self, base_mood_penalty, is_consumption=True)
            self.mood = max(0, self.mood + mood_penalty)

        # 行动持续时间增加
        self.action_duration += 1

    def assign_action(self, action: ActionType):
        """分配行动 - 委托给 ActionSystem"""
        from .action_system import ActionSystem
        ActionSystem.assign_action(self, action)

    def auto_assign_action(self):
        """根据角色状态自动分配行动 - 委托给 ActionSystem"""
        from .action_system import ActionSystem
        ActionSystem.auto_assign_action(self)

    def age_one_day(self):
        """年龄增长一天"""
        self.age_days += 1
        if self.age_days >= 365:
            self.age_years += 1
            self.age_days = 0

    def has_trait(self, trait: TraitType) -> bool:
        """检查是否拥有某个特质"""
        return trait in self.traits

    def get_trait_names(self) -> List[str]:
        """获取特质的中文名称列表"""
        from .trait_system import TraitSystem
        return [TraitSystem.get_trait_name(trait) for trait in self.traits]

    def use_item(self, item_id: str) -> bool:
        """使用物品"""
        # 检查是否拥有该物品
        if not self.inventory.has_item(item_id):
            return False

        # 获取物品效果
        for stack in self.inventory.items:
            if stack.item.item_id == item_id:
                effects = stack.item.effects
                
                # 应用效果
                if "fatigue" in effects:
                    self.fatigue = min(100, self.fatigue + effects["fatigue"])
                if "hunger" in effects:
                    self.hunger = min(100, self.hunger + effects["hunger"])
                if "mood" in effects:
                    self.mood = min(100, self.mood + effects["mood"])
                
                # 移除使用的物品
                self.inventory.remove_item(item_id, 1)
                return True

        return False

    def get_status_dict(self) -> dict:
        """获取角色状态数据"""
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender.value,
            "age_years": self.age_years,
            "age_days": self.age_days,
            "age_string": f"{self.age_years}岁+{self.age_days}天",
            "traits": [trait.value for trait in self.traits],
            "trait_names": self.get_trait_names(),
            "fatigue": round(self.fatigue, 1),
            "hunger": round(self.hunger, 1),
            "mood": round(self.mood, 1),
            "current_action": self.current_action.value,
            "action_duration": self.action_duration,
            "status_text": self._get_status_text(),
            "inventory": self.inventory.get_dict()
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
