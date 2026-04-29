<template>
  <div class="take-exam">
    <EduskillHeader />
    
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading your exam...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h2>Something went wrong</h2>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="retryLoad">Try Again</button>
    </div>

    <!-- Empty Exam Message -->
    <div v-else-if="exam && sections.length === 0" class="empty-exam">
      <div class="empty-exam-icon">📭</div>
      <h2>This Card is Empty</h2>
      <p>This exam card has no questions stored yet. Please check back later or contact your teacher.</p>
      <button class="back-btn" @click="goBack">Go Back</button>
    </div>

    <!-- Exam Content -->
    <div v-else-if="exam && sections.length > 0" class="exam-wrapper">
      
      <!-- Already Taken Banner - Beautified -->
      <div v-if="alreadyTaken" class="already-taken-banner">
        <div class="banner-card">
          <div class="banner-icon-wrapper">
            <span class="banner-icon">📊</span>
          </div>
          <div class="banner-content">
            <h3 class="banner-title">You have already taken this exam</h3>
            <div class="score-display-banner">
              <span class="score-label">Your Score</span>
              <span class="score-value">{{ previousScore }} <span class="score-divider">/</span> {{ exam.total_marks }}</span>
            </div>
            <p class="banner-subtitle">Review your answers below or view detailed results</p>
          </div>
          <button class="view-results-btn" @click="goToResults">
            <span class="btn-icon">📈</span>
            View Full Results
          </button>
        </div>
      </div>
      
      <!-- Header with Exam Info & Timer -->
      <div class="exam-header">
        <div class="exam-info">
          <h1 class="exam-title">{{ exam.name }}</h1>
          <div class="exam-meta">
            <span class="meta-badge">
              <span class="meta-icon">📝</span>
              {{ exam.total_questions }} Questions
            </span>
            <span class="meta-badge">
              <span class="meta-icon">⏱️</span>
              {{ exam.duration }} minutes
            </span>
            <span class="meta-badge">
              <span class="meta-icon">🏆</span>
              {{ exam.total_marks }} Marks
            </span>
          </div>
        </div>
        
        <div class="timer-container" :class="{ 'timer-warning': timeLeft <= warningTime }">
          <div class="timer-icon">⏳</div>
          <div class="timer-display">{{ formattedTime }}</div>
          <div class="timer-label">Time Remaining</div>
        </div>
      </div>

      <!-- Main Exam Grid -->
      <div class="exam-grid">
        
        <!-- Left Sidebar - Sections -->
        <div class="sections-sidebar">
          <div class="sidebar-header">
            <h3>Sections</h3>
            <span class="section-count">{{ sections.length }}</span>
          </div>
          
          <div class="sections-list">
            <button
              v-for="section in sections"
              :key="section.id"
              class="section-btn"
              :class="{ 'active-section': currentSection === section.id }"
              :style="{ borderLeftColor: section.color || '#2563eb' }"
              @click="changeSection(section.id)"
            >
              <div class="section-info">
                <span class="section-name">{{ section.name }}</span>
                <span class="question-badge">{{ getSectionProgress(section.id) }}/{{ section.question_count }}</span>
              </div>
              <div class="section-progress">
                <div 
                  class="progress-bar" 
                  :style="{ 
                    width: `${(getSectionProgress(section.id) / section.question_count) * 100}%`,
                    backgroundColor: section.color || '#2563eb'
                  }"
                ></div>
              </div>
            </button>
          </div>

          <!-- Overall Progress -->
          <div class="overall-progress">
            <div class="progress-header">
              <span>Overall Progress</span>
              <span>{{ Object.keys(answers).length }}/{{ exam.total_questions }}</span>
            </div>
            <div class="progress-track">
              <div 
                class="progress-fill" 
                :style="{ width: `${(Object.keys(answers).length / exam.total_questions) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Main Question Area -->
        <div class="question-container">
          <QuestionArea
            v-if="currentQuestion"
            :currentQuestion="currentQuestion"
            :currentQuestionIndex="currentQuestionIndexInSection"
            :totalQuestionsInSection="currentSectionQuestions.length"
            :currentSection="getCurrentSectionName()"
            :sectionColor="getCurrentSectionColor()"
            :selectedOption="getSelectedOptionForCurrentQuestion()"
            :isMarked="isQuestionMarked(currentQuestion.id)"
            :isReviewMode="alreadyTaken"
            :correctAnswer="getCorrectAnswerForCurrentQuestion()"
            :isCorrect="getIsCorrectForCurrentQuestion()"
            @select-option="selectOption"
            @previous="prevQuestion"
            @next="nextQuestion"
            @toggle-mark="toggleMarkForReview"
            @clear-response="clearAnswer"
          />
          
          <!-- Empty State (no questions in section) -->
          <div v-else-if="currentSection" class="empty-section">
            <div class="empty-icon">📭</div>
            <h3>No Questions in This Section</h3>
            <p>This section currently has no questions. Please select another section.</p>
          </div>
        </div>

        <!-- Right Sidebar - Question Palette -->
        <div class="palette-sidebar">
          <div class="palette-header">
            <h3>Question Palette</h3>
            <div class="palette-legend">
              <div class="legend-item">
                <span class="legend-dot answered"></span>
                <span>Answered</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot marked"></span>
                <span>Marked</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot current"></span>
                <span>Current</span>
              </div>
            </div>
          </div>

          <div class="sections-palette">
            <div v-for="section in sections" :key="section.id" class="palette-section">
              <div class="palette-section-title" :style="{ color: section.color || '#2563eb' }">
                {{ section.name }}
                <span class="section-count">{{ getSectionProgress(section.id) }}/{{ section.question_count }}</span>
              </div>
              <div class="palette-grid">
                <button
                  v-for="(question, idx) in section.questions"
                  :key="question.id"
                  class="palette-btn"
                  :class="{
                    'answered': isQuestionAnswered(question.id),
                    'marked': isQuestionMarked(question.id),
                    'current': currentQuestion?.id === question.id
                  }"
                  :style="{
                    backgroundColor: currentQuestion?.id === question.id ? (section.color || '#2563eb') : '',
                    borderColor: isQuestionAnswered(question.id) ? (section.color || '#2563eb') : ''
                  }"
                  @click="jumpToQuestion(section.id, question.id)"
                >
                  {{ idx + 1 }}
                </button>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            class="submit-exam-btn"
            :class="{ 'ready': Object.keys(answers).length === exam.total_questions }"
            @click="showSubmitModal = true"
            :disabled="submitting || alreadyTaken"
          >
            <span class="btn-icon">📋</span>
            <span>{{ submitting ? 'Submitting...' : alreadyTaken ? 'Already Submitted' : 'Submit Exam' }}</span>
          </button>
        </div>

      </div>
    </div>

    <!-- Submit Confirmation Modal -->
    <transition name="modal-fade">
      <div v-if="showSubmitModal" class="modal-overlay" @click.self="showSubmitModal = false">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Submit Exam</h3>
            <button class="close-btn" @click="showSubmitModal = false">✕</button>
          </div>
          <div class="modal-body">
            <div class="submission-summary">
              <div class="summary-item">
                <span class="summary-label">Answered</span>
                <span class="summary-value">{{ Object.keys(answers).length }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Unanswered</span>
                <span class="summary-value">{{ exam.total_questions - Object.keys(answers).length }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">Marked for Review</span>
                <span class="summary-value">{{ markedQuestions.size }}</span>
              </div>
            </div>
            <p class="warning-text" v-if="Object.keys(answers).length < exam.total_questions">
              ⚠️ You have {{ exam.total_questions - Object.keys(answers).length }} unanswered questions.
            </p>
          </div>
          <div class="modal-footer">
            <button class="modal-btn cancel" @click="showSubmitModal = false">Cancel</button>
            <button class="modal-btn confirm" @click="submitExam">Yes, Submit</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Time Warning Modal -->
    <transition name="modal-fade">
      <div v-if="showTimeWarning" class="modal-overlay" @click.self="showTimeWarning = false">
        <div class="modal-content warning">
          <div class="modal-header">
            <h3>⚠️ Time is Running Out!</h3>
          </div>
          <div class="modal-body">
            <p>You have <strong>{{ Math.floor(timeLeft / 60) }} minutes</strong> remaining (10% of total time). Please save your answers and submit soon.</p>
          </div>
          <div class="modal-footer">
            <button class="modal-btn primary" @click="showTimeWarning = false">Continue</button>
            <button class="modal-btn confirm" @click="submitExam">Submit Now</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Success Modal -->
    <transition name="modal-fade">
      <div v-if="showSuccessModal" class="modal-overlay">
        <div class="modal-content success">
          <div class="modal-header">
            <h3>✅ Exam Submitted Successfully!</h3>
          </div>
          <div class="modal-body">
            <p>{{ successMessage }}</p>
            <div class="loading-indicator">
              <div class="spinner"></div>
              <span>Redirecting to results...</span>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Subscription Warning Modal -->
    <transition name="modal-fade">
      <div v-if="showSubscriptionModal" class="modal-overlay" @click.self="goBack">
        <div class="modal-content premium-warning">
          <div class="modal-header">
            <h3>🔒 Premium Exam</h3>
          </div>
          <div class="modal-body">
            <div class="premium-icon">💎</div>
            <p class="premium-title">This is a <strong>Premium Exam</strong></p>
            <p class="premium-description">
              You need an active subscription to access this exam. 
              The exam costs <strong>{{ examPricing.amount }} ETB</strong>.
            </p>
            <div class="premium-features">
              <div class="feature-item">
                <span class="check">✓</span>
                <span>Access to all premium exams</span>
              </div>
              <div class="feature-item">
                <span class="check">✓</span>
                <span>Detailed performance analytics</span>
              </div>
              <div class="feature-item">
                <span class="check">✓</span>
                <span>Priority support</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="modal-btn cancel" @click="goBack" :disabled="subscribing">Go Back</button>
            <button class="modal-btn subscribe" @click="goToSubscriptionPremium" :disabled="subscribing">
              <span v-if="subscribing" class="subscribe-loading">
                <span class="loading-dots">Redirecting</span>
              </span>
              <span v-else>Subscribe Now</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>


<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import EduskillHeader from '@/components/Header/EduskillHeader.vue';
import QuestionArea from '@/components/student/exam/QuestionArea.vue';
import api from '@/services/api';

export default {
  name: 'TakeExam',
  components: {
    EduskillHeader,
    QuestionArea
  },
  props: {
    examId: {
      type: [String, Number],
      default: null
    }
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    
    // State
    const loading = ref(true);
    const error = ref(null);
    const submitting = ref(false);
    const showSubmitModal = ref(false);
    const showTimeWarning = ref(false);
    const warningShown = ref(false);
    const showSuccessModal = ref(false);
    const successMessage = ref('');
    
    // Already taken exam state
    const alreadyTaken = ref(false);
    const previousScore = ref(0);
    
    // Subscription check
    const showSubscriptionModal = ref(false);
    const examPricing = ref({ pricing_type: 'Free', amount: 0 });
    const subscribing = ref(false);
    
    const goBack = () => {
      router.push('/available-tests');
    };
    
    const goToSubscription = () => {
      router.push('/subscription');
    };
    
    const goToSubscriptionPremium = () => {
      subscribing.value = true;
      setTimeout(() => {
        router.push('/premium');
      }, 3000);
    };
    
    const goToResults = () => {
      router.push({
        path: '/student/exam-result',
        query: { 
          attemptId: attemptId.value,
          score: previousScore.value,
          total: exam.value.total_questions,
          percentage: Math.round((previousScore.value / exam.value.total_marks) * 100)
        }
      });
    };
    
    const exam = ref(null);
    const sections = ref([]);
    const attemptId = ref(null);
    
    const currentSection = ref(null);
    const currentQuestionId = ref(null);
    
    const answers = reactive({});
    const markedQuestions = ref(new Set());
    
    const timer = ref(null);
    const timeLeft = ref(0);
    const totalTime = ref(0);
    
    // Calculate warning time at 10% of total exam duration

    const warningTime = computed(() => {
      if (!exam.value || !exam.value.duration) return 300; // Default 5 minutes
      return Math.max(Math.floor(exam.value.duration * 60 * 0.1), 60); // 10% or minimum 1 minute
    });
    
    // Format warning time for display
    const formattedWarningTime = computed(() => {
      const mins = Math.floor(warningTime.value / 60);
      const secs = warningTime.value % 60;
      if (mins > 0) {
        return secs > 0 ? `${mins} minute${mins > 1 ? 's' : ''} and ${secs} seconds` : `${mins} minute${mins > 1 ? 's' : ''}`;
      }
      return `${secs} seconds`;
    });
    
    // Computed
    const allQuestions = computed(() => {
      return sections.value.flatMap(section => 
        (section.questions || []).map(q => ({
          ...q,
          sectionId: section.id,
          sectionName: section.name,
          sectionColor: section.color
        }))
      );
    });
    
    const currentQuestion = computed(() => {
      if (!currentQuestionId.value) return null;
      return allQuestions.value.find(q => q.id === currentQuestionId.value) || null;
    });
    
    const currentSectionQuestions = computed(() => {
      const section = sections.value.find(s => s.id === currentSection.value);
      return section ? section.questions : [];
    });
    
    const currentQuestionIndexInSection = computed(() => {
      return currentSectionQuestions.value.findIndex(
        q => q.id === currentQuestionId.value
      );
    });
    
    const formattedTime = computed(() => {
      const mins = Math.floor(timeLeft.value / 60);
      const secs = timeLeft.value % 60;
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    });
    
    // Methods
    const getSectionProgress = (sectionId) => {
      const section = sections.value.find(s => s.id === sectionId);
      if (!section) return 0;
      return section.questions.filter(q => answers[q.id]).length;
    };
    
    const getCurrentSectionName = () => {
      const section = sections.value.find(s => s.id === currentSection.value);
      return section ? section.name : '';
    };
    
    const getCurrentSectionColor = () => {
      const section = sections.value.find(s => s.id === currentSection.value);
      return section ? section.color : '#2563eb';
    };
    
const getSelectedOptionForCurrentQuestion = () => {
      if (!currentQuestionId.value) return null;
      return answers[currentQuestionId.value] || null;
    };
    
    const getCorrectAnswerForCurrentQuestion = () => {
      if (!currentQuestionId.value || !currentQuestion.value) return null;
      return currentQuestion.value.correct_answer || null;
    };
    
    const getIsCorrectForCurrentQuestion = () => {
      if (!currentQuestionId.value || !currentQuestion.value) return null;
      return currentQuestion.value.is_correct || false;
    };
    
const isQuestionAnswered = (questionId) => {
      return !!answers[questionId];
    };
    
    const isQuestionMarked = (questionId) => {
      return markedQuestions.value.has(questionId);
    };
    
    const startExam = async () => {
      loading.value = true;
      error.value = null;
      
      try {
        // Get exam ID from props or route params
        const examId = props.examId || route.params.examId;
        
        if (!examId) {
          throw new Error('No exam ID provided');
        }
        
        console.log(`Starting exam with ID: ${examId}`);
        
        // Get student ID from localStorage (stored by Login.vue)
        // Check both 'student_id' (from Login.vue) and 'user_id' (from UserLogin.vue)
        const storedStudentId = localStorage.getItem('student_id') || localStorage.getItem('user_id');
        
        // FIX 1: Require student_id - do not default to 1
        if (!storedStudentId) {
          throw new Error('You must be logged in to take an exam. Please login first.');
        }
        
        const studentId = parseInt(storedStudentId);
        console.log('Using student_id:', studentId);
        
        // Check for difficulty filter in localStorage (set by Test Configuration in MockExamBuilder)
        const difficultyFilter = localStorage.getItem('exam_difficulty_filter');
        const payload = {
          student_id: studentId
        };
        
        // Add difficulty filter if set
        if (difficultyFilter) {
          payload.difficulty = parseInt(difficultyFilter);
          console.log('Using difficulty filter:', payload.difficulty);
          // Clear the filter after use
          localStorage.removeItem('exam_difficulty_filter');
        }
        
        const response = await api.post(`/api/exam/${examId}/start`, payload);
        
        console.log('Exam start response:', response);
        
        // Check if exam was already taken (response contains already_taken flag)
        if (response.already_taken) {
          alreadyTaken.value = true;
          previousScore.value = response.previous_score || 0;
          console.log('Exam already taken. Previous score:', previousScore.value);
        }
        
        // Extract data from response
        attemptId.value = response.attempt_id;
        
        // The exam data is nested inside response.exam
        if (response.exam) {
          exam.value = response.exam;
          // Sections are inside exam.sections
          sections.value = response.exam.sections || [];
        } else {
          // Fallback if structure is different
          exam.value = response;
          sections.value = response.sections || [];
        }
        
        console.log('Exam loaded:', exam.value);
        console.log('Sections loaded:', sections.value);
        console.log('Number of sections:', sections.value.length);
        
        // Set first section and question
        // Check if there are any questions in any section
        let hasQuestions = false;
        
        if (sections.value.length > 0) {
          currentSection.value = sections.value[0].id;
          if (sections.value[0].questions && sections.value[0].questions.length > 0) {
            currentQuestionId.value = sections.value[0].questions[0].id;
            console.log('First question ID:', currentQuestionId.value);
            hasQuestions = true;
          } else {
            console.warn('First section has no questions');
          }
        } else {
          console.warn('No sections found for this exam');
        }
        
        // FIX: Only set timer and start exam if there are questions AND exam is not already taken
        if (hasQuestions) {
          // Only start timer if exam is NOT already taken
          if (!alreadyTaken.value) {
            if (exam.value && exam.value.duration) {
              totalTime.value = exam.value.duration * 60;
              timeLeft.value = totalTime.value;
              console.log('Timer set to:', exam.value.duration, 'minutes');
            } else {
              // Default to 180 minutes if no duration
              totalTime.value = 180 * 60;
              timeLeft.value = totalTime.value;
              console.warn('No exam duration found, using default 180 minutes');
            }
            // Start timer only for new exams
            startTimer();
          } else {
            // For already taken exams, set time to 0 to hide timer
            timeLeft.value = 0;
            console.log('Timer disabled for already submitted exam');
          }

          // Initialize answers from saved data
          initializeAnswersFromSections();
          
          // Load saved answers from backend
          await loadSavedAnswers();
        } else {
          // Show error for empty exam - no timer started
          error.value = 'This exam has no questions. Please contact your teacher.';
        }
        
      } catch (err) {
        console.error('Error starting exam:', err);
        error.value = err.response?.data?.detail || err.message || 'Failed to load exam. Please try again.';
      } finally {
        loading.value = false;
      }
    };
    
    const initializeAnswersFromSections = () => {
      // Clear existing answers
      Object.keys(answers).forEach(key => delete answers[key]);
      
      // Initialize from sections if any question has selected_answer
      sections.value.forEach(section => {
        if (section.questions) {
          section.questions.forEach(question => {
            if (question.selected_answer) {
              answers[question.id] = question.selected_answer;
            }
          });
        }
      });
      
      console.log('Initialized answers from sections:', answers);
    };
    
    const loadSavedAnswers = async () => {
      try {
        if (!attemptId.value) return;
        
        const response = await api.get(`/api/attempt/${attemptId.value}/answers`);
        if (response.answers) {
          Object.assign(answers, response.answers);
        }
        console.log('Loaded saved answers:', answers);
      } catch (err) {
        console.error('Error loading saved answers:', err);
        // Non-critical error, continue
      }
    };
    
    const startTimer = () => {
      if (timer.value) {
        clearInterval(timer.value);
      }
      
      timer.value = setInterval(() => {
        if (timeLeft.value > 0) {
          timeLeft.value--;
          
          // Show warning at 10% of total time remaining
          const tenPercentTime = Math.floor(totalTime.value * 0.1);
          if (timeLeft.value === tenPercentTime && !warningShown.value) {
            showTimeWarning.value = true;
            warningShown.value = true;
          }
        } else {
          // Time's up - auto submit
          clearInterval(timer.value);
          autoSubmitExam();
        }
      }, 1000);
    };
    
    // Save exam state to localStorage for persistence

    const saveExamStateToLocalStorage = () => {
      if (!exam.value || !attemptId.value) return;
      
      const examState = {
        examId: exam.value.id,
        attemptId: attemptId.value,
        answers: { ...answers },
        markedQuestions: Array.from(markedQuestions.value),
        timeLeft: timeLeft.value,
        currentSection: currentSection.value,
        currentQuestionId: currentQuestionId.value,
        lastSaved: new Date().toISOString()
      };
      
      try {
        localStorage.setItem(`exam_state_${attemptId.value}`, JSON.stringify(examState));
        console.log('Exam state saved to localStorage');
      } catch (err) {
        console.error('Error saving exam state to localStorage:', err);
      }
    };
    
    // Load exam state from localStorage
    const loadExamStateFromLocalStorage = (attemptId) => {
      try {
        const savedState = localStorage.getItem(`exam_state_${attemptId}`);
        if (savedState) {
          const examState = JSON.parse(savedState);
          console.log('Found saved exam state:', examState);
          
          // Check if the saved state is recent (within last 24 hours)
          const lastSaved = new Date(examState.lastSaved);
          const now = new Date();
          const hoursDiff = (now - lastSaved) / (1000 * 60 * 60);
          
          if (hoursDiff < 24) {
            return examState;
          } else {
            // Clear old state
            localStorage.removeItem(`exam_state_${attemptId}`);
          }
        }
      } catch (err) {
        console.error('Error loading exam state from localStorage:', err);
      }
      return null;
    };
    
    // Clear exam state from localStorage
    const clearExamStateFromLocalStorage = () => {
      if (attemptId.value) {
        try {
          localStorage.removeItem(`exam_state_${attemptId.value}`);
          console.log('Exam state cleared from localStorage');
        } catch (err) {
          console.error('Error clearing exam state from localStorage:', err);
        }
      }
    };
    
    const changeSection = (sectionId) => {
      currentSection.value = sectionId;
      const section = sections.value.find(s => s.id === sectionId);
      if (section && section.questions && section.questions.length > 0) {
        currentQuestionId.value = section.questions[0].id;
      }
    };
    
    const jumpToQuestion = (sectionId, questionId) => {
      currentSection.value = sectionId;
      currentQuestionId.value = questionId;
    };
    
    const nextQuestion = () => {
      const currentIndex = currentQuestionIndexInSection.value;
      
      if (currentIndex < currentSectionQuestions.value.length - 1) {
        // Next in same section
        currentQuestionId.value = currentSectionQuestions.value[currentIndex + 1].id;
      } else {
        // Move to next section
        const currentSectionIndex = sections.value.findIndex(
          s => s.id === currentSection.value
        );
        
        if (currentSectionIndex < sections.value.length - 1) {
          const nextSection = sections.value[currentSectionIndex + 1];
          currentSection.value = nextSection.id;
          if (nextSection.questions && nextSection.questions.length > 0) {
            currentQuestionId.value = nextSection.questions[0].id;
          }
        }
      }
    };
    
    const prevQuestion = () => {
      const currentIndex = currentQuestionIndexInSection.value;
      
      if (currentIndex > 0) {
        // Previous in same section
        currentQuestionId.value = currentSectionQuestions.value[currentIndex - 1].id;
      } else {
        // Move to previous section
        const currentSectionIndex = sections.value.findIndex(
          s => s.id === currentSection.value
        );
        
        if (currentSectionIndex > 0) {
          const prevSection = sections.value[currentSectionIndex - 1];
          currentSection.value = prevSection.id;
          if (prevSection.questions && prevSection.questions.length > 0) {
            currentQuestionId.value = prevSection.questions[prevSection.questions.length - 1].id;
          }
        }
      }
    };
    
    const selectOption = async (questionId, option) => {
      // Update local state
      answers[questionId] = option;
      
      try {
        const studentId = parseInt(localStorage.getItem('student_id') || localStorage.getItem('user_id'));
        await api.post(`/api/attempt/${attemptId.value}/answer`, {
          question_id: questionId,
          selected_option: option,
          student_id: studentId
        });
        console.log(`Answer saved: Q${questionId} = ${option}`);
      } catch (err) {
        console.error('Error saving answer:', err);
        // Show user-friendly error
        alert('Failed to save answer. Please check your connection and try again.');
      }
    };
    
    const clearAnswer = async (questionId) => {
      // Remove from local state
      delete answers[questionId];
      
      try {
        await api.delete(`/api/attempt/${attemptId.value}/answer/${questionId}`);
        console.log(`Answer cleared: Q${questionId}`);
      } catch (err) {
        console.error('Error clearing answer:', err);
        alert('Failed to clear answer. Please try again.');
      }
    };
    
    const toggleMarkForReview = () => {
      if (!currentQuestionId.value) return;
      
      if (markedQuestions.value.has(currentQuestionId.value)) {
        markedQuestions.value.delete(currentQuestionId.value);
      } else {
        markedQuestions.value.add(currentQuestionId.value);
      }
      
      // Force reactivity
      markedQuestions.value = new Set(markedQuestions.value);
    };
    
    const autoSubmitExam = async () => {
      // Auto-submit when time runs out
      await submitExam(true);
    };
    
    const submitExam = async (isAutoSubmit = false) => {
      if (submitting.value) return;
      
      submitting.value = true;
      showSubmitModal.value = false;
      showTimeWarning.value = false;
      
      if (timer.value) {
        clearInterval(timer.value);
      }
      
      try {
        const studentId = parseInt(localStorage.getItem('student_id') || localStorage.getItem('user_id'));
        const result = await api.post(`/api/attempt/${attemptId.value}/submit`, {
          student_id: studentId
        });
        console.log('Exam submitted:', result);
        
        // Show success message
        if (isAutoSubmit) {
          successMessage.value = 'Time is up! Your exam has been automatically submitted. You will be redirected to your results page shortly.';
        } else {
          successMessage.value = 'You have successfully submitted your exam! You will be redirected to your results page to see your performance.';
        }
        showSuccessModal.value = true;
        
        // Delay navigation to show success message
        setTimeout(() => {
          showSuccessModal.value = false;
          // Navigate to result page with AI recommendation
          const queryParams = { 
            attemptId: attemptId.value,
            examId: exam.value.id,
            score: result.score,
            total: result.total_questions,
            percentage: result.percentage,
            correct_count: result.correct_count,
            unanswered_count: result.unanswered_count
          };
          
          // Pass AI recommendation if available from backend
          if (result.ai_recommendation) {
            queryParams.ai_recommendation = encodeURIComponent(JSON.stringify(result.ai_recommendation));
          }
          
          router.push({
            path: '/student/exam-result',
            query: queryParams
          });
        }, 3000); // Show message for 3 seconds
        
      } catch (err) {
        console.error('Error submitting exam:', err);
        error.value = 'Failed to submit exam. Please try again.';
        submitting.value = false;
      }
    };

    

    const retryLoad = () => {
      startExam();
    };
    
    // Lifecycle
    onMounted(() => {
      startExam();
    });
    
    onBeforeUnmount(() => {
      if (timer.value) {
        clearInterval(timer.value);
      }
    });
    
    return {
      loading,
      error,
      submitting,
      showSubmitModal,
      showTimeWarning,
      showSuccessModal,
      successMessage,
      totalTime,
      alreadyTaken,
      previousScore,

      exam,
      sections,
      attemptId,
      currentSection,
      currentQuestionId,
      answers,
      markedQuestions,
      timeLeft,
      formattedTime,
      allQuestions,
      currentQuestion,
      currentSectionQuestions,
      currentQuestionIndexInSection,
      getSectionProgress,
      getCurrentSectionName,
      getCurrentSectionColor,
getSelectedOptionForCurrentQuestion,
      getCorrectAnswerForCurrentQuestion,
      getIsCorrectForCurrentQuestion,
      isQuestionAnswered,
      isQuestionMarked,
      changeSection,
      jumpToQuestion,
      nextQuestion,
      prevQuestion,
      selectOption,
      clearAnswer,
      toggleMarkForReview,
      submitExam,
      retryLoad,
      goBack,
      goToSubscription,
      goToResults,
      showSubscriptionModal,
      examPricing,
      subscribing,
      goToSubscriptionPremium
    };
  }
};
</script>

<style scoped>
.take-exam {
  min-height: 100vh;
  background: #f8fafc;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #64748b;
  font-size: 1.1rem;
}

/* Error State */
.error-container {
  text-align: center;
  padding: 4rem 2rem;
  max-width: 500px;
  margin: 0 auto;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.error-container h2 {
  color: #1e293b;
  margin-bottom: 1rem;
}

.error-container p {
  color: #64748b;
  margin-bottom: 2rem;
}

.retry-btn {
  padding: 0.75rem 2rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.3);
}

/* Exam Wrapper */
.exam-wrapper {
  max-width: 1600px;
  margin: 0 auto;
  padding: 2rem;
}

/* Already Taken Banner - Beautified */
.already-taken-banner {
  margin-bottom: 2rem;
}

.banner-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.3);
}

