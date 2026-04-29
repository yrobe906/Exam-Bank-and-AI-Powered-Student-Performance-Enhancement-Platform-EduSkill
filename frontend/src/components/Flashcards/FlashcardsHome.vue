<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-50 via-white to-purple-50">
    <EduskillHeader />
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Hero section with flashcards -->
      <div class="bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 rounded-3xl p-8 mb-8 text-white relative overflow-hidden shadow-2xl transform hover:scale-[1.01] transition-transform duration-300">
        <!-- Decorative elements -->
        <div class="absolute top-0 right-0 w-80 h-80 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 animate-pulse"></div>
        <div class="absolute bottom-0 left-0 w-64 h-64 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2"></div>
        <div class="absolute top-1/2 left-1/2 w-40 h-40 bg-yellow-300/20 rounded-full -translate-x-1/2 -translate-y-1/2"></div>
        
        <div class="max-w-3xl relative z-10">
          <h1 class="text-4xl md:text-5xl font-bold mb-6 drop-shadow-lg">Flashcards to practice</h1>
          <div class="flex items-center mb-8 flex-wrap gap-4">
            <span class="text-3xl font-bold bg-white/20 px-5 py-2 rounded-xl backdrop-blur-sm">Cell Structure</span>
            <span class="text-xl font-semibold bg-yellow-400 text-yellow-900 px-4 py-2 rounded-full shadow-lg">{{ totalCards > 0 ? `1/${totalCards}` : '1/28' }}</span>
          </div>
          <p class="text-lg mb-8 opacity-95 leading-relaxed bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20">
            Quickly review key terms, definitions, phrases, quotes and more with Flashcards. 
            Focus on what matters most by easily sorting cards into 'I know this' and 'Still learning' 
            piles so you can optimise your revision.
          </p>
          
          <!-- Feature bullets -->
          <div class="space-y-4 mb-8">
            <div class="flex items-center bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10 hover:bg-white/20 transition-all duration-300 cursor-default">
              <svg class="w-6 h-6 mr-3 flex-shrink-0 text-yellow-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="font-medium">Written by expert teachers and examiners</span>
            </div>
            <div class="flex items-center bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10 hover:bg-white/20 transition-all duration-300 cursor-default">
              <svg class="w-6 h-6 mr-3 flex-shrink-0 text-yellow-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="font-medium">Aligned to exam specifications</span>
            </div>
            <div class="flex items-center bg-white/10 p-3 rounded-xl backdrop-blur-sm border border-white/10 hover:bg-white/20 transition-all duration-300 cursor-default">
              <svg class="w-6 h-6 mr-3 flex-shrink-0 text-yellow-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="font-medium">Ideal for on-the-go revision</span>
            </div>
          </div>
          
          <button @click="scrollToSubjects" class="bg-white text-purple-600 px-10 py-4 rounded-2xl font-bold text-lg hover:bg-yellow-400 hover:text-purple-900 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 transform">
            Explore Flashcards
          </button>
        </div>
      </div>

      <!-- Why students love our Flashcards -->
      <div class="mb-16">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-10 text-center bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent">Why students love our Flashcards</h2>
        
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="bg-white p-8 rounded-2xl shadow-md hover:shadow-2xl hover:shadow-purple-200 transition-all duration-300 border-2 border-transparent hover:border-purple-300 group cursor-default">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center mb-5 group-hover:scale-110 group-hover:rotate-6 transition-transform duration-300 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3 group-hover:text-blue-600 transition-colors">Study more efficiently</h3>
            <p class="text-gray-600 leading-relaxed">Sort cards into 'Still learning' and 'I know this' piles to avoid wasting time revising material you already know.</p>
          </div>

          <!-- Feature 2 -->
          <div class="bg-white p-8 rounded-2xl shadow-md hover:shadow-2xl hover:shadow-fuchsia-200 transition-all duration-300 border-2 border-transparent hover:border-fuchsia-300 group cursor-default">
            <div class="w-16 h-16 bg-gradient-to-br from-fuchsia-400 to-pink-600 rounded-2xl flex items-center justify-center mb-5 group-hover:scale-110 group-hover:-rotate-6 transition-transform duration-300 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3 group-hover:text-fuchsia-600 transition-colors">Revise on the go</h3>
            <p class="text-gray-600 leading-relaxed">Easily flip through flashcards while waiting in a queue, riding the bus or in between classes.</p>
          </div>

          <!-- Feature 3 -->
          <div class="bg-white p-8 rounded-2xl shadow-md hover:shadow-2xl hover:shadow-green-200 transition-all duration-300 border-2 border-transparent hover:border-green-300 group cursor-default">
            <div class="w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-600 rounded-2xl flex items-center justify-center mb-5 group-hover:scale-110 group-hover:rotate-6 transition-transform duration-300 shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold mb-3 group-hover:text-green-600 transition-colors">Boost exam confidence</h3>
            <p class="text-gray-600 leading-relaxed">Flashcards boost long-term retention so you'll feel prepared heading into your exams.</p>
          </div>
        </div>
      </div>

      <!-- How to use Flashcards effectively - 4 Steps -->
      <div class="bg-white rounded-3xl p-10 shadow-lg mb-16 border-2 border-purple-100">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4 text-center bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">How to use Flashcards effectively</h2>
        <p class="text-gray-600 mb-10 max-w-2xl mx-auto text-center text-lg">Want to make your revision more effective and boost your exam results? Here are four simple steps to help you get the most out of our Flashcards.</p>
        
        <!-- Step 1 -->
        <div class="flex items-start mb-8 group">
          <div class="w-14 h-14 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-2xl flex items-center justify-center font-bold text-xl mr-5 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">1</div>
          <div class="bg-gradient-to-r from-violet-50 to-purple-50 p-6 rounded-2xl flex-1 border border-violet-100 hover:shadow-md transition-all duration-300">
            <h3 class="text-xl font-bold mb-2 text-violet-700">Start with the most difficult topics</h3>
            <p class="text-gray-600">Use your specification to identify your most challenging topics. Use our flashcards to build core knowledge, learn key definitions and gain confidence in these areas first.</p>
          </div>
        </div>
        
        <!-- Step 2 -->
        <div class="flex items-start mb-8 group">
          <div class="w-14 h-14 bg-gradient-to-r from-fuchsia-500 to-pink-600 text-white rounded-2xl flex items-center justify-center font-bold text-xl mr-5 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">2</div>
          <div class="bg-gradient-to-r from-fuchsia-50 to-pink-50 p-6 rounded-2xl flex-1 border border-fuchsia-100 hover:shadow-md transition-all duration-300">
            <h3 class="text-xl font-bold mb-2 text-fuchsia-700">Review regularly using spaced repetition</h3>
            <p class="text-gray-600">Don't cramming! Review your flashcards in short, regular sessions. Move cards you know to the 'I know this' pile and keep practicing the ones you don't.</p>
          </div>
        </div>
        
        <!-- Step 3 -->
        <div class="flex items-start mb-8 group">
          <div class="w-14 h-14 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-2xl flex items-center justify-center font-bold text-xl mr-5 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">3</div>
          <div class="bg-gradient-to-r from-cyan-50 to-blue-50 p-6 rounded-2xl flex-1 border border-cyan-100 hover:shadow-md transition-all duration-300">
            <h3 class="text-xl font-bold mb-2 text-cyan-700">Test yourself under exam conditions</h3>
            <p class="text-gray-600">Time yourself when going through flashcards. Try to recall the answer before flipping the card. This builds speed and confidence for real exams.</p>
          </div>
        </div>
        
        <!-- Step 4 -->
        <div class="flex items-start group">
          <div class="w-14 h-14 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-2xl flex items-center justify-center font-bold text-xl mr-5 flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300">4</div>
          <div class="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-2xl flex-1 border border-green-100 hover:shadow-md transition-all duration-300">
            <h3 class="text-xl font-bold mb-2 text-green-700">Track your progress and focus on weak areas</h3>
            <p class="text-gray-600">Use the analytics to see which topics need more practice. Concentrate your revision on areas where you're making the most mistakes.</p>
          </div>
        </div>
      </div>

      <!-- Browse Flashcards by subject -->
      <div id="subjects-section" class="mb-16">
        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-8 text-center bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent">Browse Flashcards by subject</h2>
        
