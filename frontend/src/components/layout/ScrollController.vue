<template>
  <div 
    class="absolute z-50 flex flex-col items-center gap-2"
    :class="positionClass"
    :style="positionStyle"
  >
    <!-- Vertical Line with Moving Indicator -->
    <div class="relative" :class="lineHeightClass">
      <!-- Base Line -->
      <div 
        class="absolute inset-0 w-full h-full rounded-full"
        :class="lineColorClass"
      ></div>
      <!-- Moving Indicator -->
      <div 
        class="absolute left-1/2 -translate-x-1/2 rounded-full transition-all duration-300 shadow-lg"
        :class="indicatorClass"
        :style="{ top: scrollProgress + '%' }"
      ></div>
    </div>
    
    <!-- Up Button with Enhanced Hover Animation -->
    <button 
      @click="onScrollUp"
      :disabled="!canScrollUp"
      class="group flex items-center justify-center shadow-md hover:shadow-xl transition-all duration-300 ease-out transform hover:scale-110 active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:scale-100"
      :class="buttonClass"
      :title="'Scroll Up'"
    >
      <ChevronUpIcon :class="[iconClass, 'transition-transform duration-300 group-hover:-translate-y-0.5']" />
    </button>
    
    <!-- Down Button with Enhanced Hover Animation -->
    <button 
      @click="onScrollDown"
      :disabled="!canScrollDown"
      class="group flex items-center justify-center shadow-md hover:shadow-xl transition-all duration-300 ease-out transform hover:scale-110 active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:scale-100"
      :class="buttonClass"
      :title="'Scroll Down'"
    >
      <ChevronDownIcon :class="[iconClass, 'transition-transform duration-300 group-hover:translate-y-0.5']" />
    </button>
    
    <!-- Progress Percentage -->
    <div 
      class="text-xs font-medium rounded-full shadow-md border animate-pulse"
      :class="percentageClass"
    >
      {{ scrollProgress }}%
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronUpIcon, ChevronDownIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  scrollProgress: { type: Number, default: 0 },
  canScrollUp: { type: Boolean, default: false },
  canScrollDown: { type: Boolean, default: true },
  onScrollUp: { type: Function, required: true },
  onScrollDown: { type: Function, required: true },
  position: { type: String, default: 'right' }, // 'left' or 'right'
  size: { type: String, default: 'md' }, // 'sm', 'md', 'lg'
  theme: { type: String, default: 'blue' } // 'blue', 'green', 'purple'
})

// Computed classes based on props
const positionClass = computed(() => {
  if (props.position === 'right') return 'right-4'
  return 'left-4'
})

const positionStyle = computed(() => {
  return {
    top: `50%`,
    transform: `translateY(-50%)`
  }
})

const lineHeightClass = computed(() => {
  const sizes = {
    sm: 'h-20 w-0.5',
    md: 'h-32 w-0.5',
    lg: 'h-40 w-1'
  }
  return sizes[props.size] || sizes.md
})

const lineColorClass = computed(() => {
  return 'bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200'
})

const indicatorClass = computed(() => {
  const sizes = {
    sm: 'w-1 h-5',
    md: 'w-1.5 h-8',
    lg: 'w-2 h-10'
  }
  
  const themes = {
    blue: 'bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] shadow-[#0fb9b1]/30',
    green: 'bg-gradient-to-b from-green-600 to-green-400 shadow-green-400/30',
    purple: 'bg-gradient-to-b from-purple-600 to-purple-400 shadow-purple-400/30'
  }
  
  return `${sizes[props.size]} ${themes[props.theme] || themes.blue}`
})

const buttonClass = computed(() => {
  const sizes = {
    sm: 'w-6 h-6 rounded-full',
    md: 'w-8 h-8 rounded-lg',
    lg: 'w-10 h-10 rounded-lg'
  }
  
  const themes = {
    blue: 'bg-blue-600 text-white hover:bg-blue-700 border-0',
    green: 'bg-green-600 text-white hover:bg-green-700 border-0',
    purple: 'bg-purple-600 text-white hover:bg-purple-700 border-0'
  }
  
  return `${sizes[props.size]} ${themes[props.theme] || themes.blue}`
})

const iconClass = computed(() => {
  const sizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  }
  return sizes[props.size]
})

const percentageClass = computed(() => {
  const sizes = {
    sm: 'px-1.5 py-0.5 text-[10px]',
    md: 'px-2 py-1 text-xs',
    lg: 'px-2.5 py-1.5 text-sm'
  }
  
  return `${sizes[props.size]} bg-white/90 backdrop-blur-sm text-gray-600 border-gray-100`
})
</script>
