from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from models import Character, Gender, ActionType, Item, Inventory
from core import GameTime, ConnectionManager

router = APIRouter(prefix="/api", tags=["api"])

# 游戏状态实例
game_time: GameTime = None
manager: ConnectionManager = None
characters: List[Character] = []
all_items: Dict[str, Item] = {}
public_storage: Inventory = None


def init_game_state(
    game_time_instance: GameTime, 
    manager_instance: ConnectionManager, 
    characters_list: List[Character],
    items_dict: Dict[str, Item],
    public_storage_instance: Inventory
):
    """初始化游戏状态"""
    global game_time, manager, characters, all_items, public_storage
    game_time = game_time_instance
    manager = manager_instance
    characters = characters_list
    all_items = items_dict
    public_storage = public_storage_instance


class TransferItemRequest(BaseModel):
    item_id: str
    quantity: int = 1


class UseItemRequest(BaseModel):
    item_id: str


@router.get("/time")
async def get_time():
    """获取当前游戏时间"""
    return game_time.get_time_dict()


@router.get("/characters")
async def get_characters():
    """获取所有角色信息"""
    return {
        "characters": [char.get_status_dict() for char in characters]
    }


@router.get("/game-state")
async def get_game_state():
    """获取完整游戏状态"""
    return {
        "time": game_time.get_time_dict(),
        "characters": [char.get_status_dict() for char in characters],
        "public_storage": public_storage.get_dict()
    }


@router.post("/time/start")
async def start_time():
    """启动时间系统"""
    game_time.running = True
    return {"status": "started", "time": game_time.get_time_dict()}


@router.post("/time/stop")
async def stop_time():
    """暂停时间系统"""
    game_time.running = False
    return {"status": "stopped", "time": game_time.get_time_dict()}


@router.post("/time/speed/{speed}")
async def set_speed(speed: int):
    """设置时间流速"""
    if game_time.set_speed(speed):
        # 广播速度变化
        await manager.broadcast({
            "type": "speed_update",
            "data": game_time.get_time_dict()
        })
        return {"status": "success", "speed": speed, "time": game_time.get_time_dict()}
    else:
        return {"status": "error", "message": "Invalid speed. Must be 1, 2, or 5"}


@router.post("/time/toggle")
async def toggle_time():
    """切换时间运行状态（暂停/继续）"""
    game_time.running = not game_time.running
    status = "started" if game_time.running else "stopped"
    # 广播状态变化
    await manager.broadcast({
        "type": "status_update",
        "data": game_time.get_time_dict()
    })
    return {"status": status, "time": game_time.get_time_dict()}


@router.post("/characters/{character_name}/action")
async def set_character_action(character_name: str, action: str):
    """手动设置角色行动"""
    # 查找角色
    character = None
    for char in characters:
        if char.name == character_name:
            character = char
            break

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # 验证行动类型
    try:
        action_type = ActionType(action)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid action type")

    # 设置行动
    character.assign_action(action_type)

    # 广播更新
    await manager.broadcast({
        "type": "character_action_update",
        "data": {
            "character": character.get_status_dict()
        }
    })

    return {"status": "success", "character": character.get_status_dict()}


# ==================== 物品系统API ====================

@router.get("/items")
async def get_all_items():
    """获取所有可用物品"""
    return {
        "items": [item.get_dict() for item in all_items.values()]
    }


@router.get("/items/{item_id}")
async def get_item(item_id: str):
    """获取特定物品信息"""
    if item_id not in all_items:
        raise HTTPException(status_code=404, detail="Item not found")
    return all_items[item_id].get_dict()


@router.get("/public-storage")
async def get_public_storage():
    """获取公共仓库信息"""
    return public_storage.get_dict()


@router.get("/characters/{character_name}/inventory")
async def get_character_inventory(character_name: str):
    """获取角色背包信息"""
    character = None
    for char in characters:
        if char.name == character_name:
            character = char
            break

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    return character.inventory.get_dict()


@router.post("/characters/{character_name}/use-item")
async def use_item(character_name: str, request: UseItemRequest):
    """角色使用物品"""
    character = None
    for char in characters:
        if char.name == character_name:
            character = char
            break

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if request.item_id not in all_items:
        raise HTTPException(status_code=404, detail="Item not found")

    if character.use_item(request.item_id):
        # 广播更新
        await manager.broadcast({
            "type": "game_update",
            "data": {
                "time": game_time.get_time_dict(),
                "characters": [char.get_status_dict() for char in characters],
                "public_storage": public_storage.get_dict()
            }
        })
        return {"status": "success", "character": character.get_status_dict()}
    else:
        raise HTTPException(status_code=400, detail="Failed to use item")


@router.post("/characters/{character_name}/take-from-storage")
async def take_from_storage(character_name: str, request: TransferItemRequest):
    """从公共仓库取出物品到角色背包"""
    character = None
    for char in characters:
        if char.name == character_name:
            character = char
            break

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if request.item_id not in all_items:
        raise HTTPException(status_code=404, detail="Item not found")

    # 检查公共仓库是否有足够的物品
    if not public_storage.has_item(request.item_id, request.quantity):
        raise HTTPException(status_code=400, detail="Not enough items in public storage")

    # 从公共仓库移除
    item = all_items[request.item_id]
    if public_storage.remove_item(request.item_id, request.quantity):
        # 添加到角色背包
        if character.inventory.add_item(item, request.quantity):
            # 广播更新
            await manager.broadcast({
                "type": "game_update",
                "data": {
                    "time": game_time.get_time_dict(),
                    "characters": [char.get_status_dict() for char in characters],
                    "public_storage": public_storage.get_dict()
                }
            })
            return {
                "status": "success",
                "character": character.get_status_dict(),
                "public_storage": public_storage.get_dict()
            }
        else:
            # 如果添加失败，回退到公共仓库
            public_storage.add_item(item, request.quantity)
            raise HTTPException(status_code=400, detail="Character inventory is full")
    else:
        raise HTTPException(status_code=400, detail="Failed to remove item from storage")


@router.post("/characters/{character_name}/put-to-storage")
async def put_to_storage(character_name: str, request: TransferItemRequest):
    """从角色背包放入物品到公共仓库"""
    character = None
    for char in characters:
        if char.name == character_name:
            character = char
            break

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    if request.item_id not in all_items:
        raise HTTPException(status_code=404, detail="Item not found")

    # 检查角色是否有足够的物品
    if not character.inventory.has_item(request.item_id, request.quantity):
        raise HTTPException(status_code=400, detail="Not enough items in character inventory")

    # 从角色背包移除
    item = all_items[request.item_id]
    if character.inventory.remove_item(request.item_id, request.quantity):
        # 添加到公共仓库
        if public_storage.add_item(item, request.quantity):
            # 广播更新
            await manager.broadcast({
                "type": "game_update",
                "data": {
                    "time": game_time.get_time_dict(),
                    "characters": [char.get_status_dict() for char in characters],
                    "public_storage": public_storage.get_dict()
                }
            })
            return {
                "status": "success",
                "character": character.get_status_dict(),
                "public_storage": public_storage.get_dict()
            }
        else:
            # 如果添加失败，回退到角色背包
            character.inventory.add_item(item, request.quantity)
            raise HTTPException(status_code=400, detail="Public storage is full")
    else:
        raise HTTPException(status_code=400, detail="Failed to remove item from inventory")
