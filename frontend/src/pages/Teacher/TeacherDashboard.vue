<!-- TeacherDashboard.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
    <!-- Header -->
    <TeacherAppHeader 
      :teacher="teacher"
      @toggle-sidebar="toggleSidebar"
    />

    <!-- Main Layout -->
    <div class="flex pt-16 relative">
      <!-- Sidebar Overlay (Mobile) -->
      <div 
        v-if="sidebarOpen" 
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
        @click="sidebarOpen = false"
      ></div>

      <!-- Sidebar Container -->
      <div 
        class="fixed lg:relative z-50 h-[calc(100vh-4rem)] transition-all duration-300"
        :class="[
'-left-56 lg:left-0',
'w-56'
        ]"
      >
        <TeacherSidebar
          :teacher-profile="teacher"
          :is-open="sidebarOpen"
          @update:is-open="sidebarOpen = $event"
          @logout="handleLogout"
          @show-student-performance="showStudentPerformance"
          @show-subject-leaderboard="showSubjectLeaderboard"
          @redirect-change="handleRedirectChange"
        />
      </div>

      <!-- Main Content -->
      <main 
        class="flex-1 min-w-0 transition-all duration-300"
        :class="{ 'lg:ml-0': sidebarOpen }"
      >
        <div class="p-4 md:p-6 lg:p-8 xl:p-10 space-y-6 md:space-y-8">
          <!-- Loading Overlay -->
          <div v-if="isLoading" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
            <div class="bg-white p-8 rounded-2xl shadow-2xl text-center max-w-sm mx-4">
              <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600 mx-auto mb-4"></div>
              <p class="text-lg font-semibold text-gray-800 mb-2">{{ loadingMessage }}</p>
            </div>
          </div>

          <!-- Welcome Section (only show on overview) -->
          <div v-if="currentView === 'overview'" class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 class="text-2xl md:text-3xl lg:text-4xl font-black text-slate-800 mb-2">
                Welcome back, {{ teacher.full_name?.split(' ')[0] || 'Teacher' }}!
              </h1>
              <p class="text-slate-600 text-base md:text-lg">
                Here's what's happening with your class today.
              </p>
            </div>
            <div class="flex items-center gap-3">
              <span class="px-4 py-2 bg-blue-100 text-blue-700 rounded-xl font-semibold text-sm">
                {{ currentDate }}
              </span>
            </div>
          </div>

          <!-- Dynamic Content based on selected view -->
          <DashboardOverview
            v-if="currentView === 'overview'"
            :teacher="teacher"
            :stats="stats"
            :resources="resources"
            :recent-resources="recentResources"
          />

          <StudentPerformanceLeaderboard
            v-if="currentView === 'performance'"
            :teacher="teacher"
            :user-role="'teacher'"
            :student-performance-data="studentPerformanceData"
            :is-loading="isLoading"
            @back-to-dashboard="goToOverview"
          />

          <SubjectLeaderboard
            v-if="currentView === 'leaderboard'"
            :teacher="teacher"
            :user-role="'teacher'"
            :section-leaderboard-data="sectionLeaderboardData"
            :is-loading="isLoading"
            @back-to-dashboard="goToOverview"
            @refresh="loadSectionLeaderboard"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import TeacherAppHeader from '@/components/Header/TeacherAppHeader.vue'
import TeacherSidebar from '@/components/Sidebar/TeacherSidebar.vue'
import DashboardOverview from '@/pages/Teacher/DashboardOverview.vue'
import StudentPerformanceLeaderboard from '@/pages/Teacher/StudentPerformanceLeaderboard.vue'
import SubjectLeaderboard from '@/pages/Teacher/SubjectLeaderboard.vue'

const router = useRouter()

