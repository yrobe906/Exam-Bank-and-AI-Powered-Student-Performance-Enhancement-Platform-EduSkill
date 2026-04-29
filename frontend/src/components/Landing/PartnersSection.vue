<template>
  <section class="relative py-12 overflow-hidden bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <p class="text-center text-gray-500 text-sm font-medium mb-8 uppercase tracking-wider">
        Trusted by Leading Institutions
      </p>
      
      <!-- Infinite Scroll Marquee -->
      <div class="relative flex overflow-x-hidden">
        <div class="animate-marquee whitespace-nowrap flex gap-16 items-center">
          <!-- First set -->
          <div v-for="partner in partners" :key="partner.name" class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-xl">
              {{ partner.icon }}
            </div>
            <span class="text-lg font-semibold text-gray-700">{{ partner.name }}</span>
          </div>
          <!-- Duplicate -->
          <div v-for="partner in partners" :key="partner.name + '-dup'" class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-xl">
              {{ partner.icon }}
            </div>
            <span class="text-lg font-semibold text-gray-700">{{ partner.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const partners = [
  { name: 'Harvard University', icon: '🎓' },
  { name: 'MIT', icon: '🔬' },
  { name: 'Stanford', icon: '📚' },
  { name: 'Oxford', icon: '🏛️' },
  { name: 'Cambridge', icon: '🎓' },
  { name: 'Yale', icon: '📖' },
  { name: 'Princeton', icon: '🎯' },
  { name: 'Columbia', icon: '🌟' }
]
</script>

<style scoped>
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.animate-marquee {
  animation: marquee 25s linear infinite;
}
.animate-marquee:hover {
  animation-play-state: paused;
}
</style>


