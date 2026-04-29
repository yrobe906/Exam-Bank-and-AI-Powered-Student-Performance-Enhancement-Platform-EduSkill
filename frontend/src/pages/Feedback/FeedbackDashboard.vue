<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-white/80 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-600 font-medium">Loading feedback data...</p>
      </div>
    </div>

    <!-- Header -->
    <header class="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-slate-200/50 shadow-sm">
      <div class="flex items-center justify-between px-6 py-4">
        <!-- Back Button and Page Title -->
        <div class="flex items-center gap-4">
          <button 
            @click="goBack" 
            class="p-2 rounded-xl hover:bg-slate-100 transition-colors text-slate-600 hover:text-slate-800"
            title="Go Back"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-700 to-indigo-700 bg-clip-text text-transparent">
              📊 Feedback Dashboard
            </h1>
            <p class="text-sm text-slate-500 flex items-center gap-2">
              <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              {{ getRoleTitle() }}
            </p>
          </div>
        </div>

        <!-- Right Section -->
        <div class="flex items-center gap-3">
          <!-- Role Badge -->
          <div :class="roleBadgeClass" class="px-4 py-2 rounded-xl text-sm font-semibold">
            {{ roleBadgeText }}
          </div>

          <!-- Profile -->
          <div class="flex items-center gap-3 pl-3 border-l border-slate-200">
            <img
              :src="userAvatar"
              alt="Profile"
              class="w-10 h-10 rounded-xl object-cover border-2 border-white shadow-md"
            />
            <div class="hidden lg:block">
              <p class="text-sm font-bold text-gray-800">{{ userName }}</p>
              <p class="text-xs text-slate-500">{{ userRoleDisplay }}</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="p-6 space-y-6">
      <div class="h-[calc(100vh-120px)] overflow-y-auto pr-2">
        <!-- Overview Cards -->
        <section>
          <div class="flex items-center gap-2 mb-4">
            <div class="w-1 h-6 bg-gradient-to-b from-blue-600 to-indigo-600 rounded-full"></div>
            <h2 class="text-lg font-bold text-gray-800">Feedback Overview</h2>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <!-- Total Feedback -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl">
                  <ChatBubbleLeftRightIcon class="w-5 h-5 text-white" />
                </div>
                <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded-full">Total</span>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ stats.totalFeedback }}</p>
              <p class="text-sm text-slate-500 mt-1">Total Received</p>
            </div>

            <!-- This Week -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl">
                  <CalendarIcon class="w-5 h-5 text-white" />
                </div>
                <span class="text-xs font-semibold text-green-600 bg-green-50 px-2 py-1 rounded-full">This Week</span>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ stats.thisWeek }}</p>
              <p class="text-sm text-slate-500 mt-1">Feedback This Week</p>
            </div>

            <!-- Anonymous -->
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm hover:shadow-lg transition-all">
              <div class="flex items-center justify-between mb-3">
                <div class="p-2 bg-gradient-to-br from-cyan-500 to-teal-600 rounded-xl">
                  <EyeSlashIcon class="w-5 h-5 text-white" />
                </div>
                <span class="text-xs font-semibold text-cyan-600 bg-cyan-50 px-2 py-1 rounded-full">Anonymous</span>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ stats.anonymousCount }}</p>
              <p class="text-sm text-slate-500 mt-1">Anonymous ({{ stats.anonymousPercent }}%)</p>
            </div>
          </div>
        </section>

        <!-- Filters Section -->
        <section class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm">
          <div class="flex flex-wrap items-center gap-4">
            <!-- Grade Filter -->
            <div class="flex-1 min-w-[150px]" v-if="canViewAllGrades">
              <label class="block text-xs font-semibold text-slate-500 mb-1">Grade Level</label>
              <select 
                v-model="filters.grade"
                @change="applyFilters"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Grades</option>
                <option v-for="grade in availableGrades" :key="grade" :value="grade">Grade {{ grade }}</option>
              </select>
            </div>

            <!-- Section Filter -->
            <div class="flex-1 min-w-[200px]">
              <label class="block text-xs font-semibold text-slate-500 mb-1">Section/Subject</label>
              <select 
                v-model="filters.section"
                @change="applyFilters"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Sections</option>
                <option v-for="section in availableSectionsList" :key="section.id" :value="section.name">{{ section.name }}</option>
              </select>
            </div>

            <!-- Rating Filter -->
            <div class="flex-1 min-w-[150px]">
              <label class="block text-xs font-semibold text-slate-500 mb-1">Rating</label>
              <select 
                v-model="filters.rating"
                @change="applyFilters"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Ratings</option>
                <option v-for="rating in [1, 2, 3, 4, 5]" :key="rating" :value="rating">{{ rating }} Star{{ rating > 1 ? 's' : '' }}</option>
              </select>
            </div>

            <!-- Status Filter -->
            <div class="flex-1 min-w-[150px]">
              <label class="block text-xs font-semibold text-slate-500 mb-1">Status</label>
              <select 
                v-model="filters.status"
                @change="applyFilters"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="reviewed">Reviewed</option>
              </select>
            </div>
          </div>

          <!-- Active Filters -->
          <div v-if="hasActiveFilters" class="mt-4 pt-4 border-t border-slate-100">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-sm text-slate-500">Active Filters:</span>
              <button 
                v-if="filters.grade"
                @click="filters.grade = ''; applyFilters()"
                class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full flex items-center gap-1"
              >
                Grade {{ filters.grade }} <XMarkIcon class="w-3 h-3" />
              </button>
              <button 
                v-if="filters.section"
                @click="filters.section = ''; applyFilters()"
                class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full flex items-center gap-1"
              >
                {{ filters.section }} <XMarkIcon class="w-3 h-3" />
              </button>
              <button 
                v-if="filters.rating"
                @click="filters.rating = ''; applyFilters()"
                class="px-2 py-1 bg-amber-100 text-amber-700 text-xs rounded-full flex items-center gap-1"
              >
                {{ filters.rating }} Stars <XMarkIcon class="w-3 h-3" />
              </button>
              <button 
                v-if="filters.status"
                @click="filters.status = ''; applyFilters()"
                class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full flex items-center gap-1"
              >
                {{ filters.status === 'reviewed' ? 'Reviewed' : 'Pending' }} <XMarkIcon class="w-3 h-3" />
              </button>
              <button 
                @click="clearFilters"
                class="text-sm text-red-600 hover:text-red-700 font-medium"
              >
                Clear All
              </button>
            </div>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Average Rating by Section -->
          <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm">
            <h3 class="text-md font-bold text-gray-800 mb-4 flex items-center gap-2">
              <ChartBarIcon class="w-5 h-5 text-blue-600" />
              Rating by Section
            </h3>
            <div class="h-64">
              <Bar :data="sectionRatingData" :options="barChartOptions" />
            </div>
          </div>

          <!-- Feedback Over Time -->
          <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-sm">
            <h3 class="text-md font-bold text-gray-800 mb-4 flex items-center gap-2">
              <ArrowTrendingUpIcon class="w-5 h-5 text-green-600" />
              Feedback Trend
            </h3>
            <div class="h-64">
              <Line :data="feedbackTrendData" :options="lineChartOptions" />
            </div>
          </div>
        </section>

        <!-- Action Buttons -->
        <section class="flex flex-wrap items-center justify-between gap-4">
          <!-- Pagination Info -->
          <div class="flex items-center gap-2">
            <span class="text-sm text-slate-500">
              Showing {{ paginationStart }}-{{ paginationEnd }} of {{ totalFeedback }}
            </span>
            <select 
              v-model="filters.perPage"
              @change="applyFilters"
              class="px-2 py-1 bg-slate-50 border border-slate-200 rounded-lg text-sm"
            >
              <option :value="10">10 per page</option>
              <option :value="25">25 per page</option>
              <option :value="50">50 per page</option>
              <option :value="100">100 per page</option>
            </select>
          </div>
        </section>

        <!-- Feedback Table -->
        <section class="bg-white rounded-2xl border border-slate-200/50 shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
                <tr>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">
                    <button @click="sortBy('student_name')" class="flex items-center gap-1 hover:text-blue-600">
                      Student
                      <ArrowsUpDownIcon class="w-4 h-4" />
                    </button>
                  </th>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">
                    <button @click="sortBy('grade_level')" class="flex items-center gap-1 hover:text-blue-600">
                      Grade
                      <ArrowsUpDownIcon class="w-4 h-4" />
                    </button>
                  </th>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">
                    <button @click="sortBy('section_name')" class="flex items-center gap-1 hover:text-blue-600">
                      Section
                      <ArrowsUpDownIcon class="w-4 h-4" />
                    </button>
                  </th>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">
                    <button @click="sortBy('rating')" class="flex items-center gap-1 hover:text-blue-600">
                      Rating
                      <ArrowsUpDownIcon class="w-4 h-4" />
                    </button>
                  </th>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">Feedback</th>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">
                    <button @click="sortBy('created_at')" class="flex items-center gap-1 hover:text-blue-600">
                      Date
                      <ArrowsUpDownIcon class="w-4 h-4" />
                    </button>
                  </th>
                  <th class="px-4 py-3 text-left text-sm font-bold text-gray-700">Status</th>
                  <th v-if="canModerate" class="px-4 py-3 text-left text-sm font-bold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="feedback in paginatedFeedback" 
                  :key="feedback.id"
                  class="hover:bg-blue-50/50 transition-colors border-b border-slate-100"
                >
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-sm font-bold">
                        {{ getInitials(feedback.student_name) }}
                      </div>
                      <div>
                        <p class="font-medium text-gray-800">{{ feedback.is_anonymous ? 'Anonymous' : feedback.student_name }}</p>
                        <p v-if="!feedback.is_anonymous" class="text-xs text-slate-500">@{{ feedback.username }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-4 py-3">
                    <span class="px-2 py-1 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium">
                      Grade {{ feedback.grade_level }}
                    </span>
                  </td>
                  <td class="px-4 py-3">
                    <span class="font-medium text-gray-800">{{ feedback.section_name }}</span>
                  </td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-1">
                      <svg v-for="star in 5" :key="star" class="w-4 h-4 fill-current" :class="star <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                      <span class="ml-1 text-sm text-slate-600">({{ feedback.rating }})</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 max-w-md">
                    <p class="text-sm text-gray-600">{{ feedback.feedback_text || 'No feedback text provided.' }}</p>
                  </td>
                  <td class="px-4 py-3">
                    <span class="text-sm text-slate-600">{{ formatDate(feedback.created_at) }}</span>
                  </td>
                  <td class="px-4 py-3">
                    <span 
                      :class="[
                        'px-2 py-1 rounded-lg text-xs font-medium',
                        feedback.status === 'reviewed' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                      ]"
                    >
                      {{ feedback.status === 'reviewed' ? 'Reviewed' : 'Pending' }}
                    </span>
                  </td>
                  <td v-if="canModerate" class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <!-- View Details -->
                      <button 
                        @click="viewFeedback(feedback)"
                        class="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="View Details"
                      >
                        <EyeIcon class="w-4 h-4" />
                      </button>

                      <!-- Edit -->
                      <button 
                        @click="editFeedback(feedback)"
                        class="p-1.5 text-amber-600 hover:bg-amber-50 rounded-lg transition-colors"
                        title="Edit"
                      >
                        <PencilIcon class="w-4 h-4" />
                      </button>

                      <!-- Mark Reviewed -->
                      <button 
                        v-if="feedback.status !== 'reviewed'"
                        @click="markAsReviewed(feedback.id)"
                        class="p-1.5 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        title="Mark as Reviewed"
                      >
                        <CheckCircleIcon class="w-4 h-4" />
                      </button>

                      <!-- Delete -->
                      <button 
                        @click="confirmDelete(feedback)"
                        class="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete"
                      >
                        <TrashIcon class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="paginatedFeedback.length === 0">
                  <td :colspan="canModerate ? 8 : 7" class="px-4 py-12 text-center">
                    <div class="text-6xl mb-4">📭</div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">No Feedback Found</h3>
                    <p class="text-gray-500">No feedback matches your current filters.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="px-4 py-3 border-t border-slate-100 flex items-center justify-between">
            <button 
              @click="prevPage"
              :disabled="currentPage === 1"
              class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <div class="flex items-center gap-1">
              <button 
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'w-8 h-8 rounded-lg text-sm font-medium transition-colors',
                  page === currentPage 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-600 hover:bg-slate-100'
                ]"
              >
                {{ page }}
              </button>
            </div>
            <button 
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </section>
        </div>
      </main>

    <!-- View Feedback Modal -->
    <div v-if="showViewModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">Feedback Details</h3>
          <button @click="showViewModal = false" class="text-gray-400 hover:text-gray-600">
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>
        
        <div v-if="selectedFeedback" class="space-y-4">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold">
              {{ getInitials(selectedFeedback.student_name) }}
            </div>
            <div>
              <p class="font-semibold text-gray-800">{{ selectedFeedback.is_anonymous ? 'Anonymous' : selectedFeedback.student_name }}</p>
              <p class="text-sm text-slate-500">Grade {{ selectedFeedback.grade_level }} • {{ selectedFeedback.section_name }}</p>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <span class="text-sm text-slate-500">Rating:</span>
            <div class="flex">
              <svg v-for="star in 5" :key="star" class="w-5 h-5" :class="star <= selectedFeedback.rating ? 'text-yellow-400' : 'text-gray-300'" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </div>
          </div>

          <div>
            <p class="text-sm text-slate-500 mb-1">Feedback:</p>
            <p class="text-gray-700 bg-slate-50 p-3 rounded-lg whitespace-pre-wrap">{{ selectedFeedback.feedback_text || 'No feedback text provided.' }}</p>
          </div>

          <div class="flex items-center justify-between text-sm">
            <span class="text-slate-500">Submitted: {{ formatDate(selectedFeedback.created_at) }}</span>
            <span :class="[
              'px-2 py-1 rounded-lg text-xs font-medium',
              selectedFeedback.status === 'reviewed' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
            ]">
              {{ selectedFeedback.status === 'reviewed' ? 'Reviewed' : 'Pending' }}
            </span>
          </div>

          <!-- Internal Notes (EduOffice Only) -->
          <div v-if="canModerate">
            <label class="block text-sm text-slate-500 mb-1">Internal Notes:</label>
            <textarea 
              v-model="internalNotes"
              rows="2"
              placeholder="Add internal notes..."
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button 
            @click="showViewModal = false"
            class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg font-medium hover:bg-slate-200"
          >
            Close
          </button>
          <button 
            v-if="canModerate && selectedFeedback?.status !== 'reviewed'"
            @click="markAsReviewed(selectedFeedback?.id); showViewModal = false"
            class="px-4 py-2 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600"
          >
            Mark as Reviewed
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Feedback Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">Edit Feedback</h3>
          <button @click="showEditModal = false" class="text-gray-400 hover:text-gray-600">
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>
        
        <div v-if="selectedFeedback" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Rating</label>
            <div class="flex items-center gap-2">
              <button 
                v-for="star in 5" 
                :key="star"
                @click="editForm.rating = star"
                class="transform transition-all duration-200 hover:scale-110"
              >
                <svg 
                  :class="star <= editForm.rating ? 'text-yellow-400' : 'text-gray-300'"
                  class="w-8 h-8" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Feedback Text</label>
            <textarea 
              v-model="editForm.feedback_text"
              rows="4"
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Internal Notes</label>
            <textarea 
              v-model="editForm.internal_notes"
              rows="2"
              placeholder="Add internal notes..."
              class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button 
            @click="showEditModal = false"
            class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg font-medium hover:bg-slate-200"
          >
            Cancel
          </button>
          <button 
            @click="saveEdit"
            :disabled="isSaving"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50"
          >
            {{ isSaving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <div class="text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <ExclamationTriangleIcon class="w-8 h-8 text-red-600" />
          </div>
          <h3 class="text-lg font-bold text-gray-800 mb-2">Delete Feedback?</h3>
          <p class="text-gray-600 mb-6">This action cannot be undone. Are you sure you want to delete this feedback?</p>
          
          <div class="flex justify-center gap-3">
            <button 
              @click="showDeleteModal = false"
              class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg font-medium hover:bg-slate-200"
            >
              Cancel
            </button>
            <button 
              @click="deleteFeedback"
              :disabled="isDeleting"
              class="px-4 py-2 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 disabled:opacity-50"
            >
              {{ isDeleting ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast">
      <div v-if="toast.show" class="fixed bottom-4 right-4 z-50">
        <div :class="[
          'px-6 py-4 rounded-xl shadow-lg flex items-center gap-3',
          toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        ]">
          <CheckCircleIcon v-if="toast.type === 'success'" class="w-6 h-6" />
          <ExclamationCircleIcon v-else class="w-6 h-6" />
          <span class="font-medium">{{ toast.message }}</span>
          <button @click="toast.show = false" class="ml-2">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Bar, Line } from 'vue-chartjs'
import {
  ChatBubbleLeftRightIcon,
  StarIcon,
  CalendarIcon,
  EyeSlashIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  ChartBarIcon,
  ArrowTrendingUpIcon,
  DocumentArrowDownIcon,
  PrinterIcon,
  ArrowsUpDownIcon,
  EyeIcon,
  PencilIcon,
  CheckCircleIcon,
  TrashIcon,
  ExclamationTriangleIcon,
  ExclamationCircleIcon,
  HomeIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon as ChatIcon
} from '@heroicons/vue/24/outline'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default {
  name: 'FeedbackDashboard',
  components: {
    Bar,
    Line,
    ChatBubbleLeftRightIcon,
    StarIcon,
    CalendarIcon,
    EyeSlashIcon,
    MagnifyingGlassIcon,
    XMarkIcon,
    ChartBarIcon,
    ArrowTrendingUpIcon,
    DocumentArrowDownIcon,
    PrinterIcon,
    ArrowsUpDownIcon,
    EyeIcon,
    PencilIcon,
    CheckCircleIcon,
    TrashIcon,
    ExclamationTriangleIcon,
    ExclamationCircleIcon,
    HomeIcon,
    DocumentTextIcon,
    UserGroupIcon,
    ChatIcon
  },
  setup() {
    const router = useRouter()
    const route = useRoute()

    // State
    const isLoading = ref(true)
    const currentPage = ref(1)
    const sortField = ref('created_at')
    const sortOrder = ref('desc')
    const internalNotes = ref('')

    // Role and user info
    const userRole = ref('')
    const userName = ref('')
    const username = ref('')
    const teacherSubject = ref('')
    const teacherGrade = ref('')

    // Filters
    const filters = ref({
      grade: '',
      section: '',
      rating: '',
      startDate: '',
      search: '',
      status: '',
      perPage: 10
    })

    // Stats
    const stats = ref({
      totalFeedback: 0,
      averageRating: 0,
      thisWeek: 0,
      anonymousCount: 0,
      anonymousPercent: 0
    })

    // Feedback data
    const allFeedback = ref([])
    const availableSectionsList = ref(['Chemistry', 'Physics', 'Mathematics', 'English', 'Biology', 'History', 'Geography', 'Economics', 'Civics'])
    const availableGrades = ref([9, 10, 11, 12])

    // Modal states
    const showViewModal = ref(false)
    const showEditModal = ref(false)
    const showDeleteModal = ref(false)
    const selectedFeedback = ref(null)
    const editForm = ref({
      rating: 0,
      feedback_text: '',
      internal_notes: ''
    })
    const isSaving = ref(false)
    const isDeleting = ref(false)

    // Toast
    const toast = ref({
      show: false,
      message: '',
      type: 'success'
    })

    // Computed properties
const canModerate = computed(() => {
  return userRole.value === 'teacher' || userRole.value === 'eduoffice' || userRole.value === 'admin'
})

    const canViewAllGrades = computed(() => {
      // Teachers don't need client grade filter (server handles)
      // Eduoffice sees all
      return userRole.value === 'eduoffice' || userRole.value === 'admin'
    })

    const userAvatar = computed(() => {
      return `https://api.dicebear.com/7.x/avataaars/svg?seed=${userName.value}`
    })

    const roleBadgeText = computed(() => {
      if (userRole.value === 'teacher') return 'Teacher'
      if (userRole.value === 'eduoffice') return 'Education Office'
      if (userRole.value === 'admin') return 'Admin'
      return 'User'
    })

    const roleBadgeClass = computed(() => {
      if (userRole.value === 'teacher') return 'bg-blue-100 text-blue-700'
      if (userRole.value === 'eduoffice') return 'bg-purple-100 text-purple-700'
      if (userRole.value === 'admin') return 'bg-red-100 text-red-700'
      return 'bg-gray-100 text-gray-700'
    })

    const userRoleDisplay = computed(() => {
      if (userRole.value === 'teacher') return 'Teacher'
      if (userRole.value === 'eduoffice') return 'Education Office'
      if (userRole.value === 'admin') return 'Administrator'
      return 'User'
    })

    const pendingCount = computed(() => {
      return allFeedback.value.filter(f => f.status === 'pending').length
    })

    const hasActiveFilters = computed(() => {
      return filters.value.grade || filters.value.section || filters.value.rating || filters.value.startDate || filters.value.search || filters.value.status
    })

    const filteredFeedback = computed(() => {
      let result = [...allFeedback.value]

      // Server handles role-based filtering. Client-side filters only for additional filtering
      // Apply additional filters (grade filter now works for eduoffice only)
      if (filters.value.grade) {
        result = result.filter(f => f.grade_level === parseInt(filters.value.grade))
      }
      if (filters.value.section) {
        result = result.filter(f => f.section_name === filters.value.section)
      }
      if (filters.value.rating) {
        result = result.filter(f => f.rating === parseInt(filters.value.rating))
      }
      if (filters.value.startDate) {
        result = result.filter(f => new Date(f.created_at) >= new Date(filters.value.startDate))
      }
      if (filters.value.status) {
        result = result.filter(f => f.status === filters.value.status)
      }
      if (filters.value.search) {
        const search = filters.value.search.toLowerCase()
        result = result.filter(f => 
          !f.is_anonymous && f.student_name?.toLowerCase().includes(search)
        )
      }

      // Sorting
      result.sort((a, b) => {
        let aVal = a[sortField.value]
        let bVal = b[sortField.value]
        
        if (sortField.value === 'created_at') {
          aVal = new Date(aVal).getTime()
          bVal = new Date(bVal).getTime()
        }
        
        if (sortOrder.value === 'asc') {
          return aVal > bVal ? 1 : -1
        }
        return aVal < bVal ? 1 : -1
      })

      return result
    })

    const totalFeedback = computed(() => filteredFeedback.value.length)
    const totalPages = computed(() => Math.ceil(totalFeedback.value / filters.value.perPage))
    
    const paginatedFeedback = computed(() => {
      const start = (currentPage.value - 1) * filters.value.perPage
      const end = start + filters.value.perPage
      return filteredFeedback.value.slice(start, end)
    })

    const paginationStart = computed(() => {
      if (totalFeedback.value === 0) return 0
      return (currentPage.value - 1) * filters.value.perPage + 1
    })

    const paginationEnd = computed(() => {
      return Math.min(currentPage.value * filters.value.perPage, totalFeedback.value)
    })

    const visiblePages = computed(() => {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
      let end = Math.min(totalPages.value, start + maxVisible - 1)
      
      if (end - start < maxVisible - 1) {
        start = Math.max(1, end - maxVisible + 1)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    })

    // Chart data - Rating by Section
    const sectionRatingData = computed(() => {
      // Use filtered feedback for charts
      let feedbackData = [...filteredFeedback.value]

      const sections = [...new Set(feedbackData.map(f => f.section_name))]
      const ratings = sections.map(section => {
        const sectionFeedback = feedbackData.filter(f => f.section_name === section)
        const sum = sectionFeedback.reduce((acc, f) => acc + f.rating, 0)
        return sectionFeedback.length ? (sum / sectionFeedback.length).toFixed(1) : 0
      })

      return {
        labels: sections,
        datasets: [{
          label: 'Average Rating',
          data: ratings,
          backgroundColor: [
            'rgba(59, 130, 246, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(239, 68, 68, 0.8)',
            'rgba(236, 72, 153, 0.8)',
            'rgba(20, 184, 166, 0.8)',
            'rgba(249, 115, 22, 0.8)'
          ],
          borderRadius: 6,
          barThickness: 24
        }]
      }
    })

    const feedbackTrendData = computed(() => {
      const last7Days = []
      for (let i = 6; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        last7Days.push(date.toISOString().split('T')[0])
      }

      const counts = last7Days.map(date => {
        return allFeedback.value.filter(f => 
          f.created_at.startsWith(date)
        ).length
      })

      return {
        labels: last7Days.map(d => new Date(d).toLocaleDateString('en-US', { weekday: 'short' })),
        datasets: [{
          label: 'Feedback Count',
          data: counts,
          fill: true,
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderColor: '#10b981',
          tension: 0.4,
          pointBackgroundColor: '#10b981',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5
        }]
      }
    })

    // Chart options
    const barChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true, max: 5 }
      }
    }

    const lineChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { grid: { display: false } },
        y: { beginAtZero: true }
      }
    }

    // Menu items
    const getDashboardRoute = () => {
      if (userRole.value === 'teacher') return '/teacher_dashboard'
      if (userRole.value === 'eduoffice') return '/education_office_dashboard'
      return '/admin_dashboard'
    }

    const menuItems = computed(() => {
      const items = [
        { label: 'Overview', icon: HomeIcon, to: getDashboardRoute() }
      ]

      if (userRole.value === 'teacher') {
        items.push(
          { label: 'Student Performance', icon: ChartBarIcon, to: '/teacher/student-performance' },
          { label: 'Subject Leaderboard', icon: StarIcon, to: '/teacher/subject-leaderboard' },
          { label: 'Student Feedback', icon: ChatBubbleLeftRightIcon, to: '/teacher/feedback' }
        )
      } else if (userRole.value === 'eduoffice' || userRole.value === 'admin') {
        items.push(
          { label: 'All Feedback', icon: ChatBubbleLeftRightIcon, to: '/eduoffice/feedback' }
        )
      }

      return items
    })

    // Methods
    const getRoleTitle = () => {
      if (userRole.value === 'teacher') return `Teacher - ${teacherSubject.value || 'All Subjects'} (Grade ${teacherGrade.value || 'All'})`
if (userRole.value === 'eduoffice') return 'All Grades View'
      if (userRole.value === 'admin') return 'Administrator - All Grades View'
      return 'User View'
    }

    const getInitials = (name) => {
      if (!name) return '?'
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    }

    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      })
    }

    const isActive = (path) => {
      return route.path === path
    }

    const applyFilters = () => {
      currentPage.value = 1
      loadFeedback()
    }

    const clearFilters = () => {
      filters.value = {
        grade: '',
        section: '',
        rating: '',
        startDate: '',
        search: '',
        status: '',
        perPage: 10
      }
      currentPage.value = 1
      loadFeedback()
    }

    let searchTimeout = null
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        applyFilters()
      }, 300)
    }

    const sortBy = (field) => {
      if (sortField.value === field) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortField.value = field
        sortOrder.value = 'desc'
      }
    }

    const prevPage = () => {
      if (currentPage.value > 1) currentPage.value--
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++
    }

    const goToPage = (page) => {
      currentPage.value = page
    }

    // Go back to the appropriate dashboard based on user role
    const goBack = () => {
      if (userRole.value === 'teacher') {
        router.push('/teacher_dashboard')
      } else if (userRole.value === 'eduoffice') {
        router.push('/education_office_dashboard')
      } else {
        router.push('/admin_dashboard')
      }
    }

    // Actions
    const viewFeedback = (feedback) => {
      selectedFeedback.value = feedback
      internalNotes.value = feedback.internal_notes || ''
      showViewModal.value = true
    }

    const editFeedback = (feedback) => {
      selectedFeedback.value = feedback
      editForm.value = {
        rating: feedback.rating,
        feedback_text: feedback.feedback_text,
        internal_notes: feedback.internal_notes || ''
      }
      showEditModal.value = true
    }

    const confirmDelete = (feedback) => {
      selectedFeedback.value = feedback
      showDeleteModal.value = true
    }

    const markAsReviewed = async (id) => {
      try {
        const token = getToken()
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/moderate/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            status: 'reviewed',
            internal_notes: internalNotes.value 
          })
        })

        if (response.ok) {
          showToast('Feedback marked as reviewed', 'success')
          loadFeedback()
        } else {
          showToast('Failed to update feedback', 'error')
        }
      } catch (error) {
        console.error('Error updating feedback:', error)
        showToast('Error updating feedback', 'error')
      }
    }

    const saveEdit = async () => {
      isSaving.value = true
      try {
        const token = getToken()
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/moderate/${selectedFeedback.value.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            rating: editForm.value.rating,
            feedback_text: editForm.value.feedback_text,
            internal_notes: editForm.value.internal_notes
          })
        })

        if (response.ok) {
          showToast('Feedback updated successfully', 'success')
          showEditModal.value = false
          loadFeedback()
        } else {
          showToast('Failed to update feedback', 'error')
        }
      } catch (error) {
        console.error('Error saving feedback:', error)
        showToast('Error saving feedback', 'error')
      } finally {
        isSaving.value = false
      }
    }

    const deleteFeedback = async () => {
      isDeleting.value = true
      try {
        const token = getToken()
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/moderate/${selectedFeedback.value.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          showToast('Feedback deleted successfully', 'success')
          showDeleteModal.value = false
          loadFeedback()
        } else {
          showToast('Failed to delete feedback', 'error')
        }
      } catch (error) {
        console.error('Error deleting feedback:', error)
        showToast('Error deleting feedback', 'error')
      } finally {
        isDeleting.value = false
      }
    }

    const exportReport = (format) => {
      showToast(`Exporting to ${format.toUpperCase()}...`, 'success')
      console.log('Exporting to', format)
    }

    const printReport = () => {
      window.print()
    }

    const showToast = (message, type = 'success') => {
      toast.value = { show: true, message, type }
      setTimeout(() => {
        toast.value.show = false
      }, 3000)
    }

    const getToken = () => {
      console.log('Getting token for role:', userRole.value);
      let token;
      if (userRole.value === 'admin') {
        token = localStorage.getItem('admin_token') || sessionStorage.getItem('admin_token');
      } else {
        token = localStorage.getItem('token');
      }
      console.log('Token found:', !!token);
      return token;
    }

    const loadFeedback = async () => {
      isLoading.value = true
      try {
        const token = getToken()
        
        // Build query params
        const params = new URLSearchParams()
        
        // Let server handle teacher filtering. Client ?grade= only for additional eduoffice filters
        if (filters.value.grade) {
          params.append('grade', filters.value.grade)
        }
        
        if (filters.value.section) params.append('section', filters.value.section)
        if (filters.value.rating) params.append('rating', filters.value.rating)
        if (filters.value.status) params.append('status', filters.value.status)
        params.append('page', currentPage.value)
        params.append('per_page', 100) // Get more data for stats
        
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/feedback?${params}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const data = await response.json()
          console.log('Feedback API response:', data);
          allFeedback.value = data.feedback || data || []
          stats.value = data.stats || stats.value; // Use backend stats if available
          
          // Calculate stats based on filtered data
          calculateStats()
        } else {
          const errorText = await response.text();
          console.error('Feedback API failed:', response.status, errorText);
          showToast(`Server error: ${response.status} - ${errorText.substring(0, 100)}`, 'error');
          allFeedback.value = [];
        }
      } catch (error) {
        console.error('Error loading feedback:', error)
        showToast('Network error loading feedback. Please check server.', 'error');
        allFeedback.value = [];
      } finally {
        isLoading.value = false
      }
    }

    // Load sections from API
    const loadSections = async () => {
      try {
        const token = getToken()
        const response = await fetch('http://127.0.0.1:8000/api/section-feedback/sections-list', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          const data = await response.json()
          if (data && Array.isArray(data) && data.length > 0) {
            // Transform API response to simpler format for dropdown
            availableSectionsList.value = data.map(section => ({
              id: section.id,
              name: section.name
            }))
          }
        }
      } catch (error) {
        console.error('Error loading sections:', error)
        // Keep default sections on error
      }
    }

    const calculateStats = () => {
      const data = filteredFeedback.value
      stats.value.totalFeedback = data.length
      
      if (data.length) {
        const totalRating = data.reduce((sum, f) => sum + f.rating, 0)
        stats.value.averageRating = data.length ? (totalRating / data.length).toFixed(1) : 0
        stats.value.anonymousCount = data.filter(f => f.is_anonymous).length
        stats.value.anonymousPercent = Math.round((stats.value.anonymousCount / data.length) * 100)
        
        // This week
        const weekAgo = new Date()
        weekAgo.setDate(weekAgo.getDate() - 7)
        stats.value.thisWeek = data.filter(f => new Date(f.created_at) >= weekAgo).length
      } else {
        stats.value.averageRating = 0
        stats.value.anonymousCount = 0
        stats.value.anonymousPercent = 0
        stats.value.thisWeek = 0
      }
    }

          const loadMockData = () => {
      console.warn('Using mock data - backend API failed');
      const sections = ['Chemistry', 'Physics', 'Mathematics', 'English', 'Biology']
      const names = ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams', 'David Brown', 'Emily Davis', 'Chris Wilson', 'Amanda Taylor']
      
      allFeedback.value = Array.from({ length: 25 }, (_, i) => ({
        id: i + 1,
        student_name: names[Math.floor(Math.random() * names.length)],
        username: `student${i + 1}`,
        grade_level: [9, 10, 11, 12][Math.floor(Math.random() * 4)],
        section_name: sections[Math.floor(Math.random() * sections.length)],
        rating: Math.floor(Math.random() * 5) + 1,
        feedback_text: ['Great teacher! Very helpful lessons and explanations.', 'Could improve on giving more examples during class.', 'Excellent explanations and very patient.', 'Needs more practice problems in class.', 'Very engaging lessons, I learned a lot!'][Math.floor(Math.random() * 5)],
        is_anonymous: Math.random() > 0.5,
        status: Math.random() > 0.3 ? 'reviewed' : 'pending',
        created_at: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
        internal_notes: ''
      }))

      calculateStats()
    }

    const loadUserProfile = async () => {
      userRole.value = localStorage.getItem('role') || ''
      username.value = localStorage.getItem('username') || ''

      // Get teacher info if teacher
      if (userRole.value === 'teacher') {
        try {
          const token = localStorage.getItem('token')
          const response = await fetch(`http://127.0.0.1:8000/api/users/profile/${username.value}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          })
          if (response.ok) {
            const data = await response.json()
            userName.value = data.full_name || username.value
            teacherSubject.value = data.subject_assigned || ''
            teacherGrade.value = data.teaching_grade || ''
          } else {
            userName.value = username.value
          }
        } catch (error) {
          console.error('Error loading teacher profile:', error)
          userName.value = username.value
        }
      } else {
        userName.value = username.value || 'Admin'
      }

      // Check if role is admin/eduoffice from sessionStorage
      const adminUser = sessionStorage.getItem('admin_user')
      if (adminUser) {
        try {
          const user = JSON.parse(adminUser)
          userName.value = user.full_name || user.email?.split('@')[0] || 'Admin'
          
          // Check role
          const storedRole = localStorage.getItem('role')
          if (storedRole === 'eduoffice' || storedRole === 'admin') {
            userRole.value = storedRole
          } else if (!userRole.value) {
            userRole.value = 'admin' // Default for admin routes
          }
        } catch (e) {
          console.error('Error parsing admin user:', e)
        }
      }

      // If still no role, default based on route
      if (!userRole.value) {
        if (route.path.includes('teacher')) {
          userRole.value = 'teacher'
        } else if (route.path.includes('eduoffice')) {
          userRole.value = 'eduoffice'
        } else {
          userRole.value = 'admin'
        }
      }
    }

    // Watch for filter changes to recalculate stats
    watch(filters, () => {
      calculateStats()
    }, { deep: true })

    onMounted(async () => {
      await loadUserProfile()
      await Promise.all([
        loadFeedback(),
        loadSections()
      ])
    })

    return {
      // State
      isLoading,
      currentPage,
      sortField,
      sortOrder,
      filters,
      stats,
      allFeedback,
      availableSectionsList,
      availableGrades,
      userRole,
      userName,
      username,
      teacherSubject,
      teacherGrade,
      
      // Modal states
      showViewModal,
      showEditModal,
      showDeleteModal,
      selectedFeedback,
      editForm,
      isSaving,
      isDeleting,
      internalNotes,
      toast,

      // Computed
      canModerate,
      canViewAllGrades,
      userAvatar,
      roleBadgeText,
      roleBadgeClass,
      userRoleDisplay,
      pendingCount,
      hasActiveFilters,
      filteredFeedback,
      totalFeedback,
      totalPages,
      paginatedFeedback,
      paginationStart,
      paginationEnd,
      visiblePages,
      sectionRatingData,
      feedbackTrendData,
      menuItems,

      // Chart options
      barChartOptions,
      lineChartOptions,

      // Methods
      getRoleTitle,
      getInitials,
      formatDate,
      isActive,
      applyFilters,
      clearFilters,
      debouncedSearch,
      sortBy,
      prevPage,
      nextPage,
      goToPage,
      goBack,
      viewFeedback,
      editFeedback,
      confirmDelete,
      markAsReviewed,
      saveEdit,
      deleteFeedback,
      exportReport,
      printReport
    }
  }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Custom scrollbar */
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

@media print {
  .no-print {
    display: none !important;
  }
}
</style>

