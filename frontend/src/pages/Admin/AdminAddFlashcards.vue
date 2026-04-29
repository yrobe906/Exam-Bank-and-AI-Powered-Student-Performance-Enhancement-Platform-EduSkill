<template>
  <div class="min-h-screen bg-gray-50">
    <Header />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Breadcrumb -->
      <div class="flex items-center text-sm text-gray-500 mb-6">
        <router-link to="/admin_dashboard" class="hover:text-blue-600 transition-colors">Dashboard</router-link>
        <svg class="w-4 h-4 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
        <span class="text-gray-900 font-medium">Add Flashcards</span>
      </div>

      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Add Flashcards</h1>
        <p class="text-gray-600 mt-2">Create new flashcard decks and add cards to them</p>
      </div>

      <!-- Main Form -->
      <div class="grid lg:grid-cols-3 gap-8">
        <!-- Left Column - Deck Form -->
        <div class="lg:col-span-2">
          <!-- Create/Edit Deck Card -->
          <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">{{ editingDeck ? 'Edit Deck' : 'Create New Deck' }}</h2>
            
            <form @submit.prevent="saveDeck" class="space-y-4">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Deck Name *</label>
                  <input 
                    v-model="deckForm.name" 
                    type="text" 
                    required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Cell Structure"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Subject *</label>
                  <select 
                    v-model="deckForm.subject" 
                    required
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Subject</option>
                    <option value="Biology">Biology</option>
                    <option value="Physics">Physics</option>
                    <option value="Chemistry">Chemistry</option>
                    <option value="Maths">Maths</option>
                    <option value="English">English</option>
                  </select>
                </div>
              </div>

              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Topic</label>
                  <input 
                    v-model="deckForm.topic" 
                    type="text" 
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., Cell Biology"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Exam Board</label>
                  <select 
                    v-model="deckForm.exam_board" 
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Exam Type</option>
                    <option value="Entrance Exam">Entrance Exam</option>
                    <option value="Model Exam">Model Exam</option>
                    <option value="Worksheet">Worksheet</option>
                    <option value="Practice Questions">Practice Questions</option>
                    <option value="Scenario Question">Scenario Question</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea 
                  v-model="deckForm.description" 
                  rows="3"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Brief description of this flashcard deck..."
                ></textarea>
              </div>

              <div class="flex gap-3">
                <button 
                  type="submit" 
                  class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  {{ editingDeck ? 'Update Deck' : 'Create Deck' }}
                </button>
                <button 
                  v-if="editingDeck"
                  type="button" 
                  @click="cancelEdit"
                  class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>

          <!-- Add Flashcards Card -->
          <div class="bg-white rounded-xl shadow-sm p-6" v-if="currentDeckId">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Add Flashcards</h2>
              <span class="text-sm text-gray-500">Deck: {{ deckForm.name }}</span>
            </div>

            <!-- Bulk Add -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Add Multiple Cards (Question | Answer format)</label>
              <textarea 
                v-model="bulkCards"
                rows="6"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                placeholder="What is the mitochondria? | The powerhouse of the cell&#10;What is a prokaryote? | A cell without a nucleus"
              ></textarea>
              <p class="text-xs text-gray-500 mt-1">Separate each card with a new line, and question/answer with a pipe (|) symbol</p>
              <button 
                @click="addBulkCards"
                :disabled="!bulkCards.trim()"
                class="mt-3 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Add Bulk Cards
              </button>
            </div>

            <hr class="my-6">

            <!-- Single Card Add -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Add Single Card</label>
              
              <div class="space-y-4">
                <div>
                  <input 
                    v-model="cardForm.question" 
                    type="text" 
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Question (front of card)"
                  />
                </div>
                <div>
                  <textarea 
                    v-model="cardForm.answer" 
                    rows="3"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Answer (back of card)"
                  ></textarea>
                </div>
                <button 
                  @click="addSingleCard"
                  :disabled="!cardForm.question.trim() || !cardForm.answer.trim()"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Add Card
                </button>
              </div>
            </div>

            <!-- Current Cards List -->
            <div class="mt-8" v-if="currentDeckCards.length > 0">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Cards in this deck ({{ currentDeckCards.length }})</h3>
              
              <div class="space-y-3 max-h-96 overflow-y-auto">
                <div 
                  v-for="(card, index) in currentDeckCards" 
                  :key="card.id"
                  class="flex items-start justify-between p-4 bg-gray-50 rounded-lg group"
                >
                  <div class="flex-1 min-w-0">
                    <p class="font-medium text-gray-900 truncate">{{ card.question }}</p>
                    <p class="text-sm text-gray-500 truncate mt-1">{{ card.answer }}</p>
                  </div>
                  <div class="flex items-center gap-2 ml-4">
                    <button 
                      @click="deleteCard(card.id)"
                      class="p-2 text-gray-400 hover:text-red-600 transition-colors"
                      title="Delete card"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- No Deck Selected -->
          <div v-else class="bg-white rounded-xl shadow-sm p-12 text-center">
            <svg class="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Create a Deck First</h3>
            <p class="text-gray-600">Create a flashcard deck above to start adding cards.</p>
          </div>
        </div>

        <!-- Right Column - Existing Decks -->
        <div>
          <div class="bg-white rounded-xl shadow-sm p-6 sticky top-8">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Existing Decks</h2>
            
            <!-- Loading -->
            <div v-if="loadingDecks" class="flex justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>

            <!-- Decks List -->
            <div v-else class="space-y-3">
              <div 
                v-for="deck in decks" 
                :key="deck.id"
                class="p-4 border rounded-lg hover:border-blue-300 transition-colors cursor-pointer"
                :class="currentDeckId === deck.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
                @click="selectDeck(deck)"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1 min-w-0">
                    <h3 class="font-medium text-gray-900 truncate">{{ deck.name }}</h3>
                    <p class="text-sm text-gray-500">{{ deck.subject }} • {{ deck.card_count || 0 }} cards</p>
                  </div>
                  <div class="flex gap-1 ml-2">
                    <button 
                      @click.stop="editDeck(deck)"
                      class="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Edit deck"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button 
                      @click.stop="confirmDeleteDeck(deck.id)"
                      class="p-1 text-gray-400 hover:text-red-600 transition-colors"
                      title="Delete deck"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <p v-if="decks.length === 0" class="text-gray-500 text-sm text-center py-4">
                No decks yet. Create one to get started.
              </p>
            </div>

            <!-- Refresh Button -->
            <button 
              @click="loadDecks"
              class="mt-4 w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              Refresh Decks
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import * as flashcardService from '@/services/flashcardService'

