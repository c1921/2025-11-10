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
        from .trait_system import TraitSystem
        
        if character.current_action == ActionType.REST:
            # 休息恢复疲劳 - 应用高效睡眠特质
            base_fatigue_recovery = 10
            fatigue_recovery = TraitSystem.apply_fatigue_change(character, base_fatigue_recovery, is_consumption=False)
            character.fatigue = min(100, character.fatigue + fatigue_recovery)
            
            # 休息时也会饿 - 应用坚韧特质
            base_hunger_consumption = -1
            hunger_consumption = TraitSystem.apply_hunger_change(character, base_hunger_consumption, is_consumption=True)
            character.hunger = max(0, character.hunger + hunger_consumption)

        elif character.current_action == ActionType.EAT:
            # 进食需要消耗食物
            from .food_system import FoodSystem
            
            # 计算饥饿缺口
            hunger_gap = 100 - character.hunger
            
            if hunger_gap <= 0:
                print(f"[行动系统] {character.name} - 已经饱了 (饥饿度: {character.hunger:.1f})")
                character.fatigue = max(0, character.fatigue - 1)
                return
            
            # 选择食物
            selected_foods = FoodSystem.select_food_to_eat(character, hunger_gap)
            
            if not selected_foods:
                print(f"[行动系统] ❌ {character.name} - 没有食物可吃！切换到休息")
                character.fatigue = max(0, character.fatigue - 1)
                # 立即切换到休息状态
                ActionSystem.assign_action(character, ActionType.REST)
                return
            
            # 消耗食物并恢复饥饿 - 应用好胃口和美食家特质
            total_recovery = 0
            for item_id, quantity, recovery in selected_foods:
                character.inventory.remove_item(item_id, quantity)
                total_recovery += recovery
            
            # 应用好胃口特质修正
            total_recovery = TraitSystem.apply_hunger_change(character, total_recovery, is_consumption=False)
            character.hunger = min(100, character.hunger + total_recovery)
            
            # 应用美食家特质的心情加成
            mood_bonus = TraitSystem.apply_mood_change(character, 0, is_eating=True)
            if mood_bonus > 0:
                character.mood = min(100, character.mood + mood_bonus)
            
            character.fatigue = max(0, character.fatigue - 1)
            print(f"[行动系统] ✅ {character.name} - 进食完成，恢复 {total_recovery:.1f}，饥饿度: {character.hunger:.1f}")
            
            # 检查吃完后是否还有食物，且饥饿度仍低于阈值
            if character.hunger < 40:
                has_more_food = FoodSystem.has_any_food(character)
                if not has_more_food:
                    print(f"[行动系统] ⚠️ {character.name} - 食物吃完但仍然饥饿 (饥饿度: {character.hunger:.1f})，切换到休息")
                    ActionSystem.assign_action(character, ActionType.REST)

        elif character.current_action == ActionType.ENTERTAINMENT:
            # 娱乐恢复心情 - 应用开朗特质
            base_mood_recovery = 8
            mood_recovery = TraitSystem.apply_mood_change(character, base_mood_recovery, is_entertainment=True)
            character.mood = min(100, character.mood + mood_recovery)
            
            # 娱乐会消耗精力和饥饿 - 应用坚韧特质
            base_fatigue_consumption = -2
            base_hunger_consumption = -2
            fatigue_consumption = TraitSystem.apply_fatigue_change(character, base_fatigue_consumption, is_consumption=True)
            hunger_consumption = TraitSystem.apply_hunger_change(character, base_hunger_consumption, is_consumption=True)
            character.fatigue = max(0, character.fatigue + fatigue_consumption)
            character.hunger = max(0, character.hunger + hunger_consumption)

        elif character.current_action in [ActionType.LUMBERING, ActionType.MINING, ActionType.GATHERING, ActionType.FARMING]:
            # 劳动消耗疲劳和饥饿 - 应用强壮和坚韧特质
            base_fatigue_consumption = -5
            base_hunger_consumption = -4
            fatigue_consumption = TraitSystem.apply_fatigue_change(character, base_fatigue_consumption, is_consumption=True)
            hunger_consumption = TraitSystem.apply_hunger_change(character, base_hunger_consumption, is_consumption=True)
            character.fatigue = max(0, character.fatigue + fatigue_consumption)
            character.hunger = max(0, character.hunger + hunger_consumption)
            
            # 增加当前劳动类型的进度 - 应用手巧特质
            base_progress = 1
            progress_modifier = TraitSystem.get_trait_modifier(character, "work_progress_modifier", 1.0)
            progress_increment = base_progress * progress_modifier
            character.work_progress[character.current_action] += progress_increment
            current_progress = character.work_progress[character.current_action]
            print(f"[行动系统] {character.name} - {character.current_action.value} 进度 +{progress_increment:.2f} → {current_progress:.2f}/4")
            
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
        
        # 如果饥饿度低于40，去进食（前提是有食物）
        if character.hunger < 40:
            from .food_system import FoodSystem
            has_food = FoodSystem.has_any_food(character)
            
            if has_food:
                print(f"[行动系统] {character.name} - 决策：进食（饥饿度 {character.hunger:.1f} < 40）")
                ActionSystem.assign_action(character, ActionType.EAT)
            else:
                print(f"[行动系统] ⚠️ {character.name} - 警告：饥饿但没有食物！优先休息（饥饿度 {character.hunger:.1f}）")
                ActionSystem.assign_action(character, ActionType.REST)
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

