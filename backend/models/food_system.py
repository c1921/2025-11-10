"""食物系统模块 - 负责角色进食相关逻辑"""
from typing import TYPE_CHECKING, List, Tuple, Optional
from .item import ItemCategory

if TYPE_CHECKING:
    from .character import Character


class FoodSystem:
    """食物系统 - 处理角色的进食和食物选择"""

    @staticmethod
    def has_any_food(character: "Character") -> bool:
        """检查角色是否有任何食物"""
        for stack in character.inventory.items:
            if stack.item.category == ItemCategory.FOOD:
                hunger_recovery = stack.item.effects.get("hunger", 0)
                if hunger_recovery > 0:
                    return True
        return False

    @staticmethod
    def get_all_foods(character: "Character") -> List[dict]:
        """获取背包中所有食物及其恢复值"""
        foods = []
        for stack in character.inventory.items:
            if stack.item.category == ItemCategory.FOOD:
                hunger_recovery = stack.item.effects.get("hunger", 0)
                if hunger_recovery > 0:
                    foods.append({
                        "item_id": stack.item.item_id,
                        "name": stack.item.name,
                        "quantity": stack.quantity,
                        "recovery_per_unit": hunger_recovery,
                        "total_recovery": hunger_recovery * stack.quantity
                    })
        return foods

    @staticmethod
    def select_food_to_eat(character: "Character", hunger_gap: float) -> Optional[List[Tuple[str, int, float]]]:
        """
        智能选择食物来恢复饥饿度
        
        参数:
            character: 角色对象
            hunger_gap: 饥饿缺口 (100 - current_hunger)
        
        返回:
            list[(item_id, quantity, recovery)]: 选中的食物列表
            或 None: 如果没有食物
        """
        # 获取所有食物
        foods = FoodSystem.get_all_foods(character)
        
        if not foods:
            return None
        
        print(f"[食物系统] {character.name} - 饥饿缺口: {hunger_gap:.1f}")
        print(f"[食物系统] {character.name} - 背包食物:")
        for food in foods:
            print(f"  - {food['name']} x{food['quantity']} (每个恢复{food['recovery_per_unit']})")
        
        # 使用贪心算法选择食物
        selected = FoodSystem._greedy_select(foods, hunger_gap)
        
        if selected:
            total_recovery = sum(recovery for _, _, recovery in selected)
            print(f"[食物系统] {character.name} - 选择策略: 总恢复 {total_recovery:.1f} (缺口 {hunger_gap:.1f})")
            for item_id, quantity, recovery in selected:
                food_name = next(f['name'] for f in foods if f['item_id'] == item_id)
                print(f"  → {food_name} x{quantity} (恢复 {recovery:.1f})")
        
        return selected

    @staticmethod
    def _greedy_select(foods: List[dict], hunger_gap: float) -> List[Tuple[str, int, float]]:
        """
        贪心算法选择食物
        
        策略:
        1. 优先找单个食物恢复值接近缺口的（±20%容差）
        2. 如果没有接近的，尝试多个食物组合
        3. 如果所有食物总和不足，全部消耗
        """
        # 按单位恢复值排序（从大到小）
        foods_sorted = sorted(foods, key=lambda x: x['recovery_per_unit'], reverse=True)
        
        # 策略1: 找单个食物接近缺口的
        for food in foods_sorted:
            per_unit = food['recovery_per_unit']
            # 计算需要多少个才能接近缺口
            needed = hunger_gap / per_unit
            
            # 如果1个就足够或接近（80%-120%范围内）
            if 0.8 <= needed <= 1.2:
                quantity = 1
                recovery = per_unit * quantity
                return [(food['item_id'], quantity, recovery)]
            
            # 如果需要多个，选择最接近的数量
            if needed <= food['quantity']:
                # 可以选择 floor(needed) 或 ceil(needed)，选择更接近的
                import math
                quantity_floor = math.floor(needed)
                quantity_ceil = math.ceil(needed)
                
                # 选择恢复值更接近缺口的数量
                if quantity_floor > 0:
                    diff_floor = abs(per_unit * quantity_floor - hunger_gap)
                    diff_ceil = abs(per_unit * quantity_ceil - hunger_gap)
                    quantity = quantity_floor if diff_floor <= diff_ceil else quantity_ceil
                else:
                    quantity = quantity_ceil
                
                # 确保不超过拥有数量
                quantity = min(quantity, food['quantity'])
                recovery = per_unit * quantity
                
                # 如果这个选择能满足至少70%的缺口，接受它
                if recovery >= hunger_gap * 0.7:
                    return [(food['item_id'], quantity, recovery)]
        
        # 策略2: 组合多种食物
        selected = []
        remaining_gap = hunger_gap
        
        for food in foods_sorted:
            if remaining_gap <= 0:
                break
            
            per_unit = food['recovery_per_unit']
            # 计算需要多少个
            import math
            needed = math.ceil(remaining_gap / per_unit)
            quantity = min(needed, food['quantity'])
            
            if quantity > 0:
                recovery = per_unit * quantity
                selected.append((food['item_id'], quantity, recovery))
                remaining_gap -= recovery
        
        return selected if selected else None