.banner-icon-wrapper {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.banner-icon {
  font-size: 2.5rem;
}

.banner-content {
  flex: 1;
}

.banner-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #92400e;
  margin: 0 0 0.5rem 0;
}

.score-display-banner {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.score-label {
  font-size: 1rem;
  color: #b45309;
  font-weight: 500;
}

.score-value {
  font-size: 2rem;
  font-weight: 800;
  color: #92400e;
}

.score-divider {
  font-size: 1.5rem;
  color: #b45309;
  font-weight: 500;
}

.banner-subtitle {
  font-size: 0.95rem;
  color: #b45309;
  margin: 0;
  opacity: 0.9;
}

.view-results-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.view-results-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4);
}

.view-results-btn .btn-icon {
  font-size: 1.3rem;
}

@media (max-width: 768px) {
  .banner-card {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }
  
  .banner-icon-wrapper {
    width: 60px;
    height: 60px;
  }
  
  .banner-icon {
    font-size: 2rem;
  }
  
  .score-display-banner {
    justify-content: center;
  }
  
  .view-results-btn {
    width: 100%;
    justify-content: center;
  }
}

/* Exam Header */
.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-radius: 20px;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.exam-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.exam-meta {
  display: flex;
  gap: 1.5rem;
}

.meta-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  border-radius: 30px;
  color: #475569;
  font-size: 0.95rem;
}

