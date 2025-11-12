from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
from models import Character, Item, Inventory
from core import GameTime, ConnectionManager

router = APIRouter(tags=["websocket"])

# 游戏状态实例
game_time: GameTime = None
manager: ConnectionManager = None
characters: List[Character] = []
all_items: Dict[str, Item] = {}
public_storage: Inventory = None


def init_websocket_state(
    game_time_instance: GameTime, 
    manager_instance: ConnectionManager, 
    characters_list: List[Character],
    items_dict: Dict[str, Item],
    public_storage_instance: Inventory
):
    """初始化WebSocket状态"""
    global game_time, manager, characters, all_items, public_storage
    game_time = game_time_instance
    manager = manager_instance
    characters = characters_list
    all_items = items_dict
    public_storage = public_storage_instance


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接端点"""
    await manager.connect(websocket)
    try:
        # 发送当前游戏状态
        await websocket.send_json({
            "type": "game_update",
            "data": {
                "time": game_time.get_time_dict(),
                "characters": [char.get_status_dict() for char in characters],
                "public_storage": public_storage.get_dict()
            }
        })

        # 保持连接
        while True:
            data = await websocket.receive_text()
            # 可以处理客户端发来的消息
            if data == "get_state":
                await websocket.send_json({
                    "type": "game_update",
                    "data": {
                        "time": game_time.get_time_dict(),
                        "characters": [char.get_status_dict() for char in characters],
                        "public_storage": public_storage.get_dict()
                    }
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
