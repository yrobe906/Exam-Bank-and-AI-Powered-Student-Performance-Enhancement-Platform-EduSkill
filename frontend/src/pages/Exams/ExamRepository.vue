<template>
  <div class="min-h-screen bg-gray-900 p-6 lg:p-10">
    <div class="max-w-5xl mx-auto">
      <!-- Filters -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-8">
        <!-- Subject -->
        <select v-model="filters.subjectId" @change="loadTopics"
                class="bg-gray-800 text-white rounded-xl px-4 py-3">
          <option value="">Select Subject</option>
          <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>

        <!-- Topic -->
        <select v-model="filters.topicId" :disabled="!filters.subjectId"
                class="bg-gray-800 text-white rounded-xl px-4 py-3">
          <option value="">{{ filters.subjectId ? 'Select Topic' : 'Select Subject First' }}</option>
          <option v-for="t in topics" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>

        <!-- Exam Type -->
        <select v-model="filters.examType" class="bg-gray-800 text-white rounded-xl px-4 py-3">
          <option value="">Select Exam Type</option>
          <option v-for="type in examTypes" :key="type" :value="type">{{ type }}</option>
        </select>

        <!-- Year -->
        <select v-model="filters.year" class="bg-gray-800 text-white rounded-xl px-4 py-3">
          <option value="">Select Year</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>

      <!-- Questions List -->
      <div class="space-y-6">
        <div v-for="q in filteredQuestions" :key="q.id" class="bg-gray-800 rounded-2xl p-6 border border-gray-700">
          <!-- Question -->
          <p class="text-white font-semibold mb-3">{{ q.question_text }}</p>

          <!-- Options -->
          <ul class="list-none space-y-2">
            <li v-for="opt in ['a','b','c','d']" :key="opt"
                class="flex items-center gap-2 p-3 rounded-xl border"
                :class="{
                  'border-green-500 bg-green-600/20': opt.toUpperCase() === q.correct_answer,
                  'border-gray-700 bg-gray-700/50': opt.toUpperCase() !== q.correct_answer
                }">
              <span class="font-bold text-white">{{ opt.toUpperCase() }}.</span>
              <span class="text-white">{{ q['option_' + opt] }}</span>
            </li>
          </ul>

          <!-- Optional Explanation -->
          <p v-if="q.explanation" class="mt-3 text-sm text-gray-300">
            Explanation: {{ q.explanation }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      subjects: [],
      topics: [],
      examTypes: ['Midterm', 'Final', 'Quiz'],
      years: [2023, 2024, 2025],
      filters: {
        subjectId: '',
        topicId: '',
        examType: '',
        year: ''
      },
      questions: []
    };
  },
  mounted() {
    this.loadSubjects();
    this.loadQuestions();
  },
  methods: {
    async loadSubjects() {
      const res = await fetch('/api/subjects');
      this.subjects = await res.json();
    },
    async loadTopics() {
      if (!this.filters.subjectId) return;
      const res = await fetch(`/api/topics?subject_id=${this.filters.subjectId}`);
      this.topics = await res.json();
      this.filters.topicId = '';
    },
    async loadQuestions() {
      // Fetch all questions initially, filtering can be done in computed
      const res = await fetch('/api/questions');
      this.questions = await res.json();
    }
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter(q => {
        return (!this.filters.subjectId || q.subject_id === this.filters.subjectId) &&
               (!this.filters.topicId || q.topic_id === this.filters.topicId) &&
               (!this.filters.examType || q.exam_type === this.filters.examType) &&
               (!this.filters.year || q.year === this.filters.year);
      });
    }
  }
};
</script>