.meta-icon {
  font-size: 1.1rem;
}

.timer-container {
  text-align: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  border-radius: 16px;
  color: white;
  min-width: 180px;
}

.timer-container.timer-warning {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.9; }
  100% { opacity: 1; }
}

.timer-icon {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.timer-display {
  font-size: 2.5rem;
  font-weight: 700;
  font-family: monospace;
  line-height: 1.2;
}

.timer-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

/* Exam Grid */
.exam-grid {
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: 1.5rem;
}

/* Sections Sidebar */
.sections-sidebar {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.sidebar-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
}

.section-count {
  padding: 0.25rem 0.75rem;
  background: #f1f5f9;
  border-radius: 20px;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 600;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.section-btn {
  width: 100%;
  padding: 1rem;
  background: #f8fafc;
  border: 2px solid transparent;
  border-left-width: 4px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.section-btn:hover {
  background: #f1f5f9;
  transform: translateX(4px);
}

.section-btn.active-section {
  background: #eff6ff;
  border-color: #2563eb;
}

.section-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.section-name {
  font-weight: 600;
  color: #1e293b;
}

.question-badge {
  font-size: 0.85rem;
  color: #64748b;
}

.active-section .section-name {
  color: #2563eb;
}

.section-progress {
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  transition: width 0.3s ease;
}

/* Overall Progress */
.overall-progress {
  padding-top: 1rem;
  border-top: 2px dashed #e2e8f0;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #64748b;
  font-size: 0.9rem;
}

.progress-track {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #7c3aed);
  transition: width 0.3s ease;
}

/* Question Container */
.question-container {
  min-height: 500px;
}

.empty-section {
  background: white;
  border-radius: 20px;
  padding: 4rem 2rem;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-section h3 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.empty-section p {
  color: #64748b;
}

/* Palette Sidebar */
.palette-sidebar {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 100px;
}

.palette-header {
  margin-bottom: 1.5rem;
}

.palette-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

.palette-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #64748b;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-dot.answered {
  background: #2563eb;
}

.legend-dot.marked {
  background: #f59e0b;
}

.legend-dot.current {
  background: white;
  border: 2px solid #2563eb;
}

.sections-palette {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
}

.palette-section {
  margin-bottom: 1.5rem;
}

.palette-section-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: space-between;
}

.palette-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}

.palette-btn {
  aspect-ratio: 1;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: #475569;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.palette-btn:hover {
  transform: scale(1.05);
  border-color: #2563eb;
}

.palette-btn.answered {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.palette-btn.marked {
  position: relative;
}

.palette-btn.marked::after {
  content: '';
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  background: #f59e0b;
  border-radius: 50%;
}

.palette-btn.current {
  border: 2px solid #2563eb;
  transform: scale(1.05);
  font-weight: 700;
}

/* Submit Button */
.submit-exam-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-exam-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
}

.submit-exam-btn.ready {
  background: linear-gradient(135deg, #10b981, #059669);
  animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.btn-icon {
  font-size: 1.2rem;
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 400px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-content.warning {
  border-top: 4px solid #f59e0b;
}

.modal-content.success {
  border-top: 4px solid #10b981;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f0fdf4;
  border-radius: 12px;
}

.loading-indicator .spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #bbf7d0;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-indicator span {
  color: #166534;
  font-size: 0.95rem;
  font-weight: 500;
}


.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid #f1f5f9;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #64748b;
}

.modal-body {
  padding: 1.5rem;
}

.submission-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.summary-item {
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
}

.summary-label {
  display: block;
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.summary-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2563eb;
}

.warning-text {
  color: #dc2626;
  font-size: 0.95rem;
  padding: 0.75rem;
  background: #fee2e2;
  border-radius: 8px;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 2px solid #f1f5f9;
}

.modal-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-btn.cancel {
  background: #f1f5f9;
  color: #64748b;
}

.modal-btn.cancel:hover {
  background: #e2e8f0;
}

.modal-btn.confirm {
  background: #2563eb;
  color: white;
}

.modal-btn.confirm:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.3);
}

