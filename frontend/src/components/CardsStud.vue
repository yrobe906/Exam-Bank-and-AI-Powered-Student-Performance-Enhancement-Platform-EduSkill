<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Performance Summary Card -->
    <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow duration-300">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-800">Performance Summary</h3>
        <div class="w-10 h-10 bg-gradient-to-br from-green-400 to-blue-500 rounded-lg flex items-center justify-center">
          <ChartBarIcon class="w-6 h-6 text-white" />
        </div>
      </div>
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-gray-600">Overall Score</span>
          <span class="text-2xl font-bold text-blue-600">{{ overallScore }}%</span>
        </div>
        <div class="space-y-2">
          <div v-for="subject in performanceData" :key="subject.name" class="flex justify-between items-center">
            <span class="text-gray-600">{{ subject.name }}</span>
            <div class="flex items-center space-x-2">
              <span class="font-medium">{{ subject.score }}%</span>
              <div class="w-24 bg-gray-200 rounded-full h-2">
                <div 
                  :class="getScoreColor(subject.score)" 
                  class="h-2 rounded-full" 
                  :style="{ width: subject.score + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Upcoming Exams Card -->
    <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow duration-300">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-semibold text-gray-800">Upcoming Mock Exams</h3>
        <div class="w-20 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center">
          <CalendarIcon class="w-6 h-6 text-white" />
        </div>
      </div>
      <div class="space-y-4">
        <div v-for="exam in upcomingExams" :key="exam.id" class="border-l-4 border-blue-500 pl-4 py-2 cursor-pointer hover:bg-blue-50 transition-colors" @click="startExam(exam)">
          <div class="flex justify-between items-start">
            <div>
              <h4 class="font-medium text-gray-800">{{ exam.subject }}</h4>
              <p class="text-sm text-gray-600">{{ exam.topic }}</p>
              <p class="text-xs text-gray-500">{{ exam.section }}</p>
            </div>
            <span v-if="exam.pricing_type === 'Premium'" @click.stop="goToPremium" class="text-sm font-semibold bg-yellow-100 text-yellow-600 px-2 py-1 rounded cursor-pointer">
              Subscribe
            </span>
          </div>
          <div class="flex items-center mt-2 text-sm text-gray-500">
            <ClockIcon class="w-4 h-4 mr-1" />
            {{ exam.duration }} | {{ exam.questions }} questions
          </div>
        </div>
      </div>
     
    </div>


   
  </div>
</template>

<script>
// Heroicons v2 syntax - use 24/outline for 24px outline icons
import { 
  ChartBarIcon,
  CalendarIcon,
  ArrowRightIcon,
  ClockIcon,
  BoltIcon,
  FireIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'CardsStud',
  components: {
    ChartBarIcon,
    CalendarIcon,
    ArrowRightIcon,
    ClockIcon,
    BoltIcon,
    FireIcon,
  },
  data() {
    return {
      overallScore: 0,
      performanceData: [],
      upcomingExams: [],
      quickAccessSubjects: [
        { name: 'Maths', icon: 'M', color: 'bg-gradient-to-br from-blue-500 to-cyan-400' },
        { name: 'English', icon: 'E', color: 'bg-gradient-to-br from-green-500 to-emerald-400' },
        { name: 'Physics', icon: 'P', color: 'bg-gradient-to-br from-orange-500 to-yellow-400' },
        { name: 'Biology', icon: 'B', color: 'bg-gradient-to-br from-purple-500 to-pink-400' },
        { name: 'Chemistry', icon: 'C', color: 'bg-gradient-to-br from-red-500 to-orange-400' },
        { name: 'History', icon: 'H', color: 'bg-gradient-to-br from-indigo-500 to-purple-400' },
      ],
      streakDays: 0,
      totalHours: 0,
      completedTests: 0,
    };
  },
  async mounted() {
    await this.loadAvailableExams();
    await this.loadAnalytics();
  },
  methods: {
    getScoreColor(score) {
      if (score >= 90) return 'bg-gradient-to-r from-green-400 to-green-500';
      if (score >= 80) return 'bg-gradient-to-r from-blue-400 to-blue-500';
      if (score >= 70) return 'bg-gradient-to-r from-yellow-400 to-yellow-500';
      return 'bg-gradient-to-r from-red-400 to-red-500';
    },
    async loadAvailableExams() {
      const userId = localStorage.getItem('user_id');
      if (!userId) return;
      
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${userId}/available-exams`);
        if (!response.ok) throw new Error('Failed to fetch available exams');
        const data = await response.json();
        
        // Format exams for display - remove date, show sector, section, exam, duration, questions
        this.upcomingExams = (data.exams || []).slice(0, 4).map(exam => ({
          id: exam.id,
          subject: exam.sector_name,
          topic: exam.exam_name,
          section: exam.section_name,
          duration: exam.duration + ' min',
          questions: exam.total_questions,
          pricing_type: exam.pricing_type,
          amount: exam.amount
        }));
      } catch (error) {
        console.error('Error loading available exams:', error);
        this.upcomingExams = [];
      }
    },
    async loadAnalytics() {
      const userId = localStorage.getItem('user_id');
      if (!userId) return;
      
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/analytics/student/${userId}/dashboard`);
        if (!response.ok) throw new Error('Failed to fetch analytics');
        const data = await response.json();
        
        this.overallScore = data.average_score || 0;
        this.performanceData = (data.subjects || []).map(s => ({
          name: s.sector_name,
          score: s.average_score
        }));
      } catch (error) {
        console.error('Error loading analytics:', error);
      }
    },
    navigateToSubject(subject) {
      console.log(`Navigating to ${subject.name}`);
      alert(`Opening ${subject.name} resources...`);
    },
    startExam(exam) {
      if (exam.pricing_type === 'Premium') {
        this.$router.push('/premium');
        return;
      }
      this.$router.push(`/student/take-exam/${exam.id}`);
    },
    goToPremium() {
      this.$router.push('/premium');
    }
  },
};
</script>

<style scoped>
/* Optional: Add custom animations */
.card-hover {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-5px);
}

/* Custom progress bar animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.high-score {
  animation: pulse 2s infinite;
}
</style>