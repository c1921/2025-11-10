from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List

from models import Character, Gender
from core import GameTime, ConnectionManager
from routers import api_router, websocket_router
from routers.api import init_game_state
from routers.websocket import init_websocket_state

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局游戏时间实例
game_time = GameTime()

# 创建默认角色
characters: List[Character] = [
    Character("小明", Gender.MALE),
    Character("小红", Gender.FEMALE)
]

# 连接管理器
manager = ConnectionManager()


async def time_loop():
    """时间循环任务"""
    while True:
        if game_time.running:
            game_time.tick()

            # 更新所有角色状态
            for character in characters:
                # 自动分配行动
                character.auto_assign_action()
                # 更新状态
                character.update_status()

            # 广播时间和角色状态更新给所有客户端
            await manager.broadcast({
                "type": "game_update",
                "data": {
                    "time": game_time.get_time_dict(),
                    "characters": [char.get_status_dict() for char in characters]
                }
            })
        await asyncio.sleep(game_time.hour_duration)


# 初始化路由模块的游戏状态
init_game_state(game_time, manager, characters)
init_websocket_state(game_time, manager, characters)

# 注册路由
app.include_router(api_router)
app.include_router(websocket_router)


@app.on_event("startup")
async def startup_event():
    """启动时自动开始时间系统"""
    game_time.running = False
    asyncio.create_task(time_loop())


@app.get("/")
async def root():
    return {"message": "Game Server is running"}
