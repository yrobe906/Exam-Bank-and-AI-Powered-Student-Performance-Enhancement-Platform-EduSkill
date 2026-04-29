<template>
  <div class="question-area">

    <div class="question-header">
      <div class="section-badge" :style="{ backgroundColor: sectionColor + '20', color: sectionColor }">
        {{ currentSection }}
      </div>

      <div class="question-meta">
        <span class="difficulty" :class="difficultyClass">
          {{ difficultyText }}
        </span>
        <span class="marks">{{ currentQuestion.marks }} Marks</span>
      </div>
    </div>

    <div class="question-text">
      Q{{ currentQuestionIndex + 1 }}. {{ currentQuestion.question_text }}
    </div>

<div class="options-container">
      <div 
        v-for="option in options" 
        :key="option.key"
        class="option-item"
        :class="{ 
          'option-selected': selectedOption === option.key && !isReviewMode,
          'option-marked': isMarked && selectedOption === option.key,
          'option-correct': isReviewMode && correctAnswer === option.key,
          'option-incorrect': isReviewMode && selectedOption === option.key && !isCorrect
        }"
        @click="!isReviewMode && $emit('select-option', currentQuestion.id, option.key)"
      >
        <div class="option-marker" :style="getOptionMarkerStyle(option.key)">
          {{ option.key }}
        </div>
        <div class="option-text">{{ option.text }}</div>
        
        <!-- Review Mode Indicators -->
        <span v-if="isReviewMode && correctAnswer === option.key" class="option-badge correct-badge">✓ Correct</span>
        <span v-if="isReviewMode && selectedOption === option.key && !isCorrect" class="option-badge incorrect-badge">✗ Your Answer</span>
        <span v-else-if="selectedOption === option.key && !isReviewMode" class="option-check" :style="{ color: sectionColor }">✓</span>
      </div>
    </div>

    <!-- Clear Answer Button (if answer selected) -->
    <div v-if="selectedOption" class="clear-answer-container">
      <button class="clear-answer-btn" @click="$emit('clear-response', currentQuestion.id)">
        <span class="clear-icon">✕</span> Clear Answer
      </button>
    </div>

    <div class="navigation-buttons">
      <button 
        class="nav-btn prev-btn"
        @click="$emit('previous')"
        :disabled="currentQuestionIndex === 0"
      >
        ← Prev
      </button>

      <button 
        class="nav-btn review-btn"
        :class="{ 'marked': isMarked }"
        @click="$emit('toggle-mark')"
      >
        <span v-if="isMarked" class="mark-icon">✓</span>
        <span v-else class="mark-icon">🏷️</span>
        {{ isMarked ? 'Marked' : 'Mark for Review' }}
      </button>

      <button 
        class="nav-btn next-btn"
        @click="$emit('next')"
      >
        Save & Next →
      </button>
    </div>

    <!-- Question Progress -->
    <div class="question-progress">
      Question {{ currentQuestionIndex + 1 }} of {{ totalQuestionsInSection }}
    </div>

  </div>
</template>

<script>
export default {
  name: 'QuestionArea',
  props: {
    currentQuestion: {
      type: Object,
      required: true
    },
    currentQuestionIndex: {
      type: Number,
      required: true
    },
    totalQuestionsInSection: {
      type: Number,
      default: 0
    },
    currentSection: {
      type: String,
      required: true
    },
    sectionColor: {
      type: String,
      default: '#2563eb'
    },
    selectedOption: {
      type: String,
      default: null
    },
isMarked: {
      type: Boolean,
      default: false
    },
    isReviewMode: {
      type: Boolean,
      default: false
    },
    correctAnswer: {
      type: String,
      default: null
    },
    isCorrect: {
      type: Boolean,
      default: null
    }
  },
  computed: {
    // Format options from the question data
    options() {
      if (!this.currentQuestion) return []
      
      return [
        { key: 'A', text: this.currentQuestion.option_a },
        { key: 'B', text: this.currentQuestion.option_b },
        { key: 'C', text: this.currentQuestion.option_c },
        { key: 'D', text: this.currentQuestion.option_d }
      ].filter(opt => opt.text) // Filter out empty options
    },
    
    difficultyText() {
      const difficulty = this.currentQuestion.difficulty
      if (typeof difficulty === 'number') {
        const levels = ['Easy', 'Easy', 'Medium', 'Hard', 'Very Hard']
        return levels[difficulty] || 'Medium'
      }
      return difficulty || 'Medium'
    },
    
difficultyClass() {
      const difficulty = this.currentQuestion.difficulty
      if (typeof difficulty === 'number') {
        if (difficulty <= 2) return 'easy'
        if (difficulty === 3) return 'medium'
        return 'hard'
      }
      return 'medium'
    }
  },
  methods: {
    getOptionMarkerStyle(optionKey) {
      if (this.isReviewMode) {
        if (this.correctAnswer === optionKey) {
          return { backgroundColor: '#16a34a', borderColor: '#16a34a', color: 'white' }
        }
        if (this.selectedOption === optionKey && !this.isCorrect) {
          return { backgroundColor: '#dc2626', borderColor: '#dc2626', color: 'white' }
        }
      }
      if (this.selectedOption === optionKey) {
        return { backgroundColor: this.sectionColor, borderColor: this.sectionColor, color: 'white' }
      }
      return { borderColor: this.sectionColor }
    }
  }
}
</script>

