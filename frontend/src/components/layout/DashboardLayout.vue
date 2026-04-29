<template>
<div class="h-screen flex flex-col bg-[#f8fafc]">
    <!-- Initial Loading Screen -->
    <div
      v-if="isInitialLoading" 
      class="fixed inset-0 bg-gradient-to-br from-[#1e3c72] to-[#2a5298] z-50 flex items-center justify-center"
    >
      <!-- Mobile Backdrop Overlay for Sidebar -->
      <div 
        v-if="sidebarOpen && window.innerWidth < 1024"
        class="fixed inset-0 bg-black/50 z-40"
        @click="closeSidebar"
      ></div>
      <div class="text-center">
        <div class="relative mb-8">
          <div class="animate-spin rounded-full h-20 w-20 border-4 border-white/30 mx-auto"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <img src="@/assets/images/eduskill-logo.png" alt="Logo" class="w-12 h-12 rounded-xl object-contain" />
          </div>
        </div>
        <h2 class="text-2xl font-bold text-white mb-2">EduSkill Hub</h2>
        <p class="text-white/70">Loading City Overview...</p>
        <div class="mt-6 w-48 mx-auto bg-white/20 rounded-full h-1 overflow-hidden">
          <div class="h-full bg-white rounded-full animate-pulse" style="width: 60%"></div>
        </div>
      </div>
    </div>

    <!-- Background Pattern -->
    <div class="fixed inset-0 opacity-[0.03] pointer-events-none bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%231e3c72%22%20fill-opacity%3D%221%22%3E%3Cpath%20d%3D%22M36%2034v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6%2034v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6%204V0H4v4H0v2h4v4h2V6h4V4H6z%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E')]">
    </div>

    <!-- Header Slot - Fixed at top, edge to edge on all screens -->
    <div class="flex-shrink-0 w-full z-40 relative">
      <slot 
        name="header"
        :activeNav="activeNav"
        :toggleMobileMenu="toggleMobileMenu"
        :handleNavClick="handleNavClick"
      />
    </div>

    <!-- Main Content Area with Sidebar and Main -->
    <div class="flex flex-1 overflow-hidden relative">
      <!-- Sidebar Slot - Fixed left on desktop, overlay on mobile -->
      <div 
        :class="[
          'lg:w-64 lg:flex-shrink-0 transition-all duration-300 ease-in-out lg:translate-x-0 fixed lg:relative z-30 h-full',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
      >
        <slot 
          name="sidebar"
          :sidebarOpen="sidebarOpen"
          :activeNav="activeNav"
          :handleNavClick="handleNavClick"
          :closeSidebar="closeSidebar"
          :canScrollSidebarUp="canScrollSidebarUp"
          :canScrollSidebarDown="canScrollSidebarDown"
          :scrollSidebarUp="scrollSidebarUp"
          :scrollSidebarDown="scrollSidebarDown"
        />
      </div>

      <!-- Mobile Overlay -->
      <div 
        v-if="sidebarOpen" 
        class="fixed inset-0 bg-black/50 z-20 lg:hidden"
        @click="closeSidebar"
      ></div>

      <!-- Scrollable Main Content - FIXED: Proper spacing for all screen sizes -->
      <main 
        ref="mainContentRef"
        @scroll="checkScrollPosition"
        class="flex-1 overflow-y-auto overflow-x-hidden relative bg-[#f8fafc] w-full"
        :class="{
          'lg:ml-0': true
        }"
      >
        <!-- Beautiful Vertical Line Scroll Indicator (NO BUTTONS) - Hidden on mobile -->
        <div class="hidden md:fixed md:right-8 md:top-1/2 md:-translate-y-1/2 md:z-50 md:flex md:flex-col md:items-center">
          <!-- Vertical Line with Moving Indicator -->
          <div class="relative h-32 w-1">
            <!-- Base Line -->
            <div class="absolute inset-0 w-full h-full bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200 rounded-full"></div>
            <!-- Moving Indicator -->
            <div 
              class="absolute left-1/2 -translate-x-1/2 w-1.5 h-8 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full transition-all duration-300 shadow-lg shadow-[#0fb9b1]/30"
              :style="{ top: scrollProgress + '%' }"
            ></div>
          </div>
          
          <!-- Progress Percentage -->
          <div class="mt-3 text-xs font-medium text-gray-600 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full shadow-md border border-gray-100">
            {{ scrollProgress }}%
          </div>
        </div>

        <!-- Mobile Scroll Progress Indicator (Simplified) -->
        <div class="md:hidden fixed bottom-4 right-4 z-50 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-full shadow-md border border-gray-200 text-xs font-medium text-gray-600">
          {{ scrollProgress }}%
        </div>

        <!-- Main Content Slot - No padding here, let child components handle it -->
        <slot name="main" :currentView="currentView" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Props
