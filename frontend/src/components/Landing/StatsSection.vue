<template>
  <section class="relative py-20 overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 -z-10"></div>
    
    <!-- Decorative circles -->
    <div class="absolute top-0 left-0 w-64 h-64 bg-white/10 rounded-full -translate-x-1/2 -translate-y-1/2"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 bg-white/10 rounded-full translate-x-1/2 translate-y-1/2"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
        <div 
          v-for="(stat, index) in stats" 
          :key="stat.label"
          class="text-center"
        >
          <!-- Icon -->
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white/20 backdrop-blur-sm mb-4">
            <span class="text-3xl">{{ stat.icon }}</span>
          </div>
          
          <!-- Number -->
          <div class="text-4xl md:text-5xl font-bold text-white mb-2">
            <span>{{ animatedValues[index] }}</span>
            <span class="text-2xl">{{ stat.suffix }}</span>
          </div>
          
          <!-- Label -->
          <p class="text-white/90 font-medium">{{ stat.label }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stats = [
  { value: 50, suffix: 'K+', label: 'Active Students', icon: '👨‍🎓' },
  { value: 500, suffix: '+', label: 'Partner Schools', icon: '🏫' },
  { value: 98, suffix: '%', label: 'Success Rate', icon: '🎯' },
  { value: 10, suffix: 'K+', label: 'Questions Bank', icon: '📚' }
]

const animatedValues = ref(stats.map(() => '0'))

const animateValue = (index, start, end, duration) => {
  const startTime = performance.now()
  
  const update = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)
    const current = Math.floor(start + (end - start) * easeOutQuart)
    
    animatedValues.value[index] = current.toLocaleString()
    
    if (progress < 1) {
      requestAnimationFrame(update)
    }
  }
  
  requestAnimationFrame(update)
}

onMounted(() => {
  setTimeout(() => {
    stats.forEach((stat, index) => {
      setTimeout(() => {
        animateValue(index, 0, stat.value, 2000)
      }, index * 200)
    })
  }, 500)
})
</script>


