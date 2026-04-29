<template>
  <div @click="$emit('click')"
       class="flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all"
       :class="[
         active ? 'bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-600' : 'hover:bg-gray-50',
         completed ? 'opacity-75' : ''
       ]">
    <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
         :class="[
           active ? 'bg-blue-600 text-white' :
           completed ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-600'
         ]">
      <span v-if="completed">✓</span>
      <span v-else>{{ index }}</span>
    </div>
    <div>
      <div class="text-sm font-medium" :class="active ? 'text-blue-600' : 'text-gray-700'">
        {{ step }}
      </div>
      <div class="text-xs text-gray-500" v-if="active">Current step</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  step: String,
  index: Number,
  active: Boolean,
  completed: Boolean
})
</script>

<style scoped>
</style>
