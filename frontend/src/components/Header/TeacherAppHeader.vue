<!-- TeacherAppHeader.vue -->
<template>
  <header class="fixed top-0 left-0 right-0 bg-gradient-to-r from-slate-50/95 to-white/95 backdrop-blur-xl border-b border-slate-200/50 shadow-lg z-50">
    <div class="px-4 md:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Left Section -->
      <div class="flex items-center gap-3 md:gap-6">
        <!-- Mobile Menu Toggle -->
        <button 
          @click="$emit('toggle-sidebar')"
          class="lg:hidden p-2.5 rounded-xl hover:bg-slate-100 transition-all duration-200 group"
        >
          <Bars3Icon class="w-6 h-6 text-slate-600 group-hover:text-blue-600" />
        </button>

        <!-- Logo & Brand -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl shadow-lg flex items-center justify-center">
            <AcademicCapIcon class="w-6 h-6 text-white" />
          </div>
          <div class="hidden sm:block">
            <h1 class="text-xl font-black bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
              Teacher Portal
            </h1>
            <p class="text-xs text-slate-500 font-medium">Grade {{ teacher.teaching_grade }} • {{ teacher.subject_assigned }}</p>
          </div>
        </div>
      </div>

      <!-- Right Section -->
      <div class="flex items-center gap-2 md:gap-4">
        <!-- Notifications -->

        <!-- User Menu -->
        <div class="relative">
          <button class="flex items-center gap-3 p-1.5 pl-3 rounded-xl hover:bg-slate-100 transition-all group">
            <div class="hidden lg:block text-right">
              <p class="text-sm font-semibold text-slate-800">{{ teacher.full_name || 'Teacher' }}</p>
              <p class="text-xs text-slate-500">{{ teacher.school_name || 'School' }}</p>
            </div>
            <div class="relative">
              <img 
                :src="teacherImage" 
                :alt="teacher.full_name"
                class="w-9 h-9 rounded-xl object-cover border-2 border-white shadow-md group-hover:shadow-xl transition-all"
              />
              <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-white"></div>
            </div>
            <ChevronDownIcon class="w-4 h-4 text-slate-400 hidden lg:block" />
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import {
  Bars3Icon,
  AcademicCapIcon,
  BellIcon,
  ChatBubbleLeftRightIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  teacher: {
    type: Object,
    default: () => ({
      full_name: '',
      username: '',
      profile_photo: '',
      teaching_grade: '',
      subject_assigned: '',
      school_name: ''
    })
  }
})

defineEmits(['toggle-sidebar'])

const getProfilePhotoUrl = (profilePhoto, username) => {
  if (!profilePhoto) {
    return `https://api.dicebear.com/7.x/avataaars/svg?seed=${username || 'teacher'}`
  }

  let normalizedPath = profilePhoto.replace(/\\/g, '/').replace(/^\/+/, '')
  if (!normalizedPath.startsWith('uploads/')) {
    normalizedPath = `uploads/${normalizedPath}`
  }

  return `http://127.0.0.1:8000/${normalizedPath}`
}

const teacherImage = computed(() => getProfilePhotoUrl(props.teacher.profile_photo, props.teacher.username))
</script>