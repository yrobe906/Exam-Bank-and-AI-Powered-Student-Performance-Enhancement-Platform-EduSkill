<template>
  <div @click="$emit('update:selected', !selected)"
       class="relative p-3 rounded-lg cursor-pointer overflow-hidden transition-all duration-300"
       :class="[
         selected ? selectedClass : 'bg-gray-50 hover:bg-white border border-gray-200 hover:border-blue-500'
       ]">
    <div class="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity"></div>
    
    <div class="flex items-center gap-2">
      <div class="w-5 h-5 rounded border-2 flex items-center justify-center transition-all"
           :class="selected ? 'border-white bg-white/20' : 'border-gray-400'">
        <span v-if="selected" class="text-xs">✓</span>
      </div>
      
      <div>
        <div class="font-medium text-sm" :class="selected ? 'text-white' : 'text-gray-900'">
          {{ section.name }}
        </div>
        <div class="text-xs" :class="selected ? 'text-white/80' : 'text-gray-500'">
          {{ section.count }} questions
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  section: Object,
  selected: Boolean
})

// Use computed property with static class mapping
const selectedClass = computed(() => {
  const colorMap = {
    blue: 'bg-blue-500 text-white shadow-lg scale-105',
    green: 'bg-green-500 text-white shadow-lg scale-105',
    purple: 'bg-purple-500 text-white shadow-lg scale-105',
    orange: 'bg-orange-500 text-white shadow-lg scale-105'
  }
  return colorMap[props.section.color] || colorMap.blue
})
</script>

<style scoped>
</style>
