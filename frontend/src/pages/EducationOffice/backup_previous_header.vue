<template>
  <!-- PREVIOUS HEADER - FULLY FUNCTIONAL BACKUP -->
  <!-- This is a standalone top header component that can be used independently -->
  
  <header class="bg-white shadow-lg border-b border-gray-100 relative z-50">
    <!-- Main Header Container -->
    <div class="flex items-center justify-between px-6 py-3">
      
      <!-- Left Section: Logo & Brand -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-3">
          <div class="relative">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-[#1e3c72] to-[#2a5298] flex items-center justify-center shadow-lg">
              <img 
                src="@/assets/images/eduskill-logo.png" 
                alt="Eduskill Logo" 
                class="w-8 h-8 rounded-lg object-contain"
              />
            </div>
            <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
          </div>
          <div>
            <h2 class="text-gray-800 text-lg font-bold leading-tight">Eduskill</h2>
            <p class="text-gray-500 text-xs">Education Office</p>
          </div>
        </div>
        
        <!-- Divider -->
        <div class="hidden md:block w-px h-10 bg-gray-200"></div>
        
        <!-- Navigation Menu (Desktop) -->
        <nav class="hidden md:flex items-center gap-1">
          <button
            v-for="item in navItems"
            :key="item.label"
            @click="handleNavClick(item)"
            class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="[
              activeNav === item.index 
                ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-800'
            ]"
          >
            <component :is="item.icon" class="w-4 h-4" />
            <span>{{ item.label }}</span>
          </button>
        </nav>
      </div>

      <!-- Right Section: Actions & User -->
      <div class="flex items-center gap-3">
        
        <!-- Search Bar -->
        <div class="hidden lg:block relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="w-64 pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
          />
          <MagnifyingGlassIcon class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center gap-2">
          <!-- Refresh Button -->
          <button
            @click="refreshData"
            class="p-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-600"
            title="Refresh Data"
          >
            <ArrowPathIcon class="w-5 h-5" :class="{ 'animate-spin': isRefreshing }" />
          </button>
          
          <!-- Notifications -->
          <button
            class="relative p-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-600"
            title="Notifications"
          >
            <BellIcon class="w-5 h-5" />
            <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
        </div>

        <!-- Divider -->
        <div class="hidden md:block w-px h-8 bg-gray-200"></div>

        <!-- User Profile Dropdown -->
        <div class="relative" ref="userMenuRef">
          <button
            @click="toggleUserMenu"
            class="flex items-center gap-3 p-2 rounded-xl hover:bg-gray-50 transition-colors"
          >
            <div class="w-9 h-9 rounded-xl bg-gradient-to-r from-[#0fb9b1] to-[#3b82f6] flex items-center justify-center text-white font-bold text-sm shadow">
              EO
            </div>
            <div class="hidden md:block text-left">
              <p class="text-sm font-semibold text-gray-800">Education Officer</p>
              <p class="text-xs text-gray-500">Jimma City</p>
            </div>
            <ChevronDownIcon class="w-4 h-4 text-gray-400 hidden md:block" />
          </button>

          <!-- Dropdown Menu -->
          <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-50"
            >
              <div class="px-4 py-3 border-b border-gray-100">
                <p class="text-sm font-semibold text-gray-800">Education Officer</p>
                <p class="text-xs text-gray-500">edu@jimmacity.gov</p>
              </div>
              
              <div class="py-1">
                <button
                  @click="handleProfileClick"
                  class="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <UserIcon class="w-4 h-4" />
                  <span>Profile Settings</span>
                </button>
                
                <button
                  @click="handleSettingsClick"
                  class="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <Cog6ToothIcon class="w-4 h-4" />
                  <span>Preferences</span>
                </button>
                
                <div class="border-t border-gray-100 my-1"></div>
                
                <button
                  @click="handleLogout"
                  class="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <ArrowRightOnRectangleIcon class="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Mobile Menu Toggle -->
        <button
          @click="toggleMobileMenu"
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-600"
        >
          <Bars3Icon class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Mobile Navigation Menu -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="showMobileMenu"
        class="md:hidden border-t border-gray-100 bg-white"
      >
        <nav class="px-4 py-3 space-y-1">
          <button
            v-for="item in navItems"
            :key="item.label"
            @click="handleNavClick(item); showMobileMenu = false"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors"
            :class="[
              activeNav === item.index 
                ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            <component :is="item.icon" class="w-5 h-5" />
            <span>{{ item.label }}</span>
          </button>
        </nav>
        
        <!-- Mobile Search -->
        <div class="px-4 pb-3">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              class="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50"
            />
            <MagnifyingGlassIcon class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          </div>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ChartBarIcon,
  ChartPieIcon,
  BookOpenIcon,
  UserGroupIcon,
  DocumentTextIcon,
  MegaphoneIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  BellIcon,
  MagnifyingGlassIcon,
  ArrowPathIcon,
  ChevronDownIcon,
  Bars3Icon,
  UserIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

// State
const searchQuery = ref('')
const activeNav = ref(0)
const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const isRefreshing = ref(false)
const userMenuRef = ref(null)

// Navigation Items
const navItems = [
  { icon: ChartBarIcon, label: 'City Overview', view: 'overview', index: 0 },
  { icon: ChartPieIcon, label: 'Grade Performance', view: 'grade-performance', index: 1 },
  { icon: BookOpenIcon, label: 'Subject Leaderboard', view: 'subject-leaderboard', index: 2 },
  { icon: UserGroupIcon, label: 'Student Engagement', view: 'student-performance', index: 3 },
  { icon: DocumentTextIcon, label: 'Reports Center', view: 'reports', index: 4 },
  { icon: MegaphoneIcon, label: 'Announcements', view: 'announcements', index: 5 }
]

// Computed
const currentTime = computed(() => {
  return new Date().toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true 
  })
})

// Methods
const handleNavClick = (item) => {
  activeNav.value = item.index
  // Emit event or handle navigation
  console.log('Navigation clicked:', item.view)
  // You can emit to parent component or handle internally
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const refreshData = () => {
  isRefreshing.value = true
  setTimeout(() => {
    isRefreshing.value = false
  }, 1500)
}

const handleProfileClick = () => {
  showUserMenu.value = false
  console.log('Profile clicked')
}

const handleSettingsClick = () => {
  showUserMenu.value = false
  console.log('Settings clicked')
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/user_login')
}

// Click outside to close user menu
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Header Styles */
header {
  background: linear-gradient(to right, #ffffff, #f8fafc);
}

.bg-gradient-to-br {
  background: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

.from-blue-50 {
  --tw-gradient-from: #eff6ff;
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(239, 246, 255, 0));
}

.to-indigo-50 {
  --tw-gradient-to: #eef2ff;
}

.rounded-xl {
  border-radius: 0.75rem;
}

.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.shadow-xl {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.border-2 {
  border-width: 2px;
}

.border-white {
  --tw-border-opacity: 1;
  border-color: rgba(255, 255, 255, var(--tw-border-opacity));
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Focus styles */
input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

button:focus {
  outline: none;
}

button:focus-visible {
  ring: 2px;
  ring-offset: 2px;
}
</style>

