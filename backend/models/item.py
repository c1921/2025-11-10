from enum import Enum
from typing import Optional


class ItemCategory(str, Enum):
    """物品类别枚举"""
    FOOD = "food"           # 食物
    TOOL = "tool"           # 工具
    MATERIAL = "material"   # 材料
    EQUIPMENT = "equipment" # 装备
    CONSUMABLE = "consumable" # 消耗品
    MISC = "misc"          # 杂项


class ItemRarity(str, Enum):
    """物品稀有度枚举"""
    COMMON = "common"       # 普通
    UNCOMMON = "uncommon"   # 非凡
    RARE = "rare"          # 稀有
    EPIC = "epic"          # 史诗
    LEGENDARY = "legendary" # 传说


class Item:
    """物品基类"""
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        category: ItemCategory,
        rarity: ItemRarity = ItemRarity.COMMON,
        stackable: bool = True,
        max_stack: int = 99,
        weight: float = 1.0,
        value: int = 0,
        effects: Optional[dict] = None
    ):
        self.item_id = item_id          # 物品ID（唯一标识）
        self.name = name                # 物品名称
        self.description = description  # 物品描述
        self.category = category        # 物品类别
        self.rarity = rarity           # 稀有度
        self.stackable = stackable     # 是否可堆叠
        self.max_stack = max_stack     # 最大堆叠数量
        self.weight = weight           # 重量
        self.value = value             # 价值
        self.effects = effects or {}   # 物品效果（如恢复值等）

    def get_dict(self) -> dict:
        """获取物品数据字典"""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "rarity": self.rarity.value,
            "stackable": self.stackable,
            "max_stack": self.max_stack,
            "weight": self.weight,
            "value": self.value,
            "effects": self.effects
        }


class ItemStack:
    """物品堆叠类（用于背包系统）"""
    def __init__(self, item: Item, quantity: int = 1):
        self.item = item
        self.quantity = min(quantity, item.max_stack if item.stackable else 1)

    def add(self, amount: int) -> int:
        """添加数量，返回无法添加的剩余数量"""
        max_can_add = self.item.max_stack - self.quantity if self.item.stackable else 0
        actual_add = min(amount, max_can_add)
        self.quantity += actual_add
        return amount - actual_add

    def remove(self, amount: int) -> int:
        """移除数量，返回实际移除的数量"""
        actual_remove = min(amount, self.quantity)
        self.quantity -= actual_remove
        return actual_remove

    def get_dict(self) -> dict:
        """获取物品堆叠数据"""
        return {
            "item": self.item.get_dict(),
            "quantity": self.quantity
        }


class Inventory:
    """背包/仓库类"""
    def __init__(self, max_slots: int = 30):
        self.max_slots = max_slots
        self.items: list[ItemStack] = []

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """添加物品到背包"""
        remaining = quantity

        # 如果物品可堆叠，先尝试添加到已有的堆叠中
        if item.stackable:
            for stack in self.items:
                if stack.item.item_id == item.item_id:
                    remaining = stack.add(remaining)
                    if remaining == 0:
                        return True

        # 如果还有剩余，创建新的堆叠
        while remaining > 0 and len(self.items) < self.max_slots:
            new_stack_amount = min(remaining, item.max_stack)
            self.items.append(ItemStack(item, new_stack_amount))
            remaining -= new_stack_amount

        return remaining == 0

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """从背包移除物品"""
        remaining = quantity

        # 从后往前遍历，方便删除空堆叠
        for i in range(len(self.items) - 1, -1, -1):
            if self.items[i].item.item_id == item_id:
                removed = self.items[i].remove(remaining)
                remaining -= removed

                # 如果堆叠为空，移除它
                if self.items[i].quantity == 0:
                    self.items.pop(i)

                if remaining == 0:
                    return True

        return remaining == 0

    def get_item_count(self, item_id: str) -> int:
        """获取指定物品的总数量"""
        total = 0
        for stack in self.items:
            if stack.item.item_id == item_id:
                total += stack.quantity
        return total

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """检查是否拥有足够数量的物品"""
        return self.get_item_count(item_id) >= quantity

    def get_all_items(self) -> list[dict]:
        """获取所有物品数据"""
        return [stack.get_dict() for stack in self.items]

    def get_dict(self) -> dict:
        """获取背包数据"""
        return {
            "max_slots": self.max_slots,
            "used_slots": len(self.items),
            "items": self.get_all_items()
        }


