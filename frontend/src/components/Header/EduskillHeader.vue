<template>
  <header class="glass-nav fixed top-0 left-0 w-full z-50">
    <!-- Animated gradient border top -->
    <div class="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 animate-gradient"></div>
    
    <!-- Left-aligned container -->
    <div class="max-w-7xl px-2 sm:px-3 lg:px-4">
      <div class="flex items-center justify-start h-16 md:h-18">
        
        <!-- Logo Section - Left Edge (Non-clickable) -->
        <div class="flex items-center gap-1.5 sm:gap-2 group logo-wrapper relative">
          <!-- Animated background glow -->
          <div class="absolute -inset-2 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-xl blur-lg opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <!-- Logo Container -->
          <div class="logo-container relative rounded-xl p-1.5 bg-gradient-to-br from-white via-indigo-50 to-purple-50 shadow-md border border-white/80 group-hover:shadow-xl transition-all duration-500 group-hover:scale-105">
            <!-- Inner glow ring -->
            <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-xl opacity-0 group-hover:opacity-30 blur transition-opacity duration-500"></div>
            
            <img 
              src="/eduSkill-logo.png" 
              alt="EduSkill Logo" 
              class="logo-image relative h-7 w-auto sm:h-8 md:h-9 object-contain"
              @error="handleLogoError"
              v-show="!logoFailed"
            />
            
            <!-- Fallback Logo -->
            <div 
              v-if="logoFailed" 
              class="logo-fallback relative h-7 w-7 sm:h-8 sm:w-8 md:h-9 md:w-9 flex items-center justify-center"
            >
              <div class="relative">
                <div class="absolute inset-0 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg blur-md animate-pulse"></div>
                <div class="relative bg-gradient-to-br from-indigo-600 to-purple-700 rounded-lg shadow-md flex items-center justify-center p-2">
                  <span class="text-white font-bold text-lg sm:text-xl">E</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Brand Text with Animation -->
          <div class="brand-text relative overflow-hidden">
            <span class="hidden sm:inline-block text-lg md:text-xl font-extrabold tracking-tight">
              <span class="bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                EduSkill
              </span>
              <span class="relative">
                <span class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent animate-gradient-text">
                  Hub
                </span>
                <!-- Decorative dot -->
                <span class="absolute -top-0.5 -right-1.5 w-1.5 h-1.5 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full animate-pulse"></span>
              </span>
            </span>
          </div>
          
          <!-- Shine effect on hover -->
          <div class="absolute inset-0 -z-10 bg-gradient-to-r from-transparent via-white/20 to-transparent -skew-x-12 translate-x-[-100%] group-hover:translate-x-[200%] transition-transform duration-1000"></div>
        </div>
        
        <!-- Mobile Menu Toggle - Right side on mobile -->
        <button 
          @click="toggleMobileMenu" 
          class="md:hidden relative group p-2 rounded-lg text-gray-700 hover:text-indigo-600 focus:outline-none transition-all duration-300"
          aria-label="Toggle menu"
        >
          <!-- Hover background effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          
          <svg 
            class="relative w-5 h-5 transition-all duration-300" 
            :class="{ 'rotate-90 text-indigo-600': mobileOpen }" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              v-if="!mobileOpen" 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2.5" 
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path 
              v-else 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2.5" 
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        
      </div>
    </div>
    
    <!-- Mobile Menu with beautiful styling -->
    <transition name="mobile-menu">
      <div 
        v-show="mobileOpen" 
        class="md:hidden bg-gradient-to-b from-white/95 via-indigo-50/95 to-purple-50/95 backdrop-blur-2xl border-t border-indigo-100 shadow-2xl"
      >
        <div class="px-4 pt-4 pb-6 space-y-2 flex flex-col">
          <!-- Decorative header in mobile menu -->
          <div class="flex items-center justify-center gap-2 mb-3">
            <div class="w-8 h-0.5 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-full"></div>
            <span class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Menu</span>
            <div class="w-8 h-0.5 bg-gradient-to-r from-purple-400 to-indigo-400 rounded-full"></div>
          </div>
          <p class="text-center text-gray-500 text-xs py-3">✨ Menu items coming soon ✨</p>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Reactive state
const mobileOpen = ref(false)
const logoFailed = ref(false)

// Methods
const toggleMobileMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

const handleLogoError = (event) => {
  console.warn('Logo not found at: ../../Symbols and Icons/EduSkill logo.png')
  logoFailed.value = true
}

// Responsive handling - close mobile menu on desktop
const handleResize = () => {
  if (window.innerWidth >= 768) {
    mobileOpen.value = false
  }
}

// Lifecycle
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* Import Google Font for better typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=swap');

* {
  font-family: 'Inter', system-ui, sans-serif;
}

/* Glass navigation with enhanced blur - FIXED at top */
.glass-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  background: rgba(255, 255, 255, 0.75);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

/* Animated gradient border */
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
}

/* Animated gradient text */
@keyframes gradientText {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient-text {
  background-size: 200% 200%;
  animation: gradientText 4s ease infinite;
}

/* Logo container enhancements */
.logo-container {
  position: relative;
  overflow: hidden;
  cursor: default; /* Non-clickable indicator */
}

.logo-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.5s;
  pointer-events: none;
}

.logo-container:hover::before {
  opacity: 0.6;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Logo image styling */
.logo-image {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.07));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none; /* Prevent clicking on image */
}

.group:hover .logo-image {
  filter: drop-shadow(0 6px 8px rgba(79, 70, 229, 0.2));
}

/* Fallback logo animation */
.logo-fallback {
  animation: float 3s ease-in-out infinite;
  pointer-events: none; /* Prevent clicking on fallback */
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-2px);
  }
}

/* Brand text hover effect */
.brand-text {
  position: relative;
  cursor: default; /* Non-clickable indicator */
  pointer-events: none; /* Prevent clicking on text */
}

.brand-text::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 0%;
  height: 1.5px;
  background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
  border-radius: 2px;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.group:hover .brand-text::after {
  width: 100%;
}

/* Logo wrapper enhancements */
.logo-wrapper {
  position: relative;
  padding: 0.375rem;
  margin-left: -0.375rem;
  border-radius: 0.75rem;
  cursor: default; /* Non-clickable */
  user-select: none; /* Prevent text selection */
}

/* Mobile menu transitions */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-menu-enter-from {
  opacity: 0;
  transform: translateY(-15px) scale(0.95);
}

.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Glass effect enhancement */
@supports (backdrop-filter: blur(20px)) {
  .glass-nav {
    background: rgba(255, 255, 255, 0.65);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .logo-image {
    height: 1.75rem;
  }
  
  .logo-wrapper {
    margin-left: -0.25rem;
    padding: 0.25rem;
  }
}

/* Add subtle shadow */
.glass-nav {
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Interactive glow effect - removed click effect */
.logo-wrapper:active .logo-container {
  transform: scale(1); /* No scale on click */
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Ensure logo area shows default cursor */
.logo-wrapper,
.logo-container,
.brand-text,
.logo-image {
  cursor: default !important;
}
</style>