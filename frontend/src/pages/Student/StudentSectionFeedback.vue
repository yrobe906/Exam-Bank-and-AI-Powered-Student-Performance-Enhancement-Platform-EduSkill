<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- EduSkill Header -->
    <EduskillHeader />

    <!-- Mobile Overlay -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 bg-black/50 z-40 lg:hidden"
      @click="closeSidebar"
    ></div>

    <div class="flex">
      <!-- Sidebar with Independent Scroll -->
      <div 
        :class="[
          'fixed lg:relative z-50 lg:z-auto transition-transform duration-300',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
      class="h-[calc(100vh_-_80px)] lg:h-screen overflow-y-auto">
          <SidebarStud @close-sidebar="closeSidebar" />
        </div>

      <!-- Main Content with Independent Scroll -->
      <main class="flex-1 p-4 md:p-8 w-full lg:w-auto">
        <div class="h-[calc(100vh_-_80px)] overflow-y-auto pr-2 scroll-smooth">
        <!-- Page Header -->
        <div class="mb-8">
          <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
            📊 Section Feedback & Ratings
          </h1>
          <p class="text-gray-600 mt-2 text-sm md:text-base">
            Help us improve! Rate sections and share anonymous feedback.
          </p>
        </div>

        <!-- Feedback Counter Banner -->
        <div class="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-2xl p-4 md:p-6 mb-6 text-white shadow-lg">
          <div class="flex items-center justify-between flex-wrap gap-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                <span class="text-2xl">💬</span>
              </div>
              <div>
                <p class="font-semibold text-lg">{{ feedbackStats.today_feedbacks }} students shared feedback today</p>
                <p class="text-white/80 text-sm">{{ feedbackStats.total_feedbacks }} total feedbacks</p>
              </div>
            </div>
            <div class="flex items-center gap-2 bg-white/20 px-4 py-2 rounded-xl">
              <span class="text-2xl">🔒</span>
              <span class="font-medium">Your identity is protected</span>
            </div>
          </div>
        </div>

        <!-- Grade Filter Pills -->
        <div class="mb-6">
          <div class="flex items-center gap-2 mb-3">
            <span class="text-gray-700 font-medium">Filter by Grade:</span>
          </div>
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="grade in [9, 10, 11, 12]" 
              :key="grade"
              @click="setGradeFilter(grade)"
              :class="[
                'px-4 py-2 rounded-full font-medium transition-all duration-300 transform hover:scale-105',
                selectedGrade === grade 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/30' 
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
              ]"
            >
              Grade {{ grade }}
            </button>
            <button 
              @click="setGradeFilter(null)"
              :class="[
                'px-4 py-2 rounded-full font-medium transition-all duration-300 transform hover:scale-105',
                selectedGrade === null 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/30' 
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
              ]"
            >
              All Grades
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="bg-white rounded-2xl p-6 shadow-lg animate-pulse">
            <div class="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div class="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div class="h-3 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="sections.length === 0" class="text-center py-16">
          <div class="text-6xl mb-4">📭</div>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">No Sections Found</h3>
          <p class="text-gray-600">No sections available for the selected grade level.</p>
        </div>

        <!-- Sections Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div 
            v-for="section in sections" 
            :key="section.section_id"
            @click="selectSection(section)"
            :class="[
              'bg-white rounded-2xl p-6 shadow-lg cursor-pointer transition-all duration-300 transform hover:scale-[1.02] hover:shadow-xl',
              selectedSection?.section_id === section.section_id 
                ? 'ring-4 ring-blue-500 ring-offset-2' 
                : ''
            ]"
          >
            <!-- Section Header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-3">
                <div :class="getSubjectColorClass(section.sector_name)" class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl">
                  {{ getSubjectIcon(section.sector_icon, section.sector_name) }}
                </div>
                <div>
                  <h3 class="font-bold text-gray-800">{{ section.section_name }}</h3>
                  <p class="text-sm text-gray-500">{{ section.sector_name }}</p>
                </div>
              </div>
              <span class="text-xs font-medium px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
                Grade {{ section.grade_level }}
              </span>
            </div>

            <!-- Exam Title -->
            <p class="text-sm text-gray-600 mb-4">
              📝 {{ section.exam_title }}
            </p>

            <!-- Rating Display -->
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="flex">
                  <span v-for="star in 5" :key="star" class="text-lg">
                    <svg 
                      :class="star <= Math.round(section.average_rating) ? 'text-yellow-400' : 'text-gray-300'"
                      class="w-5 h-5" 
                      fill="currentColor" 
                      viewBox="0 0 20 20"
                    >
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                  </span>
                </div>
                <span class="text-sm font-medium text-gray-700">{{ section.average_rating }}</span>
              </div>
              <span class="text-xs text-gray-500">{{ section.total_ratings }} ratings</span>
            </div>

            <!-- User's Rating Badge -->
            <div v-if="section.user_rating" class="mt-3 pt-3 border-t border-gray-100">
              <span class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">
                ⭐ You rated: {{ section.user_rating }}/5
              </span>
            </div>

            <!-- My Feedback Cards -->
            <div v-if="myFeedback.length > 0" class="mt-4 pt-4 border-t border-gray-100">
              <h4 class="font-semibold text-gray-800 mb-3 text-sm flex items-center gap-2">
                💬 My Feedback ({{ myFeedback.length }})
              </h4>
              <div v-for="feedback in myFeedback" :key="feedback.id" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-3 mb-2 last:mb-0 border">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-1">
                      <div class="flex">
                        <svg v-for="star in 5" :key="`fb-${star}`" class="w-4 h-4" :class="star <= feedback.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24 .588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3 .921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784 .57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81 .588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                      </div>
                      <span class="text-xs font-medium text-gray-700">{{ feedback.rating }}/5</span>
                    </div>
                    <p class="text-xs text-gray-600 line-clamp-2">{{ feedback.feedback_text }}</p>
                    <span class="text-xs font-medium mt-1 inline-block" :class="feedback.status === 'reviewed' ? 'text-green-600 bg-green-100 px-2 py-0.5 rounded-full' : 'text-amber-600 bg-amber-100 px-2 py-0.5 rounded-full'">
                      {{ feedback.status === 'reviewed' ? '✅ Reviewed' : '⏳ Pending Review' }}
                    </span>
                  </div>
                  <div class="flex gap-1 ml-2">
                    <button @click="editFeedback(feedback)" class="p-1 text-blue-600 hover:bg-blue-100 rounded transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button @click="deleteFeedback(feedback)" class="p-1 text-red-600 hover:bg-red-100 rounded transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>


        <!-- Rating & Feedback Panel -->
        <div v-if="selectedSection" class="bg-white rounded-3xl shadow-xl p-6 md:p-8 animate-fade-in">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl md:text-2xl font-bold text-gray-800">
              Rate: {{ selectedSection.section_name }}
            </h2>
            <button 
              @click="selectedSection = null"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Star Rating -->
          <div class="mb-8">
            <label class="block text-gray-700 font-medium mb-3">Your Rating</label>
            <div class="flex items-center gap-2">
              <button 
                v-for="star in 5" 
                :key="star"
                @mouseenter="hoverRating = star"
                @mouseleave="hoverRating = 0"
                @click="setRating(star)"
                class="transform transition-all duration-200 hover:scale-110"
                :class="{ 'animate-bounce': hoverRating === star }"
              >
                <svg 
                  :class="star <= (hoverRating || userRating) ? 'text-yellow-400' : 'text-gray-300'"
                  class="w-10 h-10 md:w-12 md:h-12" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </button>
              <span v-if="userRating" class="ml-3 text-lg font-medium text-gray-700">
                {{ userRating }}/5 stars
              </span>
            </div>
          </div>

          <!-- Feedback Text Area -->
          <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-3">
              Share Your Feedback (Optional)
              <span class="text-gray-400 font-normal text-sm ml-2">- Max 500 characters</span>
            </label>
            <textarea 
              v-model="feedbackText"
              maxlength="500"
              rows="4"
              placeholder="What did you like? What can be improved? Your feedback helps us grow!"
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all resize-none"
            ></textarea>
            <div class="text-right text-sm text-gray-500 mt-1">
              {{ feedbackText.length }}/500
            </div>
          </div>

          <!-- Anonymous Toggle -->
          <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 mb-6 border border-green-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <span class="text-xl">🔒</span>
                </div>
                <div>
                  <p class="font-medium text-gray-800">Send Anonymously</p>
                  <p class="text-sm text-gray-500">Your identity will be protected</p>
                </div>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input 
                  type="checkbox" 
                  v-model="isAnonymous" 
                  class="sr-only peer"
                  checked
                >
                <div class="w-14 h-7 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-green-500"></div>
              </label>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            @click="submitFeedback"
            :disabled="submitting"
            :class="[
              'w-full py-4 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-[1.02]',
              submitting 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-500 text-white shadow-lg hover:shadow-xl'
            ]"
          >
            <span v-if="submitting" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else class="flex items-center justify-center gap-2">
              <span>🚀</span>
              Submit Feedback
            </span>
          </button>
        </div>

        <!-- Success Message -->
        <div v-if="showSuccess" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/50" @click="showSuccess = false"></div>
          <div class="bg-white rounded-3xl p-8 max-w-md w-full text-center shadow-2xl animate-scale-in relative overflow-hidden">
            <!-- Confetti -->
            <div class="confetti-container">
              <div v-for="i in 50" :key="i" class="confetti" :style="getConfettiStyle(i)"></div>
            </div>
            
            <div class="text-6xl mb-4">🎉</div>
            <h2 class="text-2xl font-bold text-gray-800 mb-2">Thank You!</h2>
            <p class="text-gray-600 mb-6">Your feedback has been submitted successfully.</p>
            <button 
              @click="showSuccess = false"
              class="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-xl font-bold hover:shadow-lg transition-all"
            >
              Continue
            </button>
          </div>
        </div>

        <!-- Edit Feedback Modal -->
        <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div class="bg-white rounded-3xl p-6 md:p-8 max-w-md w-full shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-bold text-gray-800">Edit Your Feedback</h3>
              <button @click="cancelEditFeedback" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            
            <div v-if="editingFeedback" class="space-y-4">
              <!-- Stars -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Rating</label>
                <div class="flex items-center gap-2">
                  <button v-for="star in 5" :key="star" @click="editRating = star" 
                    :class="['w-10 h-10 rounded-lg transition-all hover:scale-110', star <= editRating ? 'bg-yellow-400 text-white' : 'bg-gray-200 text-gray-500']">
                    ⭐
                  </button>
                  <span class="ml-3 text-sm font-medium">{{ editRating }}/5</span>
                </div>
              </div>

              <!-- Text -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Feedback</label>
                <textarea v-model="editFeedbackText" rows="4" maxlength="500" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                  placeholder="Update your feedback..."></textarea>
                <div class="text-right text-xs text-gray-500 mt-1">{{ editFeedbackText.length }}/500</div>
              </div>

              <!-- Actions -->
              <div class="flex gap-3 pt-4">
                <button @click="cancelEditFeedback" class="flex-1 px-4 py-2 text-gray-700 bg-gray-200 rounded-xl hover:bg-gray-300 transition">
                  Cancel
                </button>
                <button @click="saveEditFeedback" :disabled="!editRating && !editFeedbackText.trim()" 
                  class="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl hover:shadow-lg transition font-medium disabled:opacity-50">
                  Save Changes
                </button>
              </div>
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
import EduskillHeader from '@/components/Header/EduskillHeader.vue';
import SidebarStud from '@/components/SidebarStud.vue';
import FooterStud from '@/components/FooterStud.vue';

