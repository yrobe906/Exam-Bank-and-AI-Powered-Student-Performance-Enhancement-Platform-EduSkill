<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 p-6 lg:p-10">
    <div class="max-w-6xl mx-auto relative">
      <ExamStructureHeader />

      <form @submit.prevent="saveAll" class="relative">
        <!-- Glow background -->
        <div class="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-3xl blur-2xl opacity-20 animate-pulse-slow"></div>

        <div class="relative bg-white/10 backdrop-blur-2xl rounded-3xl p-8 lg:p-10 border border-white/20 shadow-2xl">
          <!-- Form header -->
          <div class="flex items-center justify-between mb-8 pb-6 border-b border-white/10">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-2xl font-bold text-white">Exam Hierarchy Builder</h2>
                <p class="text-white/60 text-sm">Create your complete exam structure in 3 simple steps</p>
              </div>
            </div>
            <div class="bg-white/5 px-4 py-2 rounded-full border border-white/10">
              <span class="text-white/80 text-sm font-medium">Step 1 of 3</span>
            </div>
          </div>

          <!-- Error Alert -->
          <div v-if="errors.length" class="mb-6 bg-red-500/10 border border-red-500/20 rounded-xl p-4 backdrop-blur-xl">
            <div class="flex items-start gap-3">
              <svg class="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div>
                <h3 class="text-white font-semibold mb-1">Please fix the following errors:</h3>
                <ul class="list-disc list-inside text-red-200 text-sm">
                  <li v-for="error in errors" :key="error">{{ error }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Form sections -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left: Exam Type -->
            <div class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-gradient-to-br from-amber-400/20 to-orange-500/20 rounded-lg flex items-center justify-center">
                  <span class="text-amber-400 font-bold">1</span>
                </div>
                <h3 class="text-white font-semibold text-lg">Exam Type Configuration</h3>
              </div>

              <div class="group">
                <label class="block text-white/90 text-sm font-semibold mb-2">Select Exam Type <span class="text-red-400">*</span></label>
                <select v-model="examType" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white">
                  <option v-for="type in examTypes" :key="type" :value="type">{{ type }}</option>
                </select>
              </div>

              <div v-if="examType==='Entrance'">
                <label class="block text-white/90 text-sm font-semibold mb-2">Exam Year *</label>
                <select v-model="year" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white">
                  <option disabled value="">Select Year</option>
                  <option v-for="y in entranceYears" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>

              <div v-if="examType==='Remedial'">
                <label class="block text-white/90 text-sm font-semibold mb-2">University *</label>
                <select v-model="university" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white">
                  <option disabled value="">Select University</option>
                  <option v-for="u in universities" :key="u" :value="u">{{ u }}</option>
                </select>
              </div>

              <div v-if="examType==='Model'">
                <label class="block text-white/90 text-sm font-semibold mb-2">Model Type *</label>
                <select v-model="modelType" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white">
                  <option disabled value="">Select Model Type</option>
                  <option value="Regional">Regional</option>
                  <option value="Zone">Zone</option>
                  <option value="City">City</option>
                  <option value="School">School</option>
                </select>

                <div v-if="modelType==='Regional'">
                  <label class="block text-white/90 text-sm font-semibold mb-2">Exam Year *</label>
                  <select v-model="year" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white">
                    <option disabled value="">Select Year</option>
                    <option v-for="y in modelYears" :key="y" :value="y">{{ y }}</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Right: Subject & Topic -->
            <div class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-gradient-to-br from-amber-400/20 to-orange-500/20 rounded-lg flex items-center justify-center">
                  <span class="text-amber-400 font-bold">2</span>
                </div>
                <h3 class="text-white font-semibold text-lg">Subject & Topic Setup</h3>
              </div>

              <div>
                <label class="block text-white/90 text-sm font-semibold mb-2">Subject Name *</label>
                <select v-model="subject" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white">
                  <option disabled value="">Select Subject</option>
                  <option v-for="s in subjects" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>

              <div>
                <label class="block text-white/90 text-sm font-semibold mb-2">Topic Name *</label>
                <input v-model="topic" placeholder="e.g., Algebra, Mechanics" class="w-full bg-white/5 border-2 border-white/10 rounded-xl px-4 py-4 text-white" />
              </div>
            </div>
          </div>

          <!-- Buttons -->
          <div class="mt-10 pt-6 border-t border-white/10 flex items-center justify-between">
            <button type="button" @click="resetForm" class="px-6 py-3 rounded-xl text-white/70 hover:text-white hover:bg-white/10">
              Reset
            </button>

            <button type="submit" class="px-10 py-4 bg-gradient-to-r from-amber-400 to-orange-500 rounded-xl text-white font-semibold" :disabled="searching">
              <span v-if="!searching">Create Exam Structure</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              </span>
            </button>
          </div>
        </div>
      </form>

      <!-- Success Overlay with Search Icon -->
      <div v-if="showSuccess" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-white/10 backdrop-blur-2xl rounded-3xl p-12 border border-white/20 shadow-2xl max-w-md w-full mx-4">
          <div class="text-center">
            <!-- Animated Search Icon -->
            <div class="relative w-32 h-32 mx-auto mb-6">
              <!-- Outer ring -->
              <div class="absolute inset-0 border-4 border-amber-400/30 rounded-full animate-ping"></div>
              <!-- Middle ring -->
              <div class="absolute inset-2 border-4 border-orange-400/40 rounded-full animate-spin-slow"></div>
              <!-- Inner circle with search icon -->
              <div class="absolute inset-4 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center">
                <svg class="w-12 h-12 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
            </div>
            
            <h3 class="text-2xl font-bold text-white mb-2">Searching Questions...</h3>
            <p class="text-white/60 mb-4">We're finding the best questions for your exam structure</p>
            
            <!-- Progress bar -->
            <div class="w-full bg-white/10 rounded-full h-2 mb-2">
              <div class="bg-gradient-to-r from-amber-400 to-orange-500 h-2 rounded-full animate-progress"></div>
            </div>
            
            <p class="text-white/40 text-sm">Redirecting in {{ countdown }} seconds...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ExamStructureHeader from '../../../components/Header/ExamStructureHeader.vue'

export default {
  components: { ExamStructureHeader },
  data() {
    return {
      examTypes: ['Entrance', 'Remedial', 'Model'],
      examType: 'Entrance',
      entranceYears: [2022, 2023, 2024, 2025, 2026],
      modelYears: [2024, 2025, 2026],
      universities: ['AAU', 'Jimma', 'Meda Wolabu', 'Hawassa'],
      subjects: ['Mathematics', 'Chemistry', 'Biology', 'IT', 'Physics', 'English', 'Aptitude'],

      year: null,
      university: null,
      modelType: null,
      subject: null,
      topic: '',

      errors: [],
      searching: false,
      showSuccess: false,
      countdown: 2,
      timer: null
    };
  },

  methods: {
    validateForm() {
      this.errors = [];
      if (this.examType==='Entrance' && !this.year) this.errors.push('Select entrance year');
      if (this.examType==='Remedial' && !this.university) this.errors.push('Select university');
      if (this.examType==='Model' && !this.modelType) this.errors.push('Select model type');
      if (this.examType==='Model' && this.modelType==='Regional' && !this.year) this.errors.push('Select exam year');
      if (!this.subject) this.errors.push('Select subject');
      if (!this.topic.trim()) this.errors.push('Enter topic');
      return this.errors.length===0;
    },

    async saveAll() {
      if (!this.validateForm()) return;

      this.searching = true;

      try {
        const res = await fetch("http://127.0.0.1:8000/api/exam-structure", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            exam_type: this.examType,
            year: this.year || null,
            university: this.university || null,
            model_type: this.modelType || null,
            subject: this.subject,
            topic: this.topic.trim()
          })
        });

        if (!res.ok) throw new Error('Failed to create exam structure');
        const structure = await res.json();
        console.log("Created Structure ID:", structure.id);

        // Show success overlay with search icon
        this.searching = false;
        this.showSuccess = true;
        this.countdown = 2;
        
        // Clear any existing timer
        if (this.timer) clearInterval(this.timer);
        
        // Start countdown
        this.timer = setInterval(() => {
          this.countdown--;
          if (this.countdown <= 0) {
            clearInterval(this.timer);
            this.redirectToQuestions();
          }
        }, 1000);

      } catch (err) {
        console.error(err);
        this.errors.push('Backend connection failed');
        this.searching = false;
      }
    },

    redirectToQuestions() {
  this.showSuccess = false;
  // Use path instead of name
  this.$router.push({ path: '/question_repository' }); // or whatever your actual path is
},

    resetForm() {
      this.examType = 'Entrance';
      this.year = null;
      this.university = null;
      this.modelType = null;
      this.subject = null;
      this.topic = '';
      this.errors = [];
      this.showSuccess = false;
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    }
  },

  beforeDestroy() {
    // Clean up timer when component is destroyed
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
}
</script>

