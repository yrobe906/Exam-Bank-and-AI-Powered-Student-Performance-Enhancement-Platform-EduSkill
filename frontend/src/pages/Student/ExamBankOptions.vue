<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50/30">
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
        Back to Dashboard
      </button>
    </div>

    <!-- Main Content -->
    <div class="max-w-4xl mx-auto px-4 py-12">
      <!-- Page Title -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
          📚 Exam Bank
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Choose how you want to practice for your exams
        </p>
      </div>

      <!-- Option Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        <!-- Option 1: Downloadable Exam Questions -->
        <div 
          class="option-card group cursor-pointer"
          @click="navigateToExamBank"
        >
          <div class="card-inner">
            <!-- Icon -->
            <div class="icon-wrapper bg-gradient-to-br from-blue-500 to-cyan-400">
              <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>

            <!-- Content -->
            <h2 class="card-title">Downloadable Exam Questions</h2>
            <p class="card-description">
              Access and download past exam papers, practice questions, and study materials in PDF format for offline study.
            </p>

            <!-- Features List -->
            <ul class="features-list">
              <li>
                <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Download PDF materials
              </li>
              <li>
                <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Past exam papers
              </li>
              <li>
                <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Model answers included
              </li>
            </ul>

            <!-- Action Button -->
            <div class="card-action">
              <span class="btn-text">Browse Downloads</span>
              <svg class="w-5 h-5 btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Option 2: Online Practice Mock Test -->
        <div 
          class="option-card group cursor-pointer"
          @click="navigateToMockTest"
        >
          <div class="card-inner">
            <!-- Icon -->
            <div class="icon-wrapper bg-gradient-to-br from-purple-500 to-pink-400">
              <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>

            <!-- Content -->
            <h2 class="card-title">Online Practice Mock Test</h2>
            <p class="card-description">
              Take interactive mock exams online with instant feedback, explanations, and track your performance.
            </p>

            <!-- Features List -->
            <ul class="features-list">
              <li>
                <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Interactive online tests
              </li>
              <li>
                <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Instant feedback & explanations
              </li>
              <li>
                <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Performance tracking
              </li>
            </ul>

            <!-- Action Button -->
            <div class="card-action purple">
              <span class="btn-text">Start Practice</span>
              <svg class="w-5 h-5 btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MainHeader from '@/components/Header/MainHeader.vue';

export default {
  name: 'ExamBankOptions',
  components: {
    MainHeader
  },
  methods: {
    goBack() {
      this.$router.push('/student_dashboard');
    },
    navigateToExamBank() {
      // Navigate to exam papers page (using example examId=1, adjust as needed)
      this.$router.push('/library/books');
    }, 
    navigateToMockTest() {
      // Slow transition to mock test subject selection page
      // Using setTimeout to create a smooth transition effect
      setTimeout(() => {
        this.$router.push('/mock-test-subject');
      }, 150);
    }
  }
};
</script>

<style scoped>
/* Main container */
.min-h-screen {
  min-height: 100vh;
}

/* Option Card Styles */
.option-card {
  perspective: 1000px;
}

.card-inner {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 32px;
  padding: 40px 32px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.15),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.card-inner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #06b6d4);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.card-inner::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, transparent 100%);
  pointer-events: none;
}

/* Hover effects */
.option-card:hover .card-inner {
  transform: translateY(-8px);
  box-shadow: 
    0 35px 60px -15px rgba(0, 0, 0, 0.2),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
}

.option-card:hover .card-inner::before {
  transform: scaleX(1);
}

/* Icon wrapper */
.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
  transition: transform 0.3s ease;
}

.option-card:hover .icon-wrapper {
  transform: scale(1.05) rotate(3deg);
}

/* Card title */
.card-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
  line-height: 1.3;
}

/* Card description */
.card-description {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 24px;
  line-height: 1.6;
}

/* Features list */
.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 28px 0;
}

.features-list li {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  color: #475569;
  margin-bottom: 10px;
  padding: 8px 0;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.features-list li:hover {
  background: rgba(59, 130, 246, 0.05);
}

/* Card action button */
.card-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 16px;
  box-shadow: 0 8px 20px -6px rgba(59, 130, 246, 0.5);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card-action::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.option-card:hover .card-action::before {
  left: 100%;
}

.card-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px -8px rgba(59, 130, 246, 0.6);
}

.card-action:active {
  transform: translateY(0);
}

.card-action.purple {
  background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
  box-shadow: 0 8px 20px -6px rgba(168, 85, 247, 0.5);
}

.card-action.purple:hover {
  box-shadow: 0 12px 28px -8px rgba(168, 85, 247, 0.6);
}

.card-action.purple::before {
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
}

.btn-icon {
  transition: transform 0.3s ease;
}

.option-card:hover .btn-icon {
  transform: translateX(4px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .card-inner {
    padding: 28px 24px;
  }
  
  .card-title {
    font-size: 1.5rem;
  }
  
  .icon-wrapper {
    width: 64px;
    height: 64px;
    border-radius: 20px;
  }
  
  .icon-wrapper svg {
    width: 32px;
    height: 32px;
  }
  
  .card-action {
    width: 100%;
    justify-content: center;
  }
}

/* Animation for page load */
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

.option-card:nth-child(1) {
  animation: fadeInUp 0.6s ease forwards;
  animation-delay: 0.1s;
  opacity: 0;
}

.option-card:nth-child(2) {
  animation: fadeInUp 0.6s ease forwards;
  animation-delay: 0.25s;
  opacity: 0;
}
</style>
