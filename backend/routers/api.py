from fastapi import APIRouter
from typing import List
from models import Character, Gender
from core import GameTime, ConnectionManager

router = APIRouter(prefix="/api", tags=["api"])

# 游戏状态实例
game_time: GameTime = None
manager: ConnectionManager = None
characters: List[Character] = []


def init_game_state(game_time_instance: GameTime, manager_instance: ConnectionManager, characters_list: List[Character]):
    """初始化游戏状态"""
    global game_time, manager, characters
    game_time = game_time_instance
    manager = manager_instance
    characters = characters_list


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
        "characters": [char.get_status_dict() for char in characters]
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
