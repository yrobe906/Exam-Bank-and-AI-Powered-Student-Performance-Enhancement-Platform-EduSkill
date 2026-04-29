<template>
  <!-- Main container with centered, balanced layout -->
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50 py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Loading Overlay (unchanged for safety) -->
      <div v-if="isLoading" class="fixed inset-0 bg-gradient-to-br from-emerald-50/95 via-white/95 to-blue-50/90 z-50 flex items-center justify-center backdrop-blur-2xl">
        <!-- Loading content same as first page -->
        <div class="relative bg-white/95 p-12 rounded-3xl shadow-2xl border border-emerald-200/50 max-w-lg mx-auto text-center">
          <div class="relative mb-8">
            <div class="absolute inset-0 w-24 h-24 bg-gradient-to-r from-emerald-500 to-blue-600 rounded-full blur-xl opacity-30 animate-pulse"></div>
            <div class="animate-spin rounded-full h-24 w-24 bg-gradient-to-r from-emerald-500 via-blue-500 to-indigo-600 shadow-xl mx-auto border-4 border-white relative z-10"></div>
            <TrophyIcon class="absolute inset-0 w-12 h-12 text-white mx-auto animate-pulse relative z-20" />
          </div>
          <h2 class="text-2xl font-bold text-slate-800 mb-3">Loading Rankings...</h2>
          <p class="text-slate-600 mb-6">{{ loadingMessage }}</p>
        </div>
      </div>

      <!-- Header Section -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div class="flex items-center gap-4">
          <button 
            @click="goBack"
            class="p-3 rounded-xl bg-white hover:bg-slate-50 shadow-md hover:shadow-lg transition-all border border-slate-200"
          >
            <ArrowLeftIcon class="w-5 h-5 text-slate-600" />
          </button>
          <div>
            <h1 class="text-2xl md:text-3xl font-bold text-slate-800">Student Performance</h1>
            <p class="text-sm text-slate-500 mt-1">
              {{ userRole === 'eduoffice' ? 'All Grades Overview' : `Grade ${teacher?.teaching_grade || ''} Class` }}
            </p>
          </div>
        </div>
        
        <!-- Refresh Button -->
        <button 
          @click="$emit('refresh')"
          class="px-4 py-2 bg-white rounded-xl shadow-md hover:shadow-lg transition-all border border-slate-200 text-sm font-medium text-slate-600 flex items-center gap-2 self-start"
        >
          <ArrowPathIcon class="w-4 h-4" />
          Refresh Data
        </button>
      </div>

      <!-- Stats Overview - Balanced Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
        <!-- Total Students -->
        <div class="bg-white rounded-xl p-6 shadow-md border border-slate-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-500 mb-1">Total Students</p>
              <p class="text-3xl font-bold text-slate-800">{{ sortedStudents.length }}</p>
            </div>
            <div class="p-3 bg-emerald-100 rounded-lg">
              <UserGroupIcon class="w-6 h-6 text-emerald-600" />
            </div>
          </div>
        </div>

        <!-- Class Average -->
        <div class="bg-white rounded-xl p-6 shadow-md border border-slate-100">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-500 mb-1">Class Average</p>
              <p class="text-3xl font-bold text-slate-800">{{ averageClassScore }}%</p>
            </div>
            <div class="p-3 bg-blue-100 rounded-lg">
              <ChartBarIcon class="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <!-- Top Performer -->
        <div class="bg-white rounded-xl p-6 shadow-md border border-slate-100 cursor-pointer hover:shadow-lg transition-all" @click="scrollToTop">
          <div class="flex items-center justify-between">
            <div class="min-w-0 flex-1">
              <p class="text-sm text-slate-500 mb-1">Top Performer</p>
              <p class="text-lg font-semibold text-slate-800 truncate">{{ topPerformer?.full_name || 'N/A' }}</p>
              <p class="text-xs text-slate-500">{{ topPerformer?.average_score || 0 }}% average</p>
            </div>
            <div class="p-3 bg-orange-100 rounded-lg ml-3">
              <TrophyIcon class="w-6 h-6 text-orange-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Controls Bar -->
      <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div class="flex items-center gap-3">
          <span class="text-sm font-medium text-slate-600">Sort by:</span>
          <select 
            v-model="sortBy"
            class="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="rank">Rank</option>
            <option value="average_score">Average Score</option>
            <option value="total_exams">Exams Taken</option>
          </select>
        </div>
        <span class="text-sm text-slate-500">{{ sortedStudents.length }} students</span>
      </div>

      <!-- Leaderboard Table - Clean & Balanced -->
      <div class="bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50 border-b border-slate-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Rank</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Student</th>
                <th v-if="userRole === 'eduoffice'" class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Grade</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Exams</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Avg Score</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr 
                v-for="student in paginatedStudents" 
                :key="student.id"
                class="hover:bg-slate-50 transition-colors"
              >
                <!-- Rank -->
                <td class="px-6 py-4">
                  <span class="inline-flex items-center justify-center w-7 h-7 rounded-full text-sm font-medium"
                        :class="getRankClass(student.rank)">
                    {{ getRankDisplay(student.rank) }}
                  </span>
                </td>

                <!-- Student Info -->
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <img
                      :src="getProfilePhotoUrl(student.profile_photo, student.username)"
                      :alt="student.username"
                      class="w-9 h-9 rounded-full object-cover border-2 border-white shadow-sm"
                      @error="handleImageError"
                    />
                    <div>
                      <p class="font-medium text-slate-800">{{ student.full_name || student.username }}</p>
                      <p class="text-xs text-slate-500">@{{ student.username }}</p>
                    </div>
                  </div>
                </td>

                <!-- Grade (EduOffice) -->
                <td v-if="userRole === 'eduoffice'" class="px-6 py-4">
                  <span class="px-2 py-1 bg-blue-50 text-blue-600 rounded-md text-xs font-medium">
                    Grade {{ student.grade }}
                  </span>
                </td>

                <!-- Exams Taken -->
                <td class="px-6 py-4">
                  <span class="font-medium text-slate-700">{{ student.total_exams_taken }}</span>
                </td>

                <!-- Score with Progress -->
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-20 bg-slate-100 rounded-full h-1.5">
                      <div 
                        class="h-1.5 rounded-full transition-all duration-500"
                        :class="getProgressClass(student.average_score)"
                        :style="{ width: Math.min(student.average_score, 100) + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium" :class="getScoreClass(student.average_score)">
                      {{ student.average_score }}%
                    </span>
                  </div>
                </td>

                <!-- Status Badge -->
                <td class="px-6 py-4">
                  <span class="px-2 py-1 rounded-md text-xs font-medium"
                        :class="getStatusClass(student.average_score)">
                    {{ getStatusLabel(student.average_score) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="sortedStudents.length > pageSize" class="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
          <p class="text-sm text-slate-600">
            Showing {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, sortedStudents.length) }} of {{ sortedStudents.length }}
          </p>
          <div class="flex gap-2">
            <button 
              @click="currentPage--" 
              :disabled="currentPage === 1"
              class="px-3 py-1 bg-white border border-slate-200 rounded-md text-sm disabled:opacity-50"
            >
              Previous
            </button>
            <button 
              @click="currentPage++" 
              :disabled="currentPage * pageSize >= sortedStudents.length"
              class="px-3 py-1 bg-white border border-slate-200 rounded-md text-sm disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="sortedStudents.length === 0 && !isLoading" class="bg-white rounded-xl shadow-md border border-slate-200 p-12 text-center">
        <TrophyIcon class="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <h3 class="text-lg font-semibold text-slate-700 mb-1">No Students Yet</h3>
        <p class="text-sm text-slate-500">Students will appear here once they start taking exams.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon, ArrowPathIcon, TrophyIcon, UserGroupIcon, ChartBarIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const emit = defineEmits(['refresh', 'back'])

