<template>
  <div class="bg-white rounded-2xl shadow-lg p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <span class="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full"></span>
      Questions Preview ({{ questions.length }})
    </h3>
    <div class="space-y-3 max-h-96 overflow-y-auto">
      <div v-for="(q, i) in questions" :key="q.id"
           class="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-blue-500 transition-all group">
        <div class="flex justify-between items-center">
          <span class="font-medium text-blue-600">
            Q{{ i+1 }}
            <span v-if="q.section_id" class="text-xs text-gray-400">(Section {{ q.section_id }})</span>
          </span>
          <div class="flex gap-2">
            <button @click="$emit('edit', q)" title="Edit" class="text-blue-500 hover:text-blue-700">
              ✎
            </button>
            <button @click="deleteQuestion(q.id)" title="Delete" class="text-red-500 hover:text-red-700">
              🗑
            </button>
          </div>
        </div>
        <p class="text-gray-700">{{ q.question_text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  sectionId: { type: [Number, String], default: null } // Optional: filter by section
})

const emit = defineEmits(['edit', 'deleted'])

const questions = ref([])

async function fetchQuestions() {
  let url = 'http://localhost:8000/api/questions'
  if (props.sectionId) {
    url += `?section_id=${props.sectionId}`
  }
  try {
    const res = await fetch(url)
    questions.value = await res.json()
  } catch (err) {
    questions.value = []
  }
}

async function deleteQuestion(id) {
  if (!confirm('Delete this question?')) return
  try {
    const res = await fetch(`http://localhost:8000/api/questions/${id}`, { method: 'DELETE' })
    if (res.ok) {
      questions.value = questions.value.filter(q => q.id !== id)
      emit('deleted', id)
    } else {
      alert('Failed to delete question')
    }
  } catch (err) {
    alert('Error deleting question')
  }
}

onMounted(fetchQuestions)
watch(() => props.sectionId, fetchQuestions)
</script>