// State
const teacher = ref({ 
  full_name: '', 
  username: '', 
  profile_photo: '', 
  teaching_grade: '', 
  subject_assigned: '',
  school_name: '' 
})
const stats = ref({ totalStudents: 0, activeThisWeek: 0, avgReadiness: 0 })
const resources = ref({ notes: 0, slides: 0, videos: 0, books: 0 })
const recentResources = ref([])
const isLoading = ref(false)
const loadingMessage = ref('Loading dashboard...')
const studentPerformanceData = ref([])
const sectionLeaderboardData = ref([])
const sidebarOpen = ref(true) // Start with sidebar open on desktop
const currentView = ref('overview') // overview, performance, leaderboard

// Current date formatted
const currentDate = computed(() => {
  return new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    month: 'long', 
    day: 'numeric' 
  })
})

// Check if mobile on mount and adjust sidebar
const checkMobile = () => {
  if (window.innerWidth < 1024) {
    sidebarOpen.value = false
  } else {
    sidebarOpen.value = true
  }
}

// Toggle sidebar
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// Navigate to overview
const goToOverview = () => {
  currentView.value = 'overview'
}

// Handle logout
const handleLogout = () => {
  localStorage.clear()
  router.push('/user_login')
}

// Handle redirect loading
const handleRedirectChange = (loading) => {
  isLoading.value = loading
}

// Show student performance
const showStudentPerformance = async () => {
  currentView.value = 'performance'
  isLoading.value = true
  loadingMessage.value = 'Fetching student performance...'
  
  const token = localStorage.getItem('token')
  try {
    const res = await fetch('http://127.0.0.1:8000/api/users/teacher/student-performance', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      studentPerformanceData.value = (data.students || data).map((student, index) => ({
        ...student,
        rank: index + 1
      }))
    }
  } catch (e) {
    console.error('Load performance error:', e)
  } finally {
    isLoading.value = false
  }
}

// Load section leaderboard
const loadSectionLeaderboard = async () => {
  isLoading.value = true
  loadingMessage.value = 'Loading section leaderboard...'
  
  const token = localStorage.getItem('token')
  try {
    const res = await fetch('http://127.0.0.1:8000/api/analytics/section-leaderboard', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      sectionLeaderboardData.value = data.sections || data.map((section, index) => ({
        ...section,
        rank: index + 1
      }))
    }
  } catch (e) {
    console.error('Load section leaderboard error:', e)
  } finally {
    isLoading.value = false
  }
}

// Show subject leaderboard
const showSubjectLeaderboard = () => {
  currentView.value = 'leaderboard'
  loadSectionLeaderboard()
}

// Load dashboard data
onMounted(async () => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  
  const username = localStorage.getItem('username')
  const role = localStorage.getItem('role')
  const token = localStorage.getItem('token')
  
  if (!username || role !== 'teacher' || !token) {
    router.push('/user_login')
    return
  }
  
  isLoading.value = true
  
  try {
    // Load profile
    const profileRes = await fetch(`http://127.0.0.1:8000/api/users/profile/${username}`)
    if (profileRes.ok) {
      teacher.value = await profileRes.json()
    }
    
    // Load stats
    const statsRes = await fetch('http://127.0.0.1:8000/api/users/teacher/dashboard-stats', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (statsRes.ok) {
      stats.value = await statsRes.json()
    }
    
    // Load resources
    const resourcesRes = await fetch('http://127.0.0.1:8000/api/users/teacher/resources', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (resourcesRes.ok) {
      resources.value = await resourcesRes.json()
    }
    
    // Load recent uploads
    const recentRes = await fetch('http://127.0.0.1:8000/api/users/teacher/recent-uploads', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (recentRes.ok) {
      recentResources.value = await recentRes.json()
    }
    
  } catch (error) {
    console.error('Dashboard load error:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.min-h-screen {
  min-height: 100vh;
}

/* Custom scrollbar */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Smooth transitions */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Sidebar positioning */
.fixed.left-0 {
  left: 0;
}

.-left-64 {
  left: -16rem;
}

@media (min-width: 1024px) {
  .lg\:left-0 {
    left: 0;
  }
}
</style>