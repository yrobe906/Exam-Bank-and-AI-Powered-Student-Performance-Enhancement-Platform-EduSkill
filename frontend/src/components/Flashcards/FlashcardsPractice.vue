<template>
  <div class="min-h-screen bg-gray-50">
    <EduskillHeader>
      <p>Flashcards Practice</p>
    </EduskillHeader>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb and navigation -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center text-sm text-gray-500">
          <router-link to="/flashcards" class="hover:text-blue-600 transition-colors">Home</router-link>
          <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          <router-link :to="`/flashcards/subject/${subjectId}`" class="hover:text-blue-600 transition-colors">{{ subjectName }}</router-link>
          <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
          <span class="text-gray-900 font-medium">{{ currentTopic }}</span>
        </div>
        
        <button class="text-gray-500 hover:text-gray-700 p-2 rounded-lg hover:bg-gray-100 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-500 mb-4">{{ error }}</p>
        <button @click="loadDeck" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          Try Again
        </button>
      </div>

      <!-- Main content -->
      <div v-else-if="deck" class="flex flex-col lg:flex-row gap-8">
        <!-- Left sidebar -->
        <aside class="w-full lg:w-64 flex-shrink-0 order-2 lg:order-1">
          <div class="bg-white rounded-xl shadow-sm p-4">
            <div class="mb-4">
              <h3 class="font-semibold text-gray-900 mb-2">Course</h3>
              <p class="text-sm text-gray-600">GCSE / {{ subjectName }} / {{ selectedBoard }} / Flashcards</p>
            </div>
            
            <nav class="space-y-1">
              <router-link to="/library" class="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
                Course Resources
              </router-link>
              <router-link to="/flashcards" class="block px-3 py-2 bg-blue-50 text-blue-600 font-medium rounded-lg">
                Flashcards
              </router-link>
              <a href="#" class="block px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
                Exam Practice
              </a>
            </nav>
          </div>

          <!-- Topics list -->
          <div class="bg-white rounded-xl shadow-sm p-4 mt-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-semibold text-gray-900">Topics</h3>
              <button class="text-sm text-blue-600 hover:text-blue-800">View all</button>
            </div>
            
            <div class="space-y-4">
              <div v-for="topic in topics" :key="topic.id">
                <div class="flex items-center justify-between mb-2">
                  <span class="font-medium text-gray-900 text-sm">{{ topic.name }}</span>
                  <span class="text-xs text-gray-500">{{ topic.card_count || 0 }}</span>
                </div>
                <button 
                  v-if="topic.id === deckId"
                  class="block w-full text-left px-2 py-1.5 text-sm rounded bg-blue-100 text-blue-700 font-medium">
                  {{ deck.name }}
                </button>
              </div>
            </div>
          </div>
        </aside>

        <!-- Main content -->
        <div class="flex-1 order-1 lg:order-2">
          <!-- Flashcard stats -->
          <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <h2 class="text-2xl font-bold text-gray-900">{{ deck.name }} Flashcards</h2>
              
              <!-- Exam board selector -->
              <div class="flex gap-2">
                <button v-for="board in examBoards" :key="board"
                        @click="selectedBoard = board; loadDeck()"
                        :class="[
                          'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                          selectedBoard === board 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        ]">
                  {{ board }}
                </button>
              </div>
            </div>
            
            <div class="flex flex-wrap gap-4 mt-6">
              <div class="flex-1 min-w-[120px] bg-yellow-50 rounded-xl p-4 border border-yellow-100">
                <div class="text-sm text-gray-600 mb-1">Still learning</div>
                <div class="text-3xl font-bold text-gray-900">{{ stillLearning }}</div>
                <div class="text-xs text-gray-500">cards</div>
              </div>
              <div class="flex-1 min-w-[120px] bg-green-50 rounded-xl p-4 border border-green-100">
                <div class="text-sm text-gray-600 mb-1">Know</div>
                <div class="text-3xl font-bold text-gray-900">{{ know }}</div>
                <div class="text-xs text-gray-500">cards</div>
              </div>
              <div class="flex-1 min-w-[120px] bg-purple-50 rounded-xl p-4 border border-purple-100">
                <div class="text-sm text-gray-600 mb-1">Revisit</div>
                <div class="text-3xl font-bold text-gray-900">{{ revisit }}</div>
                <div class="text-xs text-gray-500">cards</div>
              </div>
            </div>
          </div>

          <!-- Flashcard -->
          <div class="bg-white rounded-xl shadow-sm mb-6 overflow-hidden" v-if="cards.length > 0">
            <!-- Progress bar -->
            <div class="h-1 bg-gray-100">
              <div class="h-full bg-blue-600 transition-all duration-500" :style="{ width: `${progressPercentage}%` }"></div>
            </div>
            
            <div class="p-6 sm:p-8">
              <!-- Card header -->
              <div class="flex justify-between items-start mb-6">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ deck.name }}</h3>
                  <p class="text-sm text-gray-500">Card {{ currentCardIndex + 1 }} of {{ totalCards }}</p>
                </div>
                <button class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100 transition-colors" title="Share">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                </button>
              </div>

              <!-- Flashcard content - Flip animation with 3D effect -->
              <div class="relative mb-8" style="perspective: 1000px;">
                <div 
                  @click="flipCard" 
                  class="cursor-pointer min-h-[280px] flex items-center justify-center p-8 rounded-2xl border-2 transition-all duration-700"
                  :class="isFlipped ? 'rotate-y-180' : ''"
                  style="transform-style: preserve-3d; transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);"
                >
                  <!-- Front side - Question -->
                  <div 
                    v-if="!isFlipped"
                    class="absolute inset-0 flex items-center justify-center p-8 bg-gradient-to-br from-violet-500 via-purple-500 to-fuchsia-500 rounded-xl shadow-2xl"
                    style="backface-visibility: hidden;"
                  >
                    <div class="text-center">
                      <div class="inline-flex items-center justify-center w-12 h-12 bg-white/20 rounded-full mb-4">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <p class="text-xl sm:text-2xl text-white font-medium leading-relaxed drop-shadow-md">
                        {{ currentCard.question }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Back side - Answer -->
                  <div 
                    v-else
                    class="absolute inset-0 flex items-center justify-center p-8 bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-500 rounded-xl shadow-2xl"
                    style="backface-visibility: hidden; transform: rotateY(180deg);"
                  >
                    <div class="text-center">
                      <div class="inline-flex items-center justify-center w-12 h-12 bg-white/20 rounded-full mb-4">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <p class="text-xl sm:text-2xl text-white font-medium leading-relaxed drop-shadow-md">
                        {{ currentCard.answer }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Flip hint -->
                <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-white px-4 py-2 rounded-full shadow-lg flex items-center text-sm text-purple-600 font-medium">
                  <svg class="w-4 h-4 mr-2 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Click to flip
                </div>
              </div>

              <!-- Actions -->
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div class="flex flex-wrap gap-2">
                  <button @click="markAs('learning')" 
                          class="px-5 py-2.5 bg-yellow-100 text-yellow-700 rounded-xl font-medium hover:bg-yellow-200 transition-colors flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Still learning
                  </button>
                  <button @click="markAs('known')"
                          class="px-5 py-2.5 bg-green-100 text-green-700 rounded-xl font-medium hover:bg-green-200 transition-colors flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    I know this
                  </button>
                </div>
                
                <div class="flex items-center gap-2">
                  <button @click="prevCard" 
                          :disabled="currentCardIndex === 0"
                          class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Previous
                  </button>
                  <button @click="nextCard"
                          :disabled="currentCardIndex === totalCards - 1"
                          class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center">
                    Next
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Help section -->
              <div class="mt-6 pt-6 border-t border-gray-200">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <button class="text-gray-600 hover:text-gray-900 flex items-center self-start">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Stuck? Help with this card
                  </button>
                  
                  <div class="flex items-center space-x-3">
                    <span class="text-sm text-gray-500">Was this flashcard deck helpful?</span>
                    <button class="px-3 py-1.5 bg-gray-100 rounded-lg hover:bg-gray-200 text-sm transition-colors">Yes</button>
                    <button class="px-3 py-1.5 bg-gray-100 rounded-lg hover:bg-gray-200 text-sm transition-colors">No</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty cards state -->
          <div v-else class="bg-white rounded-xl shadow-sm p-12 text-center">
            <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">No Cards Available</h3>
            <p class="text-gray-600">This deck doesn't have any flashcards yet.</p>
          </div>

          <!-- Cards in this collection -->
          <div class="bg-white rounded-xl shadow-sm p-6" v-if="cards.length > 0">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Cards in this collection ({{ totalCards }})</h3>
            
            <div class="space-y-3">
              <div v-for="(card, index) in cards" :key="card.id"
                   class="border border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:bg-blue-50/50 transition-all cursor-pointer"
                   @click="goToCard(index)"
                   :class="{ 'border-blue-500 bg-blue-50': currentCardIndex === index }">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <p class="text-gray-900 mb-1.5 font-medium">{{ card.question }}</p>
                    <p class="text-gray-600 text-sm line-clamp-2">{{ card.answer }}</p>
                  </div>
                  <span class="text-xs text-gray-400 ml-4 flex-shrink-0">#{{ index + 1 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer tip -->
      <div class="mt-8 text-center text-sm text-gray-500 bg-white py-4 px-6 rounded-xl shadow-sm">
        <span class="font-medium text-blue-600">Pro tip:</span> There are 1000 μm in 1 mm
      </div>
    </div>
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
const deck = ref(null)
const cards = ref([])
const topics = ref([])
const currentCardIndex = ref(0)
const isFlipped = ref(false)
const stillLearning = ref(0)
const know = ref(0)
const revisit = ref(0)
const selectedBoard = ref('Entrance Exam')
const userId = ref(1) // Default user ID for demo

const examBoards = ['Entrance Exam', 'Model Exam', 'Worksheet', 'Practice Questions', 'Scenario Question']

const deckId = computed(() => {
  const id = route.params.subjectId
  return isNaN(parseInt(id)) ? 1 : parseInt(id)
})

const subjectId = computed(() => {
  return deck.value?.subject?.toLowerCase() || 'biology'
})

const subjectName = computed(() => {
  return deck.value?.subject || 'Biology'
})

const currentTopic = computed(() => deck.value?.name || 'Flashcards')

const totalCards = computed(() => cards.value.length)
const currentCard = computed(() => cards.value[currentCardIndex.value] || {})
const progressPercentage = computed(() => totalCards.value > 0 ? ((currentCardIndex.value + 1) / totalCards.value) * 100 : 0)

// Methods
async function loadDeck() {
  loading.value = true
  error.value = null
  
  try {
    // Get deck details with cards
    const deckResponse = await flashcardService.getDeck(deckId.value)
    deck.value = deckResponse
    cards.value = deckResponse.cards || []
    
    // Get deck statistics
    try {
      const stats = await flashcardService.getDeckStats(deckId.value, userId.value)
      stillLearning.value = stats.learning_count || 0
      know.value = stats.known_count || 0
      revisit.value = stats.revisit_count || 0
    } catch (statsError) {
      console.log('Could not load stats:', statsError)
    }
    
    // Load topics (all decks for this subject)
    try {
      const decksResponse = await flashcardService.getDecksBySubject(subjectName.value, selectedBoard.value)
      topics.value = decksResponse || []
    } catch (topicsError) {
      console.log('Could not load topics:', topicsError)
    }
  } catch (err) {
    console.error('Error loading deck:', err)
    error.value = 'Failed to load flashcards. Please try again.'
  } finally {
    loading.value = false
  }
}

function flipCard() {
  isFlipped.value = !isFlipped.value
}

function nextCard() {
  if (currentCardIndex.value < totalCards.value - 1) {
    currentCardIndex.value++
    isFlipped.value = false
  }
}

function prevCard() {
  if (currentCardIndex.value > 0) {
    currentCardIndex.value--
    isFlipped.value = false
  }
}

function goToCard(index) {
  currentCardIndex.value = index
  isFlipped.value = false
}

async function markAs(status) {
  const card = currentCard.value
  if (!card) return
  
  try {
    await flashcardService.updateCardProgress(card.id, userId.value, status)
    
    // Update local counts
    if (status === 'learning') {
      stillLearning.value++
    } else if (status === 'known') {
      know.value++
    } else if (status === 'revisit') {
      revisit.value++
    }
  } catch (err) {
    console.error('Error updating progress:', err)
  }
  
  nextCard()
}

// Watch for deck ID changes
watch(() => route.params.subjectId, () => {
  loadDeck()
})

// Lifecycle
onMounted(() => {
  loadDeck()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 3D Flip Animation Styles */
.perspective-1000 {
  perspective: 1000px;
}

.preserve-3d {
  transform-style: preserve-3d;
}

.rotate-y-180 {
  transform: rotateY(180deg);
}

/* Smooth flip transition */
div[style*="transform-style: preserve-3d"] {
  transform-style: preserve-3d;
}

div[style*="transform: rotateY(180deg)"] {
  transform: rotateY(180deg);
}
</style>