export default {
  name: 'StudentSectionFeedback',
  components: {
    EduskillHeader,
    SidebarStud,
    FooterStud
  },
  data() {
    return {
      sidebarOpen: false,
      loading: true,
      sections: [],
      selectedSection: null,
      selectedGrade: null,
      userRating: 0,
      hoverRating: 0,
      feedbackText: '',
      isAnonymous: true,
      submitting: false,
      showSuccess: false,
      feedbackStats: {
        total_feedbacks: 0,
        today_feedbacks: 0,
        anonymous_count: 0
      },
      studentGrade: null,
      myFeedback: [],
      editingFeedback: null,
      showEditModal: false,
      editRating: 0,
      editFeedbackText: ''
    };
  },
  computed: {
    allSections: {
      get() {
        return this.sections;
      },
      set(value) {
        this.sections = value;
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
    setGradeFilter(grade) {
      this.selectedGrade = grade;
      this.filterSections();
    },
    filterSections() {
      if (this.allSections.length === 0) return;
      if (!this.selectedGrade) {
        this.sections = [...this.allSections];
      } else {
        this.sections = this.allSections.filter(section => section.grade_level === this.selectedGrade);
      }
    },
    async loadSections() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        if (!token) throw new Error('No token found');
        
        const response = await fetch('http://127.0.0.1:8000/api/section-feedback/sections', {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          this.allSections = await response.json();
          this.filterSections();
          if (this.allSections.length > 0) {
            this.studentGrade = this.allSections[0].grade_level;
          }
        } else {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Failed to load sections');
        }
      } catch (error) {
        console.error('Error loading sections:', error);
        alert(`Failed to load sections: ${error.message}`);
        this.sections = [];
      } finally {
        this.loading = false;
      }
    },
    async loadFeedbackStats() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:8000/api/section-feedback/stats', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const stats = await response.json();
          this.feedbackStats = {
            total_feedbacks: stats.total_feedbacks || 0,
            today_feedbacks: stats.today_feedbacks || 0,
            anonymous_count: stats.anonymous_count || 0
          };
        }
      } catch (error) {
        console.error('Error loading stats:', error);
        this.feedbackStats = { total_feedbacks: 0, today_feedbacks: 0, anonymous_count: 0 };
      }
    },
    selectSection(section) {
      this.selectedSection = section;
      this.userRating = section.user_rating || 0;
      this.loadMyFeedback(section.section_id);
    },
    async loadMyFeedback(sectionId) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/my-feedback?section_id=${sectionId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          this.myFeedback = await response.json();
        } else {
          this.myFeedback = [];
        }
      } catch (error) {
        console.error('Error loading my feedback:', error);
        this.myFeedback = [];
      }
    },
    setRating(rating) {
      this.userRating = rating;
    },
    editFeedback(feedback) {
      this.editingFeedback = feedback;
      this.editRating = feedback.rating || 0;
      this.editFeedbackText = feedback.feedback_text || '';
      this.showEditModal = true;
    },
    async deleteFeedback(fb) {
      if (!confirm(`Delete feedback "${fb.feedback_text?.substring(0, 30)}..."?`)) return;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/my-feedback/${fb.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          this.myFeedback = this.myFeedback.filter(f => f.id !== fb.id);
        } else {
          alert('Delete failed');
        }
      } catch (error) {
        console.error('Delete error:', error);
        alert('Delete failed');
      }
    },
    async saveEditFeedback() {
      if (!this.editingFeedback) return;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/my-feedback/${this.editingFeedback.id}`, {
          method: 'PUT',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            rating: this.editRating > 0 ? this.editRating : null,
            feedback_text: this.editFeedbackText.trim() || null
          })
        });
        if (response.ok) {
          const updated = await response.json();
          const index = this.myFeedback.findIndex(f => f.id === updated.id);
          if (index !== -1) this.myFeedback[index] = updated;
          this.cancelEditFeedback();
        } else {
          alert('Update failed');
        }
      } catch (error) {
        console.error('Update error:', error);
        alert('Update failed');
      }
    },
    cancelEditFeedback() {
      this.editingFeedback = null;
      this.editRating = 0;
      this.editFeedbackText = '';
      this.showEditModal = false;
    },
    async submitFeedback() {
      if (!this.selectedSection) return;
      if (this.userRating === 0 && !this.feedbackText.trim()) {
        alert('Please rate or write feedback');
        return;
      }
      this.submitting = true;
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:8000/api/section-feedback/feedback/${this.selectedSection.section_id}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            rating: this.userRating || null,
            feedback_text: this.feedbackText.trim() || null,
            is_anonymous: this.isAnonymous
          })
        });
        if (response.ok) {
          this.showSuccess = true;
          this.userRating = 0;
          this.feedbackText = '';
          await Promise.all([this.loadSections(), this.loadFeedbackStats()]);
        } else {
          const err = await response.json();
          alert(err.detail || 'Submit failed');
        }
      } catch (error) {
        alert('Submit failed - backend may not be running');
      } finally {
        this.submitting = false;
      }
    },
    getSubjectIcon(icon, subject) {
      if (icon) return icon;
      const map = {
        'Mathematics': '🔢', 'Physics': '⚛️', 'Chemistry': '🧪', 'Biology': '🧬',
        'English': '📚', 'History': '🏛️', 'Geography': '🌍', 'Economics': '💰', 'Civics': '⚖️'
      };
      return map[subject] || '📖';
    },
    getSubjectColorClass(subject) {
      const map = {
        'Mathematics': 'bg-blue-100', 'Physics': 'bg-purple-100', 'Chemistry': 'bg-green-100',
        'Biology': 'bg-emerald-100', 'English': 'bg-yellow-100', 'History': 'bg-amber-100',
        'Geography': 'bg-cyan-100', 'Economics': 'bg-green-100', 'Civics': 'bg-indigo-100'
      };
      return map[subject] || 'bg-gray-100';
    },
    getConfettiStyle(i) {
      const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#dfe6e9'];
      return {
        left: `${(i * 3.6) % 100}%`,
        backgroundColor: colors[i % colors.length],
        animationDelay: `${i % 2}s`,
        animationDuration: `${2 + i % 3}s`
      };
    }
  },
  async mounted() {
    await Promise.all([this.loadSections(), this.loadFeedbackStats()]);
  }
}
</script>

<style scoped>
.animate-fade-in { animation: fadeIn .3s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-scale-in { animation: scaleIn .3s ease-out; }
@keyframes scaleIn { from { opacity: 0; transform: scale(.9); } to { opacity: 1; transform: scale(1); } }
.confetti-container { position: absolute; top: 0; left: 0; right: 0; bottom: 0; overflow: hidden; pointer-events: none; z-index: -1; }
.confetti { position: absolute; width: 10px; height: 10px; top: -10px; border-radius: 2px; animation: confettiFall 3s ease-in-out forwards; }
@keyframes confettiFall { 0% { top: -10px; transform: rotate(0); } 100% { top: 100%; transform: rotate(720deg); } }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: linear-gradient(to bottom, #f1f5f9, #e2e8f0); }
::-webkit-scrollbar-thumb { background: linear-gradient(to bottom, #3b82f6, #8b5cf6); border-radius: 4px; }
</style>
