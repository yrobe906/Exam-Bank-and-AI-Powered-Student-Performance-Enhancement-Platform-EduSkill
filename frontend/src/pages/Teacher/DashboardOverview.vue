<!-- DashboardOverview.vue -->
<template>
  <div class="space-y-6 md:space-y-8">
    <!-- Stats Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
      <!-- Total Students Card -->
      <div class="group bg-white/90 backdrop-blur rounded-2xl md:rounded-3xl p-6 md:p-8 border border-slate-200/50 shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-500">
        <div class="flex items-center justify-between mb-4 md:mb-6">
          <div class="p-3 md:p-4 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl md:rounded-2xl shadow-2xl group-hover:scale-110 transition-all">
            <UserGroupIcon class="w-5 h-5 md:w-7 md:h-7 text-white" />
          </div>
          <span class="text-xs font-bold px-2 md:px-3 py-1 md:py-1.5 bg-purple-100 text-purple-800 rounded-lg md:rounded-xl border border-purple-200">
            Grade {{ teacher.teaching_grade }}
          </span>
        </div>
        <div class="text-3xl md:text-4xl lg:text-5xl font-black text-slate-900 mb-1 md:mb-2 leading-tight">{{ stats.totalStudents }}</div>
        <p class="text-sm md:text-base text-slate-600 font-medium">Total Students</p>
        <div class="mt-3 md:mt-4 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div class="h-full bg-purple-500 rounded-full" :style="{ width: Math.min((stats.totalStudents / 40) * 100, 100) + '%' }"></div>
        </div>
      </div>

      <!-- Active Students Card -->
      <div class="group bg-white/90 backdrop-blur rounded-2xl md:rounded-3xl p-6 md:p-8 border border-slate-200/50 shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-500">
        <div class="flex items-center justify-between mb-4 md:mb-6">
          <div class="p-3 md:p-4 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl md:rounded-2xl shadow-2xl group-hover:scale-110 transition-all">
            <ChartBarIcon class="w-5 h-5 md:w-7 md:h-7 text-white" />
          </div>
          <span class="text-xs font-bold px-2 md:px-3 py-1 md:py-1.5 bg-emerald-100 text-emerald-800 rounded-lg md:rounded-xl border border-emerald-200">
            This Week
          </span>
        </div>
        <div class="text-3xl md:text-4xl lg:text-5xl font-black text-slate-900 mb-1 md:mb-2 leading-tight">{{ stats.activeThisWeek }}</div>
        <p class="text-sm md:text-base text-slate-600 font-medium">Active Students</p>
        <div class="mt-3 md:mt-4 flex items-center gap-2">
          <span class="text-xs md:text-sm text-emerald-600 font-semibold flex items-center gap-1">
            <ArrowTrendingUpIcon class="w-3 h-3" />
            ↑ 12%
          </span>
          <span class="text-xs text-slate-400">from last week</span>
        </div>
      </div>

      <!-- Avg Readiness Card -->
      <div class="group bg-white/90 backdrop-blur rounded-2xl md:rounded-3xl p-6 md:p-8 border border-slate-200/50 shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-500 sm:col-span-2 lg:col-span-1">
        <div class="flex items-center justify-between mb-4 md:mb-6">
          <div class="p-3 md:p-4 bg-gradient-to-br from-amber-500 via-orange-500 to-red-500 rounded-xl md:rounded-2xl shadow-2xl group-hover:scale-110 transition-all">
            <SparklesIcon class="w-5 h-5 md:w-7 md:h-7 text-white" />
          </div>
        </div>
        <div class="text-3xl md:text-4xl lg:text-5xl font-black text-slate-900 mb-1 md:mb-2 leading-tight">{{ stats.avgReadiness }}%</div>
        <p class="text-sm md:text-base text-slate-600 font-medium">Avg Readiness</p>
        <div class="mt-3 md:mt-4 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div class="h-full bg-gradient-to-r from-amber-500 to-orange-500 rounded-full transition-all duration-1000" 
               :style="{ width: Math.min(stats.avgReadiness, 100) + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Library & Resources -->
    <div class="bg-white/90 backdrop-blur rounded-2xl md:rounded-3xl border border-slate-200/50 shadow-xl p-6 md:p-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6 md:mb-8 pb-4 md:pb-6 border-b border-slate-200">
        <div class="flex items-center gap-3 md:gap-4">
          <div class="p-2 md:p-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl md:rounded-2xl shadow-xl">
            <BookOpenIcon class="w-5 h-5 md:w-6 md:h-6 text-white" />
          </div>
          <div>
            <h3 class="text-xl md:text-2xl font-bold text-slate-900">Library & Resources</h3>
            <p class="text-xs md:text-sm text-slate-600">Your teaching materials overview</p>
          </div>
        </div>
        <button class="px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 rounded-xl hover:bg-indigo-100 transition-all self-start md:self-auto">
          View All →
        </button>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 md:gap-6">
        <!-- Notes -->
        <div class="group text-center p-4 md:p-6 rounded-xl md:rounded-2xl hover:shadow-xl transition-all border border-slate-200/50 hover:border-indigo-200 bg-indigo-50/30">
          <DocumentTextIcon class="w-8 h-8 md:w-12 md:h-12 text-indigo-600 mx-auto mb-2 md:mb-4 group-hover:scale-110 transition-transform" />
          <div class="text-xl md:text-3xl font-black text-slate-900 mb-1">{{ resources.notes }}</div>
          <p class="text-xs md:text-sm text-slate-600 font-semibold">Notes</p>
        </div>

        <!-- Slides -->
        <div class="group text-center p-4 md:p-6 rounded-xl md:rounded-2xl hover:shadow-xl transition-all border border-slate-200/50 hover:border-purple-200 bg-purple-50/30">
          <RectangleStackIcon class="w-8 h-8 md:w-12 md:h-12 text-purple-600 mx-auto mb-2 md:mb-4 group-hover:scale-110 transition-transform" />
          <div class="text-xl md:text-3xl font-black text-slate-900 mb-1">{{ resources.slides }}</div>
          <p class="text-xs md:text-sm text-slate-600 font-semibold">Slides</p>
        </div>

        <!-- Videos -->
        <div class="group text-center p-4 md:p-6 rounded-xl md:rounded-2xl hover:shadow-xl transition-all border border-slate-200/50 hover:border-emerald-200 bg-emerald-50/30">
          <VideoCameraIcon class="w-8 h-8 md:w-12 md:h-12 text-emerald-600 mx-auto mb-2 md:mb-4 group-hover:scale-110 transition-transform" />
          <div class="text-xl md:text-3xl font-black text-slate-900 mb-1">{{ resources.videos }}</div>
          <p class="text-xs md:text-sm text-slate-600 font-semibold">Videos</p>
        </div>

        <!-- Books -->
        <div class="group text-center p-4 md:p-6 rounded-xl md:rounded-2xl hover:shadow-xl transition-all border border-slate-200/50 hover:border-amber-200 bg-amber-50/30">
          <BookOpenIcon class="w-8 h-8 md:w-12 md:h-12 text-amber-600 mx-auto mb-2 md:mb-4 group-hover:scale-110 transition-transform" />
          <div class="text-xl md:text-3xl font-black text-slate-900 mb-1">{{ resources.books }}</div>
          <p class="text-xs md:text-sm text-slate-600 font-semibold">Books</p>
        </div>
      </div>

      <!-- Recent Uploads -->
      <div v-if="recentResources.length" class="mt-6 md:mt-8 pt-6 md:pt-8 border-t border-slate-200">
        <h4 class="text-lg md:text-xl font-bold text-slate-900 mb-4 md:mb-6 flex items-center gap-2 md:gap-3">
          <CloudArrowUpIcon class="w-5 h-5 md:w-6 md:h-6 text-emerald-600" />
          Recent Uploads
        </h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
          <div v-for="resource in recentResources.slice(0,3)" :key="resource.id" 
               class="group p-4 md:p-5 rounded-xl md:rounded-2xl border border-slate-200/50 hover:shadow-lg hover:border-emerald-200 bg-emerald-50/30 transition-all">
            <div class="flex items-start gap-3">
              <div class="p-2 bg-emerald-100 rounded-lg group-hover:bg-emerald-200 transition-colors">
                <CloudArrowUpIcon class="w-4 h-4 text-emerald-700" />
              </div>
              <div class="flex-1 min-w-0">
                <h5 class="font-semibold text-slate-900 text-sm md:text-base mb-1 truncate">{{ resource.title }}</h5>
                <span class="inline-block px-2 py-0.5 bg-white text-xs font-medium text-slate-600 rounded-lg border">{{ resource.type }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Empty State for Recent Uploads -->
      <div v-else class="mt-6 md:mt-8 pt-6 md:pt-8 border-t border-slate-200 text-center py-8">
        <CloudArrowUpIcon class="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <p class="text-slate-500">No recent uploads</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import {
  UserGroupIcon,
  ChartBarIcon,
  SparklesIcon,
  BookOpenIcon,
  DocumentTextIcon,
  RectangleStackIcon,
  VideoCameraIcon,
  CloudArrowUpIcon,
  PlusIcon,
  DocumentPlusIcon,
  ChatBubbleLeftRightIcon,
  ArrowTrendingUpIcon
} from '@heroicons/vue/24/outline'

defineProps({
  teacher: {
    type: Object,
    required: true
  },
  stats: {
    type: Object,
    required: true
  },
  resources: {
    type: Object,
    required: true
  },
  recentResources: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
/* Smooth transitions */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Progress bar animations */
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}
</style>