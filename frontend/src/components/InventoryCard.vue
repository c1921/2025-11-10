<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Inventory } from '@/types/game'
import ItemCard from './ItemCard.vue'

const props = defineProps<{
  inventory: Inventory
  title: string
  isPublicStorage?: boolean
}>()

const isExpanded = ref(true)

const usagePercent = computed(() => {
  return (props.inventory.used_slots / props.inventory.max_slots) * 100
})

const getUsageColor = computed(() => {
  if (usagePercent.value >= 90) return 'bg-red-500'
  if (usagePercent.value >= 70) return 'bg-yellow-500'
  return 'bg-green-500'
})
</script>

<template>
  <div class="rounded-xl shadow-lg p-5">
    <!-- 标题栏 -->
    <div class="flex items-center justify-between mb-4 cursor-pointer" @click="isExpanded = !isExpanded">
      <div class="flex items-center gap-3">
        <span class="text-3xl">{{ isPublicStorage ? '🏛️' : '🎒' }}</span>
        <div>
          <h2 class="text-2xl font-bold">{{ title }}</h2>
          <p class="text-sm">
            {{ inventory.used_slots }} / {{ inventory.max_slots }} 格
          </p>
        </div>
      </div>
      <button class="text-2xl transition-transform" :class="{ 'rotate-180': !isExpanded }">
        ▼
      </button>
    </div>

    <!-- 容量进度条 -->
    <div class="w-full bg-gray-200 rounded-full h-3 mb-4">
      <div
        class="h-3 rounded-full transition-all duration-300"
        :class="getUsageColor"
        :style="{ width: `${usagePercent}%` }"
      ></div>
    </div>

    <!-- 物品列表 -->
    <div v-if="isExpanded">
      <div v-if="inventory.items.length === 0" class="text-center text-gray-500 py-8">
        <p class="text-xl">📭</p>
        <p>空空如也</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <ItemCard
          v-for="(itemStack, index) in inventory.items"
          :key="`${itemStack.item.item_id}-${index}`"
          :item-stack="itemStack"
        />
      </div>
    </div>
  </div>
</template>

