from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import random
from typing import List

from models import Character, Gender, Inventory, create_default_items
from core import GameTime, ConnectionManager
from routers import api_router, websocket_router
from routers.api import init_game_state
from routers.websocket import init_websocket_state
from utils.character_generator import CharacterGenerator
from config import GameConfig

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
game_time.hour_duration = GameConfig.HOUR_DURATION

print(f"\n{'='*50}")
print(f"游戏初始化")
print(f"{'='*50}\n")

# 物品系统
all_items = create_default_items()  # 所有可用物品的字典

# 使用配置生成角色
print(f"[初始化] 生成 {GameConfig.CHARACTER_COUNT} 个角色...")
characters = CharacterGenerator.generate_characters(
    count=GameConfig.CHARACTER_COUNT,
    inventory_slots=GameConfig.CHARACTER_INVENTORY_SLOTS
)

# 为角色分配初始物品
print(f"\n[初始化] 分配初始物品...")
for character in characters:
    for item_id, quantity in GameConfig.INITIAL_CHARACTER_ITEMS.items():
        if item_id in all_items:
            character.inventory.add_item(all_items[item_id], quantity)
            print(f"  {character.name} 获得: {all_items[item_id].name} x{quantity}")
    
    # 设置物品字典引用
    character.all_items_ref = all_items

# 随机给角色分配工具
print(f"\n[初始化] 随机分配工具...")
for tool in GameConfig.INITIAL_TOOLS:
    if tool in all_items:
        lucky_character = random.choice(characters)
        lucky_character.inventory.add_item(all_items[tool], 1)
        print(f"  {lucky_character.name} 获得工具: {all_items[tool].name}")

# 创建公共仓库
public_storage = Inventory(max_slots=GameConfig.PUBLIC_STORAGE_SLOTS)

# 初始化公共仓库的物品
print(f"\n[初始化] 初始化公共仓库...")
for item_id, quantity in GameConfig.PUBLIC_STORAGE_INITIAL_ITEMS.items():
    if item_id in all_items:
        public_storage.add_item(all_items[item_id], quantity)
        print(f"  公共仓库: {all_items[item_id].name} x{quantity}")

print(f"\n{'='*50}")
print(f"初始化完成! 游戏即将开始...")
print(f"{'='*50}\n")

# 连接管理器
manager = ConnectionManager()


async def time_loop():
    """时间循环任务"""
    while True:
        if game_time.running:
            game_time.tick()

            # 如果是新的一天（0时），所有角色年龄增长
            if game_time.hour == 0:
                for character in characters:
                    character.age_one_day()

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
                    "characters": [char.get_status_dict() for char in characters],
                    "public_storage": public_storage.get_dict()
                }
            })
        await asyncio.sleep(game_time.hour_duration)


# 初始化路由模块的游戏状态
init_game_state(game_time, manager, characters, all_items, public_storage)
init_websocket_state(game_time, manager, characters, all_items, public_storage)

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
