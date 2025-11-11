<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface GameTime {
  day: number
  hour: number
  time_string: string
  running: boolean
  speed: number
}

interface Character {
  name: string
  gender: string
  fatigue: number
  hunger: number
  mood: number
  status_text: string
}

interface GameUpdate {
  time: GameTime
  characters: Character[]
}

const timeString = ref<string>('第1天 0时')
const isConnected = ref<boolean>(false)
const isRunning = ref<boolean>(true)
const currentSpeed = ref<number>(1)
const characters = ref<Character[]>([])
let ws: WebSocket | null = null

const connectWebSocket = () => {
  ws = new WebSocket('ws://localhost:8000/ws')

  ws.onopen = () => {
    isConnected.value = true
    console.log('WebSocket连接成功')
  }

  ws.onmessage = (event) => {
    const message = JSON.parse(event.data)
    if (message.type === 'game_update') {
      const data: GameUpdate = message.data
      timeString.value = data.time.time_string
      isRunning.value = data.time.running
      currentSpeed.value = data.time.speed
      characters.value = data.characters
    } else if (message.type === 'speed_update' || message.type === 'status_update') {
      const data: GameTime = message.data
      isRunning.value = data.running
      currentSpeed.value = data.speed
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket错误:', error)
    isConnected.value = false
  }

  ws.onclose = () => {
    isConnected.value = false
    console.log('WebSocket连接关闭')
    // 尝试重连
    setTimeout(connectWebSocket, 3000)
  }
}

const toggleTime = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/time/toggle', {
      method: 'POST'
    })
    const data = await response.json()
    isRunning.value = data.time.running
  } catch (error) {
    console.error('切换时间状态失败:', error)
  }
}

const setSpeed = async (speed: number) => {
  try {
    const response = await fetch(`http://localhost:8000/api/time/speed/${speed}`, {
      method: 'POST'
    })
    const data = await response.json()
    if (data.status === 'success') {
      currentSpeed.value = speed
    }
  } catch (error) {
    console.error('设置速度失败:', error)
  }
}

const getStatusColor = (value: number, reverse: boolean = false): string => {
  if (reverse) {
    // 对于心情，值越高越好
    if (value > 70) return '#4caf50'
    if (value > 40) return '#ff9800'
    return '#f44336'
  } else {
    // 对于疲劳和饥饿，值越低越好
    if (value < 30) return '#4caf50'
    if (value < 60) return '#ff9800'
    return '#f44336'
  }
}

onMounted(() => {
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})
</script>

