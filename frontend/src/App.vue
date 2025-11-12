<script setup lang="ts">
import { onMounted } from 'vue'
import GameHeader from './components/GameHeader.vue'
import CharacterCard from './components/CharacterCard.vue'
import InventoryCard from './components/InventoryCard.vue'
import { useWebSocket } from './composables/useWebSocket'

const { timeString, isConnected, isRunning, currentSpeed, characters, publicStorage } = useWebSocket()

onMounted(() => {
  setTimeout(() => window.HSStaticMethods.autoInit(), 100)
})
</script>

<template>
  <div class="min-h-screen w-full">
    <!-- Header -->
    <div class="fixed top-0 left-0 right-0 z-50 bg-base-100 px-4 pt-4 pb-2">
      <GameHeader 
        :time-string="timeString" 
        :is-connected="isConnected"
        :is-running="isRunning"
        :current-speed="currentSpeed"
        @update:is-running="isRunning = $event"
        @update:current-speed="currentSpeed = $event"
      />
    </div>

    <!-- Main Content -->
    <div class="text-center pt-32">

      <!-- Tab Navigation -->
      <nav class="tabs tabs-bordered overflow-x-auto max-w-6xl mx-auto my-6 justify-center" aria-label="Tabs" role="tablist" aria-orientation="horizontal">
        <button
          type="button"
          class="tab active-tab:tab-active active"
          id="tab-characters-btn"
          data-tab="#tab-characters"
          aria-controls="tab-characters"
          role="tab"
        >
          <span class="icon-[tabler--users] size-5 shrink-0 me-2"></span>
          角色状态
        </button>
        <button
          type="button"
          class="tab active-tab:tab-active"
          id="tab-inventory-btn"
          data-tab="#tab-inventory"
          aria-controls="tab-inventory"
          role="tab"
        >
          <span class="icon-[tabler--package] size-5 shrink-0 me-2"></span>
          物品系统
        </button>
      </nav>

      <!-- Tab Content -->
      <div class="mt-6">
        <!-- Characters Section -->
        <div id="tab-characters" role="tabpanel" aria-labelledby="tab-characters-btn">
          <div class="max-w-6xl mx-auto my-8">
            <h2 class="text-4xl font-bold mb-5 drop-shadow-md">角色状态</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
              <CharacterCard
                v-for="char in characters"
                :key="char.id"
                :character="char"
              />
            </div>
          </div>
        </div>

        <!-- Inventory Section -->
        <div id="tab-inventory" class="hidden" role="tabpanel" aria-labelledby="tab-inventory-btn">
          <div class="max-w-7xl mx-auto my-8">
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
                :key="char.id"
                :inventory="char.inventory"
                :title="`${char.name}的背包`"
                :is-public-storage="false"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
