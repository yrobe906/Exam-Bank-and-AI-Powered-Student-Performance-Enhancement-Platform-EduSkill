<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50/30">
    <!-- Enhanced Header -->
    <HeaderStud @toggle-sidebar="toggleSidebar" />

    <div class="flex">
      <!-- Modern Sidebar with Independent Scroll -->
      <div 
        :class="[
          'fixed lg:relative z-50 lg:z-auto transition-transform duration-300',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
      >
        <div class="h-[calc(100vh-80px)] lg:h-screen overflow-y-auto">
          <SidebarStud />
        </div>
      </div>

      <!-- Main Content with Independent Scroll -->
      <main class="flex-1 p-4 md:p-8 w-full">
        <!-- Scroll Container for Main Content -->
        <div class="h-[calc(100vh-80px)] lg:h-[calc(100vh-60px)] overflow-y-auto pr-2 scroll-smooth">
        
        <!-- Page Title -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">Available Mock Tests</h1>
          <p class="text-gray-600">Choose from a variety of mock exams to test your knowledge</p>
        </div>
        
        <!-- Filters Section -->
        <div class="flex flex-col lg:flex-row gap-6 mb-8">
          <!-- Left Sidebar - Categories -->
          <div class="lg:w-72 bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl p-6 h-fit border border-white/50">
            <h3 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Filters
            </h3>
            
            <!-- Real Sector Categories from API -->
            <div class="space-y-4">
              <div v-for="sector in sectorData" :key="sector.id" 
                   class="sector-item group cursor-pointer p-3 rounded-xl hover:bg-blue-50 transition-all duration-300"
                   @click="filterByCategory(sector.name)"
                   :class="{'bg-blue-50 border-l-4 border-blue-500': selectedCategory === sector.name}">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <span class="text-2xl transition-transform duration-300 group-hover:scale-110">{{ sector.icon }}</span>
                    <span class="text-sm font-medium text-gray-700 group-hover:text-blue-700 transition-colors">{{ sector.name }}</span>
                  </div>
                  <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium">
                    {{ sector.examCount }} exams
                  </span>
                </div>
                <div class="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-blue-400 to-blue-600 rounded-full transition-all duration-500" 
                       :style="{ width: sector.percentage + '%' }"></div>
                </div>
              </div>
            </div>
            
            <!-- Category List -->
            <div class="mt-6 pt-4 border-t border-gray-100">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">All Categories</span>
                <button v-if="selectedCategory" @click="clearFilter" class="text-xs text-blue-600 hover:text-blue-700">Clear</button>
              </div>
              <div class="space-y-1 max-h-48 overflow-y-auto">
                <div v-for="cat in sectorNames" :key="cat" 
                     class="flex items-center gap-2 text-sm py-2 px-2 rounded-lg hover:bg-gray-50 cursor-pointer transition-all duration-200"
                     :class="{'text-blue-600 bg-blue-50': selectedCategory === cat}"
                     @click="filterByCategory(cat)">
                  <span class="w-1.5 h-1.5 rounded-full transition-colors duration-200"
                        :class="selectedCategory === cat ? 'bg-blue-500' : 'bg-gray-300'"></span>
                  {{ cat }}
                </div>
              </div>
            </div>
            
            <!-- Search Box -->
            <div class="mt-6">
              <div class="relative">
                <input type="text" 
                       v-model="searchQuery"
                       @input="searchTests"
                       placeholder="Search by exam name..."
                       class="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all duration-300 pl-10">
                <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </div>
          
          <!-- Right Side - Test Cards -->
          <div class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Test Card -->
            <div 
              v-for="(test, index) in filteredTests" 
              :key="test.id"
              class="test-card group bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg p-6 border border-white/50 hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 cursor-pointer"
              :style="{ animationDelay: (index * 0.1) + 's' }"
              @click="startTest(test)"
            >
              <!-- Decorative gradient line -->
              <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 rounded-t-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              
              <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                  <h3 class="font-bold text-gray-800 text-lg mb-1 group-hover:text-blue-700 transition-colors duration-300 line-clamp-2">{{ test.title }}</h3>
                  <p class="text-sm text-gray-500 flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    {{ test.authority }}
                  </p>
                </div>
                <div class="flex flex-col items-end gap-1">
                  <!-- Pricing Badge with Amount -->
                  <div v-if="test.pricing_type === 'Premium'" class="flex flex-col items-end">
                    <span :class="getPricingClass(test.pricing_type)" class="px-3 py-1 rounded-full text-xs font-semibold shadow-sm flex items-center gap-1">
                      <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.736 6.979C9.208 6.193 9.696 6 10 6c.304 0 .792.193 1.264.979a1 1 0 001.715-1.029C12.279 4.784 11.232 4 10 4s-2.279.784-2.979 1.95c-.285.475-.507 1-.67 1.55H6a1 1 0 000 2h.013a9.358 9.358 0 010 1H6a1 1 0 100 2h.351c.163.55.385 1.075.67 1.55C7.721 15.216 8.768 16 10 16s2.279-.784 2.979-1.95a1 1 0 10-1.715-1.029c-.472.786-.96.979-1.264.979-.304 0-.792-.193-1.264-.979a4.265 4.265 0 01-.264-.521H10a1 1 0 100-2H8.017a7.36 7.36 0 010-1H10a1 1 0 100-2H8.472c.08-.185.167-.36.264-.521z"/>
                      </svg>
                      Premium
                    </span>
                    <span class="text-xs font-bold text-purple-600 mt-1">{{ test.amount }} ETB</span>
                  </div>
                  <span v-else :class="getPricingClass(test.pricing_type)" class="px-3 py-1 rounded-full text-xs font-semibold shadow-sm flex items-center gap-1">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                    Free
                  </span>
                  <span :class="getDifficultyClass(test.difficulty)" class="px-3 py-1 rounded-full text-xs font-semibold shadow-sm">
                    {{ test.difficulty }}
                  </span>
                </div>
              </div>
              
              <div class="grid grid-cols-3 gap-3 mb-4">
                <div class="bg-gray-50 rounded-lg p-2 text-center group-hover:bg-blue-50 transition-colors duration-300">
                  <div class="text-lg font-bold text-gray-800">{{ test.questions }}</div>
                  <div class="text-xs text-gray-500">Questions</div>
                </div>
                <div class="bg-gray-50 rounded-lg p-2 text-center group-hover:bg-purple-50 transition-colors duration-300">
                  <div class="text-lg font-bold text-gray-800">{{ test.time }}</div>
                  <div class="text-xs text-gray-500">Minutes</div>
                </div>
                <div class="bg-gray-50 rounded-lg p-2 text-center group-hover:bg-green-50 transition-colors duration-300">
                  <div class="text-lg font-bold text-gray-800">{{ test.marks }}</div>
                  <div class="text-xs text-gray-500">Marks</div>
                </div>
              </div>
              
              <!-- Smart button based on access status -->
              <template v-if="test.pricing_type === 'Premium'">
                <div v-if="checkingUnlocked" class="w-full py-3 bg-gray-100 rounded-xl flex items-center justify-center">
                  <div class="w-6 h-6 border-2 border-purple-200 border-t-purple-500 rounded-full animate-spin"></div>
                  <span class="ml-2 text-sm text-gray-600 font-medium">Checking access...</span>
                </div>
                <button v-else-if="unlockedExams[test.id]" @click.stop="startTest(test)" class="w-full py-3 bg-gradient-to-r from-emerald-500 via-green-600 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:via-green-700 hover:to-emerald-700 transition-all duration-300 font-semibold flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>✅ Start Test (Unlocked!)</span>
                </button>
                <button v-else class="w-full py-3 bg-gradient-to-r from-purple-500 via-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-600 hover:via-purple-700 hover:to-pink-700 transition-all duration-300 font-semibold flex items-center justify-center gap-2 shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  <span>Subscribe to Access</span>
                </button>
              </template>
              <button v-else class="w-full py-3 bg-gradient-to-r from-blue-500 via-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-600 hover:via-blue-700 hover:to-purple-700 transition-all duration-300 font-semibold flex items-center justify-center gap-2 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40">
                <span>Start Test</span>
                <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </button>
            </div>
            
            <!-- Loading State -->
            <div v-if="loading" class="col-span-2 text-center py-16">
              <div class="relative">
                <div class="w-16 h-16 border-4 border-blue-100 border-t-blue-500 rounded-full animate-spin"></div>
                <div class="absolute inset-0 w-16 h-16 border-4 border-purple-100 border-t-purple-500 rounded-full animate-spin" style="animation-delay: 0.2s"></div>
              </div>
              <p class="mt-4 text-gray-600 font-medium">Loading tests...</p>
            </div>
            
            <!-- Empty State -->
            <div v-if="!loading && filteredTests.length === 0" class="col-span-2 text-center py-16 bg-white/50 rounded-2xl border-2 border-dashed border-gray-200">
              <svg class="w-20 h-20 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 class="text-xl font-semibold text-gray-700 mb-2">No tests found</h3>
              <p class="text-gray-500">Try adjusting your filters or search query</p>
            </div>
          </div>
        </div>
        </div>
        </main>
      </div>

    <FooterStud />

    <!-- Premium Exam Warning Modal -->
    <div v-if="showPremiumModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl p-8 max-w-md mx-4 text-center">
        <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Premium Exam</h3>
        <p class="text-gray-600 mb-2">This is a premium exam that requires a subscription.</p>
        <p class="text-lg font-semibold text-purple-600 mb-6">Price: {{ premiumExamAmount }} ETB</p>
        <div class="flex gap-3">
          <button @click="showPremiumModal = false" class="flex-1 py-3 px-4 border border-gray-300 rounded-xl text-gray-700 hover:bg-gray-50 transition-colors">
            Cancel
          </button>
          <button @click="goToSubscription" class="flex-1 py-3 px-4 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-colors font-semibold">
            Subscribe Now
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderStud from '@/components/HeaderStud.vue'
import SidebarStud from '@/components/SidebarStud.vue'
import FooterStud from '@/components/FooterStud.vue'
import api from '@/services/api'
import unlockApi from '@/services/unlockApi.js'

