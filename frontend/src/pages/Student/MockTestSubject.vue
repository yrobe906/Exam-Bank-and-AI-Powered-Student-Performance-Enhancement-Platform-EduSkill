<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50/30">
    <!-- EduSkill Header -->
    <EduskillHeader />

    <!-- Back button -->
    <div class="max-w-6xl mx-auto pt-6 px-4">
      <button 
        @click="goBack" 
        class="flex items-center text-blue-600 hover:text-blue-700 font-medium transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Exam Options
      </button>
    </div>

    <!-- Subject Selection -->
    <div class="max-w-6xl mx-auto px-4 py-8">
      <!-- Page Title -->
      <div class="text-center mb-8">
        <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
          📚 Available Mock Tests
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Choose a subject to practice your mock test
        </p>
      </div>

      <!-- Search and Filter Bar -->
      <div class="bg-white rounded-2xl shadow-lg p-4 mb-8 border border-gray-100">
        <div class="flex flex-col md:flex-row gap-4">
          <!-- Search Input -->
          <div class="flex-1 relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search subjects..."
              class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>
          
          <!-- Filter Dropdown -->
          <div class="relative">
            <select
              v-model="selectedSector"
              class="appearance-none w-full md:w-64 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all cursor-pointer pr-10"
            >
              <option value="">All Sectors</option>
              <option v-for="sector in sectors" :key="sector.id" :value="sector.id">
                {{ sector.icon }} {{ sector.name }}
              </option>
            </select>
            <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="text-gray-500 mt-4">Loading subjects...</p>
      </div>

      <!-- Subject Cards Grid -->
      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="subject in filteredSubjects"
          :key="subject.id"
          class="subject-card group cursor-pointer"
          @click="selectSubject(subject)"
        >
          <div class="subject-inner">
            <!-- Icon -->
            <div class="subject-icon" :class="subject.iconBg">
              <span class="text-3xl">{{ subject.icon }}</span>
            </div>
            
            <!-- Name -->
            <h3 class="subject-name">{{ subject.name }}</h3>
            
            <!-- Question count -->
            <p class="subject-count">{{ subject.questionCount }} Questions</p>
            
            <!-- Exam count -->
            <p class="exam-count">{{ subject.examCount }} Exams</p>
          </div>
        </div>
      </div>

      <!-- No Subjects Available -->
      <div v-if="!loading && filteredSubjects.length === 0" class="text-center py-12 bg-white rounded-xl border border-gray-200">
        <p class="text-gray-500">No mock tests available. Please check back later!</p>
      </div>
    </div>
  </div>
</template>

<script>
import MainHeader from '@/components/Header/MainHeader.vue';

const API_URL = 'http://127.0.0.1:8000';

// Sector icon mapping with real data
const sectorIcons = {
  'Natural Science': { icon: '🔬', iconBg: 'bg-gradient-to-br from-green-400 to-emerald-600' },
  'Social Science': { icon: '🌍', iconBg: 'bg-gradient-to-br from-blue-400 to-cyan-600' },
  'Mathematics': { icon: '📐', iconBg: 'bg-gradient-to-br from-purple-400 to-indigo-600' },
  'Information Technology': { icon: '💻', iconBg: 'bg-gradient-to-br from-gray-600 to-gray-800' },
  'Language': { icon: '📝', iconBg: 'bg-gradient-to-br from-pink-400 to-rose-600' },
};

export default {
  name: 'MockTestSubject',
  components: {
    MainHeader
  },
  data() {
    return {
      loading: false,
      subjects: [],
      sectors: [],
      searchQuery: '',
      selectedSector: ''
    };
  },
  computed: {
    filteredSubjects() {
      let filtered = this.subjects;
      
      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(subject => 
          subject.name.toLowerCase().includes(query)
        );
      }
      
      // Filter by selected sector
      if (this.selectedSector) {
        filtered = filtered.filter(subject => 
          subject.sectorId === this.selectedSector
        );
      }
      
      return filtered;
    }
  },
  mounted() {
    this.loadSectors();
    this.loadSubjects();
  },
  methods: {
    goBack() {
      this.$router.push('/exam-bank-options');
    },
    async loadSectors() {
      try {
        const res = await fetch(`${API_URL}/api/sectors`);
        if (res.ok) {
          const data = await res.json();
          this.sectors = data.map(sector => {
            const iconData = sectorIcons[sector.name] || { icon: '📚', iconBg: 'bg-gradient-to-br from-gray-400 to-gray-600' };
            return {
              id: sector.id,
              name: sector.name,
              ...iconData
            };
          });
        }
      } catch (error) {
        console.error('Error loading sectors:', error);
      }
    },
    async loadSubjects() {
      this.loading = true;
      try {
        const res = await fetch(`${API_URL}/api/practice-mock/subjects-with-counts`);
        if (res.ok) {
          const data = await res.json();
          this.subjects = data.map(subject => {
            const iconData = sectorIcons[subject.name] || { icon: '📚', iconBg: 'bg-gradient-to-br from-gray-400 to-gray-600' };
            return {
              id: subject.name.toLowerCase().replace(/\s+/g, '-'),
              name: subject.name,
              questionCount: subject.question_count,
              examCount: subject.exam_count || 0,
              sectorId: subject.sector_id,
              ...iconData
            };
          });
        } else {
          console.error('Failed to load subjects');
        }
      } catch (error) {
        console.error('Error loading subjects:', error);
      } finally {
        this.loading = false;
      }
    },
    selectSubject(subject) {
      // Navigate to mock test practice with subject parameter
      this.$router.push({
        path: '/mock-test-practice',
        query: { subject: subject.name }
      });
    }
  }
};
</script>

<style scoped>
/* Subject Card Styles */
.subject-card {
  perspective: 1000px;
}

.subject-inner {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 24px 16px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 
    0 10px 30px -10px rgba(0, 0, 0, 0.15),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.subject-inner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #8b5cf6, #ec4899);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
  border-radius: 20px 20px 0 0;
}

/* Hover effects */
.subject-card:hover .subject-inner {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 25px 50px -15px rgba(0, 0, 0, 0.2),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
}

.subject-card:hover .subject-inner::before {
  transform: scaleX(1);
}

/* Icon */
.subject-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.subject-card:hover .subject-icon {
  transform: scale(1.1) rotate(3deg);
}

/* Subject name */
.subject-name {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 6px;
}

/* Question count */
.subject-count {
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 2px;
}

/* Exam count */
.exam-count {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Animation for page load */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.subject-card {
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

.subject-card:nth-child(1) { animation-delay: 0.05s; }
.subject-card:nth-child(2) { animation-delay: 0.1s; }
.subject-card:nth-child(3) { animation-delay: 0.15s; }
.subject-card:nth-child(4) { animation-delay: 0.2s; }
.subject-card:nth-child(5) { animation-delay: 0.25s; }
.subject-card:nth-child(6) { animation-delay: 0.3s; }
.subject-card:nth-child(7) { animation-delay: 0.35s; }
.subject-card:nth-child(8) { animation-delay: 0.4s; }

/* Responsive */
@media (max-width: 768px) {
  .subject-inner {
    padding: 20px 12px;
  }
  
  .subject-icon {
    width: 52px;
    height: 52px;
  }
  
  .subject-icon span {
    font-size: 1.5rem;
  }
  
  .subject-name {
    font-size: 0.9rem;
  }
}
</style>
