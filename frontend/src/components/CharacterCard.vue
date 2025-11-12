<script setup lang="ts">
import type { Character } from '../types/game'
import StatusBar from './StatusBar.vue'

defineProps<{
  character: Character
}>()

// 行动类型的中文映射
const actionLabels: Record<string, string> = {
  rest: '休息',
  lumbering: '伐木',
  mining: '采石',
  gathering: '采集浆果',
  farming: '种植',
  eat: '进食',
  entertainment: '娱乐'
}

// 行动类型的图标映射
const actionIcons: Record<string, string> = {
  rest: '😴',
  lumbering: '🪓',
  mining: '⛏️',
  gathering: '🫐',
  farming: '🌾',
  eat: '🍽️',
  entertainment: '🎮'
}

const getActionLabel = (action: string) => actionLabels[action] || action
const getActionIcon = (action: string) => actionIcons[action] || '❓'
</script>

<template>
  <div
    class="p-6 rounded-2xl shadow-lg transition-transform duration-300 hover:-translate-y-1"
  >
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-2xl font-bold">{{ character.name }}</h3>
      <span class="badge badge-primary">
        {{ character.gender === 'male' ? '♂ 男' : '♀ 女' }}
      </span>
    </div>

    <!-- 当前行动 -->
    <div
      class="mb-4 p-3 rounded-xl border border-blue-200"
    >
      <div class="flex items-center justify-between">
        <span class="font-medium">
          {{ getActionIcon(character.current_action) }}
          {{ getActionLabel(character.current_action) }}
        </span>
        <span class="text-sm text-gray-500">
          {{ character.action_duration }}小时
        </span>
      </div>
    </div>

    <p class="text-sm mb-5 italic">
      {{ character.status_text }}
    </p>

    <div class="flex flex-col gap-4">
      <StatusBar label="疲劳" :value="character.fatigue" :reverse="true" />
      <StatusBar label="饥饿" :value="character.hunger" :reverse="true" />
      <StatusBar label="心情" :value="character.mood" :reverse="true" />
    </div>
  </div>
</template>
