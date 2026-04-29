<template>
  <div class="palette-sidebar">
    <h3 class="palette-title">Question Palette</h3>
    <div class="section-indicator">{{ currentSection }}</div>
    
    <div class="question-grid">
      <button v-for="q in questions" :key="q.id"
              class="palette-item"
              :class="getPaletteItemClass(q)"
              @click="$emit('jump-to', q.id)">
        {{ q.number }}
      </button>
    </div>

    <div class="legend">
      <div v-for="item in legendItems" :key="item.label" class="legend-item">
        <span class="legend-color" :class="item.colorClass"></span>
        <span>{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaletteSidebar',
  props: {
    questions: Array,
    currentQuestionId: [Number, String],
    answers: Object,
    markedForReview: Array,
    visitedQuestions: Set,
    currentSection: String
  },
  computed: {
    legendItems() {
      return [
        { label: 'Answered', colorClass: 'answered' },
        { label: 'Marked Review', colorClass: 'marked' },
        { label: 'Not Answered', colorClass: 'not-answered' },
        { label: 'Not Visited', colorClass: 'not-visited' },
        { label: 'Ans & Marked', colorClass: 'ans-marked' }
      ]
    }
  },
  methods: {
    getPaletteItemClass(question) {
      const isAnswered = this.answers[question.id]
      const isMarked = this.markedForReview.includes(question.id)
      const isVisited = this.visitedQuestions.has(question.id)
      const isCurrent = this.currentQuestionId === question.id
      
      return {
        'answered': isAnswered && !isMarked,
        'marked': !isAnswered && isMarked,
        'not-answered': !isAnswered && !isMarked && isVisited,
        'not-visited': !isVisited,
        'ans-marked': isAnswered && isMarked,
        'current': isCurrent
      }
    }
  }
}
</script>

<style scoped>

.palette-sidebar {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.palette-title {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

.section-indicator {
  font-size: 0.9rem;
  color: #2563eb;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.palette-item {
  aspect-ratio: 1;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.palette-item:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.palette-item.current {
  ring: 2px solid #2563eb;
  ring-offset: 2px;
}

.palette-item.answered {
  background: #10b981;
  color: white;
}

.palette-item.marked {
  background: #f59e0b;
  color: white;
}

.palette-item.not-answered {
  background: #f87171;
  color: white;
}

.palette-item.not-visited {
  background: #e2e8f0;
  color: #64748b;
}

.palette-item.ans-marked {
  background: linear-gradient(135deg, #10b981, #f59e0b);
  color: white;
}

.legend {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #64748b;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.legend-color.answered {
  background: #10b981;
}

.legend-color.marked {
  background: #f59e0b;
}

.legend-color.not-answered {
  background: #f87171;
}

.legend-color.not-visited {
  background: #e2e8f0;
}

.legend-color.ans-marked {
  background: linear-gradient(135deg, #10b981, #f59e0b);
}
</style>