<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-white/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-600 font-medium">Loading all grades feedback data (9-12)...</p>
      </div>
    </div>

    <!-- Header - Education Office Specific -->
    <header class="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-slate-200/50 shadow-sm">
      <div class="flex items-center justify-between px-6 py-4">
        <!-- Back Button and Page Title -->
        <div class="flex items-center gap-4">
          <button 
            @click="goBack" 
            class="p-2 rounded-xl hover:bg-slate-100 transition-colors text-slate-600 hover:text-slate-800"
            title="Back to Dashboard"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-purple-700 to-blue-700 bg-clip-text text-transparent">
              📊 All Grades Feedback Management
            </h1>
            <p class="text-sm text-slate-500 flex items-center gap-2">
              <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
              Grades 9-12 • {{ stats.totalFeedback }} Total Feedbacks
            </p>
          </div>
        </div>

        <!-- Right Section - Export + Refresh -->
        <div class="flex items-center gap-3">
          <!-- Refresh Button -->
          <button 
            @click="loadFeedback"
            class="p-2 rounded-xl bg-emerald-50 text-emerald-600 hover:bg-emerald-100 transition-colors shadow-sm"
            title="Refresh Data"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
          
          <!-- Export Dropdown -->
          <div class="relative">
            <button class="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-xl font-medium shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Export Report
            </button>
          </div>

          <!-- Role Badge - Header Office -->
          <div class="px-4 py-2 bg-gradient-to-r from-purple-100 to-blue-100 text-purple-700 rounded-xl font-semibold shadow-sm">
            👑 Office
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="p-6 space-y-6">
      <div class="h-[calc(100vh-140px)] overflow-y-auto pr-2">
        <!-- ✅ Overview Cards - EDUOFFICE (All Grades 9-12) -->
        <section>
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-6 bg-gradient-to-b from-purple-600 to-blue-600 rounded-full"></div>
            <h2 class="text-lg font-bold text-gray-800">Grades 9-12 Feedback Overview</h2>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- Total Feedback -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-purple-500 to-blue-600 rounded-xl">
                  <ChatBubbleLeftRightIcon class="w-5 h-5 text-white" />
                </div>
                <span class="text-xs font-semibold text-purple-600 bg-purple-50 px-2 py-1 rounded-full">All Grades</span>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ stats.total_feedback }}</p>
              <p class="text-sm text-slate-500 mt-1">Total Feedbacks (9-12)</p>
            </div>

            <!-- Pending for Review -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-amber-400 to-orange-400 rounded-xl">
                  <ClockIcon class="w-5 h-5 text-white" />
                </div>
              </div>
              <p class="text-3xl font-bold text-amber-600">{{ stats.pending_count }}</p>
              <p class="text-sm text-slate-500 mt-1">Pending Review</p>
            </div>

            <!-- Reviewed -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl">
                  <CheckCircleIcon class="w-5 h-5 text-white" />
                </div>
              </div>
              <p class="text-3xl font-bold text-emerald-600">{{ stats.reviewed_count }}</p>
              <p class="text-sm text-slate-500 mt-1">Reviewed</p>
            </div>

            <!-- This Month -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl">
                  <CalendarIcon class="w-5 h-5 text-white" />
                </div>
              </div>
              <p class="text-3xl font-bold text-indigo-600">{{ stats.this_month }}</p>
              <p class="text-sm text-slate-500 mt-1">This Month</p>
            </div>
          </div>
        </section>

        <!-- Filters - Full Access for EduOffice -->
        <section class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm">
          <div class="flex flex-wrap items-center gap-4 mb-4">
            <h3 class="font-bold text-gray-800 flex items-center gap-2">
              <FilterIcon class="w-5 h-5 text-blue-600" />
              Filters (All Grades 9-12)
            </h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Grade Filter -->
            <select v-model="filters.grade" @change="applyFilters" class="px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50">
              <option value="">All Grades (9-12)</option>
              <option v-for="grade in [9,10,11,12]" :key="grade" :value="grade">Grade {{ grade }}</option>
            </select>
            <!-- Section Filter -->
            <select v-model="filters.section" @change="applyFilters" class="px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50">
              <option value="">All Sections</option>
              <option v-for="section in availableSectionsList" :key="section.id" :value="section.name">{{ section.name }}</option>
            </select>
            <!-- Rating Filter -->
            <select v-model="filters.rating" @change="applyFilters" class="px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50">
              <option value="">All Ratings</option>
              <option v-for="r in [1,2,3,4,5]" :key="r" :value="r">{{ r }} ⭐</option>
            </select>
            <!-- Status Filter -->
            <select v-model="filters.status" @change="applyFilters" class="px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50">
              <option value="">All Status</option>
              <option value="pending">Pending ({{ stats.pending_count }})</option>
              <option value="reviewed">Reviewed ({{ stats.reviewed_count }})</option>
            </select>
          </div>
          <!-- Clear Filters -->
          <button v-if="hasActiveFilters" @click="clearFilters" class="mt-4 px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all">
            Clear All Filters ({{ Object.keys(filters).filter(k => filters[k]).length }} active)
          </button>
        </section>

        <!-- ✅ Charts Section - Rating by Section + Trends -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Rating by Section Chart ✅ -->
          <div class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
              📈 Rating by Section ({{ allFeedback.length }} feedbacks)
            </h3>
            <div class="h-72">
              <Bar :data="sectionRatingData" :options="barChartOptions" />
            </div>
          </div>

          <!-- Feedback Trends -->
          <div class="bg-white rounded-2xl p-6 border border-slate-200/50 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
              📊 Feedback Trends (Last 30 Days)
            </h3>
            <div class="h-72">
              <Line :data="feedbackTrendData" :options="lineChartOptions" />
            </div>
          </div>
        </section>

        <!-- ✅ Feedback Table with Moderation -->
        <section class="bg-white rounded-2xl border border-slate-200/50 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gradient-to-r from-purple-50 to-blue-50">
                <tr>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Student</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Grade</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Section</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Rating</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Feedback</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Status</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="feedback in paginatedFeedback" :key="feedback.id" class="hover:bg-blue-50/50 transition-colors border-b border-slate-100 last:border-b-0">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center text-white font-bold text-sm">
                        {{ getInitials(feedback.student_name || 'Anonymous') }}
                      </div>
                      <div>
                        <p class="font-semibold text-gray-800">{{ feedback.is_anonymous ? 'Anonymous Student' : feedback.student_name }}</p>
                        <p v-if="!feedback.is_anonymous" class="text-xs text-slate-500">@{{ feedback.username }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span class="px-3 py-1 bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 rounded-full text-sm font-semibold">
                      Grade {{ feedback.grade_level }}
                    </span>
                  </td>
                  <td class="px-6 py-4 font-semibold text-gray-800">{{ feedback.section_name }}</td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-1">
                      <svg v-for="star in 5" :key="star" class="w-5 h-5" :class="star <= feedback.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                      <span class="ml-2 font-bold text-sm">({{ feedback.rating }})</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 max-w-lg">
                    <p class="text-sm text-gray-700 line-clamp-2">{{ feedback.feedback_text }}</p>
                  </td>
                  <td class="px-6 py-4">
                    <span :class="[
                      'px-3 py-1 rounded-full text-xs font-bold',
                      feedback.status === 'reviewed' 
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' 
                        : 'bg-amber-100 text-amber-800 border border-amber-200 animate-pulse'
                    ]">
                      {{ feedback.status === 'reviewed' ? '✅ Reviewed' : '⏳ Pending' }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                      <!-- Quick Review -->
                      <button 
                        v-if="feedback.status !== 'reviewed'"
                        @click="markAsReviewed(feedback.id)"
                        class="p-2 bg-emerald-100 hover:bg-emerald-200 text-emerald-700 rounded-lg transition-colors shadow-sm"
                        title="Mark Reviewed (Quick Action)"
                      >
                        <CheckIcon class="w-4 h-4" />
                      </button>
                      <!-- View Details -->
                      <button 
                        @click="viewFeedback(feedback)"
                        class="p-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg transition-colors shadow-sm"
                      >
                        <EyeIcon class="w-4 h-4" />
                      </button>
                      <!-- Delete -->
                      <button 
                        @click="confirmDelete(feedback)"
                        class="p-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition-colors shadow-sm"
                      >
                        <TrashIcon class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
                <!-- Empty State -->
                <tr v-if="paginatedFeedback.length === 0">
                  <td :colspan="7" class="px-12 py-16 text-center">
                    <div class="text-6xl mb-6 opacity-20">📭</div>
                    <h3 class="text-2xl font-bold text-gray-500 mb-2">No Feedback Found</h3>
                    <p class="text-gray-400 text-lg mb-4">No feedback matches your current filters</p>
                    <p v-if="!stats.total_feedback" class="text-slate-500 text-sm">Students haven't submitted feedback yet</p>
                    <button @click="clearFilters" class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">
                      Reset Filters
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="px-6 py-4 border-t bg-slate-50 flex items-center justify-between">
            <span class="text-sm text-slate-600">
              Showing {{ paginationStart }} - {{ paginationEnd }} of {{ totalFeedback }} feedbacks
            </span>
            <div class="flex items-center gap-2">
              <button @click="prevPage" :disabled="currentPage === 1" class="px-4 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-50">
                Previous
              </button>
              <button v-for="page in visiblePages" :key="page" @click="goToPage(page)" 
                :class="[
                  'w-10 h-10 rounded-xl text-sm font-semibold flex items-center justify-center transition-all',
                  page === currentPage 
                    ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white shadow-lg' 
                    : 'text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 hover:shadow-md'
                ]">
                {{ page }}
              </button>
              <button @click="nextPage" :disabled="currentPage === totalPages" class="px-4 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-50">
                Next
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Quick Moderation Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/50 backdrop-blur-sm">
      <div class="bg-white rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <div class="sticky top-0 bg-white p-6 border-b border-slate-200 z-10">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-bold text-gray-800">
              {{ modalAction === 'review' ? 'Mark Reviewed' : modalAction === 'delete' ? 'Delete Feedback' : 'Details' }}
            </h3>
            <button @click="closeModal" class="p-2 rounded-xl hover:bg-slate-100 text-slate-500">
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>
        </div>
        <div class="p-6 space-y-4">
          <div v-if="selectedFeedback" class="space-y-3">
            <!-- Student Info -->
            <div class="flex items-center gap-4 p-4 bg-slate-50 rounded-xl">
              <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center text-white font-bold text-lg">
                {{ getInitials(selectedFeedback.student_name) }}
              </div>
              <div>
                <p class="font-bold text-gray-900">{{ selectedFeedback.student_name || 'Anonymous' }}</p>
                <p class="text-sm text-slate-600">Grade {{ selectedFeedback.grade_level }} • {{ selectedFeedback.section_name }}</p>
              </div>
            </div>
            
            <!-- Rating -->
            <div class="flex items-center gap-2 p-4 bg-amber-50 rounded-xl border border-amber-100">
              <span class="text-sm font-semibold text-slate-500">Rating:</span>
              <div class="flex items-center gap-3">
                <div class="flex">
                  <svg v-for="star in 5" :key="star" class="w-6 h-6" :class="star <= selectedFeedback.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </div>
                <span class="font-bold text-lg text-gray-900">({{ selectedFeedback.rating }}/5)</span>
              </div>
            </div>

            <!-- Feedback Text -->
            <div>
              <p class="text-sm text-gray-700 whitespace-pre-wrap bg-white p-4 rounded-xl border">{{ selectedFeedback.feedback_text }}</p>
            </div>

            <!-- Status & Actions -->
            <div v-if="modalAction === 'review'" class="space-y-3">
              <div class="flex items-center justify-between p-3 bg-emerald-50 rounded-xl border border-emerald-200">
                <div>
                  <p class="font-semibold text-emerald-800">Mark as Reviewed</p>
                  <p class="text-sm text-emerald-700">This will update status to "Reviewed" and sync across all dashboards</p>
                </div>
                <button @click="confirmReview" class="px-6 py-2 bg-emerald-600 text-white rounded-xl font-semibold hover:bg-emerald-700 shadow-lg">
                  ✅ Mark Reviewed
                </button>
              </div>
            </div>

            <!-- Delete Confirmation -->
            <div v-if="modalAction === 'delete'" class="space-y-3">
              <div class="flex items-center justify-between p-3 bg-red-50 rounded-xl border border-red-200">
                <div>
                  <p class="font-semibold text-red-800">Delete Feedback</p>
                  <p class="text-sm text-red-700">This action cannot be undone</p>
                </div>
                <button @click="confirmDeleteAction" class="px-6 py-2 bg-red-600 text-white rounded-xl font-semibold hover:bg-red-700 shadow-lg">
                  🗑️ Delete Permanently
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Bar, Line
} from 'vue-chartjs'
import {
  ChatBubbleLeftRightIcon, StarIcon, CalendarIcon, ClockIcon, CheckCircleIcon, 
  FilterIcon, EyeIcon, CheckIcon, XMarkIcon, TrashIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

// Default to eduoffice role
const userRole = ref('eduoffice')

// State from FeedbackDashboard (simplified for eduoffice)
const isLoading = ref(false)
const currentPage = ref(1)
const filters = ref({ grade: '', section: '', rating: '', status: '', perPage: 25 })
const allFeedback = ref([])
const stats = ref({
  total_feedback: 0, average_rating: 0, pending_count: 0, reviewed_count: 0, this_month: 0
})
const availableSectionsList = ref([])

const showModal = ref(false)
const selectedFeedback = ref(null)
const modalAction = ref('')

// Computed - Charts ✅ (Rating by Section & Trends)
const filteredFeedback = computed(() => allFeedback.value)

const sectionRatingData = computed(() => {
  const feedbackBySection = {}
  filteredFeedback.value.forEach(fb => {
    const section = fb.section_name || 'Unknown'
    if (!feedbackBySection[section]) feedbackBySection[section] = []
    feedbackBySection[section].push(fb.rating || 0)
  })

  return {
    labels: Object.keys(feedbackBySection),
    datasets: [{
      label: 'Average Rating',
      data: Object.values(feedbackBySection).map(ratings => {
        const avg = ratings.reduce((a, b) => a + b, 0) / ratings.length
        return Math.round(avg * 10) / 10
      }),
      backgroundColor: 'rgba(139, 92, 246, 0.7)',
      borderColor: 'rgba(139, 92, 246, 1)',
      borderRadius: 8
    }]
  }
})

const feedbackTrendData = computed(() => ({
  labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
  datasets: [{
    label: 'New Feedback',
    data: [12, 19, 15, 22],
    fill: true,
    backgroundColor: 'rgba(34, 197, 94, 0.1)',
    borderColor: 'rgba(34, 197, 94, 1)',
    tension: 0.4
  }]
}))

// Chart Options
const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, max: 5, grid: { color: 'rgba(0,0,0,0.05)' } }
  }
}

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } }
  }
}