<!-- Loading state -->
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
        </div>
        
        <!-- Error state -->
        <div v-else-if="error" class="text-center py-12">
          <p class="text-red-500 mb-4">{{ error }}</p>
          <button @click="loadDecks" class="px-6 py-3 bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all">
            Try Again
          </button>
        </div>
        
        <!-- Subjects list -->
        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          <router-link 
            v-for="subject in subjects" 
            :key="subject.name"
            :to="`/flashcards/subject/${subject.name.toLowerCase()}`" 
            class="bg-white p-6 rounded-2xl shadow-md hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 border-2 border-transparent hover:border-purple-300 group cursor-pointer"
          >
            <div class="flex items-center justify-between">
              <div>
                <span class="text-lg font-bold text-gray-900 group-hover:text-purple-600 transition-colors">{{ subject.name }} Flashcards</span>
                <span class="block text-sm text-gray-500 mt-1">{{ subject.count }} decks • {{ subject.totalCards }} cards</span>
              </div>
              <div :class="subject.colorClass" class="w-12 h-12 rounded-xl flex items-center justify-center group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 shadow-md">
                <component :is="subject.icon" class="w-6 h-6" />
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </main>
    
    <!-- Main Footer -->
    <MainFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, h } from 'vue'
import EduskillHeader from '@/components/Header/EduskillHeader.vue'
import MainFooter from '@/components/Footer/MainFooter.vue'
import * as flashcardService from '@/services/flashcardService'

