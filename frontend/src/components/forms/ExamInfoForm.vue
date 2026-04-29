<template>
  <div class="bg-white rounded-2xl shadow-lg p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <span class="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full"></span>
      Exam Information
    </h3>
    
    <div class="grid grid-cols-1 gap-4">
      <div>
        <label class="text-sm text-gray-600">Topic</label>
        <input
          type="text"
          :value="topic"
          @input="$emit('update:topic', $event.target.value)"
          class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-0 transition-all"
          placeholder="e.g., Algebra — Quadratic Equations"
        />
      </div>

      <div>
        <label class="text-sm text-gray-600">Exam Title</label>
        <input
          type="text"
          :value="title"
          @input="$emit('update:title', $event.target.value)"
          class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-0 transition-all"
          placeholder="e.g., Mid-term Mathematics Exam"
        />
      </div>

      <div>
        <label class="text-sm text-gray-600">Total Marks</label>
        <input
          type="number"
          :value="totalMarks"
          readonly
          class="w-full px-4 py-2 bg-gray-100 border-2 border-gray-200 rounded-xl"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  topic: { type: String, default: '' },
  title: { type: String, default: '' },
  totalMarks: { type: Number, default: 0 }
})

defineEmits(['update:topic', 'update:title'])
</script>

<style scoped>
</style>
