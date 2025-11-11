# 游戏项目 - 时间系统

基于 Python FastAPI + Vue 3 + TypeScript + Vite 开发的游戏项目。

## 功能特性

### 时间系统 ✅
- 24小时制，每小时现实时间200ms
- 时间格式：第X天 Y时
- WebSocket实时同步
- 自动流逝，支持暂停/重置

## 技术栈

### 后端
- Python 3.x
- FastAPI
- WebSocket
- Uvicorn

### 前端
- Vue 3
- TypeScript
- Vite
- WebSocket Client

## 安装与运行

### 方式1：使用启动脚本（Windows）

1. 安装后端依赖：
```bash
pip install -r requirements.txt
```

2. 安装前端依赖：
```bash
cd frontend
npm install
```

3. 运行启动脚本：
```bash
start.bat
```

### 方式2：手动启动

#### 后端
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端
```bash
cd frontend
npm install
npm run dev
```

## 访问地址

- 前端界面: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## API端点

### REST API
- `GET /api/time` - 获取当前游戏时间
- `POST /api/time/start` - 启动时间系统
- `POST /api/time/stop` - 暂停时间系统
- `POST /api/time/reset` - 重置时间

### WebSocket
- `ws://localhost:8000/ws` - 实时时间更新

## 项目结构

```
.
├── backend/
│   └── main.py          # FastAPI后端服务
├── frontend/
│   ├── src/
│   │   ├── App.vue      # 主组件
│   │   ├── main.ts      # 入口文件
│   │   └── style.css    # 全局样式
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt      # Python依赖
├── start.bat            # Windows启动脚本
└── README.md

```

## 时间系统说明

游戏时间以24小时为一个周期：
- 每小时 = 200ms 现实时间
- 每天 = 4.8秒 现实时间 (24小时 × 200ms)
- 时间到达24时后自动进入下一天
- 服务器启动后时间自动开始流逝

时间通过WebSocket实时推送到所有连接的客户端，确保同步。