// State
const loading = ref(true)
const error = ref(null)
const decks = ref([])

// Subject icons as render functions
const BiologyIcon = () => h('svg', { class: 'w-5 h-5 text-green-600', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z' })
])

const EnglishIcon = () => h('svg', { class: 'w-5 h-5 text-purple-600', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' })
])

const PhysicsIcon = () => h('svg', { class: 'w-5 h-5 text-blue-600', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
])

const ChemistryIcon = () => h('svg', { class: 'w-5 h-5 text-yellow-600', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z' })
])

const MathsIcon = () => h('svg', { class: 'w-5 h-5 text-red-600', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z' })
])

// Subject configuration
const subjectConfig = {
  'Biology': { icon: BiologyIcon, colorClass: 'bg-green-100' },
  'English': { icon: EnglishIcon, colorClass: 'bg-purple-100' },
  'Physics': { icon: PhysicsIcon, colorClass: 'bg-blue-100' },
  'Chemistry': { icon: ChemistryIcon, colorClass: 'bg-yellow-100' },
  'Maths': { icon: MathsIcon, colorClass: 'bg-red-100' }
}

// Group decks by subject
const subjects = computed(() => {
  const grouped = {}
  
  decks.value.forEach(deck => {
    const subject = deck.subject || 'Other'
    if (!grouped[subject]) {
      grouped[subject] = {
        name: subject,
        count: 0,
        totalCards: 0,
        ...(subjectConfig[subject] || { icon: BiologyIcon, colorClass: 'bg-gray-100' })
      }
    }
    grouped[subject].count++
    grouped[subject].totalCards += deck.card_count || 0
  })
  
  return Object.values(grouped)
})

const totalCards = computed(() => {
  return decks.value.reduce((sum, deck) => sum + (deck.card_count || 0), 0)
})

// Methods
async function loadDecks() {
  loading.value = true
  error.value = null
  
  try {
    const response = await flashcardService.getAllDecks()
    decks.value = response || []
    
    // If no decks, try to seed sample data
    if (decks.value.length === 0) {
      try {
        await flashcardService.seedSampleDecks()
        const newDecks = await flashcardService.getAllDecks()
        decks.value = newDecks || []
      } catch (seedError) {
        console.log('Could not seed sample data:', seedError)
      }
    }
  } catch (err) {
    console.error('Error loading decks:', err)
    error.value = 'Failed to load flashcards. Please try again.'
  } finally {
    loading.value = false
  }
}

function scrollToSubjects() {
  document.getElementById('subjects-section')?.scrollIntoView({ behavior: 'smooth' })
}

// Lifecycle
onMounted(() => {
  loadDecks()
})
</script>
