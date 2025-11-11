<script setup lang="ts">
import type { Character } from '../types/game'
import StatusBar from './StatusBar.vue'

defineProps<{
  character: Character
}>()
</script>

<template>
  <div
    class="bg-white/95 p-6 rounded-2xl shadow-lg transition-transform duration-300 hover:-translate-y-1"
  >
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-2xl font-bold text-gray-800">{{ character.name }}</h3>
      <span class="badge badge-primary">
        {{ character.gender === 'male' ? '♂ 男' : '♀ 女' }}
      </span>
    </div>

    <p class="text-gray-600 text-sm mb-5 italic">
      {{ character.status_text }}
    </p>

    <div class="flex flex-col gap-4">
      <StatusBar label="疲劳" :value="character.fatigue" :reverse="false" />
      <StatusBar label="饥饿" :value="character.hunger" :reverse="false" />
      <StatusBar label="心情" :value="character.mood" :reverse="true" />
    </div>
  </div>
</template>
