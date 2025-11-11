<script setup lang="ts">
import { onMounted } from 'vue'
import GameHeader from './components/GameHeader.vue'
import CharacterCard from './components/CharacterCard.vue'
import TimeControl from './components/TimeControl.vue'
import { useWebSocket } from './composables/useWebSocket'

const { timeString, isConnected, isRunning, currentSpeed, characters } = useWebSocket()

onMounted(() => {
  setTimeout(() => window.HSStaticMethods.autoInit(), 100)
})
</script>

<template>
  <div class="min-h-screen w-full bg-linear-to-br from-primary to-purple-700 p-5">
    <!-- Header -->
    <GameHeader :time-string="timeString" :is-connected="isConnected" />

    <!-- Main Content -->
    <div class="text-center text-white mt-5">
      <h1 class="text-5xl font-bold mb-5 drop-shadow-lg">游戏时间系统</h1>
      <p class="text-xl my-2 opacity-90">一天24小时，每小时200ms</p>
      <p class="text-xl my-2 opacity-90">时间会自动流逝并实时更新</p>

      <!-- Characters Section -->
      <div class="max-w-6xl mx-auto my-8">
        <h2 class="text-4xl font-bold mb-5 drop-shadow-md">角色状态</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
          <CharacterCard
            v-for="char in characters"
            :key="char.name"
            :character="char"
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