# 预定义一些物品
def create_default_items() -> dict[str, Item]:
    """创建默认物品库"""
    items = {}

    # 食物类
    items["bread"] = Item(
        item_id="bread",
        name="面包",
        description="普通的面包，可以恢复饥饿度",
        category=ItemCategory.FOOD,
        rarity=ItemRarity.COMMON,
        stackable=True,
        max_stack=50,
        weight=0.5,
        value=5,
        effects={"hunger": 20}
    )

    items["apple"] = Item(
        item_id="apple",
        name="苹果",
        description="新鲜的苹果，可以恢复少量饥饿度",
        category=ItemCategory.FOOD,
        rarity=ItemRarity.COMMON,
        stackable=True,
        max_stack=50,
        weight=0.3,
        value=3,
        effects={"hunger": 10}
    )

    items["cooked_meat"] = Item(
        item_id="cooked_meat",
        name="熟肉",
        description="烹饪好的肉类，可以恢复大量饥饿度",
        category=ItemCategory.FOOD,
        rarity=ItemRarity.UNCOMMON,
        stackable=True,
        max_stack=30,
        weight=1.0,
        value=15,
        effects={"hunger": 40}
    )

    # 工具类
    items["pickaxe"] = Item(
        item_id="pickaxe",
        name="镐子",
        description="用于采矿的工具",
        category=ItemCategory.TOOL,
        rarity=ItemRarity.COMMON,
        stackable=False,
        max_stack=1,
        weight=3.0,
        value=50
    )

    items["axe"] = Item(
        item_id="axe",
        name="斧头",
        description="用于伐木的工具",
        category=ItemCategory.TOOL,
        rarity=ItemRarity.COMMON,
        stackable=False,
        max_stack=1,
        weight=2.5,
        value=45
    )

    # 材料类
    items["wood"] = Item(
        item_id="wood",
        name="木材",
        description="基础建筑材料",
        category=ItemCategory.MATERIAL,
        rarity=ItemRarity.COMMON,
        stackable=True,
        max_stack=100,
        weight=2.0,
        value=2
    )

    items["stone"] = Item(
        item_id="stone",
        name="石头",
        description="坚硬的石材",
        category=ItemCategory.MATERIAL,
        rarity=ItemRarity.COMMON,
        stackable=True,
        max_stack=100,
        weight=3.0,
        value=3
    )

    items["iron_ore"] = Item(
        item_id="iron_ore",
        name="铁矿石",
        description="可以冶炼成铁锭的矿石",
        category=ItemCategory.MATERIAL,
        rarity=ItemRarity.UNCOMMON,
        stackable=True,
        max_stack=50,
        weight=4.0,
        value=10
    )

    # 消耗品
    items["health_potion"] = Item(
        item_id="health_potion",
        name="生命药水",
        description="可以恢复疲劳度的神奇药水",
        category=ItemCategory.CONSUMABLE,
        rarity=ItemRarity.RARE,
        stackable=True,
        max_stack=20,
        weight=0.5,
        value=50,
        effects={"fatigue": 30}
    )

    items["mood_potion"] = Item(
        item_id="mood_potion",
        name="心情药水",
        description="可以提升心情的魔法药水",
        category=ItemCategory.CONSUMABLE,
        rarity=ItemRarity.RARE,
        stackable=True,
        max_stack=20,
        weight=0.5,
        value=40,
        effects={"mood": 25}
    )

    return items

