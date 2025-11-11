<script setup lang="ts">
import { useGameControl } from '../composables/useGameControl'

defineProps<{
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
  <div class="max-w-3xl mx-auto bg-white/95 p-8 rounded-3xl shadow-xl">
    <!-- 时间控制 -->
    <div class="mb-8">
      <h3 class="text-xl font-bold text-gray-800 mb-4">时间控制</h3>
      <div class="flex gap-4 justify-center">
        <button
          @click="handleToggleTime"
          class="btn btn-lg"
          :class="isRunning ? 'btn-primary' : 'btn-outline btn-primary'"
        >
          {{ isRunning ? '⏸ 暂停' : '▶ 继续' }}
        </button>
      </div>
    </div>

    <!-- 时间流速 -->
    <div class="mb-8">
      <h3 class="text-xl font-bold text-gray-800 mb-4">时间流速</h3>
      <div class="flex gap-4 justify-center flex-wrap">
        <button
          @click="handleSetSpeed(1)"
          class="btn btn-lg"
          :class="currentSpeed === 1 ? 'btn-success' : 'btn-outline'"
        >
          1x
        </button>
        <button
          @click="handleSetSpeed(2)"
          class="btn btn-lg"
          :class="currentSpeed === 2 ? 'btn-success' : 'btn-outline'"
        >
          2x
        </button>
        <button
          @click="handleSetSpeed(5)"
          class="btn btn-lg"
          :class="currentSpeed === 5 ? 'btn-success' : 'btn-outline'"
        >
          5x
        </button>
      </div>
    </div>

    <!-- 状态信息 -->
    <div class="flex justify-center gap-10 pt-6 border-t-2 border-gray-200">
      <div class="flex items-center gap-3">
        <span class="text-lg font-medium text-gray-600">状态:</span>
        <span
          class="text-xl font-bold"
          :class="isRunning ? 'text-success' : 'text-warning'"
        >
          {{ isRunning ? '运行中' : '已暂停' }}
        </span>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-lg font-medium text-gray-600">速度:</span>
        <span class="text-xl font-bold text-primary">{{ currentSpeed }}x</span>
      </div>
    </div>
  </div>
</template>
