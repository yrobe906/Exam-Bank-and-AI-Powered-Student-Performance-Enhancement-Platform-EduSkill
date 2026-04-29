<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50/30">
    <!-- EduSkill Header -->
    <EduskillHeader />
    
    <!-- Back button -->
    <div class="max-w-4xl mx-auto pt-6 px-4">
      <button 
        @click="goBack" 
        class="flex items-center text-blue-600 hover:text-blue-700 font-medium transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Subjects
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="text-gray-500 mt-4">Loading questions...</p>
      </div>
    </div>

    <!-- Mock Test Practice Container -->
    <div v-else class="mock-test-container">
      <!-- main card – soft glass effect -->
      <div class="exam-card">
        <!-- header with progress and logo -->
        <div class="top-bar">
          <div class="question-pill">Question {{ currentIndex + 1 }} of {{ totalQuestions }}</div>
          <div class="tests-logo">tests.com</div>
        </div>

        <!-- question header -->
        <div class="question-header">
          <div class="q-num">⚡ question {{ currentIndex + 1 }}</div>
          <div class="question-text">{{ currentQuestion?.question_text }}</div>
        </div>

        <!-- options grid -->
        <div class="options-grid">
          <div
            v-for="option in questionOptions"
            :key="option.letter"
            class="option-item"
            :class="getOptionClass(option.letter)"
            @click="handleOptionClick(option.letter)"
          >
            <span class="option-prefix">{{ option.letter }}.</span>
            <span class="option-text">{{ option.text }}</span>
            <span v-if="selectedOption === option.letter && !isSelectedCorrect" 
                  class="opt-status"
                  @click.stop="clearSelection"
                  style="cursor: pointer;"
                  title="Clear answer">
              ✕
            </span>
            <span v-else class="opt-status">{{ getOptionIcon(option.letter) }}</span>
          </div>
        </div>

        <!-- feedback and explanation panel -->
        <div v-if="selectedOption !== null" class="explanation-card">
          <!-- Correct answer feedback -->
          <div v-if="isSelectedCorrect" class="verdict correct">
            <span>✅ You are right!</span>
          </div>
          <!-- Incorrect answer feedback -->
          <div v-else class="verdict incorrect">
            <span>❌ Incorrect. Please try again!</span>
          </div>
          
          <!-- Show explanation when correct -->
          <div v-if="isSelectedCorrect && currentQuestion?.explanation" class="explanation-text">
            <strong>Explanation:</strong> {{ currentQuestion.explanation }}
          </div>
          
          <!-- Show correct answer when wrong -->
          <div v-if="!isSelectedCorrect && selectedOption" class="correct-answer-hint">
            <strong>Hint:</strong> Select the correct answer and click to confirm
          </div>
        </div>

        <!-- navigation & guarantee -->
        <div class="nav-area">
          <div class="nav-buttons">
            <button class="nav-btn" @click="prevQuestion" :disabled="currentIndex === 0">◂ Previous</button>
            <button class="nav-btn" @click="nextQuestion" :disabled="currentIndex === totalQuestions - 1 || !isSelectedCorrect">Next ▸</button>
            <button class="nav-btn finish" @click="finishExam">Finish</button>
          </div>
          <div class="guarantee">100% PASS GUARANTEE</div>
        </div>

        <hr />
        <div class="footer-small">⚡ slow & soft practice · instant feedback</div>
      </div>
    </div>
  </div>
</template>

<script>
import EduskillHeader from '@/components/Header/EduskillHeader.vue';

const API_URL = 'http://127.0.0.1:8000';

