"""行动系统模块 - 负责角色行动相关逻辑"""
from typing import TYPE_CHECKING
from .enums import ActionType

if TYPE_CHECKING:
    from .character import Character


class ActionSystem:
    """行动系统 - 处理角色的行动分配和效果应用"""

    @staticmethod
    def assign_action(character: "Character", action: ActionType):
        """分配行动"""
        old_action = character.current_action.value if character.current_action else "无"
        
        # 只在行动真正改变时才重置持续时间
        if character.current_action != action:
            print(f"[行动系统] {character.name} - 行动变更: {old_action} → {action.value}")
            character.current_action = action
            character.action_duration = 0
            # work_progress 不再重置，各工作类型的进度独立保持
        else:
            print(f"[行动系统] {character.name} - 继续当前行动: {action.value}")

    @staticmethod
    def apply_action_effects(character: "Character"):
        """应用行动效果"""
        if character.current_action == ActionType.REST:
            # 休息恢复疲劳
            character.fatigue = min(100, character.fatigue + 10)
            character.hunger = max(0, character.hunger - 1)  # 休息时也会饿

        elif character.current_action == ActionType.EAT:
            # 进食恢复饥饿
            character.hunger = min(100, character.hunger + 100)
            character.fatigue = max(0, character.fatigue - 1)  # 进食会消耗一点精力

        elif character.current_action == ActionType.ENTERTAINMENT:
            # 娱乐恢复心情
            character.mood = min(100, character.mood + 8)
            character.fatigue = max(0, character.fatigue - 2)  # 娱乐会消耗精力
            character.hunger = max(0, character.hunger - 2)    # 娱乐会消耗饥饿

        elif character.current_action in [ActionType.LUMBERING, ActionType.MINING, ActionType.GATHERING, ActionType.FARMING]:
            # 劳动消耗疲劳和饥饿
            character.fatigue = max(0, character.fatigue - 5)
            character.hunger = max(0, character.hunger - 4)
            
            # 增加当前劳动类型的进度
            character.work_progress[character.current_action] += 1
            current_progress = character.work_progress[character.current_action]
            print(f"[行动系统] {character.name} - {character.current_action.value} 进度 +1 → {current_progress}/4")
            
            # 检查是否到达产出时间（4小时）
            from .work_system import WorkSystem
            WorkSystem.try_produce_items(character)

    @staticmethod
    def auto_assign_action(character: "Character"):
        """根据角色状态自动分配行动"""
        # 优先级：饥饿 > 疲劳 > 心情
        print(f"[行动系统] {character.name} - 自动分配行动 (疲劳:{character.fatigue:.1f}, 饥饿:{character.hunger:.1f}, 心情:{character.mood:.1f})")

        # 如果当前正在休息，持续到疲劳值90以上再切换
        if character.current_action == ActionType.REST and character.fatigue < 90:
            print(f"[行动系统] {character.name} - 继续休息（疲劳未恢复到90）")
            return  # 继续休息，不切换状态
        
        # 如果饥饿度低于40，去进食
        if character.hunger < 40:
            print(f"[行动系统] {character.name} - 决策：进食（饥饿度 {character.hunger:.1f} < 40）")
            ActionSystem.assign_action(character, ActionType.EAT)
        # 如果疲劳度低于40，去休息
        elif character.fatigue < 40:
            print(f"[行动系统] {character.name} - 决策：休息（疲劳度 {character.fatigue:.1f} < 40）")
            ActionSystem.assign_action(character, ActionType.REST)
        # 如果心情低于50，去娱乐
        elif character.mood < 50:
            print(f"[行动系统] {character.name} - 决策：娱乐（心情 {character.mood:.1f} < 50）")
            ActionSystem.assign_action(character, ActionType.ENTERTAINMENT)
        # 如果状态良好（疲劳>60且饥饿>60），可以劳动
        elif character.fatigue > 60 and character.hunger > 60:
            print(f"[行动系统] {character.name} - 决策：劳动（状态良好）")
            from .work_system import WorkSystem
            WorkSystem.choose_work_action(character)
        # 状态不足以劳动，但也不紧急，优先恢复最低的状态
        else:
            # 找出最需要恢复的状态
            if character.hunger <= character.fatigue and character.hunger <= character.mood:
                print(f"[行动系统] {character.name} - 决策：进食（饥饿度最低: {character.hunger:.1f}）")
                ActionSystem.assign_action(character, ActionType.EAT)
            elif character.fatigue <= character.mood:
                print(f"[行动系统] {character.name} - 决策：休息（疲劳度最低: {character.fatigue:.1f}）")
                ActionSystem.assign_action(character, ActionType.REST)
            else:
                print(f"[行动系统] {character.name} - 决策：娱乐（心情最低: {character.mood:.1f}）")
                ActionSystem.assign_action(character, ActionType.ENTERTAINMENT)

