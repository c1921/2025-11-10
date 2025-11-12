import { ref, onMounted, onUnmounted } from 'vue'
import type { GameUpdate, GameTime, WebSocketMessage, Inventory } from '@/types/game'

export function useWebSocket() {
  const timeString = ref<string>('第1天 0时')
  const isConnected = ref<boolean>(false)
  const isRunning = ref<boolean>(true)
  const currentSpeed = ref<number>(1)
  const characters = ref<any[]>([])
  const publicStorage = ref<Inventory>({ max_slots: 0, used_slots: 0, items: [] })

  let ws: WebSocket | null = null

  const connectWebSocket = () => {
    ws = new WebSocket('ws://localhost:8000/ws')

    ws.onopen = () => {
      isConnected.value = true
      console.log('WebSocket连接成功')
    }

    ws.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data)
      if (message.type === 'game_update') {
        const data = message.data as GameUpdate
        timeString.value = data.time.time_string
        isRunning.value = data.time.running
        currentSpeed.value = data.time.speed
        characters.value = data.characters
        publicStorage.value = data.public_storage
      } else if (message.type === 'speed_update' || message.type === 'status_update') {
        const data = message.data as GameTime
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

  const disconnect = () => {
    if (ws) {
      ws.close()
    }
  }

  onMounted(() => {
    connectWebSocket()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    timeString,
    isConnected,
    isRunning,
    currentSpeed,
    characters,
    publicStorage,
    connectWebSocket,
    disconnect
  }
}