export default {
  name: 'MockTestPractice',
  components: {
    EduskillHeader
  },
  data() {
    return {
      loading: true,
      questions: [],
      currentIndex: 0,
      selectedOption: null,
      subject: null,
      testId: null
    };
  },
  computed: {
    totalQuestions() {
      return this.questions.length;
    },
    currentQuestion() {
      return this.questions[this.currentIndex] || null;
    },
    questionOptions() {
      if (!this.currentQuestion) return [];
      return [
        { letter: 'a', text: this.currentQuestion.option_a },
        { letter: 'b', text: this.currentQuestion.option_b },
        { letter: 'c', text: this.currentQuestion.option_c },
        { letter: 'd', text: this.currentQuestion.option_d }
      ];
    },
    isSelectedCorrect() {
      if (!this.selectedOption || !this.currentQuestion) return false;
      return this.selectedOption === this.currentQuestion.correct_answer;
    }
  },
  mounted() {
    this.subject = this.$route.query.subject;
    this.loadQuestions();
  },
  methods: {
    goBack() {
      this.$router.push('/mock-test-subject');
    },
    async loadQuestions() {
      this.loading = true;
      try {
        // First get tests by subject
        const res = await fetch(`${API_URL}/api/practice-mock/tests?subject=${encodeURIComponent(this.subject)}&is_active=true`);
        if (res.ok) {
          const tests = await res.json();
          
          if (tests.length > 0) {
            // Get the first active test for this subject
            this.testId = tests[0].id;
            
            // Now get questions for this test
            const questionsRes = await fetch(`${API_URL}/api/practice-mock/tests/${this.testId}/questions`);
            if (questionsRes.ok) {
              this.questions = await questionsRes.json();
            }
          }
        }
        
        if (this.questions.length === 0) {
          alert('No questions available for this subject. Please try another subject or contact admin.');
        }
      } catch (error) {
        console.error('Error loading questions:', error);
        alert('Failed to load questions. Please try again.');
      } finally {
        this.loading = false;
      }
    },
    handleOptionClick(letter) {
      // Allow clicking on any option to select it
      // This allows multiple attempts until correct answer is chosen
      this.selectedOption = letter;
    },
    clearSelection() {
      // Clear the selection to allow trying again
      this.selectedOption = null;
    },
    getOptionClass(letter) {
      if (!this.selectedOption) return '';
      
      // If answer is correct, highlight the correct one
      if (this.isSelectedCorrect) {
        if (letter === this.currentQuestion.correct_answer) {
          return 'correct-selected';
        }
        return '';
      }
      
      // If answer is incorrect - show it as incorrect (red)
      if (this.selectedOption === letter) {
        return 'incorrect-selected';
      }
      
      return '';
    },
    getOptionIcon(letter) {
      if (!this.selectedOption) return '';
      
      if (this.isSelectedCorrect) {
        if (letter === this.currentQuestion.correct_answer) {
          return '✅';
        }
        return '';
      }
      
      // Show X for selected incorrect answer
      if (this.selectedOption === letter) {
        return '';
      }
      
      return '';
    },
    prevQuestion() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.selectedOption = null;
      }
    },
    nextQuestion() {
      if (this.currentIndex < this.totalQuestions - 1 && this.isSelectedCorrect) {
        this.currentIndex++;
        this.selectedOption = null;
      }
    },
    finishExam() {
      alert('✨ Practice finished — keep going!');
      this.$router.push('/mock-test-subject');
    }
  }
};
</script>

<style scoped>
.mock-test-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: linear-gradient(145deg, #eef2f6 0%, #dce5f0 100%);
}

.exam-card {
  max-width: 780px;
  width: 100%;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 42px;
  box-shadow: 0 25px 50px -10px rgba(0, 20, 40, 0.25),
              inset 0 1px 2px rgba(255,255,255,0.6);
  padding: 32px 30px 30px 30px;
  border: 1px solid rgba(255,255,255,0.5);
  transition: all 0.3s ease;
}

/* top bar */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  color: #2f4057;
  font-weight: 500;
  font-size: 15px;
  letter-spacing: 0.2px;
}

.question-pill {
  background: rgba(45, 85, 125, 0.08);
  padding: 8px 18px;
  border-radius: 60px;
  border: 1px solid rgba(255,255,255,0.7);
  backdrop-filter: blur(4px);
  box-shadow: inset 0 1px 3px white;
}

.tests-logo {
  background: rgba(0,0,0,0.03);
  padding: 8px 20px;
  border-radius: 60px;
  font-weight: 600;
  color: #1a3b5c;
  border: 1px solid rgba(255,255,255,0.5);
}

/* question header */
.question-header {
  margin-bottom: 28px;
}

.q-num {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: #4f6b8a;
  background: rgba(110, 145, 185, 0.15);
  display: inline-block;
  padding: 5px 15px;
  border-radius: 30px;
  margin-bottom: 16px;
  border: 1px solid rgba(255,255,255,0.3);
  backdrop-filter: blur(2px);
}

