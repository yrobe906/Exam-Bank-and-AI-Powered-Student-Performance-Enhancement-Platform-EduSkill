<template>
  <aside class="w-64 bg-white border-r border-gray-200 flex flex-col shadow-lg h-full">

    <!-- Navigation with custom scrollbar -->
    <nav 
      ref="navRef" 
      class="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto custom-scrollbar" 
      @scroll="checkScrollPosition"
    >
      <template v-for="item in menuItems" :key="item.label">
        <!-- Main Menu Item - Using button instead of router-link for internal navigation -->
        <button
          v-if="!item.subItems"
          @click="handleItemClick(item)"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group relative text-left"
          :class="[
            isActive(item) 
              ? 'bg-blue-50 text-blue-700' 
              : 'text-gray-600 hover:bg-gray-100'
          ]"
        >
          <component 
            :is="item.icon" 
            class="w-5 h-5 transition-all duration-200"
            :class="isActive(item) ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'"
          />
          <span>{{ item.label }}</span>
          
          <!-- Active Indicator -->
          <span 
            v-if="isActive(item)" 
            class="absolute left-0 w-1 h-6 bg-blue-600 rounded-r-full"
          ></span>
        </button>

        <!-- Dropdown Menu Item -->
        <div v-else class="relative">
          <button
            @click="toggleDropdown(item.label)"
            class="w-full flex items-center justify-between gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group"
            :class="[
              activeDropdown === item.label
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            <div class="flex items-center gap-3">
              <component 
                :is="item.icon" 
                class="w-5 h-5 transition-all duration-200"
                :class="activeDropdown === item.label ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'"
              />
              <span>{{ item.label }}</span>
            </div>
            <ChevronDownIcon 
              class="w-4 h-4 transition-transform duration-200"
              :class="activeDropdown === item.label ? 'rotate-180' : ''"
            />
          </button>
          
          <!-- Sub Items -->
          <transition
            enter-active-class="transition-all duration-200 ease-out"
            enter-from-class="opacity-0 -translate-y-1"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-150 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-1"
          >
            <div v-if="activeDropdown === item.label" class="mt-1 ml-4 pl-3 border-l-2 border-gray-100 space-y-0.5">
              <button
                v-for="subItem in item.subItems"
                :key="subItem.label"
                @click="handleItemClick(subItem)"
                class="w-full text-left px-4 py-2 rounded-lg text-sm text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-all duration-200"
                :class="isActive(subItem) ? 'text-blue-600 bg-blue-50' : ''"
              >
                {{ subItem.label }}
              </button>
            </div>
          </transition>
        </div>
      </template>
    </nav>
  </aside>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ChartBarIcon,
  ChartPieIcon,
  BookOpenIcon,
  UserGroupIcon,
  DocumentTextIcon,
  ChevronDownIcon,
  MegaphoneIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'EducationOfficeSidebar',
  components: {
    ChartBarIcon,
    ChartPieIcon,
    BookOpenIcon,
    UserGroupIcon,
    DocumentTextIcon,
    ChevronDownIcon,
    MegaphoneIcon,
    Cog6ToothIcon
  },
  props: {
    officerProfile: {
      type: Object,
      default: () => ({
        full_name: '',
        username: '',
        profile_photo: '',
        school_name: ''
      })
    },
    activeNav: {
      type: Number,
      default: 0
    }
  },
  emits: ['nav-click'],
  setup(props, { emit }) {
    const router = useRouter()
    const activeDropdown = ref(null)
    const navRef = ref(null)
    const canScrollUp = ref(false)
    const canScrollDown = ref(true)

    // Menu items with consistent view names
    const menuItems = [
      { 
        label: 'City Overview', 
        icon: ChartBarIcon, 
        view: 'overview',
        index: 0
      },
      { 
        label: 'Grade Performance', 
        icon: ChartPieIcon, 
        view: 'grade-performance',
        index: 1
      },
      { 
        label: 'Subject Leaderboard', 
        icon: BookOpenIcon, 
        view: 'subject-leaderboard',
        index: 2
      },
      { 
        label: 'Student Performance', 
        icon: UserGroupIcon, 
        view: 'student-performance',
        index: 3
      },
      { 
        label: 'Reports Center', 
        icon: DocumentTextIcon, 
        view: 'reports',
        to: '/eduoffice/feedback', // Add the route path
        index: 4
      },
      { 
        label: 'Announcements', 
        icon: MegaphoneIcon, 
        view: 'announcements',
        to: '/eduoffice/announcements',
        index: 5
      },
      { 
        label: 'Settings', 
        icon: Cog6ToothIcon, 
        to: '/eduoffice/settings',
        index: 6
      }
    ]

    // Check if item is active based on activeNav prop
    const isActive = (item) => {
      return props.activeNav === item.index
    }

    const checkScrollPosition = () => {
      if (navRef.value) {
        const { scrollTop, scrollHeight, clientHeight } = navRef.value
        canScrollUp.value = scrollTop > 0
        canScrollDown.value = scrollTop + clientHeight < scrollHeight - 1
      }
    }

    const toggleDropdown = (label) => {
      activeDropdown.value = activeDropdown.value === label ? null : label
    }

    const handleItemClick = (item) => {
      // Check if this is the Reports Center with a direct route
      if (item.label === 'Reports Center' && item.to) {
        // Navigate directly to the route
        router.push(item.to)
      } else {
        // Emit the nav-click event with the item for internal views
        emit('nav-click', item)
      }
      // Close any open dropdown
      activeDropdown.value = null
    }

    onMounted(() => {
      checkScrollPosition()
      if (navRef.value) {
        navRef.value.addEventListener('scroll', checkScrollPosition)
      }
    })

    onUnmounted(() => {
      if (navRef.value) {
        navRef.value.removeEventListener('scroll', checkScrollPosition)
      }
    })

    return {
      menuItems,
      activeDropdown,
      isActive,
      navRef,
      canScrollUp,
      canScrollDown,
      checkScrollPosition,
      toggleDropdown,
      handleItemClick,
      getUserInitials: () => '' // Empty function since we removed the user section
    }
  }
}
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #d1d5db #f3f4f6;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
  transition: background 0.2s;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

button {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.absolute.left-0.w-1 {
  animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>