// Props
const props = defineProps({
  teacher: { type: Object, default: () => ({}) },
  userRole: { type: String, default: '' },
  studentPerformanceData: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false }
})

// State
const loadingMessage = ref('Loading...')
const sortBy = ref('rank')
const currentPage = ref(1)
const pageSize = ref(20)

// Computed
const sortedStudents = computed(() => {
  let students = [...(props.studentPerformanceData || [])]
  if (sortBy.value === 'average_score') {
    students.sort((a, b) => b.average_score - a.average_score)
  } else if (sortBy.value === 'total_exams') {
    students.sort((a, b) => b.total_exams_taken - a.total_exams_taken)
  } else {
    students.sort((a, b) => (a.rank || 0) - (b.rank || 0))
  }
  return students.map((student, index) => ({ ...student, rank: index + 1 }))
})

const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return sortedStudents.value.slice(start, start + pageSize.value)
})

const averageClassScore = computed(() => {
  if (sortedStudents.value.length === 0) return 0
  const sum = sortedStudents.value.reduce((acc, student) => acc + (student.average_score || 0), 0)
  return Math.round(sum / sortedStudents.value.length)
})

const topPerformer = computed(() => sortedStudents.value[0] || null)

// Methods
const goBack = () => {
  emit('back')
  router.push(props.userRole === 'eduoffice' ? '/education_office_dashboard' : '/teacher_dashboard')
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const getProfilePhotoUrl = (profilePhoto, username) => {
  if (!profilePhoto) return `https://api.dicebear.com/7.x/avataaars/svg?seed=${username}`
  if (profilePhoto.startsWith('http')) return profilePhoto
  return `http://127.0.0.1:8000/${profilePhoto}`
}

const handleImageError = (e) => {
  e.target.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${e.target.alt}`
}

// Styling helpers
const getRankClass = (rank) => {
  if (rank === 1) return 'bg-yellow-100 text-yellow-700'
  if (rank === 2) return 'bg-gray-100 text-gray-700'
  if (rank === 3) return 'bg-orange-100 text-orange-700'
  return 'bg-slate-100 text-slate-600'
}

const getRankDisplay = (rank) => {
  if (rank === 1) return '1'
  if (rank === 2) return '2'
  if (rank === 3) return '3'
  return rank
}

const getProgressClass = (score) => {
  if (score >= 70) return 'bg-emerald-500'
  if (score >= 50) return 'bg-amber-500'
  return 'bg-red-500'
}

const getScoreClass = (score) => {
  if (score >= 70) return 'text-emerald-600'
  if (score >= 50) return 'text-amber-600'
  return 'text-red-600'
}

const getStatusClass = (score) => {
  if (score >= 80) return 'bg-emerald-50 text-emerald-700'
  if (score >= 70) return 'bg-blue-50 text-blue-700'
  if (score >= 50) return 'bg-amber-50 text-amber-700'
  return 'bg-red-50 text-red-700'
}

const getStatusLabel = (score) => {
  if (score >= 80) return 'Legendary'
  if (score >= 70) return 'Warrior'
  if (score >= 50) return 'Fighter'
  return 'Needs Work'
}
</script>