const API_URL = 'http://127.0.0.1:8000'

const sectorIcons = {
  'Natural Science': '🔬',
  'Social Science': '🌍',
  'Mathematics': '📐',
  'Information Technology': '💻',
  'Language': '📝',
}

export default {
  name: 'AvailableTests',
  components: {
    HeaderStud,
    SidebarStud,
    FooterStud
  },
  data() {
    return {
      sidebarOpen: false,
      loading: false,
      searchQuery: '',
      selectedCategory: null,
      sectorData: [],
      sectorNames: [],
      allTests: [],
      filteredTests: [],
      showPremiumModal: false,
      premiumExamAmount: 0,
      selectedPremiumExam: null,
      checkingUnlocked: false,
      unlockedExams: {},
      accessCache: new Map(),
      accessLoading: new Set()
    }
  },
  async mounted() {
    await this.fetchSectors()
    await this.fetchTests()
    // Check initial query for unlock refresh
    const query = this.$route.query;
    if (query.unlockRefresh || localStorage.getItem('unlockRefresh')) {
      localStorage.removeItem('unlockRefresh');
      this.accessCache.clear();
      this.unlockedExams = {};
      console.log('🔓 UNLOCK REFRESH triggered for exam:', query.examId);
      await this.fetchTests();
      await this.checkPremiumAccess(query.examId);  // Pass specific examId
      this.$router.replace({ query: null });
    }
  },
  watch: {
    '$route'(to, from) {
      const query = to.query;
      if (query.unlockRefresh) {
        this.accessCache.clear();
        this.unlockedExams = {};
        console.log('🔓 Route unlockRefresh:', query.examId);
        this.fetchTests();
        this.checkPremiumAccess(query.examId);
        this.$router.replace({ query: null });
      }
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    closeSidebar() {
      this.sidebarOpen = false;
    },
    async fetchSectors() {
      try {
        const response = await fetch(`${API_URL}/api/sectors`)
        if (response.ok) {
          const sectors = await response.json()
          
          const sectorDataPromises = sectors.map(async (sector) => {
            const examResponse = await fetch(`${API_URL}/api/exams?sector_id=${sector.id}`)
            let examCount = 0
            let questionCount = 0
            
            if (examResponse.ok) {
              const exams = await examResponse.json()
              examCount = exams.length
              for (const exam of exams) {
                questionCount += exam.total_questions || 0
              }
            }
            
            return {
              id: sector.id,
              name: sector.name,
              icon: sectorIcons[sector.name] || '📚',
              examCount: examCount,
              questionCount: questionCount,
              percentage: Math.min(100, (examCount / 10) * 100)
            }
          })
          
          this.sectorData = await Promise.all(sectorDataPromises)
          this.sectorNames = sectors.map(s => s.name)
        }
      } catch (error) {
        console.error('Error fetching sectors:', error)
        this.sectorData = []
      }
    },
    
async fetchTests() {
      this.loading = true
      try {
        const response = await api.get('/api/student/available-tests')
        console.log('Available tests response:', response)
        
        if (response && (response.exams || Array.isArray(response))) {
          this.allTests = response.exams || response
        } else {
          console.warn('Unexpected API response format:', response)
          this.allTests = []
        }
        
        console.log(`Loaded ${this.allTests.length} tests`)
        // Check access for premium exams
        await this.checkPremiumAccess()
        
        this.applyFilters()
      } catch (error) {
        console.error('Error fetching tests:', error)
        this.allTests = []
        this.$toast?.error('Failed to load tests. Please refresh.')
        this.applyFilters()
      } finally {
        this.loading = false
      }
    },

    async checkHasAccess(examId) {
      // Check cache first
      if (this.accessCache.has(examId)) {
        return this.accessCache.get(examId)
      }
      
      // Check if already loading
      if (this.accessLoading.has(examId)) {
        return false
      }
      
      this.accessLoading.add(examId)
      
      try {
        const response = await unlockApi.hasAccess(api, examId)
        const hasAccess = response?.data?.has_access ?? false
        
        // Cache for 30s
        this.accessCache.set(examId, hasAccess)
        setTimeout(() => this.accessCache.delete(examId), 30000)
        
        return hasAccess
      } catch (error) {
        console.error('hasAccess error:', error)
        return false
      } finally {
        this.accessLoading.delete(examId)
      }
    },
    
    filterByCategory(category) {
      if (this.selectedCategory === category) {
        this.selectedCategory = null
      } else {
        this.selectedCategory = category
      }
      this.applyFilters()
    },
    
    clearFilter() {
      this.selectedCategory = null
      this.applyFilters()
    },
    
    searchTests() {
      this.applyFilters()
    },
    
    applyFilters() {
      this.filteredTests = this.allTests.filter(test => {
        // Category filter
        if (this.selectedCategory && test.category !== this.selectedCategory) {
          return false
        }
        
        // Search filter
        if (this.searchQuery && !test.title.toLowerCase().includes(this.searchQuery.toLowerCase())) {
          return false
        }
        
        return test.is_published !== false
      })
    },
    
async checkPremiumAccess(specificExamId = null) {
      const premiumExams = this.allTests.filter(test => test.pricing_type === 'Premium')
      
      if (premiumExams.length === 0) return
      
      this.checkingUnlocked = true
      
      try {
        // Force refresh for specific exam from query
        if (specificExamId) {
          console.log(`🔓 Force refresh hasAccess for exam ${specificExamId}`)
          const specificResult = await unlockApi.hasAccess(api, specificExamId)
          this.unlockedExams[specificExamId] = specificResult?.data?.has_access ?? false
        }
        
        // Batch check all premiums
        const accessPromises = premiumExams.map(test => 
          unlockApi.hasAccess(api, test.id).then(res => ({ id: test.id, hasAccess: res?.data?.has_access ?? false }))
            .catch(() => ({ id: test.id, hasAccess: false }))
        )
        
        const results = await Promise.all(accessPromises)
        results.forEach(({ id, hasAccess }) => {
          this.unlockedExams[id] = hasAccess
        })
        
        console.log('Unlock status updated:', this.unlockedExams)
      } catch (error) {
        console.error('Error checking premium access:', error)
        this.$toast?.error('Access check failed')
      } finally {
        this.checkingUnlocked = false
      }
    },
    
    async startTest(test) {
      console.log('Starting test:', test)

      if (test.pricing_type === 'Premium') {
        // Double-check access for unlocked button clicks
        const hasAccess = await this.checkHasAccess(test.id)
        if (hasAccess) {
          // Direct navigation for unlocked premium
          if (test.difficulty) {
            const difficultyMap = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };
            const difficultyValue = difficultyMap[test.difficulty] || test.difficulty;
            localStorage.setItem('exam_difficulty_filter', difficultyValue.toString());
          }
          this.$router.push(`/take_exam/${test.id}`)
          return
        }
        
        // Show subscription modal for locked premium
        this.selectedPremiumExam = test
        this.premiumExamAmount = test.amount || 0
        this.showPremiumModal = true
        return
      }

      // Free test - direct navigation
      if (test.difficulty) {
        const difficultyMap = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };
        const difficultyValue = difficultyMap[test.difficulty] || test.difficulty;
        localStorage.setItem('exam_difficulty_filter', difficultyValue.toString());
        console.log('Saved difficulty filter:', difficultyValue);
      }
      
      this.$router.push(`/take_exam/${test.id}`)
    },
    
    goToSubscription() {
      this.showPremiumModal = false
      // Navigate to Premium page with exam data
      if (this.selectedPremiumExam) {
        this.$router.push({
          path: '/premium',
          query: {
            examId: this.selectedPremiumExam.id,
            examTitle: this.selectedPremiumExam.title,
            examPrice: this.selectedPremiumExam.amount,
            examType: 'mock_exam',
            authority: this.selectedPremiumExam.authority
          }
        })
      } else {
        this.$router.push('/premium')
      }
    },
    
    getDifficultyClass(difficulty) {
      if (difficulty === 'Hard') {
        return 'bg-red-100 text-red-700'
      } else if (difficulty === 'Medium') {
        return 'bg-yellow-100 text-yellow-700'
      } else {
        return 'bg-green-100 text-green-700'
      }
    },
    
    getPricingClass(pricingType) {
      if (pricingType === 'Premium') {
        return 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 border border-purple-200'
      } else {
        return 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 border border-green-200'
      }
    }
  }
}
</script>

<style scoped>
.test-card {
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

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

.sector-item {
  position: relative;
  overflow: hidden;
}

.sector-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transition: left 0.5s ease;
}

.sector-item:hover::before {
  left: 100%;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #93c5fd, #60a5fa);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #60a5fa, #3b82f6);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

