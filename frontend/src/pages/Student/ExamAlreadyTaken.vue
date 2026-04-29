<template>
  <div class="already-taken-page">
    <AppHeader />
    
    <div class="content-wrapper">
      <div class="forbidden-container">
        <!-- Animated Lock Icon -->
        <div class="lock-icon-container">
          <div class="lock-icon">🔒</div>
          <div class="lock-shake">🚫</div>
        </div>
        
        <!-- Main Message -->
        <h1 class="main-title">No Way! It's Forbidden!</h1>
        <p class="subtitle">You cannot retake this exam</p>
        
        <!-- Previous Result Card -->
        <div class="result-card" v-if="previousScore !== null">
          <div class="card-header">
            <span class="card-icon">📊</span>
            <span>Your Previous Result</span>
          </div>
          
          <div class="score-display">
            <div class="score-circle" :class="scoreClass">
              <span class="percentage">{{ percentage }}%</span>
            </div>
          </div>
          
          <div class="score-details">
            <div class="detail-item">
              <span class="detail-label">Score</span>
              <span class="detail-value">{{ previousScore }} / {{ totalMarks }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Status</span>
              <span class="detail-value status" :class="statusClass">{{ statusText }}</span>
            </div>
          </div>
        </div>
        
        <!-- Message Box -->
        <div class="message-box">
          <p>{{ message }}</p>
        </div>
        
        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="btn-home" @click="goHome">
            <span class="btn-icon">🏠</span>
            Back to Home
          </button>
          <button class="btn-performance" @click="viewPerformance">
            <span class="btn-icon">📈</span>
            View My Performance
          </button>
        </div>
        
        <!-- Decorative Elements -->
        <div class="decorations">
          <span class="decoemoji emoji-1">⛔</span>
          <span class="decoemoji emoji-2">🛑</span>
          <span class="decoemoji emoji-3">❌</span>
          <span class="decoemoji emoji-4">🚷</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppHeader from '@/components/layout/AppHeader.vue';

export default {
  name: 'ExamAlreadyTaken',
  components: {
    AppHeader
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const message = ref('You have already taken this exam. Each exam can only be taken once!');
    const previousScore = ref(null);
    const totalMarks = ref(null);
    const percentage = ref(null);
    const previousAttemptId = ref(null);
    
    const scoreClass = computed(() => {
      if (percentage.value >= 70) return 'excellent';
      if (percentage.value >= 50) return 'good';
      if (percentage.value >= 30) return 'average';
      return 'needs-improvement';
    });
    
    const statusClass = computed(() => {
      if (percentage.value >= 70) return 'excellent';
      if (percentage.value >= 50) return 'good';
      if (percentage.value >= 30) return 'average';
      return 'needs-improvement';
    });
    
    const statusText = computed(() => {
      if (percentage.value >= 70) return 'Excellent!';
      if (percentage.value >= 50) return 'Good';
      if (percentage.value >= 30) return 'Keep Trying';
      return 'Need Improvement';
    });
    
    const goHome = () => {
      router.push('/student/dashboard');
    };
    
    const viewPerformance = () => {
      router.push('/student/performance-analytics');
    };
    
    onMounted(() => {
      // Get data from route query params (passed from TakeExam.vue)
      message.value = route.query.message || 'You have already taken this exam. Each exam can only be taken once!';
      previousScore.value = route.query.previous_score ? parseInt(route.query.previous_score) : null;
      totalMarks.value = route.query.total_marks ? parseInt(route.query.total_marks) : null;
      percentage.value = route.query.percentage ? parseFloat(route.query.percentage) : null;
      previousAttemptId.value = route.query.attempt_id ? parseInt(route.query.attempt_id) : null;
    });
    
    return {
      message,
      previousScore,
      totalMarks,
      percentage,
      previousAttemptId,
      scoreClass,
      statusClass,
      statusText,
      goHome,
      viewPerformance
    };
  }
};
</script>

<style scoped>
.already-taken-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  position: relative;
  overflow: hidden;
}

.content-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 80px);
  padding: 2rem;
}

.forbidden-container {
  max-width: 600px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
}

/* Lock Icon Animation */
.lock-icon-container {
  position: relative;
  margin-bottom: 1.5rem;
}

.lock-icon {
  font-size: 5rem;
  animation: float 3s ease-in-out infinite;
}

.lock-shake {
  position: absolute;
  top: -10px;
  right: -20px;
  font-size: 2.5rem;
  animation: shake 0.5s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

/* Main Title */
.main-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
}

.subtitle {
  font-size: 1.2rem;
  color: #a0a0a0;
  margin-bottom: 2rem;
}

/* Result Card */
.result-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 1.5rem;
}

.card-icon {
  font-size: 1.5rem;
}

/* Score Circle */
.score-display {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  inset: -5px;
  border-radius: 50%;
  padding: 5px;
  background: linear-gradient(135deg, var(--color-1), var(--color-2));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}

.score-circle.excellent {
  --color-1: #10b981;
  --color-2: #059669;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.1));
}

.score-circle.good {
  --color-1: #3b82f6;
  --color-2: #2563eb;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.1));
}

.score-circle.average {
  --color-1: #f59e0b;
  --color-2: #d97706;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.1));
}

.score-circle.needs-improvement {
  --color-1: #ef4444;
  --color-2: #dc2626;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.1));
}

.percentage {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
}

/* Score Details */
.score-details {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.detail-item {
  text-align: center;
}

.detail-label {
  display: block;
  font-size: 0.85rem;
  color: #a0a0a0;
  margin-bottom: 0.25rem;
}

.detail-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
}

.detail-value.status.excellent {
  color: #10b981;
}

.detail-value.status.good {
  color: #3b82f6;
}

.detail-value.status.average {
  color: #f59e0b;
}

.detail-value.status.needs-improvement {
  color: #ef4444;
}

/* Message Box */
.message-box {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
}

.message-box p {
  color: #ff6b6b;
  font-size: 1rem;
  margin: 0;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-home, .btn-performance {
  padding: 1rem 2rem;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-home {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-home:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px -5px rgba(102, 126, 234, 0.4);
}

.btn-performance {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-performance:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Decorations */
.decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.decoemoji {
  position: absolute;
  font-size: 3rem;
  opacity: 0.15;
}

.emoji-1 {
  top: 10%;
  left: 10%;
  animation: float 4s ease-in-out infinite;
}

.emoji-2 {
  top: 20%;
  right: 15%;
  animation: float 5s ease-in-out infinite 0.5s;
}

.emoji-3 {
  bottom: 30%;
  left: 5%;
  animation: float 6s ease-in-out infinite 1s;
}

.emoji-4 {
  bottom: 20%;
  right: 10%;
  animation: float 4.5s ease-in-out infinite 0.8s;
}

/* Responsive */
@media (max-width: 600px) {
  .main-title {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .score-circle {
    width: 120px;
    height: 120px;
  }
  
  .percentage {
    font-size: 2rem;
  }
  
  .score-details {
    flex-direction: column;
    gap: 1rem;
  }
  
  .score-circle.excellent,
  .score-circle.good,
  .score-circle.average,
  .score-circle.needs-improvement {
    --color-1: #fff;
    --color-2: #fff;
  }
}
</style>
