"""特质系统模块 - 负责角色特质相关逻辑"""
from typing import TYPE_CHECKING, List
from .enums import TraitType

if TYPE_CHECKING:
    from .character import Character


class TraitSystem:
    """特质系统 - 处理角色特质效果"""
    
    # 特质定义字典
    TRAIT_DEFINITIONS = {
        TraitType.STRONG: {
            "name": "强壮",
            "description": "劳动时疲劳消耗减少30%",
            "fatigue_consumption_modifier": 0.7,  # 疲劳消耗减少30%
        },
        TraitType.EFFICIENT_SLEEPER: {
            "name": "高效睡眠",
            "description": "休息时疲劳恢复提升50%",
            "fatigue_recovery_modifier": 1.5,  # 疲劳恢复提升50%
        },
        TraitType.GOOD_APPETITE: {
            "name": "好胃口",
            "description": "进食时饥饿恢复提升30%",
            "hunger_recovery_modifier": 1.3,  # 饥饿恢复提升30%
        },
        TraitType.CHEERFUL: {
            "name": "开朗",
            "description": "娱乐时心情恢复提升40%",
            "mood_recovery_modifier": 1.4,  # 心情恢复提升40%
        },
        TraitType.QUICK_LEARNER: {
            "name": "手巧",
            "description": "劳动产出进度提升25%",
            "work_progress_modifier": 1.25,  # 劳动进度提升25%
        },
        TraitType.RESILIENT: {
            "name": "坚韧",
            "description": "所有负面状态降低速度减少20%",
            "negative_reduction": 0.8,  # 负面效果减少20%
        },
        TraitType.GOURMAND: {
            "name": "美食家",
            "description": "进食时额外恢复3点心情",
            "mood_bonus": 3,  # 进食时额外心情加成
        },
        TraitType.WORKAHOLIC: {
            "name": "工作狂",
            "description": "劳动时心情降低速度减少50%",
            "mood_consumption_modifier": 0.5,  # 劳动时心情降低减少50%
        },
    }
    
    @staticmethod
    def get_trait_name(trait: TraitType) -> str:
        """获取特质的中文名称"""
        return TraitSystem.TRAIT_DEFINITIONS.get(trait, {}).get("name", trait.value)
    
    @staticmethod
    def get_trait_description(trait: TraitType) -> str:
        """获取特质的描述"""
        return TraitSystem.TRAIT_DEFINITIONS.get(trait, {}).get("description", "")
    
    @staticmethod
    def get_trait_modifier(character: "Character", modifier_type: str, default: float = 1.0) -> float:
        """
        获取角色特质对某个效果的修正值
        
        参数:
            character: 角色对象
            modifier_type: 修正类型（如 'fatigue_consumption_modifier'）
            default: 默认值（无特质时）
        
        返回:
            修正后的值
        """
        result = default
        for trait in character.traits:
            trait_def = TraitSystem.TRAIT_DEFINITIONS.get(trait, {})
            if modifier_type in trait_def:
                # 对于修正器，使用乘法叠加
                if modifier_type.endswith("_modifier"):
                    result *= trait_def[modifier_type]
        return result
    
    @staticmethod
    def get_trait_bonus(character: "Character", bonus_type: str) -> float:
        """
        获取角色特质的额外加成值（固定值，非修正器）
        
        参数:
            character: 角色对象
            bonus_type: 加成类型（如 'mood_bonus'）
        
        返回:
            加成值总和
        """
        total_bonus = 0
        for trait in character.traits:
            trait_def = TraitSystem.TRAIT_DEFINITIONS.get(trait, {})
            if bonus_type in trait_def:
                total_bonus += trait_def[bonus_type]
        return total_bonus
    
    @staticmethod
    def apply_fatigue_change(character: "Character", base_change: float, is_consumption: bool = False) -> float:
        """
        应用特质对疲劳变化的修正
        
        参数:
            character: 角色对象
            base_change: 基础变化值（正数=恢复，负数=消耗）
            is_consumption: 是否为消耗（True表示劳动等消耗，False表示休息等恢复）
        
        返回:
            修正后的变化值
        """
        if is_consumption:
            # 消耗场景：应用强壮特质和坚韧特质
            modifier = TraitSystem.get_trait_modifier(character, "fatigue_consumption_modifier", 1.0)
            # 坚韧特质影响所有负面效果
            if TraitType.RESILIENT in character.traits:
                negative_modifier = TraitSystem.get_trait_modifier(character, "negative_reduction", 1.0)
                modifier *= negative_modifier
            return base_change * modifier
        else:
            # 恢复场景：应用高效睡眠特质
            modifier = TraitSystem.get_trait_modifier(character, "fatigue_recovery_modifier", 1.0)
            return base_change * modifier
    
    @staticmethod
    def apply_hunger_change(character: "Character", base_change: float, is_consumption: bool = False) -> float:
        """
        应用特质对饥饿变化的修正
        
        参数:
            character: 角色对象
            base_change: 基础变化值
            is_consumption: 是否为消耗
        
        返回:
            修正后的变化值
        """
        if is_consumption:
            # 消耗场景：应用坚韧特质
            if TraitType.RESILIENT in character.traits:
                modifier = TraitSystem.get_trait_modifier(character, "negative_reduction", 1.0)
                return base_change * modifier
            return base_change
        else:
            # 恢复场景（进食）：应用好胃口特质
            modifier = TraitSystem.get_trait_modifier(character, "hunger_recovery_modifier", 1.0)
            return base_change * modifier
    
    @staticmethod
    def apply_mood_change(character: "Character", base_change: float, is_consumption: bool = False, is_entertainment: bool = False, is_eating: bool = False) -> float:
        """
        应用特质对心情变化的修正
        
        参数:
            character: 角色对象
            base_change: 基础变化值
            is_consumption: 是否为消耗（劳动等）
            is_entertainment: 是否为娱乐场景
            is_eating: 是否为进食场景
        
        返回:
            修正后的变化值
        """
        result = base_change
        
        if is_entertainment:
            # 娱乐场景：应用开朗特质
            modifier = TraitSystem.get_trait_modifier(character, "mood_recovery_modifier", 1.0)
            result *= modifier
        elif is_consumption:
            # 劳动场景：应用工作狂特质和坚韧特质
            modifier = TraitSystem.get_trait_modifier(character, "mood_consumption_modifier", 1.0)
            if TraitType.RESILIENT in character.traits:
                negative_modifier = TraitSystem.get_trait_modifier(character, "negative_reduction", 1.0)
                modifier *= negative_modifier
            result *= modifier
        elif is_eating:
            # 进食场景：应用美食家特质的额外加成
            bonus = TraitSystem.get_trait_bonus(character, "mood_bonus")
            result += bonus
        
        return result

