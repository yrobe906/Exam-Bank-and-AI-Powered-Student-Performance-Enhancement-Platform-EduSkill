<template>
  <header class="bg-white/95 backdrop-blur-xl shadow-lg border-b border-gray-100/50 relative z-40 flex-shrink-0 w-full">
    <div class="flex items-center justify-between px-4 sm:px-6 lg:pl-72 lg:pr-6 py-4">
      <!-- Left: Logo + Title + Hamburger (mobile) -->
      <div class="flex items-center gap-4 flex-shrink-0">
        <!-- Logo with hover glow -->
        <div class="group relative">
          <img 
            src="@/assets/images/eduskill-logo.png" 
            alt="EduSkill" 
            class="h-10 w-auto lg:h-12 object-contain transition-all duration-300 group-hover:scale-105 group-hover:shadow-lg rounded-xl"
          />
          <!-- Glow effect on hover -->
          <div class="absolute inset-0 bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] opacity-0 group-hover:opacity-20 blur-xl rounded-xl transition-opacity duration-300 -z-10"></div>
        </div>
        
        <!-- Desktop Title with gradient text -->
        <div class="hidden md:block">
          <h1 class="text-2xl font-black bg-gradient-to-r from-[#1e3c72] via-[#0fb9b1] to-[#2a5298] bg-clip-text text-transparent drop-shadow-lg">
            Teacher Portal
          </h1>
          <p class="text-xs font-medium text-gray-500 tracking-wide uppercase">Eduskill Excellence</p>
        </div>
        
        <!-- Mobile Title -->
        <div class="md:hidden text-xl font-black text-gray-900 drop-shadow-md">EduSkill</div>
        
        <!-- Enhanced Hamburger with rotation -->
        <button
          @click="$emit('toggle-sidebar')"
          class="lg:hidden p-2.5 rounded-2xl hover:bg-gradient-to-r hover:from-gray-50 hover:to-blue-50 border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all duration-300 text-gray-700 hover:text-[#1e3c72] hover:scale-110 active:scale-95"
          aria-label="Toggle sidebar"
        >
          <Bars3Icon class="w-6 h-6 transition-transform duration-300 hover:rotate-90" />
        </button>
      </div>

      <!-- Right: Teacher Info + Avatar Dropdown -->
      <div class="flex items-center gap-4 flex-shrink-0">
        <!-- Enhanced Desktop Teacher Info -->
        <div class="hidden xl:flex flex-col items-end text-right min-w-0 animate-fade-in">
          <div class="text-sm font-black text-gray-900 truncate max-w-56 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text">
            {{ teacher.full_name || 'Teacher' }}
          </div>
          <div class="flex items-center gap-2 text-xs font-semibold text-emerald-600 bg-emerald-100/60 px-2 py-1 rounded-full border border-emerald-200">
            <AcademicCapIcon class="w-3 h-3" />
            Grade {{ teacher.teaching_grade || 'X' }} • {{ teacher.subject_assigned || 'Subject' }}
          </div>
        </div>
        
        <!-- Mobile Teacher Name with badge -->
        <div class="lg:hidden flex items-center gap-2">
          <div class="text-sm font-bold text-gray-900 truncate max-w-32">
            {{ teacher.full_name?.split(' ')[0] || 'Teacher' }}
          </div>
          <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
        </div>
        
        <!-- Avatar with Dropdown -->
        <div class="relative group">
          <!-- Avatar with premium glow -->
          <button
            @click="toggleDropdown"
            class="w-12 h-12 rounded-2xl overflow-hidden border-3 border-white/50 shadow-xl hover:shadow-2xl hover:border-blue-300/50 transition-all duration-300 hover:scale-105 active:scale-95 flex-shrink-0 relative"
            :class="{ 'ring-2 ring-blue-500/30 animate-pulse': showDropdown }"
          >
            <img 
              v-if="!avatarError && teacher.profile_photo"
              :src="avatarUrl"
              :alt="teacher.full_name"
              class="w-full h-full object-cover"
              @error="avatarError = true"
            />
            <div v-else class="w-full h-full bg-gradient-to-br from-[#1e3c72] via-[#0fb9b1] to-[#2a5298] flex items-center justify-center text-sm font-black text-white relative overflow-hidden">
              {{ teacher.full_name?.charAt(0)?.toUpperCase() || 'T' }}
              <!-- Premium badge -->
              <div class="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full shadow-lg flex items-center justify-center">
                <span class="text-[8px] font-bold">★</span>
              </div>
            </div>
            
            <!-- Avatar glow effect -->
            <div class="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-emerald-500/20 opacity-0 group-hover:opacity-100 blur-xl rounded-2xl transition-all duration-500 -z-10 animate-pulse"></div>
          </button>
          
          <!-- Competitive Dropdown Menu -->
          <transition 
            enter-active-class="transition-all duration-200 ease-out"
            enter-from-class="scale-95 opacity-0 translate-y-1"
            enter-to-class="scale-100 opacity-100 translate-y-0"
            leave-active-class="transition-all duration-150 ease-in"
            leave-from-class="scale-100 opacity-100 translate-y-0"
            leave-to-class="scale-95 opacity-0 translate-y-1"
          >
            <div 
              v-if="showDropdown" 
              @click.stop
              class="absolute right-0 top-full mt-2 w-56 bg-white/95 backdrop-blur-xl border border-gray-100/50 shadow-2xl rounded-2xl py-2 z-50 animate-in slide-in-from-top-2 duration-200"
              @click.outside="showDropdown = false"
            >
              <!-- Profile Preview -->
              <div class="px-4 py-3 border-b border-gray-100">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl overflow-hidden shadow-md">
                    <img 
                      v-if="!avatarError && teacher.profile_photo"
                      :src="avatarUrl"
                      class="w-full h-full object-cover"
                      @error="avatarError = true"
                    />
                    <div v-else class="w-full h-full bg-gradient-to-br from-[#1e3c72] to-[#0fb9b1] flex items-center justify-center text-xs font-bold text-white">
                      {{ teacher.full_name?.charAt(0)?.toUpperCase() || 'T' }}
                    </div>
                  </div>
                  <div class="min-w-0">
                    <p class="font-semibold text-gray-900 text-sm">{{ teacher.full_name || 'Teacher' }}</p>
                    <p class="text-xs text-gray-500 truncate">Grade {{ teacher.teaching_grade }} • {{ teacher.subject_assigned }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Menu Items -->
              <div class="space-y-1 px-2">
                <button
                  @click="handleSettings"
                  class="group w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gradient-to-r hover:from-blue-50 hover:to-emerald-50 hover:text-[#1e3c72] transition-all duration-200 hover:shadow-sm"
                >
                  <Cog6ToothIcon class="w-4 h-4 text-gray-400 group-hover:text-[#1e3c72] transition-colors" />
                  <span>Settings</span>
                  <div class="ml-auto w-1 h-5 bg-gradient-to-b from-blue-400 to-emerald-400 rounded opacity-0 group-hover:opacity-100 transition-all duration-300 animate-pulse"></div>
                </button>
                
                <button
                  @click="handleLogout"
                  class="group w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gradient-to-r hover:from-red-50 hover:to-rose-50 hover:text-red-600 transition-all duration-200 hover:shadow-sm"
                >
                  <ArrowRightOnRectangleIcon class="w-4 h-4 text-gray-400 group-hover:text-red-600 transition-colors" />
                  <span>Logout</span>
                  <div class="ml-auto flex items-center gap-1 text-xs opacity-0 group-hover:opacity-100 transition-all">
                    <span>↗</span>
                  </div>
                </button>
              </div>
              
              <!-- Premium Badge -->
              <div class="px-4 py-2 border-t border-gray-100">
                <div class="flex items-center gap-2 text-xs bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-3 py-1.5 rounded-xl font-semibold shadow-lg">
                  <StarIcon class="w-3 h-3 fill-current" />
                  Premium Teacher
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Bars3Icon, 
  Cog6ToothIcon, 
  ArrowRightOnRectangleIcon,
  AcademicCapIcon,
  StarIcon 
} from '@heroicons/vue/24/outline'

