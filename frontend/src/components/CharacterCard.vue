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

// 特质徽章颜色映射
const getTraitBadgeClass = (trait: string): string => {
  const traitColors: Record<string, string> = {
    strong: 'badge-error',           // 强壮 - 红色
    efficient_sleeper: 'badge-info', // 高效睡眠 - 蓝色
    good_appetite: 'badge-success',  // 好胃口 - 绿色
    cheerful: 'badge-warning',       // 开朗 - 黄色
    quick_learner: 'badge-secondary',// 手巧 - 紫色
    resilient: 'badge-accent',       // 坚韧 - 青色
    gourmand: 'badge-primary',       // 美食家 - 主色
    workaholic: 'badge-neutral'      // 工作狂 - 中性色
  }
  return traitColors[trait] || 'badge-ghost'
}
</script>

<template>
  <div
    class="p-4 rounded-2xl shadow-lg transition-transform duration-300 hover:-translate-y-1"
  >
    <div class="flex items-center justify-between gap-2 mb-3">
      <h3 class="text-xl font-bold shrink-0">{{ character.name }}</h3>
      <div class="flex items-center gap-2 text-xs flex-1 min-w-0">
        <span class="font-medium truncate">
          {{ getActionIcon(character.current_action) }}
          {{ getActionLabel(character.current_action) }}
        </span>
        <span class="text-gray-500 shrink-0">
          {{ character.action_duration }}h
        </span>
      </div>
      <span class="badge badge-primary badge-sm shrink-0">
        {{ character.gender === 'male' ? '♂ 男' : '♀ 女' }}
      </span>
    </div>

    <div class="text-xs mb-2 text-gray-600">
      年龄: {{ character.age_string }}
    </div>

    <div class="flex flex-wrap gap-1 mb-2" v-if="character.trait_names && character.trait_names.length > 0">
      <span
        v-for="(traitName, index) in character.trait_names"
        :key="index"
        class="badge badge-sm"
        :class="getTraitBadgeClass(character.traits?.[index] || '')"
      >
        {{ traitName }}
      </span>
    </div>

    <p class="text-xs mb-3 italic opacity-80">
      {{ character.status_text }}
    </p>

    <div class="flex flex-col gap-2">
      <StatusBar label="疲劳" :value="character.fatigue" :reverse="true" />
      <StatusBar label="饥饿" :value="character.hunger" :reverse="true" />
      <StatusBar label="心情" :value="character.mood" :reverse="true" />
    </div>
  </div>
</template>