.question-text {
  font-size: 26px;
  font-weight: 600;
  line-height: 1.3;
  color: #0d263b;
  margin-bottom: 8px;
}

/* options grid */
.options-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin: 28px 0 30px;
}

.option-item {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,0.8);
  border-radius: 26px;
  padding: 14px 24px;
  font-size: 20px;
  font-weight: 500;
  color: #11324e;
  display: flex;
  align-items: center;
  gap: 18px;
  box-shadow: 0 6px 12px -8px rgba(0,32,64,0.2);
  transition: background 0.2s ease, border-color 0.2s, transform 0.15s, box-shadow 0.3s;
  cursor: pointer;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #a0c1d9;
  box-shadow: 0 12px 18px -12px rgba(20,80,120,0.3);
  transform: scale(1.01);
}

.option-prefix {
  width: 36px;
  height: 36px;
  background: rgba(70, 120, 170, 0.1);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #1d496d;
  border: 1px solid rgba(255,255,255,0.7);
}

.option-text {
  flex: 1;
}

.opt-status {
  font-size: 26px;
  width: 32px;
  text-align: center;
  opacity: 0.8;
}

/* selected states */
.option-item.correct-selected {
  background: #c7e6d0;
  border-color: #25835e;
  border-width: 2px;
}

.option-item.incorrect-selected {
  background: #ffe2dd;
  border-color: #c5655a;
  border-width: 2px;
}

/* explanation card */
.explanation-card {
  background: #e4edf5;
  border-radius: 32px;
  padding: 24px 28px;
  margin: 24px 0 28px;
  border-left: 8px solid #3f8ab3;
  box-shadow: inset 0 2px 6px rgba(255,255,255,0.8), 0 8px 18px -14px #1f3f5c;
  transition: all 0.4s ease;
}

.verdict {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.verdict.correct {
  color: #2e7d32;
}

.verdict.incorrect {
  color: #c62828;
}

.verdict span {
  background: #ffffffb0;
  padding: 5px 18px;
  border-radius: 60px;
  font-size: 20px;
  border: 1px solid white;
}

.explanation-text {
  font-size: 18px;
  line-height: 1.5;
  color: #103247;
  font-weight: 400;
  background: rgba(255,255,255,0.5);
  padding: 16px 20px;
  border-radius: 24px;
  backdrop-filter: blur(2px);
  margin-top: 12px;
}

.correct-answer-hint {
  font-size: 16px;
  color: #c62828;
  background: #ffebee;
  padding: 12px 16px;
  border-radius: 16px;
  margin-top: 12px;
}

/* navigation area */
.nav-area {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
}

.nav-buttons {
  display: flex;
  gap: 16px;
}

.nav-btn {
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,0.9);
  padding: 12px 32px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 18px;
  color: #1c3f5c;
  box-shadow: 0 6px 12px -10px #204b6e;
  transition: 0.2s;
  cursor: pointer;
  border: 1px solid white;
}

.nav-btn:active:not(:disabled) {
  transform: scale(0.97);
  background: rgba(255,255,255,0.9);
}

.nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.nav-btn.finish {
  background: #1f4970d9;
  color: white;
  border-color: #ffffffc0;
  box-shadow: 0 10px 18px -12px #022b49;
}

.guarantee {
  font-weight: 600;
  font-size: 20px;
  background: linear-gradient(130deg, #1d4730, #1c5f41);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  padding: 8px 20px;
  border-radius: 60px;
  background-color: #ebf8f0;
  border: 1px solid #b8dec9;
}

hr {
  margin: 20px 0 12px;
  border: none;
  border-top: 2px solid rgba(255,255,255,0.5);
}

.footer-small {
  font-size: 15px;
  color: #3f5569;
  text-align: center;
  margin-top: 8px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .exam-card {
    padding: 24px 20px;
    border-radius: 28px;
  }
  
  .question-text {
    font-size: 20px;
  }
  
  .option-item {
    font-size: 16px;
    padding: 12px 18px;
  }
  
  .nav-area {
    flex-direction: column;
    gap: 16px;
  }
  
  .nav-buttons {
    width: 100%;
    justify-content: center;
  }
  
  .nav-btn {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .guarantee {
    font-size: 16px;
  }
}
</style>
