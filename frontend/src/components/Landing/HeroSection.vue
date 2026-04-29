<template>
  <section id="home" class="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
    
    <!-- Animated Background - Light Theme -->
    <div class="absolute inset-0 -z-10">
      <!-- Base gradient - Light modern -->
      <div class="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-indigo-50"></div>
      
      <!-- Grid pattern -->
      <div class="absolute inset-0 bg-[linear-gradient(rgba(99,102,241,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(99,102,241,0.03)_1px,transparent_1px)] bg-[size:60px_60px]"></div>
      
      <!-- Floating Gradient Orbs - Subtle colors -->
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      
      <!-- Radial gradients for depth -->
      <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-200/30 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-purple-200/30 rounded-full blur-[80px]"></div>
      <div class="absolute top-1/2 left-1/2 w-[300px] h-[300px] bg-pink-100/30 rounded-full blur-[60px]"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
        
        <!-- Left Content -->
        <div class="text-center lg:text-left">
          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-100 border border-indigo-200 mb-6 animate-fade-in-up">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-sm font-medium text-indigo-700">🚀 AI-Powered Learning Platform</span>
          </div>

          <!-- Main Title with Typewriter -->
          <h1 class="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold text-gray-900 leading-tight mb-6">
            <span class="block mb-2">Master Your</span>
            <span class="block">
              <span class="typewriter-text text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600" ref="typewriterRef">{{ displayedText }}</span>
              <span class="inline-block w-1 h-10 lg:h-12 bg-indigo-600 ml-1 animate-blink" :class="{ 'opacity-0': isTyping }"></span>
            </span>
            <span class="block text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
              Journey Today
            </span>
          </h1>

          <!-- Description -->
          <p class="text-lg sm:text-xl text-gray-600 mb-8 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
            Transform your learning experience with AI-powered exams, interactive flashcards, 
            gamified learning, and real-time performance analytics. Join thousands of students 
            achieving their academic goals.
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <button 
              @click="navigateToRegister"
              class="group relative px-8 py-4 text-lg font-bold rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-indigo-500/40"
            >
              <span class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600"></span>
              <span class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-xl"></span>
              <span class="relative flex items-center justify-center gap-3 text-white">
                Start Free Trial
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
            </button>

            <button 
              @click="scrollToFeatures"
              class="group px-8 py-4 text-lg font-bold rounded-2xl border-2 border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-indigo-500 transition-all duration-300"
            >
              <span class="flex items-center justify-center gap-3">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Watch Demo
              </span>
            </button>
          </div>

          <!-- Trust Badges -->
          <div class="mt-10 pt-8 border-t border-gray-200">
            <p class="text-sm text-gray-500 mb-4">Trusted by students from</p>
            <div class="flex flex-wrap items-center justify-center lg:justify-start gap-6">
              <div class="flex items-center gap-2 text-gray-700">
                <svg class="w-5 h-5 text-indigo-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                <span class="font-medium">500+ Schools</span>
              </div>
              <div class="flex items-center gap-2 text-gray-700">
                <svg class="w-5 h-5 text-indigo-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                <span class="font-medium">50K+ Students</span>
              </div>
              <div class="flex items-center gap-2 text-gray-700">
                <svg class="w-5 h-5 text-indigo-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                <span class="font-medium">98% Success</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Content - 3D Illustration -->
        <div class="relative hidden lg:block">
          <div class="relative w-full aspect-square">
            <!-- Main floating card -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-96 bg-white rounded-3xl shadow-2xl border border-gray-100 p-6 transform hover:scale-105 transition-transform duration-500 animate-float">
              <div class="space-y-4">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-gray-900 font-bold">AI Analysis</h3>
                    <p class="text-gray-500 text-sm">Real-time insights</p>
                  </div>
                </div>
                
                <!-- Progress bars -->
                <div class="space-y-3">
                  <div>
                    <div class="flex justify-between text-gray-600 text-sm mb-1">
                      <span>Mathematics</span>
                      <span class="text-indigo-600 font-medium">92%</span>
                    </div>
                    <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div class="h-full w-[92%] bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-gray-600 text-sm mb-1">
                      <span>Physics</span>
                      <span class="text-pink-600 font-medium">85%</span>
                    </div>
                    <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div class="h-full w-[85%] bg-gradient-to-r from-pink-500 to-rose-500 rounded-full"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between text-gray-600 text-sm mb-1">
                      <span>Chemistry</span>
                      <span class="text-emerald-600 font-medium">78%</span>
                    </div>
                    <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div class="h-full w-[78%] bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Floating badges -->
            <div class="absolute top-10 right-10 w-24 h-24 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg animate-float-delayed">
              <span class="text-3xl">🏆</span>
            </div>
            <div class="absolute bottom-20 left-0 w-20 h-20 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg animate-float-slow">
              <span class="text-2xl">📊</span>
            </div>
            <div class="absolute top-20 left-10 w-16 h-16 bg-gradient-to-br from-pink-500 to-rose-500 rounded-xl flex items-center justify-center shadow-lg animate-float">
              <span class="text-xl">🎯</span>
            </div>

            <!-- Glow -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-200/30 rounded-full blur-3xl"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
      <div class="w-6 h-10 rounded-full border-2 border-gray-300 flex items-start justify-center p-2">
        <div class="w-1.5 h-3 bg-gray-400 rounded-full animate-scroll"></div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const typewriterRef = ref(null)
const displayedText = ref('')
const isTyping = ref(true)
const fullText = 'Exam Success'

const navigateToRegister = () => {
  router.push('/register')
}

const scrollToFeatures = () => {
  const element = document.querySelector('#features')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

const typeText = async () => {
  for (let i = 0; i <= fullText.length; i++) {
    displayedText.value = fullText.slice(0, i)
    await new Promise(resolve => setTimeout(resolve, 100))
  }
  isTyping.value = false
  
  setTimeout(() => {
    isTyping.value = true
    displayedText.value = ''
    setTimeout(typeText, 500)
  }, 3000)
}

onMounted(() => {
  setTimeout(typeText, 1000)
})
</script>

<style scoped>
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.6;
  animation: float-orb 20s ease-in-out infinite;
}
.orb-1 { width: 350px; height: 350px; background: radial-gradient(circle, rgba(199,210,254,0.6) 0%, transparent 70%); top: 10%; left: 10%; animation-delay: 0s; }
.orb-2 { width: 280px; height: 280px; background: radial-gradient(circle, rgba(216,180,254,0.5) 0%, transparent 70%); top: 60%; right: 10%; animation-delay: -7s; }
.orb-3 { width: 300px; height: 300px; background: radial-gradient(circle, rgba(249,168,212,0.4) 0%, transparent 70%); bottom: 10%; left: 30%; animation-delay: -14s; }

@keyframes float-orb {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(-30px, -20px) scale(1.02); }
}
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
.animate-float { animation: float 6s ease-in-out infinite; }
.animate-float-delayed { animation: float 6s ease-in-out infinite; animation-delay: -2s; }
.animate-float-slow { animation: float 8s ease-in-out infinite; animation-delay: -4s; }
@keyframes fade-in-up { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in-up { animation: fade-in-up 0.8s ease-out forwards; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
.animate-blink { animation: blink 1s step-end infinite; }
@keyframes scroll { 0%, 100% { transform: translateY(0); opacity: 1; } 50% { transform: translateY(8px); opacity: 0.5; } }
.animate-scroll { animation: scroll 2s ease-in-out infinite; }
</style>


