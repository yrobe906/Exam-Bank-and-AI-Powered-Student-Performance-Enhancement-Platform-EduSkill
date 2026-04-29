<template>
  <div class="min-h-screen bg-gray-50">
    <EduskillHeader />
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb -->
      <div class="flex items-center text-sm text-gray-500 mb-6">
        <router-link to="/flashcards" class="hover:text-blue-600 transition-colors">Home</router-link>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <router-link to="/flashcards" class="hover:text-blue-600 transition-colors">Subjects</router-link>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <span class="text-gray-900 font-medium">{{ subjectName }}</span>
      </div>

      <!-- Trustpilot rating -->
      <div class="flex items-center mb-8">
        <div class="flex items-center bg-white px-5 py-2.5 rounded-xl shadow-sm">
          <span class="text-xl font-bold text-gray-900 mr-3">Excellent</span>
          <div class="flex items-center">
            <svg v-for="i in 5" :key="i" class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            <span class="ml-2 text-gray-600 text-sm">Trustpilot</span>
          </div>
        </div>
      </div>

      <!-- Subject header -->
      <div class="mb-10">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">{{ subjectName }} Flashcards</h1>
        <p class="text-lg text-gray-600 max-w-3xl leading-relaxed">
          Focus solely on what matters for your {{ subjectName }} exams. Our flashcards are carefully aligned 
          with your exam board, ensuring you only review what's necessary. Created by specialist 
          teachers and tutors, they're regularly updated to reflect the latest curriculum changes. 
          Make revision quicker and easier with bitsized information at your fingertips. Start now 
          with our {{ subjectName }} flashcards to streamline your study sessions.
        </p>
      </div>

      <!-- Exam boards -->
      <div class="flex flex-wrap gap-3 mb-8">
        <button v-for="board in examBoards" :key="board"
                @click="selectedBoard = board; loadDecks()"
                :class="[
                  'px-5 py-2.5 rounded-xl font-medium transition-all duration-300 shadow-sm hover:shadow-md',
                  selectedBoard === board 
                    ? 'bg-blue-600 text-white shadow-lg hover:bg-blue-700' 
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
                ]">
          {{ board }}
        </button>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-500 mb-4">{{ error }}</p>
        <button @click="loadDecks" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Try Again
        </button>
      </div>

      <!-- Topics/Decks grid -->
      <div v-else-if="decks.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="deck in decks" :key="deck.id" 
             class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 hover:shadow-xl transition-all duration-300 group">
          <div class="flex items-start justify-between mb-3">
            <h3 class="text-xl font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">{{ deck.name }}</h3>
            <span class="bg-blue-100 text-blue-700 text-xs font-semibold px-2.5 py-1 rounded-full">{{ deck.card_count || 0 }} cards</span>
          </div>
          <p class="text-gray-600 mb-4">{{ deck.description || 'No description available' }}</p>
          
          <div class="pt-4 border-t border-gray-200 flex justify-between items-center">
            <span class="text-sm text-gray-500">{{ deck.topic || 'General' }}</span>
            <router-link :to="`/flashcards/practice/${deck.id}`" 
                        class="text-blue-600 font-medium hover:text-blue-800 flex items-center group/btn transition-colors">
              Start 
              <svg class="w-4 h-4 ml-1 transform group-hover/btn:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12 bg-white rounded-xl shadow-sm">
        <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No Flashcards Available</h3>
        <p class="text-gray-600 mb-4">We don't have any {{ subjectName }} flashcards for this exam board yet.</p>
        <router-link to="/flashcards" class="text-blue-600 hover:text-blue-800 font-medium">
          Browse other subjects →
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import EduskillHeader from '@/components/Header/EduskillHeader.vue'
import * as flashcardService from '@/services/flashcardService'

const route = useRoute()

// State
const loading = ref(true)
const error = ref(null)
const decks = ref([])
const selectedBoard = ref('AQA')

const examBoards = ['Entrance Exam', 'Model Exam', 'Worksheet', 'Practice Questions', 'Scenario Question']

const subjectName = computed(() => {
  const subject = route.params.subject || 'Biology'
  return subject.charAt(0).toUpperCase() + subject.slice(1)
})

// Methods
async function loadDecks() {
  loading.value = true
  error.value = null
  
  try {
    const response = await flashcardService.getDecksBySubject(subjectName.value, selectedBoard.value)
    decks.value = response || []
  } catch (err) {
    console.error('Error loading decks:', err)
    error.value = 'Failed to load flashcards. Please try again.'
  } finally {
    loading.value = false
  }
}

// Watch for exam board changes
watch(selectedBoard, () => {
  loadDecks()
})

// Lifecycle
onMounted(() => {
  loadDecks()
})
</script>
