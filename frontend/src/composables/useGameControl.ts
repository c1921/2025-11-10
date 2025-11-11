import { ref } from 'vue'

export function useGameControl() {
  const toggleTime = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/time/toggle', {
        method: 'POST'
      })
      const data = await response.json()
      return data.time.running
    } catch (error) {
      console.error('切换时间状态失败:', error)
      throw error
    }
  }

  const setSpeed = async (speed: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/time/speed/${speed}`, {
        method: 'POST'
      })
      const data = await response.json()
      if (data.status === 'success') {
        return speed
      }
      throw new Error('设置速度失败')
    } catch (error) {
      console.error('设置速度失败:', error)
      throw error
    }
  }

  return {
    toggleTime,
    setSpeed
  }
}