<style>
/* Add these new animations to your existing styles */
@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}

@keyframes progress {
  0% {
    width: 0%;
  }
  50% {
    width: 70%;
  }
  100% {
    width: 100%;
  }
}

.animate-progress {
  animation: progress 2s ease-in-out forwards;
}

/* Keep all your existing styles below */
@keyframes blob {
  0% { transform: scale(1); }
  33% { transform: scale(1.1); }
  66% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes expand {
  0% { transform: scaleX(0); }
  100% { transform: scaleX(1); }
}

.animate-expand {
  animation: expand 1.5s ease-out forwards;
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.3; }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

@keyframes slide-down {
  0% { opacity: 0; transform: translateY(-10px); }
  100% { opacity: 1; transform: translateY(0); }
}

.animate-slide-down {
  animation: slide-down 0.3s ease-out;
}

/* Custom scrollbar */
select::-webkit-scrollbar,
textarea::-webkit-scrollbar {
  width: 8px;
}

select::-webkit-scrollbar-track,
textarea::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

select::-webkit-scrollbar-thumb,
textarea::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

select::-webkit-scrollbar-thumb:hover,
textarea::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Glass morphism */
.backdrop-blur-2xl {
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .text-5xl {
    font-size: 2.5rem;
  }
  
  .lg\:text-6xl {
    font-size: 3rem;
  }
}

/* Disabled state */
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Number input spinner removal */
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}

/* Selection color */
::selection {
  background: rgba(251, 191, 36, 0.3);
  color: white;
}

/* Focus outline */
*:focus {
  outline: none;
}
</style>