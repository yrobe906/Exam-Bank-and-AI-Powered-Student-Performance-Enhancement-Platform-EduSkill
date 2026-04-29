<!-- TeacherSidebar.vue -->
<template>
  <aside 
    class="w-64 flex flex-col relative shadow-lg h-full bg-white transition-transform duration-300 ease-in-out"
    :class="[
      isOpen ? 'translate-x-0' : '-translate-x-full',
      'lg:translate-x-0'
    ]"
    :style="sidebarStyle"
  >
    <!-- Navigation -->
    <nav 
      ref="navRef" 
      class="flex-1 px-3 py-4 space-y-1 overflow-y-auto scroll-smooth" 
      @scroll="checkScrollPosition"
    >
      <template v-for="item in menuItems" :key="item.label">
        <!-- Main Menu Item with redirect and loading -->
        <a
          v-if="!item.subItems && item.action === 'redirectWithLoading'"
          href="#"
          @click.prevent="handleRedirectWithLoading(item.to)"
          class="sidebar-nav-item group relative flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300"
          :class="[
            isActive(item.to) 
              ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700' 
              : 'text-gray-600 hover:bg-gradient-to-r hover:from-gray-50 hover:to-blue-50 hover:text-gray-800'
          ]"
        >
          <component 
            v-if="!isRedirecting"
            :is="item.icon" 
            class="w-5 h-5 transition-all duration-300 group-hover:scale-110 group-hover:rotate-3"
            :class="isActive(item.to) ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-500'"
          />
          <svg v-else class="w-5 h-5 animate-spin text-blue-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="relative">
            {{ isRedirecting ? loadingMessage : item.label }}
            <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-blue-500 rounded-full transition-all duration-300 group-hover:w-full"></span>
          </span>
          <div 
            v-if="isActive(item.to) && !isRedirecting" 
            class="absolute left-0 w-1 h-8 bg-blue-600 rounded-r-full"
          ></div>
        </a>
        
        <!-- Regular Main Menu Item -->
        <router-link
          v-else-if="!item.subItems"
          :to="item.to"
          class="sidebar-nav-item group relative flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300"
          :class="[
            isActive(item.to) 
              ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700' 
              : 'text-gray-600 hover:bg-gradient-to-r hover:from-gray-50 hover:to-blue-50 hover:text-gray-800'
          ]"
        >
          <component 
            :is="item.icon" 
            class="w-5 h-5 transition-all duration-300 group-hover:scale-110 group-hover:rotate-3"
            :class="isActive(item.to) ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-500'"
          />
          <span class="relative">
            {{ item.label }}
            <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-blue-500 rounded-full transition-all duration-300 group-hover:w-full"></span>
          </span>
          <div 
            v-if="isActive(item.to)" 
            class="absolute left-0 w-1 h-8 bg-blue-600 rounded-r-full"
          ></div>
        </router-link>

        <!-- Dropdown Menu Item -->
        <div v-else class="relative">
          <button
            @click="toggleDropdown(item.label)"
            class="sidebar-nav-item w-full flex items-center justify-between gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 group"
            :class="[
              activeDropdown === item.label
                ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700'
                : 'text-gray-600 hover:bg-gradient-to-r hover:from-gray-50 hover:to-blue-50 hover:text-gray-800'
            ]"
          >
            <div class="flex items-center gap-3">
              <component 
                :is="item.icon" 
                class="w-5 h-5 transition-all duration-300 group-hover:scale-110"
                :class="activeDropdown === item.label ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-500'"
              />
              <span class="relative">
                {{ item.label }}
                <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-blue-500 rounded-full transition-all duration-300 group-hover:w-full"></span>
              </span>
            </div>
            <ChevronDownIcon 
              class="w-4 h-4 transition-all duration-300"
              :class="activeDropdown === item.label ? 'rotate-180 text-blue-600' : 'text-gray-400 group-hover:text-blue-500'"
            />
          </button>
          
          <!-- Sub Items -->
          <transition
            enter-active-class="transition-all duration-200 ease-out"
            enter-from-class="transform -translate-y-2 opacity-0"
            enter-to-class="transform translate-y-0 opacity-100"
            leave-active-class="transition-all duration-150 ease-in"
            leave-from-class="transform translate-y-0 opacity-100"
            leave-to-class="transform -translate-y-2 opacity-0"
          >
            <div v-if="activeDropdown === item.label" class="mt-1 ml-4 pl-3 border-l-2 border-gray-100 space-y-1">
              <a
                v-for="subItem in item.subItems"
                :key="subItem.label"
                href="#"
                @click.prevent="handleSubItemClick(subItem)"
                class="sidebar-sub-item block px-4 py-2.5 rounded-lg text-sm text-gray-500 hover:text-gray-700 hover:bg-gradient-to-r hover:from-gray-50 hover:to-blue-50 transition-all duration-200 group/sub"
                :class="isActive(subItem.to || '') ? 'text-blue-600 font-medium bg-gradient-to-r from-blue-50 to-indigo-50' : ''"
              >
                <span class="relative">
                  {{ subItem.label }}
                  <span class="absolute -bottom-0.5 left-0 w-0 h-0.5 bg-blue-500 rounded-full transition-all duration-300 group-hover/sub:w-full"></span>
                </span>
              </a>
            </div>
          </transition>
        </div>
      </template>
    </nav>

    <!-- User Info Section -->
    <div class="p-4 border-t border-gray-100">
      <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4">
        <div class="flex items-center gap-3 mb-3">
          <img
            :src="getProfilePhotoUrl(teacherProfile.profile_photo, teacherProfile.username)"
            alt="Profile"
            class="w-10 h-10 rounded-xl object-cover border-2 border-white shadow"
            @error="handleImageError"
          />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-gray-800 truncate">
              {{ teacherProfile.full_name || 'Teacher' }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ teacherProfile.subject_assigned || 'Subject' }}
            </p>
          </div>
        </div>
        <button
          @click="handleLogout"
          class="w-full flex items-center justify-center gap-2 px-3 py-2 bg-white rounded-lg text-sm font-medium text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200"
        >
          <ArrowRightOnRectangleIcon class="w-4 h-4" />
          Logout
        </button>
      </div>
    </div>

    <!-- Line Scroll Controller -->
    <div class="absolute right-2 top-1/2 -translate-y-1/2 z-50 flex flex-col items-center gap-2">
      <button 
        @click="scrollUp"
        :disabled="!canScrollUp"
        class="w-7 h-7 flex items-center justify-center rounded-full bg-white shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-blue-50 group"
        title="Scroll Up"
      >
        <ChevronUpIcon class="w-4 h-4 text-gray-600 group-hover:text-blue-600 transition-colors" />
      </button>
      
      <div 
        class="relative h-32 w-1 cursor-pointer group" 
        @click="handleLineClick"
        title="Click to scroll"
      >
        <div class="absolute inset-0 w-full h-full bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200 rounded-full group-hover:from-gray-300 group-hover:via-gray-400 group-hover:to-gray-300 transition-colors"></div>
        <div 
          class="absolute left-1/2 -translate-x-1/2 w-1.5 h-8 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full transition-all duration-300 shadow-lg shadow-[#0fb9b1]/30"
          :style="{ top: scrollProgress + '%' }"
        ></div>
      </div>
      
      <button 
        @click="scrollDown"
        :disabled="!canScrollDown"
        class="w-7 h-7 flex items-center justify-center rounded-full bg-white shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-blue-50 group"
        title="Scroll Down"
      >
        <ChevronDownIcon class="w-4 h-4 text-gray-600 group-hover:text-blue-600 transition-colors" />
      </button>
      
      <div class="text-[10px] font-medium text-gray-500 bg-white/90 backdrop-blur-sm px-1.5 py-0.5 rounded-full shadow border border-gray-100">
        {{ scrollProgress }}%
      </div>
    </div>
  </aside>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  HomeIcon,
  DocumentTextIcon,
  BookOpenIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  ClipboardDocumentCheckIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  ArrowRightOnRectangleIcon,
  AcademicCapIcon,
  RectangleStackIcon,
  FolderIcon,
  ChartBarSquareIcon,
  MegaphoneIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'TeacherSidebar',
  components: {
    HomeIcon,
    DocumentTextIcon,
    BookOpenIcon,
    UserGroupIcon,
    ChatBubbleLeftRightIcon,
    ChartBarIcon,
    ClipboardDocumentCheckIcon,
    ChevronDownIcon,
    ChevronUpIcon,
    ArrowRightOnRectangleIcon,
    AcademicCapIcon,
    RectangleStackIcon,
    FolderIcon,
    ChartBarSquareIcon,
    MegaphoneIcon
  },
  props: {
    teacherProfile: {
      type: Object,
      default: () => ({
        full_name: '',
        username: '',
        profile_photo: '',
        subject_assigned: ''
      })
    },
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['logout', 'show-student-performance', 'show-subject-leaderboard', 'update:is-open', 'redirect-change'],
  setup(props, { emit }) {
    const router = useRouter()
    const route = useRoute()
    const activeDropdown = ref(null)
    const isRedirecting = ref(false)
    const loadingMessage = ref('Loading')
    
    // Scroll control refs
    const navRef = ref(null)
    const canScrollUp = ref(false)
    const canScrollDown = ref(true)
    const scrollProgress = ref(0)

    // Determine if we're on mobile or desktop
    const isMobile = ref(false)

    // Check screen size
    const checkScreenSize = () => {
      isMobile.value = window.innerWidth < 1024
    }

    // Compute sidebar style based on screen size
    const sidebarStyle = computed(() => {
      return {
        position: 'fixed',
top: isMobile.value ? '2rem' : '4rem',
        left: '0',
height: isMobile.value ? 'calc(100vh - 2rem)' : 'calc(100vh - 4rem)',
        zIndex: isMobile.value ? '45' : '40',
        backgroundColor: 'white',
        borderRight: '1px solid #e5e7eb'
      }
    })

    // Check scroll position
    const checkScrollPosition = () => {
      if (navRef.value) {
        const { scrollTop, scrollHeight, clientHeight } = navRef.value
        canScrollUp.value = scrollTop > 0
        canScrollDown.value = scrollTop + clientHeight < scrollHeight
        scrollProgress.value = Math.round((scrollTop / (scrollHeight - clientHeight)) * 100) || 0
      }
    }

    // Scroll functions
    const scrollUp = () => {
      if (navRef.value && canScrollUp.value) {
        navRef.value.scrollBy({ top: -150, behavior: 'smooth' })
      }
    }

    const scrollDown = () => {
      if (navRef.value && canScrollDown.value) {
        navRef.value.scrollBy({ top: 150, behavior: 'smooth' })
      }
    }

    const handleLineClick = (event) => {
      if (navRef.value) {
        const lineRect = event.currentTarget.getBoundingClientRect()
        const clickPosition = (event.clientY - lineRect.top) / lineRect.height
        const scrollTarget = clickPosition * (navRef.value.scrollHeight - navRef.value.clientHeight)
        navRef.value.scrollTo({ top: scrollTarget, behavior: 'smooth' })
      }
    }

    // Helper functions
    const getProfilePhotoUrl = (profilePhoto, username) => {
      if (!profilePhoto) {
        return `https://api.dicebear.com/7.x/avataaars/svg?seed=${username || 'teacher'}`
      }
      if (profilePhoto.startsWith('http')) {
        return profilePhoto
      }
      return `http://127.0.0.1:8000/${profilePhoto}`
    }

    const handleImageError = (event) => {
      event.target.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${event.target.alt || 'teacher'}`
    }

    // Menu items
    const menuItems = [
      { 
        label: 'Overview', 
        icon: ChartBarSquareIcon, 
        to: '/teacher_dashboard' 
      },
      { 
        label: 'Mock Practice Test', 
        icon: DocumentTextIcon, 
        to: '/admin_add_practice_mock',
        action: 'redirectWithLoading'
      },
      { 
        label: 'Library & Resources', 
        icon: BookOpenIcon, 
        to: '/adminAddLibrary',
        action: 'redirectWithLoading'
      },
      { 
        label: 'Students & Growth', 
        icon: UserGroupIcon, 
        to: '/teacher/students',
        subItems: [
          { label: 'Student Performance', action: 'show-performance' },
          { label: 'Subject Leaderboard', action: 'show-leaderboard' }
        ]
      },
      { 
        label: 'Forum & Guidance', 
        icon: ChatBubbleLeftRightIcon, 
        to: '/teacher/room' 
      },
      { 
        label: 'Feedback & Actions', 
        icon: ClipboardDocumentCheckIcon, 
        to: '/teacher/feedback',
        action: 'redirectWithLoading'
      },
      { 
        label: 'Announcement', 
        icon: MegaphoneIcon, 
        to: '/teacher/announcements'
      },
      { 
        label: 'Settings', 
        icon: RectangleStackIcon, 
        to: '/teacher/settings' 
      }
    ]

    const isActive = (path) => {
      return route.path === path || route.path.startsWith(path + '/')
    }

    const toggleDropdown = (label) => {
      activeDropdown.value = activeDropdown.value === label ? null : label
    }

    // Handle redirect with loading
    const handleRedirectWithLoading = (path) => {
      emit('update:is-open', false)
      isRedirecting.value = true
      loadingMessage.value = 'Loading'
      emit('redirect-change', true)
      
      setTimeout(() => {
        router.push(path)
        setTimeout(() => {
          isRedirecting.value = false
          emit('redirect-change', false)
        }, 100)
      }, 2000)
    }

    // Handle sub item clicks
    const handleSubItemClick = (subItem) => {
      emit('update:is-open', false)
      
      if (subItem.label === 'Student Performance') {
        emit('show-student-performance')
      } else if (subItem.label === 'Subject Leaderboard') {
        emit('show-subject-leaderboard')
      }
    }

    const handleLogout = () => {
      localStorage.clear()
      emit('logout')
      router.push('/user_login')
    }

    // Initialize
    onMounted(() => {
      checkScreenSize()
      window.addEventListener('resize', checkScreenSize)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkScreenSize)
    })

    return {
      menuItems,
      activeDropdown,
      isActive,
      isRedirecting,
      loadingMessage,
      navRef,
      canScrollUp,
      canScrollDown,
      scrollProgress,
      scrollUp,
      scrollDown,
      checkScrollPosition,
      handleLineClick,
      sidebarStyle,
      toggleDropdown,
      handleRedirectWithLoading,
      handleSubItemClick,
      handleLogout,
      getProfilePhotoUrl,
      handleImageError
    }
  }
}
</script>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f9fafb;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Smooth transitions */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Sidebar nav item effects */
.sidebar-nav-item {
  position: relative;
  overflow: hidden;
}

.sidebar-nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(59, 130, 246, 0.1),
    transparent
  );
  transition: left 0.5s ease;
}

.sidebar-nav-item:hover::before {
  left: 100%;
}

/* Sub-item hover effects */
.sidebar-sub-item {
  position: relative;
  overflow: hidden;
}

.sidebar-sub-item::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  width: 0;
  height: 0;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  transform: translateY(-50%);
  transition: all 0.3s ease;
}

.sidebar-sub-item:hover::before {
  width: 100%;
  height: 100%;
  border-radius: 0;
}

/* Active state */
.sidebar-nav-item.bg-gradient-to-r::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: linear-gradient(to bottom, #3b82f6, #6366f1);
  border-radius: 3px;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

/* Mobile responsive */
@media (max-width: 1023px) {
  aside {
    top: 0 !important;
    height: 100vh !important;
    z-index: 45 !important;
  }
}
</style>