<template>
  <div class="bg-white rounded-2xl shadow-lg p-6">

    <!-- ================= HEADER ================= -->
    <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
      <span class="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full"></span>
      Add Custom Question
    </h3>

    <!-- Loading Overlay -->
    <div v-if="loading" class="flex justify-center py-4">
      <div class="spinner-small"></div>
    </div>

    <div v-else class="space-y-4">

      <!-- Exam Dropdown - Only show if examId not provided as prop -->
      <div v-if="!examId">
        <label class="text-sm text-gray-600">Select Exam</label>
        <select v-model="selectedExam" @change="fetchSections"
          class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-all">
          <option value="">Select Exam</option>
          <option v-for="exam in exams" :key="exam.id" :value="exam.id">
            {{ exam.name }} ({{ exam.total_questions }} Qs)
          </option>
        </select>
      </div>

      <!-- Section Dropdown - Only show if sectionId not provided as prop -->
      <div v-if="!sectionId">
        <label class="text-sm text-gray-600">Select Section</label>
        <select v-model="form.section_id" @change="handleSectionChange"
          class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-all">
          <option value="">Select Section</option>
          <option v-for="sec in sections" :key="sec.id" :value="sec.id">
            {{ sec.name }} ({{ sec.question_count }} questions)
          </option>
        </select>
        <p v-if="sectionError" class="text-xs text-red-500 mt-1">{{ sectionError }}</p>
      </div>

      <!-- Question Text -->
      <div>
        <label class="text-sm text-gray-600">Question Text</label>
        <textarea v-model="form.question_text"
          class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-all"
          rows="2"
          placeholder="Enter your question..."></textarea>
      </div>

      <!-- Options -->
      <div class="grid grid-cols-2 gap-3">
        <div v-for="opt in ['A','B','C','D']" :key="opt">
          <label class="text-sm text-gray-600">Option {{ opt }}</label>
          <input type="text"
            v-model="form[`option_${opt.toLowerCase()}`]"
            class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-all"
            :placeholder="`Option ${opt}`" />
        </div>
      </div>

      <!-- Correct, Marks -->
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-sm text-gray-600">Correct Option</label>
          <select v-model="form.correct_answer"
            class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-all">
            <option value="">Select</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
        </div>

        <div>
          <label class="text-sm text-gray-600">Marks</label>
          <input type="number" v-model.number="form.marks" min="1" max="10"
            class="w-full px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-blue-500 transition-all"/>
        </div>
      </div>

      <!-- Submit -->
      <button @click="submitQuestion"
        :disabled="!isValid || reachedLimit && !editingId || submitting"
        class="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50">
        <span v-if="submitting">Saving...</span>
        <span v-else>{{ editingId ? 'Update Question' : 'Add Question' }}</span>
      </button>

      <p v-if="reachedLimit && !editingId" class="text-xs text-red-500">
        Maximum allowed questions reached ({{ maxQuestions }})
      </p>

      <p v-if="error" class="text-xs text-red-500 mt-2">
        {{ error }}
      </p>

    </div>

    <!-- ================= PREVIEW LIST ================= -->
    <div class="mt-8">
      <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
        <span class="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full"></span>
        Questions Preview ({{ questions.length }})
      </h3>

      <div v-if="loadingQuestions" class="flex justify-center py-4">
        <div class="spinner-small"></div>
      </div>

      <div v-else-if="questions.length === 0" class="text-center py-8 text-gray-400">
        No questions added yet
      </div>

      <div v-else class="space-y-3 max-h-96 overflow-y-auto pr-2">
        <div v-for="(q,i) in questions"
          :key="q.id"
          class="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-blue-500 transition-all">

          <div class="flex justify-between items-center">
            <span class="font-medium text-blue-600">
              Q{{ i+1 }}
              <span v-if="q.section_name" class="text-xs text-gray-400 ml-2">
                ({{ q.section_name }})
              </span>
              <span v-else-if="q.section_id" class="text-xs text-gray-400 ml-2">
                (Section {{ q.section_id }})
              </span>
            </span>

            <div class="flex gap-2">
              <button @click="editQuestion(q)" class="text-blue-500 hover:text-blue-700" title="Edit">
                ✎
              </button>
              <button @click="deleteQuestion(q.id)" class="text-red-500 hover:text-red-700" title="Delete">
                🗑
              </button>
            </div>
          </div>

          <p class="text-gray-700 mt-2">{{ q.question_text }}</p>

          <div class="flex gap-4 mt-2 text-xs text-gray-500">
            <span>Marks: {{ q.marks }}</span>
            <span>Difficulty: {{ getDifficultyLabel(q.difficulty) }}</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'QuestionForm',

  props: {
    examId: {
      type: [Number, String],
      default: null
    },
    sectionId: {
      type: [Number, String],
      default: null
    },
    maxQuestions: {
      type: Number,
      default: 10
    },
    currentCount: {
      type: Number,
      default: 0
    }
  },
  emits: ['add', 'update:count'],
  data() {
    return {
      exams: [],
      sections: [],
      selectedExam: null,
      questions: [],
      editingId: null,
      loading: false,
      loadingQuestions: false,
      submitting: false,
      error: null,
      sectionError: null,
      form: {
        section_id: null,
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: '',
        marks: 1,
        difficulty: 3
      }
    }
  },
  computed: {
    isValid() {
      return this.form.section_id &&
        this.form.question_text &&
        this.form.option_a &&
        this.form.option_b &&
        this.form.correct_answer &&
        this.form.marks > 0
    },
    reachedLimit() {
      return this.questions.length >= this.maxQuestions
    }
  },
  watch: {
    examId: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.selectedExam = newVal
          this.fetchSections()
        }
      }
    },
    sectionId: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form.section_id = newVal
        }
      }
    }
  },
  mounted() {
    this.fetchExams()
    this.fetchQuestions()
  },
  methods: {
    getDifficultyLabel(level) {
      const levels = { 1: 'Easy', 2: 'Medium', 3: 'Hard' }
      return levels[level] || 'Medium'
    },

    async fetchExams() {
      if (this.examId) return
      
      this.loading = true
      try {
        this.exams = await api.get('/api/exams')
      } catch (err) {
        this.error = 'Could not load exams'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    async fetchSections() {
      const examId = this.examId || this.selectedExam
      if (!examId) return

      this.loading = true
      this.sectionError = null
      
      try {
        this.sections = await api.get(`/api/sections?exam_id=${examId}`)
        
        if (this.sections.length === 1) {
          this.form.section_id = this.sections[0].id
        }
      } catch (err) {
        this.sectionError = 'Could not load sections'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    handleSectionChange() {
      this.fetchQuestions()
    },

    async fetchQuestions() {
      this.loadingQuestions = true
      try {
        let url = '/api/exam-questions'
        
        if (this.form.section_id) {
          url += `?section_ids=${this.form.section_id}`
        }
        
        this.questions = await api.get(url)
        this.$emit('update:count', this.questions.length)
      } catch (err) {
        console.error('Error fetching questions:', err)
      } finally {
        this.loadingQuestions = false
      }
    },

    async submitQuestion() {
      if (!this.isValid || this.reachedLimit) return

      this.submitting = true
      this.error = null

      try {
        const questionData = {
          section_id: this.form.section_id,
          question_text: this.form.question_text,
          option_a: this.form.option_a,
          option_b: this.form.option_b,
          option_c: this.form.option_c || '',
          option_d: this.form.option_d || '',
          correct_answer: this.form.correct_answer,
          marks: this.form.marks,
          difficulty: this.form.difficulty
        }

        let data
        if (this.editingId) {
          data = await api.put(`/api/exam-questions/${this.editingId}`, questionData)
        } else {
          data = await api.post('/api/questions', questionData)
        }

        console.log('Response:', data)

        this.$emit('add', data)

        this.resetForm()
        await this.fetchQuestions()

      } catch (err) {
        this.error = err.message || `Error ${this.editingId ? 'updating' : 'saving'} question`
        console.error('Submit error:', err)
      } finally {
        this.submitting = false
      }
    },

    editQuestion(q) {
      this.form = {
        section_id: q.section_id,
        question_text: q.question_text,
        option_a: q.option_a,
        option_b: q.option_b,
        option_c: q.option_c || '',
        option_d: q.option_d || '',
        correct_answer: q.correct_answer,
        marks: q.marks,
        difficulty: q.difficulty
      }
      this.editingId = q.id

      window.scrollTo({ top: 0, behavior: 'smooth' })
    },

    async deleteQuestion(id) {
      if (!confirm('Delete this question?')) return

      try {
        await api.delete(`/api/exam-questions/${id}`)
        await this.fetchQuestions()

      } catch (err) {
        this.error = err.message || 'Failed to delete question'
        console.error('Delete error:', err)
      }
    },

    resetForm() {
      this.editingId = null
      this.form = {
        section_id: this.sectionId || null,
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: '',
        marks: 1,
        difficulty: 3
      }
    }
  }
}
</script>

<style scoped>
.spinner-small {
  width: 24px;
  height: 24px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
