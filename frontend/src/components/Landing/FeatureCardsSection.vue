<template>
  <section id="features" class="relative py-24 overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 bg-gradient-to-b from-white via-gray-50 to-white -z-10"></div>
    
    <!-- Decorative elements -->
    <div class="absolute top-20 left-10 w-72 h-72 bg-indigo-100 rounded-full blur-3xl opacity-50"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <span class="inline-block px-4 py-1.5 rounded-full bg-indigo-100 text-indigo-600 text-sm font-semibold mb-4">
          ✨ Powerful Features
        </span>
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Everything You Need to
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
            Succeed
          </span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Discover our comprehensive suite of learning tools designed to help you achieve your academic goals faster and more effectively.
        </p>
      </div>

      <!-- Feature Cards Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="(feature, index) in features"
          :key="feature.title"
          class="group relative"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <!-- Card -->
          <div 
            class="feature-card relative overflow-hidden rounded-3xl bg-white shadow-lg hover:shadow-2xl transition-all duration-500 cursor-pointer"
            @mouseenter="handleMouseEnter($event)"
            @mouseleave="handleMouseLeave($event)"
            @mousemove="handleMouseMove($event)"
          >
            <!-- Image -->
            <div class="relative h-56 overflow-hidden">
              <img 
                :src="feature.image" 
                :alt="feature.title"
                class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
                loading="lazy"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
              
              <!-- Icon badge -->
              <div class="absolute top-4 right-4 w-12 h-12 rounded-xl bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-lg">
                <span class="text-2xl">{{ feature.icon }}</span>
              </div>
            </div>

            <!-- Content -->
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 mb-2 group-hover:text-indigo-600 transition-colors duration-300">
                {{ feature.title }}
              </h3>
              <p class="text-gray-600 mb-4">
                {{ feature.description }}
              </p>
              
              <!-- Features list -->
              <ul class="space-y-2">
                <li 
                  v-for="item in feature.items" 
                  :key="item"
                  class="flex items-center gap-2 text-sm text-gray-500"
                >
                  <svg class="w-4 h-4 text-indigo-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  {{ item }}
                </li>
              </ul>

              <!-- Learn more link -->
              <div class="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
                <span class="text-sm font-medium text-indigo-600 group-hover:text-indigo-700 transition-colors">
                  Learn more
                </span>
                <svg class="w-5 h-5 text-indigo-600 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                </svg>
              </div>
            </div>

            <!-- Gradient border on hover -->
            <div class="absolute inset-0 rounded-3xl border-2 border-transparent group-hover:border-indigo-500/30 transition-colors duration-300 pointer-events-none"></div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="mt-16 text-center">
        <button class="group relative px-8 py-4 text-lg font-bold rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-indigo-500/30">
          <span class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600"></span>
          <span class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-xl"></span>
          <span class="relative flex items-center gap-2 text-white">
            Explore All Features
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    title: 'Exam Bank',
    description: 'Access thousands of carefully curated exam questions across all subjects with detailed explanations.',
    icon: '📝',
    image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
    items: ['50,000+ Questions', 'Detailed Solutions', 'Topic-wise Organization']
  },
  {
    title: 'Mock Tests',
    description: 'Take realistic mock exams that simulate the actual test environment with timed conditions.',
    icon: '📋',
    image: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
    items: ['Real Exam Simulation', 'Instant Results', 'Performance Comparison']
  },
  {
    title: 'Flashcards',
    description: 'Master concepts quickly with our intelligent flashcard system featuring spaced repetition.',
    icon: '🗂️',
    image: 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2022&q=80',
    items: ['Smart Review', 'Custom Decks', 'Progress Tracking']
  },
  {
    title: 'Gamification',
    description: 'Stay motivated with achievements, leaderboards, badges, and rewards as you learn.',
    icon: '🎮',
    image: 'https://images.unsplash.com/photo-1511512578047-dfb367046420?ixlib=rb-4.0.3&auto=format&fit=crop&w=2071&q=80',
    items: ['Achievements', 'Leaderboards', 'Daily Challenges']
  },
  {
    title: 'Performance Analytics',
    description: 'Track your progress with detailed analytics and insights to identify improvement areas.',
    icon: '📊',
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
    items: ['Detailed Reports', 'Weakness Analysis', 'Progress Trends']
  },
  {
    title: 'AI Integration',
    description: 'Get personalized learning recommendations and instant help from our AI-powered assistant.',
    icon: '🤖',
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
    items: ['Personalized Learning', '24/7 Support', 'Smart Suggestions']
  }
]

// 3D Tilt Effect
const handleMouseMove = (e) => {
  const card = e.currentTarget
  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  
  const rotateX = (y - centerY) / 20
  const rotateY = (centerX - x) / 20
  
  card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`
}

const handleMouseLeave = (e) => {
  const card = e.currentTarget
  card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)'
}

const handleMouseEnter = (e) => {
  // Optional: Add any enter animations
}
</script>

<style scoped>
.feature-card {
  transform-style: preserve-3d;
  transition: transform 0.1s ease-out, box-shadow 0.3s ease;
}

.feature-card:hover {
  box-shadow: 0 25px 50px -12px rgba(99, 102, 241, 0.25);
}
</style>