const props = defineProps({
  initialActiveNav: { type: Number, default: 0 },
  initialView: { type: String, default: 'overview' }
})

// Emits
const emit = defineEmits([
  'update:activeNav',
  'update:currentView',
  'nav-click',
  'view-change',
  'scroll-sidebar-up',
  'scroll-sidebar-down'
])

// Layout state
const sidebarOpen = ref(false)
const activeNav = ref(props.initialActiveNav)
const currentView = ref(props.initialView)
const isInitialLoading = ref(true)

// Scroll refs and state
const mainContentRef = ref(null)
const canScrollContentUp = ref(false)
const canScrollContentDown = ref(true)
const scrollProgress = ref(0)

// Sidebar scroll state
const canScrollSidebarUp = ref(false)
const canScrollSidebarDown = ref(true)

// Initialize
onMounted(() => {
  setTimeout(() => {
    isInitialLoading.value = false
  }, 1000)
  
  if (mainContentRef.value) {
    mainContentRef.value.addEventListener('scroll', checkScrollPosition)
  }
})

onUnmounted(() => {
  if (mainContentRef.value) {
    mainContentRef.value.removeEventListener('scroll', checkScrollPosition)
  }
})

// Methods
const checkScrollPosition = () => {
  if (mainContentRef.value) {
    const { scrollTop, scrollHeight, clientHeight } = mainContentRef.value
    canScrollContentUp.value = scrollTop > 0
    canScrollContentDown.value = scrollTop + clientHeight < scrollHeight
    scrollProgress.value = Math.round((scrollTop / (scrollHeight - clientHeight)) * 100) || 0
  }
}

const scrollContentUp = () => {
  if (mainContentRef.value && canScrollContentUp.value) {
    mainContentRef.value.scrollBy({ top: -300, behavior: 'smooth' })
  }
}

const scrollContentDown = () => {
  if (mainContentRef.value && canScrollContentDown.value) {
    mainContentRef.value.scrollBy({ top: 300, behavior: 'smooth' })
  }
}

const scrollSidebarUp = () => {
  emit('scroll-sidebar-up')
}

const scrollSidebarDown = () => {
  emit('scroll-sidebar-down')
}

const toggleMobileMenu = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const handleNavClick = (item, index) => {
  activeNav.value = item.index || index
  currentView.value = item.view || 'overview'
  closeSidebar()
  emit('nav-click', item, index)
  emit('view-change', currentView.value)
  emit('update:activeNav', activeNav.value)
  emit('update:currentView', currentView.value)
}

defineExpose({
  sidebarOpen,
  activeNav,
  currentView,
  canScrollSidebarUp,
  canScrollSidebarDown,
  canScrollContentUp,
  canScrollContentDown,
  scrollProgress,
  toggleMobileMenu,
  closeSidebar,
  handleNavClick,
  scrollSidebarUp,
  scrollSidebarDown,
  scrollContentUp,
  scrollContentDown,
  mainContentRef
})
</script>

<style scoped>
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.6s ease-out forwards; opacity: 0; }
.animate-spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>