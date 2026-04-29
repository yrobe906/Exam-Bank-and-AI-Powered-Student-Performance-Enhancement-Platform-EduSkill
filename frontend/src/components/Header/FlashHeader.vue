<template>
  <div>
    <!-- Header with dark theme -->
    <header class="relative bg-gradient-to-r from-gray-900 to-gray-800 border-b border-gray-700/50">
      <!-- Subtle overlay for depth -->
      <div class="absolute inset-0 bg-gradient-to-b from-transparent to-black/5"></div>
      
      <!-- Header content -->
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and main nav container -->
          <div class="flex items-center space-x-8">
            <!-- Logo with gradient -->
            <div class="flex-shrink-0">
              <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent hover:from-blue-300 hover:to-indigo-300 transition-all duration-500">
                EduSkill
              </h1>
            </div>

            <!-- Main Navigation -->
            <nav class="hidden md:flex items-center space-x-6">
              <!-- Start Studying Dropdown -->
              <div class="relative" @mouseenter="openDropdown = 'start'" @mouseleave="openDropdown = null">
                <button class="group flex items-center space-x-1 text-gray-400 hover:text-white font-medium transition-all duration-300 ease-in-out">
                  <span class="relative">
                    Start studying
                    <span class="absolute inset-x-0 -bottom-1 h-0.5 bg-blue-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 ease-out"></span>
                  </span>
                  <svg class="w-4 h-4 transform group-hover:rotate-180 transition-transform duration-300" :class="{ 'rotate-180': openDropdown === 'start' }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                <!-- Start Studying Dropdown Menu with enhanced hover -->
                <transition name="dropdown">
                  <div v-if="openDropdown === 'start'" 
                       class="absolute left-0 mt-2 w-64 bg-gray-800 rounded-xl shadow-2xl border border-gray-700/50 py-2 z-50 overflow-hidden backdrop-blur-sm">
                    <!-- Entrance Exam -->
                    <a href="#" class="group/item flex items-center px-4 py-3 text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/90 hover:to-indigo-600/90 hover:text-white transition-all duration-200">
                      <span class="flex-1">Entrance Exam</span>
                      <svg class="w-4 h-4 opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                    <div class="mx-3 my-1 h-px bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
                    
                    <!-- Model Exam -->
                    <a href="#" class="group/item flex items-center px-4 py-3 text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/90 hover:to-indigo-600/90 hover:text-white transition-all duration-200">
                      <span class="flex-1">Model Exam</span>
                      <svg class="w-4 h-4 opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                    <div class="mx-3 my-1 h-px bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
                    
                    <!-- Worksheet -->
                    <a href="#" class="group/item flex items-center px-4 py-3 text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/90 hover:to-indigo-600/90 hover:text-white transition-all duration-200">
                      <span class="flex-1">Worksheet</span>
                      <svg class="w-4 h-4 opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                    <div class="mx-3 my-1 h-px bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
                    
                    <!-- Practice Questions -->
                    <a href="#" class="group/item flex items-center px-4 py-3 text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/90 hover:to-indigo-600/90 hover:text-white transition-all duration-200">
                      <span class="flex-1">Practice Questions</span>
                      <svg class="w-4 h-4 opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                    <div class="mx-3 my-1 h-px bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
                    
                    <!-- Scenario Question -->
                    <a href="#" class="group/item flex items-center px-4 py-3 text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/90 hover:to-indigo-600/90 hover:text-white transition-all duration-200">
                      <span class="flex-1">Scenario Question</span>
                      <svg class="w-4 h-4 opacity-0 -translate-x-2 group-hover/item:opacity-100 group-hover/item:translate-x-0 transition-all duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                  </div>
                </transition>
              </div>

              <!-- Search with dark theme -->
              <div class="relative group">
                <input type="text" 
                       placeholder="Search for a subject" 
                       class="w-64 pl-10 pr-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm text-gray-200 placeholder-gray-500 transition-all duration-300 group-hover:border-gray-600" />
                <svg class="w-4 h-4 text-gray-500 absolute left-3 top-3 group-hover:text-blue-400 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </nav>
          </div>

          <!-- Right side actions -->
          <div class="flex items-center space-x-4">
            <a href="#" class="text-gray-400 hover:text-white font-medium transition-all duration-300 hover:scale-105 inline-block">Dashboard</a>
            <a href="#" class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 hover:-translate-y-0.5">
              Try 7 days free
            </a>
            
            <!-- Mobile menu button -->
            <button class="md:hidden text-gray-400 hover:text-white transition-colors duration-300">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const openDropdown = ref(null)
</script>

<style scoped>
/* Dropdown animations */
.dropdown-enter-active {
  transition: all 0.2s ease-out;
}

.dropdown-leave-active {
  transition: all 0.15s ease-in;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
}

/* Enhanced dropdown item hover effect */
.dropdown-item {
  position: relative;
  overflow: hidden;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 0;
  background: linear-gradient(to right, rgba(59, 130, 246, 0.2), transparent);
  transition: width 0.2s ease-out;
}

.dropdown-item:hover::before {
  width: 100%;
}

/* Arrow animation */
.group\/item:hover svg {
  animation: slideArrow 0.3s ease-out;
}

@keyframes slideArrow {
  0% {
    opacity: 0;
    transform: translateX(-8px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Rotate icon animation */
.rotate-180 {
  transform: rotate(180deg);
}

/* Smooth transitions for all interactive elements */
a, button, input {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Search icon transition */
.group:hover .search-icon {
  transform: scale(1.1);
}

/* Custom scrollbar for dropdowns */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #374151;
}

::-webkit-scrollbar-thumb {
  background: #4B5563;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #6B7280;
}

/* Pulse animation for CTA button */
@keyframes gentle-pulse {
  0%, 100% {
    box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3);
  }
  50% {
    box-shadow: 0 20px 30px -5px rgba(37, 99, 235, 0.5);
  }
}

.bg-blue-600 {
  animation: gentle-pulse 3s infinite;
}

/* Dropdown width and styling */
.absolute.w-64 {
  min-width: 16rem;
}

/* Gradient dividers */
.bg-gradient-to-r.from-transparent.via-gray-700.to-transparent {
  opacity: 0.5;
}
</style>