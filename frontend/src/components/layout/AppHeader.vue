<template>
  <header class="bg-white shadow-lg border-b border-gray-100 relative z-40 flex-shrink-0 w-full">
    <!-- Main Header Container -->
    <div class="flex items-center justify-between px-4 sm:px-6 lg:pl-72 lg:pr-6 py-3">
      <!-- Left Section: Logo + Title + Mobile Hamburger -->
      <div class="flex items-center gap-3 flex-shrink-0">
        <!-- Logo -->
        <img 
          src="@/assets/images/eduskill-logo.png" 
          alt="EduSkill" 
          class="h-9 w-auto lg:h-10 object-contain"
        />
        <!-- Title - Always visible -->
        <div class="hidden sm:block">
          <h1 class="text-xl lg:text-2xl font-bold bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] bg-clip-text text-transparent">
            EduSkill Teacher Portal
          </h1>
        </div>
        <!-- Mobile Title -->
        <div class="sm:hidden text-lg font-bold text-gray-900">Teacher Portal</div>
      </div>

      <!-- Right Section: Teacher Info + Profile Dropdown -->
      <div class="flex items-center gap-3 flex-shrink-0 relative" ref="userMenuRef">
        <!-- Teacher Info -->
        <div class="hidden lg:flex flex-col items-end text-right">
          <div class="text-sm font-semibold text-gray-900 truncate max-w-40">
            {{ user?.full_name || 'Teacher' }}
          </div>
          <div class="text-xs text-gray-500">
            Grade {{ user?.teaching_grade || 'X' }} - {{ user?.subject_assigned || 'Subject' }}
          </div>
        </div>
        <!-- Mobile Teacher Name -->
        <div class="lg:hidden text-sm font-semibold text-gray-900 truncate max-w-32">
          {{ user?.full_name || 'Teacher' }}
        </div>
        
        <!-- Profile Avatar + Dropdown Toggle -->
        <button 
          @click="toggleUserMenu"
          class="w-10 h-10 rounded-full overflow-hidden border-2 border-gray-200 shadow-md bg-gradient-to-r from-[#1e3c72]/10 to-[#0fb9b1]/10 flex-shrink-0 p-0 hover:border-[#1e3c72]/50 transition-all"
          :aria-expanded="showUserMenu"
        >
          <img 
            v-if="userImage && !userImageError"
            :src="userImage" 
            alt="Profile" 
            class="w-full h-full object-cover rounded-full"
            @error="userImageError = true"
          />
          <div v-else class="w-full h-full bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] flex items-center justify-center">
            <span class="text-white font-bold text-xs">
              {{ user?.full_name?.charAt(0)?.toUpperCase() || 'T' }}
            </span>
          </div>
        </button>

        <!-- User Dropdown Menu -->
        <transition 
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
        >
          <div 
            v-if="showUserMenu" 
            class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-gray-100 ring-1 ring-black/5 z-50 origin-top-right"
          >
            <!-- User Info -->
            <div class="px-4 py-3 border-b border-gray-100">
              <p class="text-sm font-semibold text-gray-800">{{ user?.full_name || 'Teacher' }}</p>
              <p class="text-xs text-gray-500">Grade {{ user?.teaching_grade || 'X' }} - {{ user?.subject_assigned || 'Subject' }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ user?.email || 'teacher@school.edu' }}</p>
            </div>
            
            <!-- Menu Items -->
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
                @click="$emit('logout')"
                class="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                <ArrowRightOnRectangleIcon class="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  Bars3Icon, 
  ChevronDownIcon as ChevronDownIconOutline,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  user: { 
    type: Object, 
    default: () => ({ 
      full_name: 'Teacher',
      teaching_grade: 'X',
      subject_assigned: 'Subject',
      email: 'teacher@school.edu'
    }) 
  }
})

// Emits
const emit = defineEmits([
  'logout',
  'toggle-mobile-menu'
])

// State
const showUserMenu = ref(false)
const userMenuRef = ref(null)
const userImageError = ref(false)
const userImage = computed(() => {
  if (props.user.profile_photo) {
    return `http://127.0.0.1:8000/${props.user.profile_photo}`
  }
  return `https://api.dicebear.com/7.x/avataars/svg?seed=${props.user.full_name || 'teacher'}`
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const handleProfileClick = () => {
  showUserMenu.value = false
  console.log('Profile clicked')
  // Add your profile navigation logic here
}

const handleSettingsClick = () => {
  showUserMenu.value = false
  console.log('Settings clicked')
  // Add your settings navigation logic here
}

// Click outside to close user menu
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Expose to parent if needed
defineExpose({
  toggleUserMenu
})
</script>

<style scoped>
/* Make header edge-to-edge */
header {
  width: 100%;
  margin: 0;
  padding: 0;
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
}

/* Ensure header content is properly padded for sidebar alignment */
header > div {
  max-width: 100%;
  margin: 0 auto;
}

/* On desktop, align header content with main content area */
@media (min-width: 1024px) {
  header > div {
    padding-left: 16rem; /* Exactly the sidebar width (64px * 4 = 256px = 16rem) */
    padding-right: 2rem;
  }
}

/* Hide scrollbar for navigation on mobile */
.hide-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;  /* Chrome, Safari, Opera */
}

/* Navigation styling */
nav {
  display: flex;
  align-items: center;
}

/* Ensure proper spacing on mobile */
@media (max-width: 768px) {
  .flex-1 {
    min-width: 0; /* Allows flex item to shrink below content size */
  }
  
  nav {
    flex: 1;
  }
}

/* Remove left padding on desktop - logo sits at the very left edge of the content area */
@media (min-width: 1024px) {
  .lg\:px-0 {
    padding-left: 0;
    padding-right: 0;
  }
  
  /* Adjust the padding on the header container to account for sidebar */
  header > div {
    padding-left: 16rem; /* This creates space for the sidebar, but content starts at the edge of that space */
  }
  
  /* Ensure logo is at the very left edge of the content area (right after sidebar) */
  .pl-0 {
    padding-left: 0;
  }
  
  /* Minimal spacing between logo and nav */
  .lg\:ml-1 {
    margin-left: 0.25rem;
  }
}

/* Logo image styling */
img[alt="E-Tutor Logo"] {
  max-height: 48px;
  width: auto;
}

@media (min-width: 768px) {
  img[alt="E-Tutor Logo"] {
    max-height: 56px;
  }
}
</style>