const router = useRouter()
const props = defineProps({
  teacher: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['toggle-sidebar', 'logout'])

const avatarError = ref(false)
const showDropdown = ref(false)

// Computed avatar URL
const avatarUrl = computed(() => {
  if (avatarError.value || !props.teacher?.profile_photo) {
    return null
  }
  return `http://127.0.0.1:8000/${props.teacher.profile_photo}`
})

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  // Close on mobile after interaction
  if (showDropdown.value) {
    nextTick(() => {
      document.addEventListener('click', closeDropdownOnOutsideClick)
    })
  }
}

const closeDropdownOnOutsideClick = (event) => {
  if (!event.target.closest('.group.relative')) {
    showDropdown.value = false
    document.removeEventListener('click', closeDropdownOnOutsideClick)
  }
}

const handleSettings = () => {
  showDropdown.value = false
  router.push('/teacher/settings')
}

const handleLogout = () => {
  localStorage.clear()
  emit('logout')
  router.push('/user_login')
}

onMounted(() => {
  // Close dropdown on escape key
  const handleEscape = (e) => {
    if (e.key === 'Escape') {
      showDropdown.value = false
    }
  }
  document.addEventListener('keydown', handleEscape)
  
  // Cleanup
  onUnmounted(() => {
    document.removeEventListener('keydown', handleEscape)
    document.removeEventListener('click', closeDropdownOnOutsideClick)
  })
})
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

.group:hover .avatar-glow {
  opacity: 1;
  transform: scale(1.05);
}

/* Enhanced scrollbar for dropdown */
.dropdown-menu::-webkit-scrollbar {
  width: 4px;
}

.dropdown-menu::-webkit-scrollbar-track {
  background: transparent;
}

.dropdown-menu::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 2px;
}

.dropdown-menu::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.8);
}
</style>
