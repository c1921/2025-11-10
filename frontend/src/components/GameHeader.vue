<script setup lang="ts">
defineProps<{
  timeString: string
  isConnected: boolean
}>()
</script>

<template>
  <div class="flex justify-between items-center bg-white/95 p-5 rounded-2xl shadow-lg mb-8">
    <div class="flex items-center gap-3">
      <span class="text-lg font-medium text-gray-600">游戏时间：</span>
      <span class="text-3xl font-bold text-primary font-mono drop-shadow-sm">
        {{ timeString }}
      </span>
    </div>
    <div
      class="px-4 py-2 rounded-full text-sm font-medium transition-all"
      :class="isConnected ? 'bg-success text-white' : 'bg-error text-white'"
    >
      {{ isConnected ? '已连接' : '未连接' }}
    </div>
  </div>
</template>
