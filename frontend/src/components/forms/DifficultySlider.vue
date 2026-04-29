<template>
  <div class="space-y-3">
    <div class="flex justify-between text-sm">
      <span class="text-green-600 transition-all" :class="{ 'font-bold scale-110': modelValue === 0 }">Easy</span>
      <span class="text-yellow-600 transition-all" :class="{ 'font-bold scale-110': modelValue === 1 }">Medium</span>
      <span class="text-red-600 transition-all" :class="{ 'font-bold scale-110': modelValue === 2 }">Hard</span>
    </div>
    
    <div class="relative py-2">
      <input type="range"
             :value="modelValue"
             @input="$emit('update:modelValue', parseInt($event.target.value))"
             min="0" max="2" step="1"
             class="w-full h-2 appearance-none rounded-lg cursor-pointer"
             :style="sliderStyle" />
      
      <div class="absolute top-1/2 left-0 right-0 flex justify-between px-1 -translate-y-1/2 pointer-events-none">
        <span v-for="i in 3" :key="i" 
              class="w-3 h-3 rounded-full transition-all duration-300"
              :class="modelValue >= i-1 ? 'bg-white scale-125' : 'bg-gray-300'">
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Number
})

const sliderStyle = computed(() => {
  const colors = ['#10b981', '#f59e0b', '#ef4444']
  const percentage = (props.modelValue / 2) * 100
  return {
    background: `linear-gradient(90deg, ${colors[0]} 0%, ${colors[1]} 50%, ${colors[2]} 100%)`,
    backgroundSize: `${percentage}% 100%`,
    backgroundRepeat: 'no-repeat'
  }
})
</script>

<style scoped>

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: all 0.2s;
}

input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
</style>