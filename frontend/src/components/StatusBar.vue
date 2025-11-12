<script setup lang="ts">
import { getStatusColorHex } from '../utils/statusColors'

defineProps<{
  label: string
  value: number
  reverse?: boolean
}>()
</script>

<template>
  <div class="flex items-center gap-2">
    <span class="text-sm font-semibold w-12 shrink-0">{{ label }}</span>
    <div class="flex-1 h-4 bg-gray-200 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-500 ease-in-out"
        :style="{
          width: value + '%',
          backgroundColor: getStatusColorHex(value, reverse)
        }"
      />
    </div>
    <span 
      class="text-sm font-semibold w-10 text-right shrink-0"
      :style="{ color: getStatusColorHex(value, reverse) }"
    >
      {{ value }}
    </span>
  </div>
</template>