// Pagination computed
const paginatedFeedback = computed(() => {
  const start = (currentPage.value - 1) * filters.value.perPage
  return allFeedback.value.slice(start, start + filters.value.perPage)
})

const totalFeedback = computed(() => allFeedback.value.length)
const totalPages = computed(() => Math.ceil(totalFeedback.value / filters.value.perPage))
const currentPageNum = computed(() => currentPage.value)
const paginationStart = computed(() => (currentPage.value - 1) * filters.value.perPage + 1)
const paginationEnd = computed(() => Math.min(currentPage.value * filters.value.perPage, totalFeedback.value))
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

// Methods
const getInitials = (name) => name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0,2) || '??'

const hasActiveFilters = computed(() => Object.values(filters.value).some(v => v))

const applyFilters = () => {
  currentPage.value = 1
  loadFeedback()
}

const clearFilters = () => {
  Object.keys(filters.value).forEach(key => filters.value[key] = '')
  loadFeedback()
}

const loadFeedback = async () => {
  isLoading.value = true
  try {
    const token = localStorage.getItem('token') || sessionStorage.getItem('admin_token')
    const params = new URLSearchParams()
    
    if (filters.value.grade) params.append('grade', filters.value.grade)
    if (filters.value.section) params.append('section', filters.value.section)
    if (filters.value.rating) params.append('rating', filters.value.rating)
    if (filters.value.status) params.append('status', filters.value.status)
    
    const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/feedback?${params}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const data = await response.json()
      allFeedback.value = data.feedback || []
      stats.value = { 
        total_feedback: data.total || 0,
        average_rating: data.stats?.average_rating || 0,
        pending_count: data.stats?.pending_count || 0,
        reviewed_count: data.stats?.reviewed_count || 0,
        this_month: data.stats?.this_month || 0
      }
    }
  } catch (error) {
    console.error('Error loading feedback:', error)
  } finally {
    isLoading.value = false
  }
}

// Moderation Actions ✅
const markAsReviewed = async (id) => {
  try {
    const token = localStorage.getItem('token') || sessionStorage.getItem('admin_token')
    const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/moderate/${id}`, {
      method: 'PUT',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: 'reviewed' })
    })
    
    if (response.ok) {
      loadFeedback() // Refresh immediately
      // This will instantly update teacher dashboard too!
    }
  } catch (error) {
    console.error('Error marking reviewed:', error)
  }
}

const goBack = () => router.push('/education_office_dashboard')
const prevPage = () => currentPage.value > 1 && currentPage.value--
const nextPage = () => currentPage.value < totalPages.value && currentPage.value++
const goToPage = (page) => currentPage.value = page

// Modal Methods
const viewFeedback = (feedback) => {
  selectedFeedback.value = feedback
  modalAction.value = 'view'
  showModal.value = true
}

const confirmDelete = (feedback) => {
  selectedFeedback.value = feedback
  modalAction.value = 'delete'
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  modalAction.value = ''
}

onMounted(() => {
  loadFeedback()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

