<template>
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-4"
  >
    <button
      v-show="isVisible"
      @click="scrollToTop"
      class="fixed bottom-8 right-8 z-50 group"
      aria-label="Back to top"
    >
      <!-- Progress Ring -->
      <svg class="w-16 h-16 transform -rotate-90" viewBox="0 0 64 64">
        <!-- Background circle -->
        <circle
          cx="32"
          cy="32"
          r="28"
          stroke="currentColor"
          stroke-width="4"
          fill="transparent"
          class="text-gray-200"
        />
        <!-- Progress circle -->
        <circle
          cx="32"
          cy="32"
          r="28"
          stroke="url(#gradient)"
          stroke-width="4"
          fill="transparent"
          stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="strokeDashoffset"
          class="transition-all duration-300"
        />
        <!-- Gradient definition -->
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#6366f1" />
            <stop offset="100%" stop-color="#a855f7" />
          </linearGradient>
        </defs>
      </svg>
      
      <!-- Arrow Icon -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
        <svg 
          class="w-6 h-6 text-indigo-600 transform group-hover:-translate-y-1 transition-transform duration-300" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
        </svg>
      </div>
    </button>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const scrollProgress = ref(0)

const circumference = 2 * Math.PI * 28 // r = 28
const strokeDashoffset = computed(() => {
  return circumference - (scrollProgress.value / 100) * circumference
})

const handleScroll = () => {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  
  // Show button when scrolled down 300px
  isVisible.value = scrollTop > 300
  
  // Calculate progress
  if (docHeight > 0) {
    scrollProgress.value = Math.min((scrollTop / docHeight) * 100, 100)
  }
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Check initial state
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

