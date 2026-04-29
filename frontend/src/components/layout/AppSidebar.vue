<template>
  <!-- Desktop Sidebar -->
  <aside class="hidden lg:flex lg:flex-shrink-0">
    <div class="w-64 bg-white border-r border-gray-200 flex flex-col relative shadow-lg">
      <!-- Beautiful Vertical Line Scroll Indicator for Sidebar (NO BUTTONS) -->
      <div class="absolute top-1/2 -translate-y-1/2 -right-3 z-50 flex-col items-center hidden lg:flex">
        <!-- Vertical Line with Moving Indicator -->
        <div class="relative h-32 w-0.5">
          <!-- Background gradient line -->
          <div class="absolute inset-0 w-full h-full bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200 rounded-full"></div>
          <!-- Moving indicator with glow effect -->
          <div 
            class="absolute left-1/2 -translate-x-1/2 w-1.5 h-8 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full transition-all duration-300 shadow-lg"
            :style="{ top: sidebarScrollProgress + '%', filter: 'drop-shadow(0 0 3px rgba(15,185,177,0.5))' }"
          >
            <!-- Inner glow effect -->
            <div class="absolute inset-0 bg-white opacity-30 rounded-full blur-[1px]"></div>
          </div>
          <!-- Decorative dots at ends -->
          <div class="absolute -top-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] rounded-full"></div>
          <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] rounded-full"></div>
        </div>
      </div>

      <!-- Entire Sidebar Content - Now Scrollable as One Unit -->
      <div 
        ref="sidebarContentRef"
        class="flex-1 overflow-y-auto scroll-smooth"
        @scroll="checkScrollPosition"
      >
        <!-- Navigation - Now starts directly at the top -->
        <nav class="px-3 py-4 space-y-1">
          <div
            v-for="(item, index) in navItems"
            :key="item.label"
            @click="$emit('nav-click', item, index)"
            class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group relative cursor-pointer"
            :class="[
              activeNav === item.index 
                ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-200/50 hover:text-gray-800'
            ]"
          >
            <component 
              :is="item.icon" 
              class="w-5 h-5 transition-transform duration-200 group-hover:scale-110"
              :class="activeNav === item.index ? 'text-blue-600' : 'text-gray-400'"
            />
            <span>{{ item.label }}</span>
            <div 
              v-if="activeNav === item.index" 
              class="absolute left-0 w-1 h-8 bg-blue-600 rounded-r-full"
            ></div>
          </div>
        </nav>
      </div>
    </div>
  </aside>

  <!-- Mobile Overlay -->
  <div 
    v-if="isOpen" 
    @click="$emit('update:is-open', false)"
    class="fixed inset-0 bg-black/50 z-30 lg:hidden"
  ></div>

  <!-- Mobile Sidebar - Positioned below header but overlaying content -->
  <aside 
    :class="[
      'fixed lg:hidden top-[64px] left-0 z-40 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out flex flex-col h-[calc(100vh-64px)]',
      isOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <!-- Mobile Scroll Indicator -->
    <div class="absolute top-1/2 -translate-y-1/2 -right-3 z-50 flex-col items-center hidden sm:flex">
      <div class="relative h-32 w-0.5">
        <!-- Background gradient line -->
        <div class="absolute inset-0 w-full h-full bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200 rounded-full"></div>
        <!-- Moving indicator with glow effect -->
        <div 
          class="absolute left-1/2 -translate-x-1/2 w-1.5 h-8 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full transition-all duration-300 shadow-lg"
          :style="{ top: sidebarScrollProgress + '%', filter: 'drop-shadow(0 0 3px rgba(15,185,177,0.5))' }"
        >
          <!-- Inner glow effect -->
          <div class="absolute inset-0 bg-white opacity-30 rounded-full blur-[1px]"></div>
        </div>
        <!-- Decorative dots at ends -->
        <div class="absolute -top-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] rounded-full"></div>
        <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] rounded-full"></div>
      </div>
    </div>

    <!-- Mobile Sidebar Content -->
    <div 
      ref="mobileSidebarContentRef"
      class="flex-1 overflow-y-auto scroll-smooth"
      @scroll="checkScrollPosition"
    >
      <!-- Mobile Navigation -->
      <nav class="px-3 py-4 space-y-1">
        <div
          v-for="(item, index) in navItems"
          :key="item.label"
          @click="$emit('nav-click', item, index); $emit('update:is-open', false)"
          class="flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-medium transition-all duration-200 group relative cursor-pointer"
          :class="[
            activeNav === item.index 
              ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700' 
              : 'text-gray-600 hover:bg-gray-100 hover:text-gray-800'
          ]"
        >
          <component 
            :is="item.icon" 
            class="w-5 h-5 transition-transform duration-200 group-hover:scale-110"
            :class="activeNav === item.index ? 'text-blue-600' : 'text-gray-400'"
          />
          <span class="text-base">{{ item.label }}</span>
          <div 
            v-if="activeNav === item.index" 
            class="absolute left-0 w-1 h-8 bg-blue-600 rounded-r-full"
          ></div>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

