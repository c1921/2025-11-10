"""劳动系统模块 - 负责角色劳动相关逻辑"""
import random
from typing import TYPE_CHECKING
from .enums import ActionType

if TYPE_CHECKING:
    from .character import Character


class WorkSystem:
    """劳动系统 - 处理角色的劳动工具检查、劳动选择和物品产出"""

    @staticmethod
    def has_tool_for_work(character: "Character", work_type: ActionType) -> bool:
        """检查角色是否拥有执行特定劳动所需的工具"""
        if work_type == ActionType.LUMBERING:
            return character.inventory.has_item("axe")
        elif work_type == ActionType.MINING:
            return character.inventory.has_item("pickaxe")
        elif work_type in [ActionType.GATHERING, ActionType.FARMING]:
            return True  # 采集和种植不需要工具
        return False

    @staticmethod
    def choose_work_action(character: "Character"):
        """智能选择劳动类型"""
        from .action_system import ActionSystem
        
        # 检查背包中的资源数量
        wood_count = character.inventory.get_item_count("wood")
        stone_count = character.inventory.get_item_count("stone")
        berry_count = character.inventory.get_item_count("berry")
        wheat_count = character.inventory.get_item_count("wheat")
        
        print(f"[劳动系统] {character.name} - 背包资源: 木材={wood_count}, 石头={stone_count}, 浆果={berry_count}, 小麦={wheat_count}")
        
        # 显示各工作进度
        print(f"[劳动系统] {character.name} - 工作进度: "
              f"伐木={character.work_progress[ActionType.LUMBERING]}, "
              f"采石={character.work_progress[ActionType.MINING]}, "
              f"采集={character.work_progress[ActionType.GATHERING]}, "
              f"种植={character.work_progress[ActionType.FARMING]}")
        
        # 优先级：基础资源（木材、石头）> 食物（浆果）> 农作物（小麦）
        work_options = []
        
        # 如果有斧头，可以考虑伐木
        if WorkSystem.has_tool_for_work(character, ActionType.LUMBERING):
            priority = 100 - wood_count  # 木材越少，优先级越高
            work_options.append((priority, ActionType.LUMBERING))
            print(f"[劳动系统] {character.name} - 选项：伐木（优先级 {priority}）")
        else:
            print(f"[劳动系统] {character.name} - 无法伐木：缺少斧头")
        
        # 如果有镐子，可以考虑采石
        if WorkSystem.has_tool_for_work(character, ActionType.MINING):
            priority = 100 - stone_count  # 石头越少，优先级越高
            work_options.append((priority, ActionType.MINING))
            print(f"[劳动系统] {character.name} - 选项：采石（优先级 {priority}）")
        else:
            print(f"[劳动系统] {character.name} - 无法采石：缺少镐子")
        
        # 采集浆果（不需要工具）
        priority = 80 - berry_count  # 浆果优先级略低
        work_options.append((priority, ActionType.GATHERING))
        print(f"[劳动系统] {character.name} - 选项：采集浆果（优先级 {priority}）")
        
        # 种植小麦（不需要工具）
        priority = 70 - wheat_count  # 小麦优先级最低
        work_options.append((priority, ActionType.FARMING))
        print(f"[劳动系统] {character.name} - 选项：种植（优先级 {priority}）")
        
        # 选择优先级最高的劳动类型
        if work_options:
            work_options.sort(key=lambda x: x[0], reverse=True)
            chosen_work = work_options[0][1]
            print(f"[劳动系统] {character.name} - 最终选择：{chosen_work.value}（最高优先级 {work_options[0][0]}）")
            ActionSystem.assign_action(character, chosen_work)

    @staticmethod
    def try_produce_items(character: "Character"):
        """尝试产出物品"""
        # 获取当前劳动类型的进度
        current_progress = character.work_progress.get(character.current_action, 0)
        
        # 每4小时产出一次
        if current_progress < 4:
            print(f"[劳动系统] {character.name} - {character.current_action.value} 进度: {current_progress}/4 (未达到产出条件)")
            return
        
        print(f"[劳动系统] {character.name} - 达到产出条件！进度: {current_progress}/4")
        
        # 如果没有设置物品字典引用，则无法产出
        if character.all_items_ref is None:
            print(f"[劳动系统] {character.name} - 错误：all_items_ref 未设置，无法产出物品")
            return
        
        item_id = None
        quantity = 0
        
        if character.current_action == ActionType.LUMBERING:
            # 伐木产出 2-4 个木材
            item_id = "wood"
            quantity = random.randint(2, 4)
            print(f"[劳动系统] {character.name} - 伐木产出：{quantity} 个木材")
            
        elif character.current_action == ActionType.MINING:
            # 采石产出 2-3 个石头
            item_id = "stone"
            quantity = random.randint(2, 3)
            print(f"[劳动系统] {character.name} - 采石产出：{quantity} 个石头")
            
        elif character.current_action == ActionType.GATHERING:
            # 采集浆果产出 3-5 个浆果
            item_id = "berry"
            quantity = random.randint(3, 5)
            print(f"[劳动系统] {character.name} - 采集浆果产出：{quantity} 个浆果")
            
        elif character.current_action == ActionType.FARMING:
            # 种植产出 1-2 个小麦
            item_id = "wheat"
            quantity = random.randint(1, 2)
            print(f"[劳动系统] {character.name} - 种植产出：{quantity} 个小麦")
        
        # 尝试添加物品到背包
        if item_id and item_id in character.all_items_ref:
            item = character.all_items_ref[item_id]
            success = character.inventory.add_item(item, quantity)
            if success:
                print(f"[劳动系统] ✅ {character.name} - 成功添加 {quantity} 个 {item.name} 到背包")
                used_slots = len(character.inventory.items)
                print(f"[劳动系统] {character.name} - 当前背包使用: {used_slots}/{character.inventory.max_slots} 格")
                # 产出后重置该工作类型的进度
                character.work_progress[character.current_action] = 0
                print(f"[劳动系统] {character.name} - {character.current_action.value} 进度已重置为 0/4")
            else:
                print(f"[劳动系统] ❌ {character.name} - 背包已满，无法添加 {quantity} 个 {item.name}")
                # 背包满了也重置进度，避免卡住
                character.work_progress[character.current_action] = 0
                print(f"[劳动系统] {character.name} - {character.current_action.value} 进度已重置为 0/4（背包已满）")
        else:
            if not item_id:
                print(f"[劳动系统] {character.name} - 未识别的劳动类型，无法产出")
            else:
                print(f"[劳动系统] {character.name} - 物品 {item_id} 不在物品字典中")

