<script setup lang="ts">
import { getStatusColorHex } from '../utils/statusColors'

defineProps<{
  label: string
  value: number
  reverse?: boolean
}>()
</script>

<template>
  <div class="flex flex-col gap-1">
    <div class="flex justify-between text-sm font-semibold text-gray-700">
      <span>{{ label }}</span>
      <span :style="{ color: getStatusColorHex(value, reverse) }">
        {{ value }}
      </span>
    </div>
    <div class="w-full h-5 bg-gray-200 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-500 ease-in-out"
        :style="{
          width: value + '%',
          backgroundColor: getStatusColorHex(value, reverse)
        }"
      />
    </div>
  </div>
</template>