// State
const loadingDecks = ref(false)
const decks = ref([])
const currentDeckId = ref(null)
const currentDeckCards = ref([])
const editingDeck = ref(null)
const bulkCards = ref('')

// Form State
const deckForm = ref({
  name: '',
  subject: '',
  topic: '',
  exam_board: '',
  description: ''
})

const cardForm = ref({
  question: '',
  answer: ''
})

// Methods
async function loadDecks() {
  loadingDecks.value = true
  try {
    const response = await flashcardService.getAllDecks()
    decks.value = response || []
  } catch (err) {
    console.error('Error loading decks:', err)
  } finally {
    loadingDecks.value = false
  }
}

async function saveDeck() {
  try {
    if (editingDeck.value) {
      await flashcardService.updateDeck(editingDeck.value.id, deckForm.value)
    } else {
      const newDeck = await flashcardService.createDeck(deckForm.value)
      currentDeckId.value = newDeck.id
    }
    
    await loadDecks()
    resetDeckForm()
    if (currentDeckId.value) {
      await loadDeckCards()
    }
  } catch (err) {
    console.error('Error saving deck:', err)
    alert('Failed to save deck. Please try again.')
  }
}

function editDeck(deck) {
  editingDeck.value = deck
  deckForm.value = {
    name: deck.name,
    subject: deck.subject,
    topic: deck.topic || '',
    exam_board: deck.exam_board || '',
    description: deck.description || ''
  }
  currentDeckId.value = deck.id
  loadDeckCards()
}

function cancelEdit() {
  editingDeck.value = null
  resetDeckForm()
}

function resetDeckForm() {
  editingDeck.value = null
  deckForm.value = {
    name: '',
    subject: '',
    topic: '',
    exam_board: '',
    description: ''
  }
}

async function confirmDeleteDeck(deckId) {
  if (confirm('Are you sure you want to delete this deck and all its cards?')) {
    try {
      await flashcardService.deleteDeck(deckId)
      if (currentDeckId.value === deckId) {
        currentDeckId.value = null
        currentDeckCards.value = []
      }
      await loadDecks()
    } catch (err) {
      console.error('Error deleting deck:', err)
      alert('Failed to delete deck.')
    }
  }
}

function selectDeck(deck) {
  currentDeckId.value = deck.id
  editingDeck.value = null
  deckForm.value = {
    name: deck.name,
    subject: deck.subject,
    topic: deck.topic || '',
    exam_board: deck.exam_board || '',
    description: deck.description || ''
  }
  loadDeckCards()
}

async function loadDeckCards() {
  if (!currentDeckId.value) return
  
  try {
    const response = await flashcardService.getDeckCards(currentDeckId.value)
    currentDeckCards.value = response || []
  } catch (err) {
    console.error('Error loading cards:', err)
  }
}

async function addBulkCards() {
  if (!bulkCards.value.trim() || !currentDeckId.value) return
  
  const lines = bulkCards.value.trim().split('\n')
  const cards = []
  
  for (const line of lines) {
    const parts = line.split('|')
    if (parts.length >= 2) {
      cards.push({
        deck_id: currentDeckId.value,
        question: parts[0].trim(),
        answer: parts.slice(1).join('|').trim(),
        order_index: cards.length
      })
    }
  }
  
  if (cards.length === 0) {
    alert('No valid cards found. Use format: Question | Answer')
    return
  }
  
  try {
    await flashcardService.createFlashcardsBulk(cards)
    bulkCards.value = ''
    await loadDeckCards()
    await loadDecks()
  } catch (err) {
    console.error('Error adding bulk cards:', err)
    alert('Failed to add cards.')
  }
}

async function addSingleCard() {
  if (!cardForm.value.question.trim() || !cardForm.value.answer.trim() || !currentDeckId.value) return
  
  try {
    await flashcardService.createFlashcard({
      deck_id: currentDeckId.value,
      question: cardForm.value.question,
      answer: cardForm.value.answer,
      order_index: currentDeckCards.value.length
    })
    
    cardForm.value.question = ''
    cardForm.value.answer = ''
    
    await loadDeckCards()
    await loadDecks()
  } catch (err) {
    console.error('Error adding card:', err)
    alert('Failed to add card.')
  }
}

async function deleteCard(cardId) {
  if (!confirm('Delete this card?')) return
  
  try {
    await flashcardService.deleteFlashcard(cardId)
    await loadDeckCards()
    await loadDecks()
  } catch (err) {
    console.error('Error deleting card:', err)
    alert('Failed to delete card.')
  }
}

// Lifecycle
onMounted(() => {
  loadDecks()
})
</script>
