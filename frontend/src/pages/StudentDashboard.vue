<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50/30">
    <!-- Enhanced Header -->
    <HeaderStud @toggle-sidebar="toggleSidebar" />

    <!-- Mobile Overlay -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 bg-black/50 z-40 lg:hidden"
      @click="closeSidebar"
    ></div>

    <!-- Main Content with Independent Scroll -->
    <div class="flex">
      <!-- Fixed Sidebar with Independent Scroll -->
      <div 
        :class="[
          'fixed lg:relative z-50 lg:z-auto transition-transform duration-300 ease-in-out',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
      >
        <div class="h-[calc(100vh-80px)] lg:h-screen overflow-y-auto">
          <SidebarStud @close-sidebar="closeSidebar" />
        </div>
      </div>

      <!-- Main Content Scroll Container -->
      <main class="flex-1 p-4 md:p-8 w-full">
        <div class="h-[calc(100vh-80px)] overflow-y-auto pr-2 md:pr-4 scroll-smooth">
        <!-- Hero Welcome Section -->
        <div class="relative mb-6 md:mb-10 overflow-hidden rounded-2xl md:rounded-3xl shadow-xl md:shadow-2xl">
          <!-- Animated Gradient Background -->
          <div class="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-500 opacity-90"></div>
          <!-- Animated Pattern Overlay -->
          <div class="absolute inset-0 opacity-10 pattern-overlay"></div>
          
          <div class="relative p-4 md:p-8 lg:p-12">
            <div class="flex flex-col md:flex-row md:items-center justify-between">
              <div class="mb-4 md:mb-0 md:mr-8">
                <!-- Animated Greeting -->
                <div class="flex items-center mb-3 md:mb-4">
                  <div class="h-10 w-10 md:h-12 md:w-12 bg-gradient-to-br from-white/30 to-white/10 backdrop-blur-sm rounded-xl md:rounded-2xl flex items-center justify-center mr-3 md:mr-4">
                    <span class="text-xl md:text-2xl">👋</span>
                  </div>
                  <div>
                    
                    <p class="text-white/90 text-xs md:text-sm font-medium">
                      Welcome back, {{ student.full_name }}
                    </p>
                  </div>
                </div>
                
                <!-- Quick Stats -->
                <div class="flex flex-wrap gap-2 md:gap-4 mt-4 md:mt-6">
                  <div class="flex items-center bg-white/20 backdrop-blur-sm rounded-lg md:rounded-xl px-3 md:px-4 py-2">
                    <div class="h-6 md:h-8 w-6 md:w-8 bg-white/30 rounded-lg flex items-center justify-center mr-2 md:mr-3">
                      <ClockIcon class="w-3 h-3 md:w-4 md:h-4 text-white" />
                    </div>
                    <div>
                      <p class="text-white/90 text-xs md:text-sm"> upcoming exams</p>
                    </div>
                  </div>
                  <div class="flex items-center bg-white/20 backdrop-blur-sm rounded-lg md:rounded-xl px-3 md:px-4 py-2">
                    <div class="h-6 md:h-8 w-6 md:w-8 bg-white/30 rounded-lg flex items-center justify-center mr-2 md:mr-3">
                      <ChatBubbleLeftIcon class="w-3 h-3 md:w-4 md:h-4 text-white" />
                    </div>
                    <div>
                      <p class="text-white/90 text-xs md:text-sm"> forum notifications</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- CTA Button -->
              <div class="relative group mt-4 md:mt-0">
                <button class="bg-gradient-to-r from-white to-white/90 text-blue-600 font-bold px-4 md:px-8 py-2 md:py-4 rounded-xl md:rounded-2xl shadow-xl md:shadow-2xl hover:shadow-3xl transition-all duration-500 hover:-translate-y-1 flex items-center justify-center text-sm md:text-base">
                  <span class="mr-2 md:mr-3">🚀</span>
                  Start Learning Journey
                  <span class="ml-2 md:ml-3">→</span>
                </button>
                <div class="absolute -inset-1 bg-gradient-to-r from-white/20 to-white/10 rounded-xl md:rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Performance Dashboard -->
        <div class="mb-8 md:mb-10">
          <!-- Loading State -->
          <div v-if="analyticsLoading" class="flex items-center justify-center h-64">
            <div class="text-center">
              <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p class="text-gray-600">Loading your analytics...</p>
            </div>
          </div>

          <!-- Analytics Content -->
          <div v-else>
            <!-- Page Header -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-4 md:mb-6 gap-3">
              <h2 class="text-xl md:text-2xl lg:text-3xl font-bold text-gray-800 flex items-center">
                <div class="h-8 w-8 md:h-10 md:w-10 bg-gradient-to-br from-blue-100 to-blue-50 rounded-xl flex items-center justify-center mr-3 md:mr-4">
                  <ChartBarIcon class="w-4 h-4 md:w-5 md:h-5 text-blue-600" />
                </div>
                <span class="hidden sm:inline">Performance Dashboard</span>
                <span class="sm:hidden">Dashboard</span>
              </h2>
              <button 
                @click="refreshAnalytics"
                :disabled="analyticsLoading"
                class="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 text-sm md:text-base"
              >
                <ArrowPathIcon class="w-4 h-4 md:w-5 md:h-5 mr-2" :class="{ 'animate-spin': analyticsLoading }" />
                <span class="hidden sm:inline">Refresh</span>
              </button>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
              <!-- Average Score Card -->
              <div class="group relative bg-gradient-to-br from-white to-gray-50 rounded-2xl p-4 md:p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-2">
                <div class="flex items-center justify-between mb-3 md:mb-4">
                  <div class="p-2 md:p-3 rounded-xl bg-gradient-to-br from-green-50 to-emerald-50 shadow-inner">
                    <ChartBarIcon class="w-4 h-4 md:w-6 md:h-6 text-green-600" />
                  </div>
                  <span class="text-xs font-semibold px-2 md:px-3 py-1 rounded-full bg-green-100 text-green-700">
                    Overall
                  </span>
                </div>
                <p class="text-gray-500 text-xs md:text-sm mb-2">Average Score</p>
                <p class="text-2xl md:text-3xl font-bold text-gray-800 mb-2 md:mb-3">{{ analyticsData.average_score || 0 }}%</p>
                <div class="mt-2 md:mt-3 h-1.5 md:h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    class="h-full rounded-full bg-gradient-to-r from-green-500 to-emerald-400" 
                    :style="{ width: (analyticsData.average_score || 0) + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Exams Taken Card -->
              <div class="group relative bg-gradient-to-br from-white to-gray-50 rounded-2xl p-4 md:p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-2">
                <div class="flex items-center justify-between mb-3 md:mb-4">
                  <div class="p-2 md:p-3 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50 shadow-inner">
                    <ClipboardDocumentCheckIcon class="w-4 h-4 md:w-6 md:h-6 text-blue-600" />
                  </div>
                  <span class="text-xs font-semibold px-2 md:px-3 py-1 rounded-full bg-blue-100 text-blue-700">
                    Total
                  </span>
                </div>
                <p class="text-gray-500 text-xs md:text-sm mb-2">Exams Taken</p>
                <p class="text-2xl md:text-3xl font-bold text-gray-800 mb-2 md:mb-3">{{ analyticsData.total_exams_taken || 0 }}</p>
                <p class="text-xs md:text-sm text-gray-500 mt-1 md:mt-2">Across {{ analyticsData.subjects?.length || 0 }} subjects</p>
              </div>



              <!-- Class Rank Card -->
              <div class="group relative bg-gradient-to-br from-white to-gray-50 rounded-2xl p-4 md:p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-2">
                <div class="flex items-center justify-between mb-3 md:mb-4">
                  <div class="p-2 md:p-3 rounded-xl bg-gradient-to-br from-purple-50 to-violet-50 shadow-inner">
                    <TrophyIcon class="w-4 h-4 md:w-6 md:h-6 text-purple-600" />
                  </div>
                  <span class="text-xs font-semibold px-2 md:px-3 py-1 rounded-full bg-purple-100 text-purple-700">
                    Ranking
                  </span>
                </div>
                <p class="text-gray-500 text-xs md:text-sm mb-2">Class Rank</p>
                <p class="text-2xl md:text-3xl font-bold text-gray-800 mb-2 md:mb-3">#{{ analyticsData.class_rank || '--' }}</p>
                <p class="text-xs md:text-sm text-gray-500 mt-1 md:mt-2">Top {{ analyticsData.class_rank ? Math.round((1 - analyticsData.class_rank/100)*100) : 0 }}%</p>
              </div>
            </div>

            <!-- AI Recommendations Section -->
            <div v-if="analyticsData.recent_recommendations?.length > 0" class="mb-6 md:mb-8">
              <h3 class="text-lg md:text-xl font-bold text-gray-800 mb-4 md:mb-6 flex items-center">
                <span class="mr-2 md:mr-3">🤖</span>
                AI Recommendations
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
                <div 
                  v-for="(rec, index) in analyticsData.recent_recommendations" 
                  :key="rec.title + index"
                  class="p-4 md:p-5 rounded-xl md:rounded-2xl border transition-all hover:shadow-lg cursor-pointer"
                  :class="{
                    'bg-red-50 border-red-200 hover:border-red-300': rec.priority === 1,
                    'bg-yellow-50 border-yellow-200 hover:border-yellow-300': rec.priority === 2,
                    'bg-blue-50 border-blue-200 hover:border-blue-300': rec.priority !== 1 && rec.priority !== 2
                  }"
                  @click="handleRecommendationClick(rec)"
                >
                  <div class="flex items-start justify-between mb-2 md:mb-3">
                    <span 
                      class="px-2 py-1 rounded-full text-xs font-semibold"
                      :class="{
                        'bg-red-200 text-red-800': rec.priority === 1,
                        'bg-yellow-200 text-yellow-800': rec.priority === 2,
                        'bg-blue-200 text-blue-800': rec.priority !== 1 && rec.priority !== 2
                      }"
                    >
                      {{ rec.priority === 1 ? '🔴 High' : rec.priority === 2 ? '🟡 Medium' : '🔵 Low' }}
                    </span>
                    <span v-if="rec.section_name" class="text-xs text-gray-500 hidden sm:block">{{ rec.section_name }}</span>
                  </div>
                  <h4 class="font-semibold text-gray-800 mb-1 md:mb-2 text-sm md:text-base">{{ rec.title }}</h4>
                  <p class="text-xs md:text-sm text-gray-600 line-clamp-2">{{ rec.description }}</p>
                </div>
              </div>
            </div>

            <!-- Simple Stats Cards -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 mb-6 md:mb-8">
              <!-- Subject Scores Summary -->
              <div class="bg-white rounded-2xl p-4 md:p-6 border border-gray-200 shadow-lg">
                <h3 class="text-lg md:text-xl font-bold text-gray-800 mb-4 md:mb-6 flex items-center">
                  <span class="mr-2 md:mr-3">📚</span>
                  Score by Subject
                </h3>
                <div v-if="analyticsData.subjects?.length > 0" class="space-y-3 md:space-y-4">
                  <div v-for="subject in analyticsData.subjects" :key="subject.sector_name" class="flex items-center justify-between">
                    <span class="text-gray-700 text-sm md:text-base truncate flex-1 mr-2">{{ subject.sector_name }}</span>
                    <div class="flex items-center flex-shrink-0">
                      <span class="font-semibold text-blue-600 mr-2 md:mr-3 text-sm md:text-base">{{ subject.average_score }}</span>
                      <div class="w-20 md:w-32 h-1.5 md:h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div 
                          class="h-full rounded-full bg-blue-500" 
                          :style="{ width: (subject.average_score || 0) + '%' }"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="h-48 md:h-64 flex items-center justify-center text-gray-500">
                  No subject data available yet
                </div>
              </div>

              <!-- AI Learning Recommendations - Flashcard Style -->
              <div class="bg-white rounded-2xl p-4 md:p-6 border border-gray-200 shadow-lg">
                <div class="flex items-center justify-between mb-4 md:mb-6">
                  <h3 class="text-lg md:text-xl font-bold text-gray-800 flex items-center">
                    <span class="mr-2 md:mr-3">🤖</span>
                    AI Learning Recommendations
                  </h3>
                  <button 
                    v-if="!showAIRecommendation"
                    @click="showAIRecommendation = true"
                    class="px-3 py-1.5 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs font-medium rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 flex items-center"
                  >
                    See AI Recommendation?
                  </button>
                  <button 
                    v-else
                    @click="showAIRecommendation = false"
                    class="px-3 py-1.5 bg-gray-200 text-gray-700 text-xs font-medium rounded-lg hover:bg-gray-300 transition-all duration-300 flex items-center"
                  >
                    Hide Recommendation
                  </button>
                </div>
                
                <!-- Flashcard Style AI Recommendation -->
                <div v-if="showAIRecommendation && aiRecommendation" class="space-y-4">
                  <!-- Idea Analysis -->
                  <div class="bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 rounded-xl p-4 border border-blue-100 shadow-sm">
                    <div class="flex items-center mb-2">
                      <span class="text-lg mr-2">💡</span>
                      <h4 class="font-bold text-gray-800 text-sm md:text-base">Idea Analysis</h4>
                    </div>
                    <p class="text-gray-700 text-sm md:text-base leading-relaxed">{{ aiRecommendation.overall_analysis }}</p>
                  </div>
                  
                  <!-- Strong Areas -->
                  <div v-if="aiRecommendation.performance_highlights?.length > 0" class="bg-green-50 rounded-xl p-4 border border-green-100 shadow-sm">
                    <div class="flex items-center mb-2">
                      <span class="text-lg mr-2">🌟</span>
                      <h4 class="font-bold text-green-800 text-sm md:text-base">Strong Areas</h4>
                    </div>
                    <div class="flex flex-wrap gap-2">
                      <span v-for="(highlight, idx) in aiRecommendation.performance_highlights" :key="idx" class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                        {{ highlight }}
                      </span>
                    </div>
                  </div>
                  
                  <!-- Areas to Improve -->
                  <div v-if="aiRecommendation.areas_needing_attention?.length > 0" class="bg-red-50 rounded-xl p-4 border border-red-100 shadow-sm">
                    <div class="flex items-center mb-2">
                      <span class="text-lg mr-2">⚠️</span>
                      <h4 class="font-bold text-red-800 text-sm md:text-base">Areas to Improve</h4>
                    </div>
                    <div class="space-y-2">
                      <div v-for="(area, idx) in aiRecommendation.areas_needing_attention" :key="idx" class="bg-white rounded-lg p-3 border border-red-100">
                        <div class="flex justify-between items-start">
                          <span class="text-gray-800 text-sm font-medium">{{ area.topic }}</span>
                          <span class="text-red-600 text-xs font-bold bg-red-100 px-2 py-0.5 rounded">{{ area.score }}</span>
                        </div>
                        <p class="text-gray-600 text-xs mt-1">{{ area.tip }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Study Tips -->
                  <div v-if="aiRecommendation.study_tips?.length > 0" class="bg-yellow-50 rounded-xl p-4 border border-yellow-100 shadow-sm">
                    <div class="flex items-center mb-2">
                      <span class="text-lg mr-2">📚</span>
                      <h4 class="font-bold text-yellow-800 text-sm md:text-base">Study Tips</h4>
                    </div>
                    <ul class="space-y-2">
                      <li v-for="(tip, idx) in aiRecommendation.study_tips" :key="idx" class="text-gray-700 text-xs flex items-start">
                        <span class="text-yellow-600 mr-2 mt-0.5">✓</span>
                        {{ tip }}
                      </li>
                    </ul>
                  </div>
                  
                  <!-- Ethiopian Exam Prep -->
                  <div class="bg-gradient-to-r from-purple-50 via-pink-50 to-rose-50 rounded-xl p-4 border border-purple-100 shadow-sm">
                    <div class="flex items-center mb-2">
                      <span class="text-lg mr-2">🎯</span>
                      <h4 class="font-bold text-purple-800 text-sm md:text-base">Ethiopian Exam Prep</h4>
                    </div>
                    <p class="text-gray-700 text-sm leading-relaxed">{{ aiRecommendation.ethiopian_exam_prep }}</p>
                  </div>
                  
                  <!-- Next Steps -->
                  <div v-if="aiRecommendation.next_steps" class="bg-blue-50 rounded-xl p-4 border border-blue-100 shadow-sm">
                    <div class="flex items-center mb-2">
                      <span class="text-lg mr-2">🚀</span>
                      <h4 class="font-bold text-blue-800 text-sm md:text-base">Next Steps</h4>
                    </div>
                    <p class="text-gray-700 text-sm">{{ aiRecommendation.next_steps }}</p>
                  </div>
                </div>
                
                <!-- Hidden State -->
                <div v-else-if="!showAIRecommendation" class="h-48 md:h-64 flex flex-col items-center justify-center text-gray-500">
                  <div class="text-4xl mb-3">🤖</div>
                  <p class="text-sm text-center px-4">Click "See AI Recommendation?" to view your personalized learning insights</p>
                </div>
                
                <!-- Loading State -->
                <div v-else-if="analyticsLoading" class="h-48 flex items-center justify-center">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
                
                <!-- No Data State -->
                <div v-else class="h-48 md:h-64 flex flex-col items-center justify-center text-gray-500">
                  <div class="text-4xl mb-3">📝</div>
                  <p class="text-sm text-center px-4">Take some exams to get AI recommendations</p>
                </div>
              </div>
            </div>

            <!-- All Topics Performance Table -->
            <div class="mb-6 md:mb-8">
              <h3 class="text-lg md:text-xl font-bold text-gray-800 mb-4 md:mb-6 flex items-center">
                <span class="mr-2 md:mr-3">📋</span>
                All Topics Performance
              </h3>
              <div class="bg-white rounded-2xl border border-gray-200 shadow-lg overflow-hidden">
                <div class="overflow-x-auto">
                  <table class="w-full min-w-[600px]">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-3 md:px-6 py-3 md:py-4 text-left text-xs md:text-sm font-semibold text-gray-600">Subject</th>
                        <th class="px-3 md:px-6 py-3 md:py-4 text-left text-xs md:text-sm font-semibold text-gray-600">Topic</th>
                        <th class="px-3 md:px-6 py-3 md:py-4 text-left text-xs md:text-sm font-semibold text-gray-600">Exams</th>
                        <th class="px-3 md:px-6 py-3 md:py-4 text-left text-xs md:text-sm font-semibold text-gray-600">Avg</th>
                        <th class="px-3 md:px-6 py-3 md:py-4 text-left text-xs md:text-sm font-semibold text-gray-600">Status</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                      <tr 
                        v-for="(topic, index) in allTopics" 
                        :key="topic.section_id || index"
                        class="hover:bg-gray-50 transition-colors"
                      >
                        <td class="px-3 md:px-6 py-3 md:py-4 text-xs md:text-sm text-gray-800">{{ topic.sector_name }}</td>
                        <td class="px-3 md:px-6 py-3 md:py-4 text-xs md:text-sm text-gray-800 font-medium">{{ topic.section_name }}</td>
                        <td class="px-3 md:px-6 py-3 md:py-4 text-xs md:text-sm text-gray-600">{{ topic.total_exams_taken }}</td>
                        <td class="px-3 md:px-6 py-3 md:py-4 text-xs md:text-sm">
                          <div class="flex items-center">
                            <span class="font-semibold mr-1 md:mr-2">{{ topic.average_score?.toFixed(1) }}%</span>
                          </div>
                        </td>
                        <td class="px-3 md:px-6 py-3 md:py-4">
                          <span 
                            class="px-2 md:px-3 py-1 rounded-full text-xs font-semibold"
                            :class="{
                              'bg-green-100 text-green-800': topic.average_score >= 70,
                              'bg-yellow-100 text-yellow-800': topic.average_score >= 50 && topic.average_score < 70,
                              'bg-red-100 text-red-800': topic.average_score < 50
                            }"
                          >
                            {{ topic.average_score >= 70 ? '✅ Strong' : topic.average_score >= 50 ? '⚠️' : '❌' }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>

<!-- Feature Cards -->
        <CardsStud />

        
       

          
         
        
        </div>
        </main>
      </div>

    <FooterStud />
  </div>
</template>

<script>
import HeaderStud from '../components/HeaderStud.vue';
import FooterStud from '../components/FooterStud.vue';
import SidebarStud from '../components/SidebarStud.vue';
import CardsStud from '../components/CardsStud.vue';
import { 
  ChartBarIcon,
  ClockIcon,
  ClipboardDocumentCheckIcon,
  TrophyIcon,
  ChatBubbleLeftIcon,
  ArrowTrendingUpIcon,
  ChevronRightIcon,
  ArrowPathIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'StudentDashboard',
  components: {
    HeaderStud,
    FooterStud,
    SidebarStud,
    CardsStud,
    ChartBarIcon,
    ClockIcon,
    ClipboardDocumentCheckIcon,
    TrophyIcon,
    ChatBubbleLeftIcon,
    ArrowTrendingUpIcon,
    ChevronRightIcon,
    ArrowPathIcon,
    ExclamationTriangleIcon
  },
  data() {
    return {
      sidebarOpen: false,
      student: {
        full_name: '',
        username: '',
        grade: '',
        profile_photo: '',
        school_id: ''
      },
      analyticsLoading: true,
      studentId: null,
      analyticsData: {
        average_score: 0,
        total_exams_taken: 0,
        weak_topics_count: 0,
        class_rank: null,
        subjects: [],
        weak_topics: [],
        recent_recommendations: [],
        weekly_progress: []
      },
      aiRecommendation: null,
      allTopics: [],
      showAIRecommendation: false,
      recentActivities: [
        {
          id: 1,
          iconBg: 'bg-gradient-to-br from-green-500 to-emerald-400',
          dotColor: 'bg-green-500',
          borderColor: 'border-green-100',
          description: 'Aced Mathematics Mock Test with 92% score',
          time: '2 hours ago',
          status: 'Excellence',
          badgeColor: 'bg-green-100 text-green-800'
        },
        {
          id: 2,
          iconBg: 'bg-gradient-to-br from-blue-500 to-cyan-400',
          dotColor: 'bg-blue-500',
          borderColor: 'border-blue-100',
          description: 'Completed Physics Chapter 5: Quantum Mechanics',
          time: 'Yesterday, 4:30 PM',
          status: 'Completed',
          badgeColor: 'bg-blue-100 text-blue-800'
        },
        {
          id: 3,
          iconBg: 'bg-gradient-to-br from-orange-500 to-amber-400',
          dotColor: 'bg-orange-500',
          borderColor: 'border-orange-100',
          description: 'Moved up to #8 position in class rankings',
          time: '2 days ago',
          status: 'Achievement',
          badgeColor: 'bg-orange-100 text-orange-800'
        },
        {
          id: 4,
          iconBg: 'bg-gradient-to-br from-purple-500 to-pink-400',
          dotColor: 'bg-purple-500',
          borderColor: 'border-purple-100',
          description: 'Active participation in Chemistry forum',
          time: '3 days ago',
          status: 'Engaged',
          badgeColor: 'bg-purple-100 text-purple-800'
        }
      ]
    };
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    closeSidebar() {
      this.sidebarOpen = false;
    },
    async loadFullName() {
      const username = localStorage.getItem("username");
      if (!username) return;
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/users/profile/${username}`);
        if (!res.ok) throw new Error("Failed to fetch full name");
        const data = await res.json();
        this.student.full_name = data.full_name || '';
      } catch (err) {
        console.error(err);
      }
    },
    async loadAnalytics() {
      this.analyticsLoading = true;
      try {
        await fetch(`http://127.0.0.1:8000/api/analytics/calculate/${this.studentId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ force_refresh: true })
        });
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/dashboard`);
        if (!response.ok) throw new Error('Failed to fetch analytics');
        const data = await response.json();
        this.analyticsData = data;
      } catch (error) {
        console.error('Error loading analytics:', error);
      } finally {
        this.analyticsLoading = false;
      }
    },
    async loadAllTopics() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/topics`);
        if (!response.ok) throw new Error('Failed to fetch topics');
        const data = await response.json();
        this.allTopics = data;
      } catch (error) {
        console.error('Error loading topics:', error);
      }
    },
    async loadAIRecommendation() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/ai-recommendation`);
        if (!response.ok) throw new Error('Failed to fetch AI recommendation');
        const data = await response.json();
        if (data.success && data.recommendation) {
          this.aiRecommendation = data.recommendation;
        }
      } catch (error) {
        console.error('Error loading AI recommendation:', error);
      }
    },
    async loadClassRank() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/class-rank`);
        if (!response.ok) throw new Error('Failed to fetch class rank');
        const data = await response.json();
        if (data.class_rank) {
          this.analyticsData.class_rank = data.class_rank;
        }
      } catch (error) {
        console.error('Error loading class rank:', error);
      }
    },
    async refreshAnalytics() {
      this.analyticsLoading = true;
      try {
        await fetch(`http://127.0.0.1:8000/api/analytics/calculate/${this.studentId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ force_refresh: true })
        });
        await this.loadAnalytics();
        await this.loadAllTopics();
      } catch (error) {
        console.error('Error refreshing analytics:', error);
      } finally {
        this.analyticsLoading = false;
      }
    },
    async loadAvailableExams() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/available-exams`);
        if (!response.ok) throw new Error('Failed to fetch available exams');
        const data = await response.json();
        this.availableExams = data.exams || [];
      } catch (error) {
        console.error('Error loading available exams:', error);
      }
    },
    startExam(exam) {
      if (exam.pricing_type === 'Premium') {
        this.goToPremium();
        return;
      }
      this.$router.push(`/student/take-exam/${exam.id}`);
    },
    goToPremium() {
      this.$router.push('/premium');
    },
    viewAIRecommendation() {
      console.log('Viewing AI recommendation');
    },
    handleRecommendationClick(recommendation) {
      if (recommendation.section_id) {
        this.$router.push(`/student/topic/${recommendation.section_id}`);
      }
    },
    practiceTopic(topic) {
      this.$router.push(`/student/available-tests?topic=${topic.section_id}`);
    }
  },
  async mounted() {
    const username = localStorage.getItem("username");
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    
    if (!username || !token || role !== 'student') {
      return;
    }

    this.loadFullName();
    
    const userId = localStorage.getItem('user_id');
    if (userId) {
      this.studentId = parseInt(userId);
      await this.loadAnalytics();
      await this.loadAllTopics();
      await this.loadAIRecommendation();
      await this.loadClassRank();
      await this.loadAvailableExams();
    }
  }
};
</script>

<style scoped>
@keyframes gradientShift {
 0%, 100% { background-position: 0% 50%; }
 50% { background-position: 100% 50%; }
}

.gradient-animate {
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
}

.pattern-overlay {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  background-repeat: repeat;
}

* {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: linear-gradient(to bottom, #f8fafc, #e2e8f0);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #3b82f6, #8b5cf6);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #2563eb, #7c3aed);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