// Props
const props = defineProps({
  isOpen: { type: Boolean, default: false },
  activeNav: { type: Number, default: 0 },
  navItems: { type: Array, required: true },
  canScrollUp: { type: Boolean, default: false },
  canScrollDown: { type: Boolean, default: true }
})

// Emits
const emit = defineEmits([
  'update:is-open',
  'nav-click',
  'scroll-up',
  'scroll-down',
  'logout'
])

// Refs
const sidebarContentRef = ref(null)
const mobileSidebarContentRef = ref(null)
const sidebarScrollProgress = ref(0)

// Check scroll position
const checkScrollPosition = () => {
  // Check desktop sidebar
  if (sidebarContentRef.value) {
    const { scrollTop, scrollHeight, clientHeight } = sidebarContentRef.value
    // Calculate progress percentage (0-100)
    const maxScroll = scrollHeight - clientHeight
    sidebarScrollProgress.value = maxScroll > 0 
      ? Math.min(100, Math.max(0, (scrollTop / maxScroll) * 100))
      : 0
  }
  
  // Check mobile sidebar
  if (mobileSidebarContentRef.value) {
    const { scrollTop, scrollHeight, clientHeight } = mobileSidebarContentRef.value
    const maxScroll = scrollHeight - clientHeight
    sidebarScrollProgress.value = maxScroll > 0 
      ? Math.min(100, Math.max(0, (scrollTop / maxScroll) * 100))
      : 0
  }
}

// Reset scroll progress when mobile sidebar closes
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    sidebarScrollProgress.value = 0
  }
})

// Add scroll listeners
onMounted(() => {
  if (sidebarContentRef.value) {
    sidebarContentRef.value.addEventListener('scroll', checkScrollPosition)
    // Initial check
    checkScrollPosition()
  }
  if (mobileSidebarContentRef.value) {
    mobileSidebarContentRef.value.addEventListener('scroll', checkScrollPosition)
    // Initial check
    checkScrollPosition()
  }
})

onUnmounted(() => {
  if (sidebarContentRef.value) {
    sidebarContentRef.value.removeEventListener('scroll', checkScrollPosition)
  }
  if (mobileSidebarContentRef.value) {
    mobileSidebarContentRef.value.removeEventListener('scroll', checkScrollPosition)
  }
})

// Expose
defineExpose({
  sidebarContentRef,
  mobileSidebarContentRef,
  sidebarScrollProgress,
  checkScrollPosition
})
</script>

<style scoped>
/* Smooth scrolling for the entire sidebar */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 8px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 8px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Hide scrollbar when not hovering (optional) */
.overflow-y-auto:not(:hover)::-webkit-scrollbar {
  width: 2px;
}

.overflow-y-auto:not(:hover)::-webkit-scrollbar-thumb {
  background: #e2e8f0;
}

/* Animation for the scroll indicator */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.shadow-lg {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Mobile styles */
@media (max-width: 1023px) {
  .overflow-y-auto {
    -webkit-overflow-scrolling: touch;
  }
  
  /* Slightly larger tap targets for mobile */
  nav .px-4.py-3 {
    min-height: 48px;
  }
}

/* Ensure main content doesn't get pushed */
:deep(.main-content) {
  transition: margin-left 0.3s ease-in-out;
}

@media (max-width: 1023px) {
  :deep(.main-content) {
    margin-left: 0 !important;
    width: 100%;
  }
}
</style>