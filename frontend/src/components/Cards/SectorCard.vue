<template>
  <div @click="$emit('select', sector)"
       class="group relative p-6 rounded-xl cursor-pointer transition-all duration-300 hover:scale-105"
       :class="[
         selected 
           ? 'bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-xl' 
           : 'bg-gray-50 hover:bg-white hover:shadow-lg text-gray-700 border-2 border-transparent hover:border-blue-200'
       ]">
    <div class="relative">
      <span class="text-4xl mb-3 block transform group-hover:scale-110 group-hover:rotate-3 transition-transform">
        {{ sector.icon }}
      </span>
      
      <h3 class="font-semibold text-lg mb-1">{{ sector.name }}</h3>
      <p class="text-sm" :class="selected ? 'text-blue-100' : 'text-gray-500'">
        {{ sector.description }}
      </p>
    </div>

    <transition name="bounce">
      <div v-if="selected" class="absolute top-2 right-2 text-white">
        <span class="text-2xl">✓</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
defineProps({
  sector: Object,
  selected: Boolean
})
</script>

<style scoped>
.bounce-enter-active {
  animation: bounce 0.3s;
}

@keyframes bounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
</style>