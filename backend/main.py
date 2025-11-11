from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime
from typing import List

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GameTime:
    """游戏时间系统"""
    def __init__(self):
        self.day = 1
        self.hour = 0
        self.running = False
        self.base_hour_duration = 0.2  # 基础每小时200ms
        self.speed = 1  # 速度倍率：1, 2, 5
        self.hour_duration = self.base_hour_duration / self.speed

    def tick(self):
        """时间推进"""
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1

    def get_time_string(self) -> str:
        """获取格式化的时间字符串"""
        return f"第{self.day}天 {self.hour}时"

    def get_time_dict(self) -> dict:
        """获取时间数据"""
        return {
            "day": self.day,
            "hour": self.hour,
            "time_string": self.get_time_string(),
            "running": self.running,
            "speed": self.speed
        }

    def set_speed(self, speed: int):
        """设置时间流速"""
        if speed in [1, 2, 5]:
            self.speed = speed
            self.hour_duration = self.base_hour_duration / self.speed
            return True
        return False


# 全局游戏时间实例
game_time = GameTime()

# 存储所有连接的WebSocket客户端
active_connections: List[WebSocket] = []


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """广播消息给所有连接的客户端"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


async def time_loop():
    """时间循环任务"""
    while True:
        if game_time.running:
            game_time.tick()
            # 广播时间更新给所有客户端
            await manager.broadcast({
                "type": "time_update",
                "data": game_time.get_time_dict()
            })
        await asyncio.sleep(game_time.hour_duration)


@app.on_event("startup")
async def startup_event():
    """启动时自动开始时间系统"""
    game_time.running = True
    asyncio.create_task(time_loop())


@app.get("/")
async def root():
    return {"message": "Game Server is running"}


@app.get("/api/time")
async def get_time():
    """获取当前游戏时间"""
    return game_time.get_time_dict()


@app.post("/api/time/start")
async def start_time():
    """启动时间系统"""
    game_time.running = True
    return {"status": "started", "time": game_time.get_time_dict()}


@app.post("/api/time/stop")
async def stop_time():
    """暂停时间系统"""
    game_time.running = False
    return {"status": "stopped", "time": game_time.get_time_dict()}


@app.post("/api/time/speed/{speed}")
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


@app.post("/api/time/toggle")
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接端点"""
    await manager.connect(websocket)
    try:
        # 发送当前时间
        await websocket.send_json({
            "type": "time_update",
            "data": game_time.get_time_dict()
        })

        # 保持连接
        while True:
            data = await websocket.receive_text()
            # 可以处理客户端发来的消息
            if data == "get_time":
                await websocket.send_json({
                    "type": "time_update",
                    "data": game_time.get_time_dict()
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