.modal-btn.primary {
  background: #f59e0b;
  color: white;
}

.modal-btn.primary:hover {
  background: #d97706;
}

/* Subscribe button loading state */
.modal-btn.subscribe:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.subscribe-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.loading-dots {
  animation: loadingDots 1.5s infinite;
}

@keyframes loadingDots {
  0% { content: 'Redirecting'; }
  25% { content: 'Redirecting.'; }
  50% { content: 'Redirecting..'; }
  75% { content: 'Redirecting...'; }
  100% { content: 'Redirecting'; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal Animation */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Responsive - Palette goes below when page shrinks */
@media (max-width: 1400px) {
  .exam-grid {
    grid-template-columns: 260px 1fr 280px;
  }
}

@media (max-width: 1200px) {
  .exam-grid {
    grid-template-columns: 1fr;
    display: flex;
    flex-direction: column;
  }
  
  .sections-sidebar {
    position: static;
    order: 1;
  }
  
  .question-container {
    order: 2;
    min-height: 400px;
  }
  
  .palette-sidebar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 100;
    border-radius: 20px 20px 0 0;
    max-height: 50vh;
    overflow-y: auto;
    box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.15);
    order: 3;
  }
  
  .palette-header {
    position: sticky;
    top: 0;
    background: white;
    padding: 1rem;
    margin: -1.5rem -1.5rem 1rem -1.5rem;
    border-bottom: 1px solid #e2e8f0;
    z-index: 1;
  }
  
  .sections-palette {
    max-height: 30vh;
  }
}

@media (max-width: 768px) {
  .exam-wrapper {
    padding: 1rem;
  }
  
  .exam-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .exam-meta {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .exam-grid {
    grid-template-columns: 1fr;
  }
  
  .sections-sidebar {
    display: none;
  }
  
  .timer-container {
    width: 100%;
  }
}
</style>
