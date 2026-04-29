<template>
  <div class="bg-white rounded-2xl shadow-lg p-6 relative">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Test Summary</h3>
    
    <div class="grid grid-cols-2 gap-3 mb-6">
      <div class="bg-gray-50 rounded-xl p-3 text-center hover:scale-105 transition-transform">
        <div class="text-2xl font-bold text-blue-600">{{ totalQuestions }}</div>
        <div class="text-xs text-gray-500">Questions</div>
      </div>
      <div class="bg-gray-50 rounded-xl p-3 text-center hover:scale-105 transition-transform">
        <div class="text-2xl font-bold text-green-600">{{ totalMarks }}</div>
        <div class="text-xs text-gray-500">Marks</div>
      </div>
      <div class="bg-gray-50 rounded-xl p-3 text-center hover:scale-105 transition-transform">
        <div class="text-2xl font-bold text-orange-600">{{ duration }}m</div>
        <div class="text-xs text-gray-500">Duration</div>
      </div>
      <div class="bg-gray-50 rounded-xl p-3 text-center hover:scale-105 transition-transform">
        <div class="text-2xl font-bold text-purple-600">{{ answeredCount }}</div>
        <div class="text-xs text-gray-500">Answered</div>
      </div>
    </div>

    <h4 class="text-sm font-medium text-gray-700 mb-3">Question Palette</h4>
    <div class="grid grid-cols-5 gap-2 mb-4 relative">
      <div v-for="n in totalQuestions" :key="n"
           @mouseenter="hovered = n"
           @mouseleave="hovered = null"
           class="aspect-square rounded-lg flex items-center justify-center text-sm font-medium cursor-pointer transition-all duration-300 relative"
           :class="getClass(n)"
           :style="getStyle(n)">
        {{ n }}
        <div v-if="hovered === n" 
             class="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs py-1 px-2 rounded whitespace-nowrap z-20">
          Question {{ n }}
        </div>
      </div>
    </div>

    <div class="space-y-2 mb-6">
      <div class="flex items-center gap-2 text-xs">
        <div class="w-3 h-3 rounded bg-green-500"></div>
        <span class="text-gray-600">Answered ({{ answeredCount }})</span>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <div class="w-3 h-3 rounded bg-yellow-500"></div>
        <span class="text-gray-600">Marked ({{ markedQuestions.length }})</span>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <div class="w-3 h-3 rounded bg-gray-200"></div>
        <span class="text-gray-600">Not Visited ({{ totalQuestions - answeredCount }})</span>
      </div>
    </div>

    <!-- TAKE EXAM BUTTON - FIXED WITH CORRECT ROUTE NAME -->
    <div class="border-t pt-4 mt-2">
      <button 
        @click="goToTakeExam"
        class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-4 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 hover:shadow-lg flex items-center justify-center gap-2 group cursor-pointer"
        :disabled="!examId"
      >
        <span class="text-lg">📝</span>
        <span>{{ examId ? 'Take Exam Now' : 'Select Exam First' }}</span>
        <span class="text-lg group-hover:translate-x-1 transition-transform">→</span>
      </button>
      
      <!-- Quick Stats Tooltip -->
      <div class="mt-3 text-xs text-center text-gray-500">
        <span class="inline-flex items-center gap-1">
          <span class="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
          {{ answeredCount }} answered
        </span>
        <span class="mx-2">•</span>
        <span class="inline-flex items-center gap-1">
          <span class="w-1.5 h-1.5 bg-yellow-500 rounded-full"></span>
          {{ markedQuestions.length }} marked
        </span>
      </div>
    </div>

    <!-- Show warning if no exam selected -->
    <div v-if="!examId" class="mt-2 text-xs text-amber-600 text-center bg-amber-50 p-2 rounded-lg">
      ⚠️ Please select an exam first
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  totalQuestions: {
    type: Number,
    default: 0
  },
  answeredCount: {
    type: Number,
    default: 0
  },
  markedQuestions: {
    type: Array,
    default: () => []
  },
  totalMarks: {
    type: Number,
    default: 0
  },
  duration: {
    type: Number,
    default: 0
  },
  examId: {
    type: [Number, String],
    default: null
  }
})

const router = useRouter()
const hovered = ref(null)

const getClass = (n) => {
  if (n <= props.answeredCount) return 'bg-green-500 text-white hover:bg-green-600'
  if (props.markedQuestions.includes(n)) return 'bg-yellow-500 text-white hover:bg-yellow-600'
  return 'bg-gray-200 text-gray-600 hover:bg-gray-300'
}

const getStyle = (n) => {
  return hovered.value === n ? {
    transform: 'scale(1.2)',
    zIndex: 10,
    boxShadow: '0 8px 16px rgba(0,0,0,0.15)'
  } : {}
}

// Navigate to take exam page with correct route name 'take_exam'
const goToTakeExam = () => {
  console.log('Navigating to take_exam with ID:', props.examId)
  
  if (!props.examId) {
    console.error('No exam ID provided')
    alert('Please select an exam first')
    return
  }
  
  // Use the correct route name 'take_exam' (with underscore)
  router.push({
    name: 'take_exam',  // Changed from 'TakeExam' to 'take_exam'
    params: { examId: props.examId.toString() }
  })
}
</script>

<style scoped>

/* Add a subtle pulse animation for the button */
@keyframes gentle-pulse {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  }
  50% {
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
  }
}

button:not(:disabled) {
  animation: gentle-pulse 3s infinite;
}

button:hover:not(:disabled) {
  animation: none;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: linear-gradient(135deg, #94a3b8, #64748b);
}
</style>