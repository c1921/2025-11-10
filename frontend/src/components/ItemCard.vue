<script setup lang="ts">
import type { ItemStack } from '@/types/game'

defineProps<{
  itemStack: ItemStack
}>()

// 根据稀有度返回颜色
const getRarityColor = (rarity: string) => {
  const colors: Record<string, string> = {
    common: 'bg-gray-500',
    uncommon: 'bg-green-500',
    rare: 'bg-blue-500',
    epic: 'bg-purple-500',
    legendary: 'bg-orange-500'
  }
  return colors[rarity] || 'bg-gray-500'
}

// 根据类别返回图标
const getCategoryIcon = (category: string) => {
  const icons: Record<string, string> = {
    food: '🍖',
    tool: '🔨',
    material: '📦',
    equipment: '⚔️',
    consumable: '🧪',
    misc: '📋'
  }
  return icons[category] || '📋'
}

// 根据类别返回中文名
const getCategoryName = (category: string) => {
  const names: Record<string, string> = {
    food: '食物',
    tool: '工具',
    material: '材料',
    equipment: '装备',
    consumable: '消耗品',
    misc: '杂项'
  }
  return names[category] || '未知'
}

const getRarityName = (rarity: string) => {
  const names: Record<string, string> = {
    common: '普通',
    uncommon: '非凡',
    rare: '稀有',
    epic: '史诗',
    legendary: '传说'
  }
  return names[rarity] || '未知'
}
</script>

<template>
  <div
    class="rounded-lg p-4 shadow-md hover:shadow-lg transition-all duration-200 border-2"
    :class="getRarityColor(itemStack.item.rarity).replace('bg-', 'border-')"
  >
    <!-- 物品头部 -->
    <div class="flex items-start justify-between mb-2">
      <div class="flex items-center gap-2">
        <span class="text-3xl">{{ getCategoryIcon(itemStack.item.category) }}</span>
        <div>
          <h3 class="font-bold text-lg">{{ itemStack.item.name }}</h3>
          <div class="flex gap-2 items-center">
            <span
              class="text-xs px-2 py-0.5 rounded text-white"
              :class="getRarityColor(itemStack.item.rarity)"
            >
              {{ getRarityName(itemStack.item.rarity) }}
            </span>
            <span class="text-xs">{{ getCategoryName(itemStack.item.category) }}</span>
          </div>
        </div>
      </div>
      <div class="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">
        {{ itemStack.quantity }}
      </div>
    </div>

    <!-- 物品描述 -->
    <p class="text-sm mb-2">{{ itemStack.item.description }}</p>

    <!-- 物品效果 -->
    <div v-if="Object.keys(itemStack.item.effects).length > 0" class="mb-2">
      <div class="text-xs font-semibold mb-1">效果:</div>
      <div class="flex flex-wrap gap-1">
        <span
          v-for="(value, key) in itemStack.item.effects"
          :key="key"
          class="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded"
        >
          {{ key === 'fatigue' ? '疲劳' : key === 'hunger' ? '饥饿' : key === 'mood' ? '心情' : key }}
          +{{ value }}
        </span>
      </div>
    </div>

    <!-- 物品属性 -->
    <div class="grid grid-cols-2 gap-2 text-xs">
      <div>重量: {{ itemStack.item.weight }} kg</div>
      <div>价值: {{ itemStack.item.value }} 金币</div>
    </div>
  </div>
</template>

