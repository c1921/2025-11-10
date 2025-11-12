<script setup lang="ts">
import { useGameControl } from '../composables/useGameControl'

defineProps<{
  timeString: string
  isConnected: boolean
  isRunning: boolean
  currentSpeed: number
}>()

const emit = defineEmits<{
  'update:isRunning': [value: boolean]
  'update:currentSpeed': [value: number]
}>()

const { toggleTime, setSpeed } = useGameControl()

const handleToggleTime = async () => {
  try {
    const running = await toggleTime()
    emit('update:isRunning', running)
  } catch (error) {
    console.error('切换时间失败:', error)
  }
}

const handleSetSpeed = async (speed: number) => {
  try {
    const newSpeed = await setSpeed(speed)
    emit('update:currentSpeed', newSpeed)
  } catch (error) {
    console.error('设置速度失败:', error)
  }
}
</script>

<template>
  <div class="flex items-center justify-between gap-6 p-5 rounded-2xl shadow-lg">
    <!-- 左侧：游戏时间 -->
    <div class="flex items-center gap-3 min-w-0">
      <span class="text-lg font-medium whitespace-nowrap">游戏时间：</span>
      <span class="text-3xl font-bold text-primary font-mono drop-shadow-sm">
        {{ timeString }}
      </span>
    </div>

    <!-- 中间：时间控制 -->
    <div class="flex items-center gap-4">
      <!-- 时间控制按钮 -->
      <button
        @click="handleToggleTime"
        class="btn btn-sm"
        :class="isRunning ? 'btn-primary' : 'btn-outline btn-primary'"
      >
        {{ isRunning ? '⏸' : '▶' }}
      </button>

      <!-- 分隔线 -->
      <div class="h-8 w-px bg-base-300"></div>

      <!-- 流速按钮 -->
      <div class="flex gap-2">
        <button
          @click="handleSetSpeed(1)"
          class="btn btn-sm"
          :class="currentSpeed === 1 ? 'btn-success' : 'btn-outline'"
        >
          1x
        </button>
        <button
          @click="handleSetSpeed(2)"
          class="btn btn-sm"
          :class="currentSpeed === 2 ? 'btn-success' : 'btn-outline'"
        >
          2x
        </button>
        <button
          @click="handleSetSpeed(5)"
          class="btn btn-sm"
          :class="currentSpeed === 5 ? 'btn-success' : 'btn-outline'"
        >
          5x
        </button>
      </div>

      <!-- 分隔线 -->
      <div class="h-8 w-px bg-base-300"></div>

      <!-- 状态信息 -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="text-sm">状态:</span>
          <span
            class="text-sm font-bold"
            :class="isRunning ? 'text-success' : 'text-warning'"
          >
            {{ isRunning ? '运行' : '暂停' }}
          </span>
        </div>
      </div>
    </div>

    <!-- 右侧：连接状态 -->
    <div
      class="px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap"
      :class="isConnected ? 'bg-success text-white' : 'bg-error text-white'"
    >
      {{ isConnected ? '已连接' : '未连接' }}
    </div>
  </div>
</template>