<style scoped>
.question-area {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
  height: fit-content;
  transition: all 0.3s ease;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-badge {
  padding: 0.5rem 1.25rem;
  background: #f1f5f9;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.difficulty {
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.difficulty.easy {
  background: #dcfce7;
  color: #16a34a;
}

.difficulty.medium {
  background: #fef9c3;
  color: #ca8a04;
}

.difficulty.hard {
  background: #fee2e2;
  color: #dc2626;
}

.marks {
  font-weight: 600;
  color: #2563eb;
  background: #eff6ff;
  padding: 0.35rem 0.85rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.question-text {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 2rem;
  line-height: 1.6;
  font-weight: 500;
  padding: 1rem 0;
  border-bottom: 2px solid #f1f5f9;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.option-item:hover {
  border-color: v-bind(sectionColor);
  background: #eff6ff;
  transform: translateX(8px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
}

.option-selected {
  border-color: v-bind(sectionColor);
  background: #eff6ff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

.option-marked {
  border-left: 4px solid #f59e0b;
}

.option-marker {
  width: 36px;
  height: 36px;
  background: white;
  border: 2px solid v-bind(sectionColor);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: v-bind(sectionColor);
  flex-shrink: 0;
  transition: all 0.2s ease;
  font-size: 1.1rem;
}

.option-selected .option-marker {
  background: v-bind(sectionColor);
  color: white;
}

.option-text {
  flex: 1;
  font-size: 1rem;
  color: #1e293b;
  line-height: 1.5;
}

.option-check {
  font-size: 1.5rem;
  font-weight: bold;
  animation: scaleIn 0.2s ease;
  margin-left: auto;
  padding-left: 1rem;
}

/* Review Mode Styles */
.option-correct {
  border-color: #16a34a !important;
  background: #dcfce7 !important;
}

.option-incorrect {
  border-color: #dc2626 !important;
  background: #fee2e2 !important;
}

.option-badge {
  margin-left: auto;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  flex-shrink: 0;
}

.correct-badge {
  background: #16a34a;
  color: white;
}

.incorrect-badge {
  background: #dc2626;
  color: white;
}

.clear-answer-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.clear-answer-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 30px;
  color: #dc2626;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-answer-btn:hover {
  background: #fecaca;
  transform: scale(1.05);
}

.clear-icon {
  font-size: 1.1rem;
  font-weight: bold;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 2rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.5rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 130px;
  font-size: 0.95rem;
}

.nav-btn:hover:not(:disabled) {
  border-color: v-bind(sectionColor);
  color: v-bind(sectionColor);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px -8px rgba(37, 99, 235, 0.3);
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.prev-btn {
  background: white;
}

.review-btn {
  flex: 1;
  background: #fef3c7;
  border-color: #f59e0b;
  color: #d97706;
  min-width: 160px;
}

.review-btn:hover:not(:disabled) {
  background: #fde68a;
  border-color: #d97706;
  color: #b45309;
  box-shadow: 0 8px 16px -8px rgba(245, 158, 11, 0.3);
}

.review-btn.marked {
  background: #fde68a;
  border-color: #d97706;
  color: #b45309;
}

.next-btn {
  background: linear-gradient(135deg, v-bind(sectionColor), color-mix(in srgb, v-bind(sectionColor) 70%, black));
  border: none;
  color: white;
}

.next-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -8px v-bind(sectionColor);
}

.mark-icon {
  font-size: 1.1rem;
}

.question-progress {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px dashed #e2e8f0;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
}

@keyframes scaleIn {
  from { 
    transform: scale(0); 
    opacity: 0; 
  }
  to { 
    transform: scale(1); 
    opacity: 1; 
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .question-area {
    padding: 1.5rem;
  }
  
  .question-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .navigation-buttons {
    flex-wrap: wrap;
  }
  
  .nav-btn {
    min-width: 100px;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
  
  .review-btn {
    order: -1;
    width: 100%;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .question-area {
    background: #1e293b;
    color: #f1f5f9;
  }
  
  .question-text {
    color: #f1f5f9;
    border-bottom-color: #334155;
  }
  
  .option-item {
    background: #0f172a;
    border-color: #334155;
  }
  
  .option-text {
    color: #e2e8f0;
  }
  
  .option-marker {
    background: #1e293b;
  }
  
  .nav-btn {
    background: #0f172a;
    border-color: #334155;
    color: #94a3b8;
  }
  
  .question-progress {
    border-top-color: #334155;
    color: #94a3b8;
  }
}
</style>