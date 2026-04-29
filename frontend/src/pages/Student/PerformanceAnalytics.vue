<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50/30">
    <!-- Header -->
    <HeaderStud @toggle-sidebar="toggleSidebar" />

    <div class="flex">
      <!-- Sidebar -->
      <SidebarStud />

      <!-- Main Content -->
      <main class="flex-1 p-4 md:p-8">
        <!-- Page Header -->
        <div class="flex items-center justify-between mb-8">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold text-gray-800 flex items-center">
              <span class="mr-4">📊</span>
              Performance Analytics
            </h1>
            <p class="text-gray-600 mt-2">AI-Powered Learning Insights & Recommendations</p>
          </div>
          <button 
            @click="refreshAnalytics"
            :disabled="loading"
            class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            <ArrowPathIcon class="w-5 h-5 mr-2" :class="{ 'animate-spin': loading }" />
            Refresh
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center h-64">
          <div class="text-center">
            <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p class="text-gray-600">Loading your analytics...</p>
          </div>
        </div>

        <!-- Analytics Content -->
        <div v-else>
          <!-- Quick Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Average Score -->
            <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all">
              <div class="flex items-center justify-between mb-4">
                <div class="p-3 rounded-xl bg-gradient-to-br from-green-50 to-emerald-50">
                  <ChartBarIcon class="w-6 h-6 text-green-600" />
                </div>
                <span class="text-xs font-semibold px-3 py-1 rounded-full bg-green-100 text-green-700">
                  Overall
                </span>
              </div>
              <p class="text-gray-500 text-sm">Average Score</p>
              <p class="text-3xl font-bold text-gray-800">{{ analyticsData.average_score || 0 }}%</p>
              <div class="mt-3 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  class="h-full rounded-full bg-gradient-to-r from-green-500 to-emerald-400" 
                  :style="{ width: (analyticsData.average_score || 0) + '%' }"
                ></div>
              </div>
            </div>

            <!-- Exams Taken -->
            <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all">
              <div class="flex items-center justify-between mb-4">
                <div class="p-3 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50">
                  <ClipboardDocumentCheckIcon class="w-6 h-6 text-blue-600" />
                </div>
                <span class="text-xs font-semibold px-3 py-1 rounded-full bg-blue-100 text-blue-700">
                  Total
                </span>
              </div>
              <p class="text-gray-500 text-sm">Exams Taken</p>
              <p class="text-3xl font-bold text-gray-800">{{ analyticsData.total_exams_taken || 0 }}</p>
              <p class="text-sm text-gray-500 mt-2">Across {{ subjectsCovered }} Streams</p>
            </div>

            <!-- Weak Topics (50% threshold) -->
            <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all">
              <div class="flex items-center justify-between mb-4">
                <div class="p-3 rounded-xl bg-gradient-to-br from-red-50 to-orange-50">
                  <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
                </div>
                <span class="text-xs font-semibold px-3 py-1 rounded-full bg-red-100 text-red-700">
                  Need Focus
                </span>
              </div>
              <p class="text-gray-500 text-sm">Weak Topics (<50%)</p>
              <p class="text-3xl font-bold text-gray-800">{{ weakTopics50?.length || 0 }}</p>
              <p class="text-sm text-gray-500 mt-2">Topics below 50%</p>
            </div>

            <!-- Class Rank -->
            <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all">
              <div class="flex items-center justify-between mb-4">
                <div class="p-3 rounded-xl bg-gradient-to-br from-purple-50 to-violet-50">
                  <TrophyIcon class="w-6 h-6 text-purple-600" />
                </div>
                <span class="text-xs font-semibold px-3 py-1 rounded-full bg-purple-100 text-purple-700">
                  Ranking
                </span>
              </div>
              <p class="text-gray-500 text-sm">Class Rank</p>
              <p class="text-3xl font-bold text-gray-800">#{{ classRankData?.class_rank || '--' }}</p>
              <p class="text-sm text-gray-500 mt-2">Grade {{ classRankData?.grade || '--' }}</p>
            </div>
          </div>

          <!-- Global AI Recommendations Section -->
          <div v-if="globalRecommendations?.recommendations?.length > 0" class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span class="mr-3">🤖</span>
              Global AI Recommendations
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="rec in globalRecommendations.recommendations" 
                :key="rec.title"
                class="p-5 rounded-2xl border bg-blue-50 border-blue-200 hover:shadow-lg transition-all"
              >
                <h3 class="font-semibold text-gray-800 mb-2">{{ rec.title }}</h3>
                <p class="text-sm text-gray-600">{{ rec.description }}</p>
              </div>
            </div>
          </div>

          <!-- Score Trend -->
          <div v-if="globalRecommendations" class="mb-8">
            <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
              <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <span class="mr-3">📈</span>
                Performance Trend
              </h3>
              <div class="flex items-center space-x-8">
                <div>
                  <p class="text-sm text-gray-500">Score Trend</p>
                  <p class="text-lg font-semibold" :class="globalRecommendations.score_trend === 'improving' ? 'text-green-600' : globalRecommendations.score_trend === 'declining' ? 'text-red-600' : 'text-gray-600'">
                    {{ globalRecommendations.score_trend === 'improving' ? '📈 Improving' : globalRecommendations.score_trend === 'declining' ? '📉 Declining' : '➡️ Stable' }}
                  </p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Recent Scores</p>
                  <div class="flex space-x-2">
                    <span v-for="(score, idx) in globalRecommendations.recent_scores" :key="idx" class="px-2 py-1 bg-gray-100 rounded text-sm font-semibold">
                      {{ score?.toFixed(0) }}%
                    </span>
                  </div>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Subjects Covered</p>
                  <p class="text-lg font-semibold text-gray-800">{{ globalRecommendations.subjects_covered || 0 }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Topics Covered</p>
                  <p class="text-lg font-semibold text-gray-800">{{ globalRecommendations.topics_covered || 0 }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Recommendations Section -->
          <div v-if="analyticsData.recent_recommendations?.length > 0" class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span class="mr-3">💡</span>
              Topic-Specific Recommendations
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="rec in analyticsData.recent_recommendations" 
                :key="rec.title"
                :class="`p-5 rounded-2xl border transition-all hover:shadow-lg cursor-pointer ${
                  rec.priority === 1 ? 'bg-red-50 border-red-200 hover:border-red-300' :
                  rec.priority === 2 ? 'bg-yellow-50 border-yellow-200 hover:border-yellow-300' :
                  'bg-blue-50 border-blue-200 hover:border-blue-300'
                }`"
                @click="handleRecommendationClick(rec)"
              >
                <div class="flex items-start justify-between mb-3">
                  <span 
                    :class="`px-2 py-1 rounded-full text-xs font-semibold ${
                      rec.priority === 1 ? 'bg-red-200 text-red-800' :
                      rec.priority === 2 ? 'bg-yellow-200 text-yellow-800' :
                      'bg-blue-200 text-blue-800'
                    }`"
                  >
                    {{ rec.priority === 1 ? '🔴 High' : rec.priority === 2 ? '🟡 Medium' : '🔵 Low' }}
                  </span>
                  <span v-if="rec.section_name" class="text-xs text-gray-500">{{ rec.section_name }}</span>
                </div>
                <h3 class="font-semibold text-gray-800 mb-2">{{ rec.title }}</h3>
                <p class="text-sm text-gray-600">{{ rec.description }}</p>
              </div>
            </div>
          </div>

          <!-- Charts Section -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <!-- Subject Scores Chart -->
            <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
              <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center">
                <span class="mr-3">📚</span>
                Score by Subject
              </h3>
              <div v-if="analyticsData.subjects?.length > 0" class="h-64">
                <apexchart 
                  type="bar" 
                  height="250"
                  :options="subjectChartOptions" 
                  :series="subjectChartSeries"
                ></apexchart>
              </div>
              <div v-else class="h-64 flex items-center justify-center text-gray-500">
                No subject data available yet
              </div>
            </div>

            <!-- Progress Over Time Chart -->
            <div class="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg">
              <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center">
                <span class="mr-3">📈</span>
                Progress Over Time
              </h3>
              <div v-if="analyticsData.weekly_progress?.length > 0" class="h-64">
                <apexchart 
                  type="area" 
                  height="250"
                  :options="progressChartOptions" 
                  :series="progressChartSeries"
                ></apexchart>
              </div>
              <div v-else class="h-64 flex items-center justify-center text-gray-500">
                No progress data available yet
              </div>
            </div>
          </div>

          <!-- Score by Exam Section -->
          <div v-if="examScores.length > 0" class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span class="mr-3">📝</span>
              Score by Exam
            </h2>
            <div class="space-y-4">
              <div 
                v-for="exam in examScores" 
                :key="exam.attempt_id"
                class="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all"
              >
                <div class="flex items-center justify-between mb-4">
                  <div>
                    <h3 class="text-lg font-semibold text-gray-800">{{ exam.exam_name }}</h3>
                    <p class="text-sm text-gray-500">{{ exam.completed_at }}</p>
                  </div>
                  <div class="text-right">
                    <p class="text-3xl font-bold" :class="exam.percentage >= 70 ? 'text-green-600' : exam.percentage >= 50 ? 'text-yellow-600' : 'text-red-600'">
                      {{ exam.percentage }}%
                    </p>
                    <p class="text-sm text-gray-500">{{ exam.correct_answers }}/{{ exam.total_questions }} correct</p>
                  </div>
                </div>
                <!-- Section Breakdown -->
                <div v-if="exam.section_breakdown?.length > 0" class="mt-4 pt-4 border-t border-gray-100">
                  <p class="text-sm font-semibold text-gray-600 mb-3">Section Breakdown:</p>
                  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    <div 
                      v-for="section in exam.section_breakdown" 
                      :key="section.section_id"
                      class="bg-gray-50 rounded-lg p-3"
                    >
                      <p class="text-xs font-semibold text-gray-600">{{ section.section_name }}</p>
                      <p class="text-sm font-bold" :class="section.percentage >= 70 ? 'text-green-600' : section.percentage >= 50 ? 'text-yellow-600' : 'text-red-600'">
                        {{ section.percentage }}%
                      </p>
                      <p class="text-xs text-gray-500">{{ section.correct }}/{{ section.total }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Weak Topics Section (50% threshold) -->
          <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span class="mr-3">⚠️</span>
              Weak Topics (Below 50%)
            </h2>
            <div v-if="weakTopics50?.length > 0" class="space-y-4">
              <div 
                v-for="topic in weakTopics50" 
                :key="topic.section_id"
                class="bg-white rounded-2xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-all"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center mb-2">
                      <h3 class="text-lg font-semibold text-gray-800">{{ topic.section_name }}</h3>
                      <span class="ml-3 px-3 py-1 rounded-full text-xs font-semibold bg-red-200 text-red-800">
                        Weak
                      </span>
                    </div>
                    <p class="text-sm text-gray-500">{{ topic.sector_name }}</p>
                    <div class="flex items-center mt-3 space-x-4">
                      <div class="flex items-center">
                        <span class="text-sm text-gray-500 mr-2">Avg Score:</span>
                        <span class="font-semibold text-red-600">{{ topic.average_score?.toFixed(1) }}%</span>
                      </div>
                      <div class="flex items-center">
                        <span class="text-sm text-gray-500 mr-2">Exams:</span>
                        <span class="font-semibold text-gray-800">{{ topic.total_exams_taken }}</span>
                      </div>
                    </div>
                  </div>
                  <button 
                    @click="practiceTopic(topic)"
                    class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
                  >
                    Practice Now
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="bg-green-50 rounded-2xl p-6 border border-green-200 text-center">
              <div class="text-4xl mb-3">🎉</div>
              <h3 class="text-lg font-semibold text-green-800">Great Job!</h3>
              <p class="text-green-600">No weak topics (below 50%) detected. Keep up the excellent work!</p>
            </div>
          </div>

          <!-- All Topics Performance Table -->
          <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span class="mr-3">📋</span>
              All Topics Performance
            </h2>
            <div class="bg-white rounded-2xl border border-gray-200 shadow-lg overflow-hidden">
              <div class="overflow-x-auto">
                <table class="w-full">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">Subject</th>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">Topic</th>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">Exams</th>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">Avg Score</th>
                      <th class="px-6 py-4 text-left text-sm font-semibold text-gray-600">Status</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    <tr 
                      v-for="topic in topicsPerformance" 
                      :key="topic.section_id"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="px-6 py-4 text-sm text-gray-800">{{ topic.subject }}</td>
                      <td class="px-6 py-4 text-sm text-gray-800 font-medium">{{ topic.topic }}</td>
                      <td class="px-6 py-4 text-sm text-gray-600">{{ topic.exams_taken }}</td>
                      <td class="px-6 py-4 text-sm">
                        <div class="flex items-center">
                          <span class="font-semibold mr-2">{{ topic.avg_result }}%</span>
                          <div class="w-20 h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div 
                              :class="`h-full rounded-full ${
                                topic.avg_result >= 75 ? 'bg-green-500' :
                                topic.avg_result >= 50 ? 'bg-yellow-500' :
                                'bg-red-500'
                              }`"
                              :style="{ width: topic.avg_result + '%' }"
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4">
                        <span 
                          :class="`px-3 py-1 rounded-full text-xs font-semibold ${
                            topic.avg_result >= 75 ? 'bg-green-100 text-green-800' :
                            topic.avg_result >= 50 ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`"
                        >
                          {{ topic.avg_result >= 75 ? '✅ Strong' : topic.avg_result >= 50 ? '⚠️ Moderate' : '❌ Weak' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <FooterStud />
  </div>
</template>

<script>
import HeaderStud from '@/components/HeaderStud.vue';
import FooterStud from '@/components/FooterStud.vue';
import SidebarStud from '@/components/SidebarStud.vue';
import {
  ChartBarIcon,
  ClipboardDocumentCheckIcon,
  TrophyIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'PerformanceAnalytics',
  components: {
    HeaderStud,
    FooterStud,
    SidebarStud,
    ChartBarIcon,
    ClipboardDocumentCheckIcon,
    TrophyIcon,
    ExclamationTriangleIcon,
    ArrowPathIcon
  },
  data() {
    return {
      sidebarOpen: false,
      loading: true,
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
      // New data for enhanced analytics
      examScores: [],
      topicsPerformance: [],
      globalRecommendations: null,
      classRankData: null,
      subjectsCovered: 0,
      weakTopics50: [],
      allTopics: [],
      // ApexCharts options
      subjectChartOptions: {
        chart: {
          type: 'bar',
          toolbar: { show: false }
        },
        colors: ['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444'],
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '50%',
            borderRadius: 8
          }
        },
        dataLabels: { enabled: false },
        xaxis: {
          categories: [],
          labels: { style: { colors: '#6B7280' } }
        },
        yaxis: {
          max: 100,
          labels: { 
            style: { colors: '#6B7280' },
            formatter: (val) => val + '%'
          }
        },
        tooltip: {
          y: {
            formatter: (val) => val + '%'
          }
        }
      },
      subjectChartSeries: [{
        name: 'Score',
        data: []
      }],
      progressChartOptions: {
        chart: {
          type: 'area',
          toolbar: { show: false }
        },
        colors: ['#3B82F6'],
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.4,
            opacityTo: 0.1,
            stops: [0, 100]
          }
        },
        stroke: {
          curve: 'smooth',
          width: 3
        },
        dataLabels: { enabled: false },
        xaxis: {
          categories: [],
          labels: { style: { colors: '#6B7280' } }
        },
        yaxis: {
          max: 100,
          labels: { 
            style: { colors: '#6B7280' },
            formatter: (val) => val + '%'
          }
        },
        tooltip: {
          y: {
            formatter: (val) => val + '%'
          }
        }
      },
      progressChartSeries: [{
        name: 'Score',
        data: []
      }]
    };
  },
  async mounted() {
    // Enforce login - check if user is logged in
    const username = localStorage.getItem('username');
    if (!username) {
      this.$router.push('/user_login');
      return;
    }

    // Get role from localStorage to check if user is a student
    const role = localStorage.getItem('role');
    if (!role || role !== 'student') {
      if (role === 'teacher') {
        this.$router.push('/teacher_dashboard');
      } else if (role === 'admin') {
        this.$router.push('/admin_dashboard');
      } else {
        this.$router.push('/user_login');
      }
      return;
    }

    // Get student ID from localStorage
    const studentId = localStorage.getItem('student_id');
    if (!studentId) {
      this.$router.push('/user_login');
      return;
    }
    this.studentId = parseInt(studentId);
    
    await this.loadAnalytics();
    await this.loadAllTopics();
    await this.loadExamScores();
    await this.loadTopicsPerformance();
    await this.loadGlobalRecommendations();
    await this.loadClassRank();
    await this.loadSubjectsCovered();
    await this.loadWeakTopics50();
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    closeSidebar() {
      this.sidebarOpen = false;
    },
    async loadAnalytics() {
      this.loading = true;
      try {
        console.log('Loading analytics for student:', this.studentId);
        
        // First, calculate analytics
        const calcResponse = await fetch(`http://127.0.0.1:8000/api/analytics/calculate/${this.studentId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ force_refresh: true })
        });
        
        console.log('Calculate response status:', calcResponse.status);
        
        if (!calcResponse.ok) {
          const errorText = await calcResponse.text();
          throw new Error(`Calculate analytics failed: ${calcResponse.status} - ${errorText}`);
        }

        // Then fetch dashboard data
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/dashboard`);
        console.log('Dashboard response status:', response.status);
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to fetch analytics: ${response.status} - ${errorText}`);
        }
        
        const data = await response.json();
        console.log('Dashboard data received:', data);
        this.analyticsData = data;
        
        // Update charts
        this.updateSubjectChart();
        this.updateProgressChart();
      } catch (error) {
        console.error('Error loading analytics:', error);
        alert('Error loading analytics: ' + error.message);
      } finally {
        this.loading = false;
        console.log('Loading state set to false');
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
    async loadExamScores() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/exam-scores`);
        if (!response.ok) throw new Error('Failed to fetch exam scores');
        
        const data = await response.json();
        this.examScores = data.exam_scores || [];
      } catch (error) {
        console.error('Error loading exam scores:', error);
      }
    },
    async loadTopicsPerformance() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/topics-performance`);
        if (!response.ok) throw new Error('Failed to fetch topics performance');
        
        const data = await response.json();
        this.topicsPerformance = data.performance_table || [];
      } catch (error) {
        console.error('Error loading topics performance:', error);
      }
    },
    async loadGlobalRecommendations() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/global-recommendations`);
        if (!response.ok) throw new Error('Failed to fetch global recommendations');
        
        const data = await response.json();
        this.globalRecommendations = data.recommendation || null;
      } catch (error) {
        console.error('Error loading global recommendations:', error);
      }
    },
    async loadClassRank() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/class-rank`);
        if (!response.ok) throw new Error('Failed to fetch class rank');
        
        const data = await response.json();
        this.classRankData = data;
      } catch (error) {
        console.error('Error loading class rank:', error);
      }
    },
    async loadSubjectsCovered() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/subjects-covered`);
        if (!response.ok) throw new Error('Failed to fetch subjects covered');
        
        const data = await response.json();
        this.subjectsCovered = data.subjects_covered || 0;
      } catch (error) {
        console.error('Error loading subjects covered:', error);
      }
    },
    async loadWeakTopics50() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${this.studentId}/weak-topics-50`);
        if (!response.ok) throw new Error('Failed to fetch weak topics (50%)');
        
        const data = await response.json();
        this.weakTopics50 = data.weak_topics || [];
      } catch (error) {
        console.error('Error loading weak topics (50%):', error);
      }
    },
    updateSubjectChart() {
      if (this.analyticsData.subjects?.length > 0) {
        this.subjectChartOptions.xaxis.categories = this.analyticsData.subjects.map(s => s.sector_name);
        this.subjectChartSeries[0].data = this.analyticsData.subjects.map(s => s.average_score);
      }
    },
    updateProgressChart() {
      if (this.analyticsData.weekly_progress?.length > 0) {
        this.progressChartOptions.xaxis.categories = this.analyticsData.weekly_progress.map(p => 
          new Date(p.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        );
        this.progressChartSeries[0].data = this.analyticsData.weekly_progress.map(p => p.score);
      }
    },
    async refreshAnalytics() {
      this.loading = true;
      try {
        await fetch(`http://127.0.0.1:8000/api/analytics/calculate/${this.studentId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ force_refresh: true })
        });
        
        await this.loadAnalytics();
        await this.loadAllTopics();
        await this.loadExamScores();
        await this.loadTopicsPerformance();
        await this.loadGlobalRecommendations();
        await this.loadClassRank();
        await this.loadSubjectsCovered();
        await this.loadWeakTopics50();
      } catch (error) {
        console.error('Error refreshing analytics:', error);
      } finally {
        this.loading = false;
      }
    },
    handleRecommendationClick(recommendation) {
      console.log('Recommendation clicked:', recommendation);
      if (recommendation.section_id) {
        this.$router.push(`/student/topic/${recommendation.section_id}`);
      }
    },
    practiceTopic(topic) {
      console.log('Practice topic:', topic);
      this.$router.push(`/student/available-tests?topic=${topic.section_id}`);
    }
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

* {
  transition: all 0.3s ease;
}
</style>
