<template>
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 scale-0"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-0"
  >
    <button
      v-if="show"
      @click="toggleChat"
      class="fixed bottom-8 left-8 z-50 group"
      aria-label="Open chat"
    >
      <!-- Glow effect -->
      <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full blur-lg opacity-50 group-hover:opacity-75 transition-opacity duration-300 animate-pulse"></div>
      
      <!-- Button -->
      <div class="relative w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full flex items-center justify-center shadow-lg hover:shadow-2xl hover:shadow-indigo-500/40 transition-all duration-300 hover:scale-110">
        <!-- Chat icon -->
        <svg 
          v-if="!isOpen"
          class="w-7 h-7 text-white" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
        
        <!-- Close icon -->
        <svg 
          v-else
          class="w-7 h-7 text-white" 
          fill="none" 
          stroke="currentColor" 
