<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 p-6 lg:p-10">
    <!-- Animated background elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
    </div>

    <div class="max-w-6xl mx-auto relative">
      <!-- Header with Back Button -->
      <div class="mb-8 flex items-center justify-between">
        <button @click="goBack" class="flex items-center gap-2 text-white/70 hover:text-white transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span>Back to Structure</span>
        </button>

        <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-xl rounded-full px-4 py-2 border border-white/20">
          <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          <span class="text-white/80 text-sm">Structure ID: {{ structureId }}</span>
          <span v-if="examDetails" class="text-white/40 text-xs ml-2">{{ examDetails.exam_type }} • {{ examDetails.subject }}</span>
        </div>
      </div>

      <!-- Main Header -->
      <div class="mb-10 text-center">
        <div class="inline-flex items-center justify-center mb-4">
          <div class="relative">
            <div class="absolute inset-0 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 blur-xl opacity-50 animate-pulse-slow"></div>
            <div class="relative bg-gradient-to-r from-amber-400/20 to-orange-500/20 backdrop-blur-xl px-6 py-3 rounded-full border border-white/30">
              <span class="text-sm font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-yellow-300 to-orange-400">
                ExamCraft • Question Repository
              </span>
            </div>
          </div>
        </div>

        <h1 class="text-5xl lg:text-6xl font-black mb-4">
          <span class="bg-gradient-to-r from-amber-200 via-yellow-300 to-amber-400 bg-clip-text text-transparent">
            Manage Questions
          </span>
        </h1>
        <p class="text-white/60 text-lg max-w-2xl mx-auto">
          Add and manage questions for your exam structure
        </p>
      </div>

      <!-- MAIN GRID -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- LEFT COLUMN: MCQ Form -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Add MCQ Card -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl blur-2xl opacity-20 animate-pulse-slow"></div>
            
            <div class="relative bg-white/10 backdrop-blur-2xl rounded-3xl p-6 lg:p-8 border border-white/20 shadow-2xl">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <h2 class="text-xl font-bold text-white">{{ editingId ? 'Edit Question' : 'Add New Question' }}</h2>
              </div>

              <!-- Error Alert -->
              <div v-if="errors.length" class="mb-4 bg-red-500/10 border border-red-500/20 rounded-xl p-3">
                <ul class="list-disc list-inside text-red-200 text-xs">
                  <li v-for="error in errors" :key="error">{{ error }}</li>
                </ul>
              </div>

              <!-- Form -->
              <form @submit.prevent="addQuestion" class="space-y-4">
                <!-- Question -->
                <div>
                  <label class="block text-white/70 text-xs mb-1">Question *</label>
                  <textarea v-model="form.question" rows="2" 
                    class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-2 text-sm text-white placeholder-white/40 focus:border-amber-400 transition-all"
                    placeholder="Enter your question..."></textarea>
                </div>

                <!-- Options -->
                <div>
                  <label class="block text-white/70 text-xs mb-1">Options *</label>
                  <div class="grid grid-cols-2 gap-2">
                    <div v-for="opt in ['A','B','C','D']" :key="opt" class="relative">
                      <span class="absolute left-2 top-1/2 -translate-y-1/2 text-white/40 text-sm font-bold">{{ opt }}.</span>
                      <input v-model="form.options[opt.toLowerCase()]" :placeholder="`Option ${opt}`" 
                        class="w-full bg-white/5 border-2 border-white/10 rounded-lg pl-7 pr-2 py-2 text-sm text-white placeholder-white/40 focus:border-amber-400" />
                    </div>
                  </div>
                </div>

                <!-- Difficulty & Correct Answer -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-white/70 text-xs mb-1">Difficulty *</label>
                    <select v-model="form.difficulty" class="w-full bg-white/5 border-2 border-white/10 rounded-lg px-3 py-2 text-sm text-white">
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-white/70 text-xs mb-1">Correct Answer *</label>
                    <div class="flex gap-2">
                      <button type="button" v-for="opt in ['A','B','C','D']" :key="opt" 
                        @click="form.correct = opt" 
                        class="w-8 h-8 rounded-lg text-sm font-bold transition-all"
                        :class="form.correct === opt ? 'bg-amber-400 text-gray-900 shadow-lg' : 'bg-white/10 text-white/70 hover:bg-white/20'">
                        {{ opt }}
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Explanation -->
                <div>
                  <label class="block text-white/70 text-xs mb-1">Explanation</label>
                  <textarea v-model="form.explanation" rows="1" 
                    class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-2 text-sm text-white placeholder-white/40 focus:border-amber-400 resize-none"
                    placeholder="Optional explanation..."></textarea>
                </div>

                <!-- Form Actions -->
                <div class="flex justify-between items-center pt-4 border-t border-white/10">
                  <button type="button" @click="resetForm" class="text-xs text-white/50 hover:text-white/80 flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Reset
                  </button>
                  <button type="submit" :disabled="isSubmitting || !structureId" 
                    class="px-6 py-2 bg-gradient-to-r from-amber-400 to-orange-500 rounded-lg text-white text-sm font-semibold hover:from-amber-500 hover:to-orange-600 disabled:opacity-50 transition-all transform hover:scale-105 flex items-center gap-2">
                    <span v-if="!isSubmitting">
                      {{ editingId ? 'Update Question' : 'Save Question' }}
                    </span>
                    <span v-else class="flex items-center gap-2">
                      <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Saving...
                    </span>
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Questions List -->
          <div class="relative bg-white/5 backdrop-blur-2xl rounded-3xl p-6 border border-white/20">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-white font-bold flex items-center gap-2">
                <svg class="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Question Bank
              </h3>
              <span class="text-white/40 text-xs">{{ questions.length }} questions</span>
            </div>

            <div class="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scroll">
              <div v-for="q in questions" :key="q.id" 
                class="group bg-white/5 hover:bg-white/10 rounded-xl p-4 border border-white/10 transition-all duration-300">
                <div class="flex justify-between items-start gap-3">
                  <div class="flex-1">
                    <p class="text-white text-sm font-medium">{{ q.question_text }}</p>
                    <div class="flex flex-wrap gap-2 mt-2">
                      <span class="px-2 py-1 bg-white/10 rounded text-xs text-white/70">✅ {{ q.correct_answer }}</span>
                      <span class="px-2 py-1 rounded text-xs" :class="difficultyClass(q.difficulty)">
                        {{ q.difficulty }}
                      </span>
                      <span v-if="q.pdf_file" class="px-2 py-1 bg-emerald-500/20 rounded text-xs text-emerald-300">
                        📎 PDF
                      </span>
                    </div>
                  </div>
                  <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button @click="editQuestion(q)" class="p-1.5 bg-indigo-500/20 hover:bg-indigo-500/40 rounded-lg text-indigo-300 transition-all" title="Edit">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="deleteQuestion(q.id)" class="p-1.5 bg-red-500/20 hover:bg-red-500/40 rounded-lg text-red-300 transition-all" title="Delete">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="!questions.length" class="text-center py-12 text-white/40">
                <svg class="w-16 h-16 mx-auto mb-3 text-white/20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p class="text-sm">No questions yet. Add your first question above.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: PDF Upload & Info -->
        <div class="lg:col-span-1">
          <div class="relative sticky top-6 space-y-6">
            <!-- PDF Upload Card -->
            <div class="bg-white/10 backdrop-blur-2xl rounded-3xl p-6 border border-white/20">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-10 h-10 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 class="text-white font-bold">Upload PDF Exam</h3>
              </div>

              <div @click="triggerFileInput" @dragover.prevent="dragOver = true" @dragleave.prevent="dragOver = false"
                @drop.prevent="handleFileDrop" 
                class="border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all duration-300"
                :class="dragOver ? 'border-emerald-400 bg-emerald-500/20 scale-105' : 'border-white/30 hover:border-white/50 hover:bg-white/5'">
                
                <input ref="fileInput" type="file" accept=".pdf" @change="handleFileSelect" class="hidden" />
                
                <div class="relative mb-3">
                  <div class="absolute inset-0 bg-emerald-500 rounded-full blur-xl opacity-30"></div>
                  <div class="relative w-16 h-16 mx-auto bg-gradient-to-br from-emerald-400 to-teal-500 rounded-2xl flex items-center justify-center">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                </div>
                <p class="text-white text-sm mb-1">Click to upload or drag & drop</p>
                <p class="text-white/40 text-xs">PDF files only (max 50MB)</p>
              </div>

              <!-- PDF List -->
              <div v-if="pdfFiles.length" class="mt-4">
                <h4 class="text-white/70 text-xs mb-2">Uploaded PDFs</h4>
                <div class="space-y-2">
                  <div v-for="file in pdfFiles" :key="file.id" 
                    class="group/file flex items-center justify-between bg-white/5 hover:bg-white/10 rounded-xl p-2 border border-white/10">
                    <div class="flex items-center gap-2 min-w-0">
                      <svg class="w-4 h-4 text-emerald-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span class="text-white/80 text-xs truncate">{{ file.name }}</span>
                    </div>
                    <button @click="deletePdf(file.id)" class="opacity-0 group-hover/file:opacity-100 p-1 hover:bg-red-500/20 rounded-lg transition-all">
                      <svg class="w-3 h-3 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Stats Card -->
            <div class="bg-white/5 backdrop-blur-2xl rounded-3xl p-6 border border-white/20">
              <h4 class="text-white/70 text-xs mb-3">EXAM OVERVIEW</h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-white/50 text-xs">Structure ID</span>
                  <span class="text-white text-xs font-mono">{{ structureId }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-white/50 text-xs">Exam Type</span>
                  <span class="text-white text-xs">{{ examDetails?.exam_type || '—' }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-white/50 text-xs">Subject</span>
                  <span class="text-white text-xs">{{ examDetails?.subject || '—' }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-white/50 text-xs">Topic</span>
                  <span class="text-white text-xs">{{ examDetails?.topic || '—' }}</span>
                </div>
                <div class="pt-2 mt-2 border-t border-white/10">
                  <div class="flex justify-between items-center">
                    <span class="text-white/50 text-xs">Total Questions</span>
                    <span class="text-amber-400 font-bold">{{ questions.length }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Success Toast -->
      <transition name="toast">
        <div v-if="showToast" class="fixed bottom-8 right-8 max-w-md z-50">
          <div class="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl shadow-2xl p-1">
            <div class="bg-gray-900/95 backdrop-blur-xl rounded-xl px-6 py-4 flex items-center gap-4">
              <div class="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
                <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="text-white font-medium text-sm">{{ toastMessage }}</span>
              <button @click="showToast = false" class="text-white/40 hover:text-white">✕</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      API: "http://127.0.0.1:8000",
      structureId: null,
      examDetails: null,
      
      // Form data
      form: {
        question: "",
        options: { a: "", b: "", c: "", d: "" },
        correct: "A",
        difficulty: "easy",
        explanation: ""
      },
      
      editingId: null,
      isSubmitting: false,
      errors: [],
      showToast: false,
      toastMessage: "",
      
      questions: [],
      pdfFiles: [],
      dragOver: false
    };
  },

  mounted() {
    // Get structure_id from query params (passed from Exam Structure page)
    this.structureId = this.$route.query.structure_id;
    console.log("Structure ID from query:", this.structureId);
    
    if (this.structureId) {
      this.fetchExamDetails();
      this.fetchQuestions();
      this.fetchPdfs();
    } else {
      this.errors = ["Structure ID is missing. Please go back and create an exam structure."];
    }
  },

  methods: {
    goBack() {
      this.$router.push('/exam-structure'); // Adjust path as needed
    },

    async fetchExamDetails() {
      try {
        const res = await fetch(`${this.API}/exam-structure/${this.structureId}`);
        if (res.ok) {
          this.examDetails = await res.json();
        }
      } catch (err) {
        console.error("Failed to fetch exam details:", err);
      }
    },

    validateForm() {
      this.errors = [];
      if (!this.structureId) {
        this.errors.push("Structure ID is missing");
      }
      if (!this.form.question?.trim()) this.errors.push("Question is required");
      if (!this.form.options.a?.trim()) this.errors.push("Option A is required");
      if (!this.form.options.b?.trim()) this.errors.push("Option B is required");
      if (!this.form.options.c?.trim()) this.errors.push("Option C is required");
      if (!this.form.options.d?.trim()) this.errors.push("Option D is required");
      return this.errors.length === 0;
    },

    async addQuestion() {
      if (!this.validateForm()) return;
      
      this.isSubmitting = true;
      this.errors = [];

      const formData = new FormData();
      formData.append('structure_id', this.structureId);
      formData.append('question_text', this.form.question);
      formData.append('option_a', this.form.options.a);
      formData.append('option_b', this.form.options.b);
      formData.append('option_c', this.form.options.c);
      formData.append('option_d', this.form.options.d);
      formData.append('correct_answer', this.form.correct);
      formData.append('difficulty', this.form.difficulty);
      formData.append('explanation', this.form.explanation || '');

      try {
        const url = this.editingId 
          ? `${this.API}/questions/${this.editingId}`
          : `${this.API}/questions/`;

        const res = await fetch(url, {
          method: this.editingId ? "PUT" : "POST",
          body: formData
        });

        if (!res.ok) {
          const errorData = await res.json();
          throw new Error(errorData.detail || "Server error");
        }

        this.toastMessage = this.editingId ? "Question updated!" : "Question added!";
        this.showToast = true;
        setTimeout(() => this.showToast = false, 3000);
        
        await this.fetchQuestions();
        this.resetForm();

      } catch (err) {
        console.error("Error:", err);
        this.errors.push(err.message);
      } finally {
        this.isSubmitting = false;
      }
    },

    async fetchQuestions() {
      try {
        const res = await fetch(`${this.API}/questions/by-structure/${this.structureId}`);
        if (res.ok) {
          this.questions = await res.json();
        }
      } catch (err) {
        console.error("Failed to fetch questions:", err);
      }
    },

    async fetchPdfs() {
      try {
        const res = await fetch(`${this.API}/questions/pdfs`);
        if (res.ok) {
          this.pdfFiles = await res.json();
        }
      } catch (err) {
        console.error("Failed to fetch PDFs:", err);
      }
    },

    editQuestion(q) {
      this.editingId = q.id;
      this.form = {
        question: q.question_text,
        options: {
          a: q.option_a,
          b: q.option_b,
          c: q.option_c,
          d: q.option_d
        },
        correct: q.correct_answer,
        difficulty: q.difficulty,
        explanation: q.explanation || ''
      };
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    async deleteQuestion(id) {
      if (!confirm('Delete this question?')) return;
      
      try {
        const res = await fetch(`${this.API}/questions/${id}`, {
          method: "DELETE"
        });
        
        if (res.ok) {
          this.toastMessage = "Question deleted";
          this.showToast = true;
          setTimeout(() => this.showToast = false, 3000);
          await this.fetchQuestions();
        }
      } catch (err) {
        console.error(err);
      }
    },

    resetForm() {
      this.form = {
        question: "",
        options: { a: "", b: "", c: "", d: "" },
        correct: "A",
        difficulty: "easy",
        explanation: ""
      };
      this.editingId = null;
      this.errors = [];
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleFileSelect(e) {
      const file = e.target.files[0];
      if (file) this.uploadPdf(file);
    },

    handleFileDrop(e) {
      this.dragOver = false;
      const file = e.dataTransfer.files[0];
      if (file) this.uploadPdf(file);
    },

    async uploadPdf(file) {
      if (!file.type.includes('pdf')) {
        this.errors.push('Please upload a PDF file');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);
      formData.append('structure_id', this.structureId);
      
      // Add required fields with defaults
      formData.append('question_text', `PDF: ${file.name}`);
      formData.append('option_a', 'Option A');
      formData.append('option_b', 'Option B');
      formData.append('option_c', 'Option C');
      formData.append('option_d', 'Option D');
      formData.append('correct_answer', 'A');
      formData.append('difficulty', 'medium');
      formData.append('explanation', `Uploaded PDF: ${file.name}`);

      try {
        const res = await fetch(`${this.API}/questions/`, {
          method: "POST",
          body: formData
        });

        if (res.ok) {
          this.toastMessage = "PDF uploaded successfully!";
          this.showToast = true;
          setTimeout(() => this.showToast = false, 3000);
          await this.fetchPdfs();
          await this.fetchQuestions();
        }
      } catch (err) {
        console.error(err);
        this.errors.push('Failed to upload PDF');
      }
    },

    deletePdf(id) {
      // Implement PDF deletion if needed
    },

    difficultyClass(level) {
      const classes = {
        easy: 'bg-green-500/20 text-green-300',
        medium: 'bg-yellow-500/20 text-yellow-300',
        hard: 'bg-red-500/20 text-red-300'
      };
      return classes[level] || 'bg-white/10 text-white/70';
    }
  }
};
</script>

<style scoped>
@keyframes blob { 0%,100%{transform:scale(1)} 33%{transform:scale(1.1)} 66%{transform:scale(0.9)} }
.animate-blob { animation: blob 7s infinite; }
.animation-delay-2000 { animation-delay: 2s; }
@keyframes pulse-slow { 0%,100%{opacity:0.2} 50%{opacity:0.3} }
.animate-pulse-slow { animation: pulse-slow 4s ease-in-out infinite; }
.backdrop-blur-2xl { backdrop-filter: blur(40px); -webkit-backdrop-filter: blur(40px); }
.custom-scroll::-webkit-scrollbar { width: 5px; }
.custom-scroll::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
.custom-scroll::-webkit-scrollbar-thumb { background: rgba(251,191,36,0.3); border-radius: 10px; }
.custom-scroll::-webkit-scrollbar-thumb:hover { background: rgba(251,191,36,0.5); }
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(20px); }

/* Selection color */
::selection {
  background: rgba(251, 191, 36, 0.3);
  color: white;
}

/* Focus outline */
*:focus {
  outline: none;
}

/* Disabled state */
button:disabled {
  cursor: not-allowed;
}
</style>