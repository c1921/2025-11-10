<script setup lang="ts">
import { onMounted, ref } from 'vue'
import GameHeader from './components/GameHeader.vue'
import CharacterCard from './components/CharacterCard.vue'
import TimeControl from './components/TimeControl.vue'
import InventoryCard from './components/InventoryCard.vue'
import { useWebSocket } from './composables/useWebSocket'

const { timeString, isConnected, isRunning, currentSpeed, characters, publicStorage } = useWebSocket()

const activeTab = ref<'characters' | 'inventory'>('characters')

onMounted(() => {
  setTimeout(() => window.HSStaticMethods.autoInit(), 100)
})
</script>

<template>
  <div class="min-h-screen w-full">
    <!-- Header -->
    <GameHeader :time-string="timeString" :is-connected="isConnected" />

    <!-- Main Content -->
    <div class="text-center mt-5">
      <h1 class="text-5xl font-bold mb-5 drop-shadow-lg">游戏管理系统</h1>
      <p class="text-xl my-2 opacity-90">一天24小时，每小时200ms</p>
      <p class="text-xl my-2 opacity-90">时间会自动流逝并实时更新</p>

      <!-- Tab Navigation -->
      <div class="max-w-6xl mx-auto my-6 flex gap-4 justify-center">
        <button
          @click="activeTab = 'characters'"
          class="px-8 py-3 rounded-lg font-bold text-lg transition-all duration-200"
          :class="activeTab === 'characters' 
            ? 'shadow-lg scale-105' 
            : 'hover:bg-purple-500'"
        >
          👥 角色状态
        </button>
        <button
          @click="activeTab = 'inventory'"
          class="px-8 py-3 rounded-lg font-bold text-lg transition-all duration-200"
          :class="activeTab === 'inventory' 
            ? 'shadow-lg scale-105' 
            : 'bg-purple-600 text-white hover:bg-purple-500'"
        >
          📦 物品系统
        </button>
      </div>

      <!-- Characters Section -->
      <div v-if="activeTab === 'characters'" class="max-w-6xl mx-auto my-8">
        <h2 class="text-4xl font-bold mb-5 drop-shadow-md">角色状态</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
          <CharacterCard
            v-for="char in characters"
            :key="char.name"
            :character="char"
          />
        </div>
      </div>

      <!-- Inventory Section -->
      <div v-if="activeTab === 'inventory'" class="max-w-7xl mx-auto my-8">
        <h2 class="text-4xl font-bold mb-5 drop-shadow-md">物品与背包</h2>
        
        <!-- Public Storage -->
        <div class="mb-8">
          <InventoryCard
            :inventory="publicStorage"
            title="公共仓库"
            :is-public-storage="true"
          />
        </div>

        <!-- Character Inventories -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <InventoryCard
            v-for="char in characters"
            :key="char.name"
            :inventory="char.inventory"
            :title="`${char.name}的背包`"
            :is-public-storage="false"
          />
        </div>
      </div>

      <!-- Time Control -->
      <TimeControl
        :is-running="isRunning"
        :current-speed="currentSpeed"
        @update:is-running="isRunning = $event"
        @update:current-speed="currentSpeed = $event"
      />
    </div>
  </div>
</template>