<template>
  <div class="game-container">
    <div class="header">
      <div class="time-display">
        <span class="time-label">游戏时间：</span>
        <span class="time-value">{{ timeString }}</span>
      </div>
      <div class="connection-status" :class="{ connected: isConnected, disconnected: !isConnected }">
        {{ isConnected ? '已连接' : '未连接' }}
      </div>
    </div>

    <div class="main-content">
      <h1>游戏时间系统</h1>
      <p class="info">一天24小时，每小时200ms</p>
      <p class="info">时间会自动流逝并实时更新</p>

      <!-- 角色状态区域 -->
      <div class="characters-section">
        <h2>角色状态</h2>
        <div class="characters-grid">
          <div v-for="char in characters" :key="char.name" class="character-card">
            <div class="character-header">
              <h3>{{ char.name }}</h3>
              <span class="gender-badge">{{ char.gender === 'male' ? '♂ 男' : '♀ 女' }}</span>
            </div>
            <p class="status-description">{{ char.status_text }}</p>

            <div class="status-bars">
              <div class="status-bar-item">
                <div class="status-bar-label">
                  <span>疲劳</span>
                  <span :style="{ color: getStatusColor(char.fatigue, false) }">{{ char.fatigue }}</span>
                </div>
                <div class="status-bar-bg">
                  <div
                    class="status-bar-fill"
                    :style="{
                      width: char.fatigue + '%',
                      backgroundColor: getStatusColor(char.fatigue, false)
                    }"
                  ></div>
                </div>
              </div>

              <div class="status-bar-item">
                <div class="status-bar-label">
                  <span>饥饿</span>
                  <span :style="{ color: getStatusColor(char.hunger, false) }">{{ char.hunger }}</span>
                </div>
                <div class="status-bar-bg">
                  <div
                    class="status-bar-fill"
                    :style="{
                      width: char.hunger + '%',
                      backgroundColor: getStatusColor(char.hunger, false)
                    }"
                  ></div>
                </div>
              </div>

              <div class="status-bar-item">
                <div class="status-bar-label">
                  <span>心情</span>
                  <span :style="{ color: getStatusColor(char.mood, true) }">{{ char.mood }}</span>
                </div>
                <div class="status-bar-bg">
                  <div
                    class="status-bar-fill"
                    :style="{
                      width: char.mood + '%',
                      backgroundColor: getStatusColor(char.mood, true)
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="control-panel">
        <div class="control-section">
          <h3>时间控制</h3>
          <div class="button-group">
            <button @click="toggleTime" :class="{ active: isRunning }" class="btn btn-primary">
              {{ isRunning ? '⏸ 暂停' : '▶ 继续' }}
            </button>
          </div>
        </div>

        <div class="control-section">
          <h3>时间流速</h3>
          <div class="button-group">
            <button
              @click="setSpeed(1)"
              :class="{ active: currentSpeed === 1 }"
              class="btn btn-speed"
            >
              1x
            </button>
            <button
              @click="setSpeed(2)"
              :class="{ active: currentSpeed === 2 }"
              class="btn btn-speed"
            >
              2x
            </button>
            <button
              @click="setSpeed(5)"
              :class="{ active: currentSpeed === 5 }"
              class="btn btn-speed"
            >
              5x
            </button>
          </div>
        </div>

        <div class="status-info">
          <div class="status-item">
            <span class="status-label">状态:</span>
            <span :class="['status-value', isRunning ? 'running' : 'paused']">
              {{ isRunning ? '运行中' : '已暂停' }}
            </span>
          </div>
          <div class="status-item">
            <span class="status-label">速度:</span>
            <span class="status-value">{{ currentSpeed }}x</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-container {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 20px 30px;
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-label {
  font-size: 18px;
  font-weight: 500;
  color: #555;
}

.time-value {
  font-size: 28px;
  font-weight: bold;
  color: #667eea;
  font-family: 'Courier New', monospace;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.connection-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.connection-status.connected {
  background: #4caf50;
  color: white;
}

.connection-status.disconnected {
  background: #f44336;
  color: white;
}

.main-content {
  text-align: center;
  color: white;
  margin-top: 20px;
}

.main-content h1 {
  font-size: 48px;
  margin-bottom: 20px;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
}

.info {
  font-size: 20px;
  margin: 10px 0;
  opacity: 0.9;
}

.characters-section {
  max-width: 1200px;
  margin: 30px auto;
}

.characters-section h2 {
  font-size: 32px;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.characters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.character-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s;
}

.character-card:hover {
  transform: translateY(-5px);
}

.character-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.character-header h3 {
  color: #333;
  font-size: 24px;
  margin: 0;
}

.gender-badge {
  background: #667eea;
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: 500;
}

.status-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
  font-style: italic;
}

.status-bars {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.status-bar-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.status-bar-label {
  display: flex;
  justify-content: space-between;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.status-bar-bg {
  width: 100%;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.status-bar-fill {
  height: 100%;
  transition: width 0.5s ease, background-color 0.3s ease;
  border-radius: 10px;
}

.control-panel {
  max-width: 800px;
  margin: 40px auto;
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.control-section {
  margin-bottom: 30px;
}

.control-section h3 {
  color: #333;
  font-size: 20px;
  margin-bottom: 15px;
  text-align: left;
}

.button-group {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 30px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  min-width: 120px;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: translateY(0);
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary.active {
  background: #5568d3;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.btn-danger:hover {
  background: #da190b;
}

.btn-speed {
  background: #e0e0e0;
  color: #333;
}

.btn-speed.active {
  background: #4caf50;
  color: white;
}

.btn-speed:hover {
  background: #d0d0d0;
}

.btn-speed.active:hover {
  background: #45a049;
}

.status-info {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #e0e0e0;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-label {
  font-size: 18px;
  color: #555;
  font-weight: 500;
}

.status-value {
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
}

.status-value.running {
  color: #4caf50;
}

.status-value.paused {
  color: #ff9800;
}
</style>
