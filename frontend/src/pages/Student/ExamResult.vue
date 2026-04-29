<template>
  <div class="result-page">
    <EduskillHeader>
      <p>Exam Results</p>
    </EduskillHeader>
    
    <div class="result-container">
      <!-- Result Card -->
      <div class="result-card">
        <div class="result-header" :class="resultClass">
          <div class="result-icon">{{ resultIcon }}</div>
          <h1>Exam Result</h1>
        </div>
        
        <div class="result-body">
          <!-- Score Display -->
          <div class="score-display">
            <div class="score-circle" :class="resultClass">
              <span class="score-percentage">{{ percentage }}%</span>
            </div>
            <div class="score-details">
              <h2>Your Score</h2>
              <p class="score-value">{{ score }} / {{ total }}</p>
              <p class="score-label">Correct Answers</p>
            </div>
          </div>
          
          <!-- Stats Grid -->
          <div class="stats-grid">
            <div class="stat-item correct">
              <span class="stat-icon">✓</span>
              <span class="stat-value">{{ correctCount }}</span>
              <span class="stat-label">Correct</span>
            </div>
            <div class="stat-item wrong">
              <span class="stat-icon">✗</span>
              <span class="stat-value">{{ wrongCount }}</span>
              <span class="stat-label">Wrong</span>
            </div>
            <div class="stat-item unanswered">
              <span class="stat-icon">○</span>
              <span class="stat-value">{{ unansweredCount }}</span>
              <span class="stat-label">Unanswered</span>
            </div>
          </div>
          
          <!-- Performance Message -->
          <div class="performance-message" :class="resultClass">
            {{ performanceMessage }}
          </div>
          
          <!-- AI Recommendation Section -->
          <div v-if="aiRecommendation" class="ai-recommendation" :class="resultClass">
            <div class="ai-header">
              <span class="ai-icon">🤖</span>
              <h3>AI Recommendation</h3>
            </div>
            <div class="ai-content">
              <!-- New Groq AI Format -->
              <div v-if="aiRecommendation.overall_assessment" class="overall-assessment">
                <p class="ai-description">{{ aiRecommendation.overall_assessment }}</p>
              </div>
              <!-- Legacy Format Support -->
              <div v-else>
                <p class="ai-title">{{ aiRecommendation.title }}</p>
                <p class="ai-description">{{ aiRecommendation.description }}</p>
              </div>
              
              <!-- Strengths -->
              <div v-if="aiRecommendation.strengths && aiRecommendation.strengths.length > 0" class="strengths">
                <h4>🌟 Your Strengths:</h4>
                <ul>
                  <li v-for="(strength, index) in aiRecommendation.strengths" :key="index">{{ strength }}</li>
                </ul>
              </div>
              
              <!-- Areas for Improvement -->
              <div v-if="aiRecommendation.areas_for_improvement && aiRecommendation.areas_for_improvement.length > 0" class="weak-sections">
                <h4>🎯 Areas for Improvement:</h4>
                <ul>
                  <li v-for="(area, index) in aiRecommendation.areas_for_improvement" :key="index">{{ area }}</li>
                </ul>
              </div>
              
              <!-- Recommendations (Study Tips) -->
              <div v-if="aiRecommendation.recommendations && aiRecommendation.recommendations.length > 0" class="study-tips">
                <h4>📚 Study Recommendations:</h4>
                <ul>
                  <li v-for="(rec, index) in aiRecommendation.recommendations" :key="index">{{ rec }}</li>
                </ul>
              </div>
              
              <!-- Legacy Study Tips Support -->
              <div v-else-if="aiRecommendation.study_tips && aiRecommendation.study_tips.length > 0" class="study-tips">
                <h4>📚 Study Tips:</h4>
                <ul>
                  <li v-for="(tip, index) in aiRecommendation.study_tips" :key="index">{{ tip }}</li>
                </ul>
              </div>
              
              <!-- Encouragement Message -->
              <div v-if="aiRecommendation.encouragement" class="encouragement">
                <p class="encouragement-text">💬 {{ aiRecommendation.encouragement }}</p>
              </div>
              
              <!-- Next Exam Difficulty Suggestion -->
              <div v-if="aiRecommendation.next_exam_difficulty" class="next-difficulty">
                <p class="next-difficulty-text">📈 Suggested Next Exam: <strong>{{ aiRecommendation.next_exam_difficulty }}</strong></p>
              </div>
            </div>
          </div>
          
          <!-- Loading AI Recommendation -->
          <div v-else-if="loadingAI" class="ai-recommendation loading">
            <div class="ai-header">
              <span class="ai-icon">🤖</span>
              <h3>AI Recommendation</h3>
            </div>
            <div class="loading-content">
              <div class="loading-spinner-small"></div>
              <p>Generating personalized recommendations...</p>
            </div>
          </div>
          
          <!-- No Recommendation Available -->
          <div v-else class="ai-recommendation" :class="resultClass">
            <div class="ai-header">
              <span class="ai-icon">📊</span>
              <h3>Performance Summary</h3>
            </div>
            <div class="ai-content">
              <p class="ai-description">Keep practicing to improve your performance!</p>
            </div>
          </div>
        </div>
        
        <div class="result-footer">
          <button class="btn-dashboard" @click="goToDashboard">
            <span class="btn-icon">📊</span>
            See My Overall Performance
          </button>
          <button class="btn-home" @click="goHome">
            <span class="btn-icon">🏠</span>
            Back to Home
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import EduskillHeader from '@/components/Header/EduskillHeader.vue';
import api from '@/services/api';
import gamificationService from '@/services/gamificationService';

export default {
  name: 'ExamResult',
  components: {
    EduskillHeader
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const score = ref(0);
    const total = ref(0);
    const percentage = ref(0);
    const correctCount = ref(0);
    const unansweredCount = ref(0);
    const aiRecommendation = ref(null);
    const attemptId = ref(null);
    const examId = ref(null);
    const loadingAI = ref(false);
    
    const wrongCount = computed(() => {
      return total.value - correctCount.value - unansweredCount.value;
    });
    
    const resultClass = computed(() => {
      if (percentage.value >= 80) return 'excellent';
      if (percentage.value >= 60) return 'good';
      if (percentage.value >= 40) return 'average';
      return 'needs-improvement';
    });
    
    const resultIcon = computed(() => {
      if (percentage.value >= 80) return '🏆';
      if (percentage.value >= 60) return '🎉';
      if (percentage.value >= 40) return '👍';
      return '💪';
    });
    
    const performanceMessage = computed(() => {
      if (percentage.value >= 90) return 'Outstanding! You have mastered this subject!';
      if (percentage.value >= 80) return 'Excellent work! Keep up the great performance!';
      if (percentage.value >= 60) return 'Good job! You are on the right track!';
      if (percentage.value >= 40) return 'Not bad! Keep practicing to improve further.';
      return 'Keep practicing! You can do better with more preparation.';
    });
    
    // Simple fallback recommendation when API is not available
    const generateSimpleFallback = (scorePercent) => {
      if (scorePercent < 40) {
        return {
          overall_assessment: `Your score of ${scorePercent}% indicates that you need to focus on understanding the fundamental concepts. Don't worry - with consistent practice, you can improve!`,
          strengths: [],
          areas_for_improvement: ['Review basic concepts', 'Practice more questions', 'Focus on understanding fundamentals'],
          recommendations: ['Start with easy questions', 'Review your notes daily', 'Join study groups'],
          encouragement: 'Every expert was once a beginner. Keep practicing!',
          next_exam_difficulty: 'easy'
        };
      } else if (scorePercent >= 40 && scorePercent <= 70) {
        return {
          overall_assessment: `Your score of ${scorePercent}% shows decent understanding. Keep working on your weak areas!`,
          strengths: ['Good progress on some topics'],
          areas_for_improvement: ['Focus on weak areas', 'Practice more exercises'],
          recommendations: ['Review incorrect answers', 'Practice similar questions', 'Create summary notes'],
          encouragement: "You're on the right track! Keep it up!",
          next_exam_difficulty: 'medium'
        };
      } else if (scorePercent > 70 && scorePercent <= 90) {
        return {
          overall_assessment: `Great job! Your score of ${scorePercent}% shows strong understanding!`,
          strengths: ['Strong conceptual understanding', 'Good problem-solving skills'],
          areas_for_improvement: ['Challenge yourself with harder questions'],
          recommendations: ['Explore advanced topics', 'Help peers who are struggling'],
          encouragement: "Excellent work! You're almost at mastery level!",
          next_exam_difficulty: 'hard'
        };
      } else {
        return {
          overall_assessment: `Outstanding! Your score of ${scorePercent}% shows mastery!`,
          strengths: ['Excellent understanding of all topics'],
          areas_for_improvement: ['Maintain your performance'],
          recommendations: ['Consider mentoring other students', 'Explore advanced applications'],
          encouragement: "You're a star! Keep up the amazing work!",
          next_exam_difficulty: 'hard'
        };
      }
    };
    
    // Fetch AI recommendation from backend API
    const fetchAIRecommendation = async (studentId, examIdValue) => {
      try {
        loadingAI.value = true;
        const response = await api.get(`/api/ai/exam-recommendation/${studentId}/${examIdValue}`);
        
        if (response && response.recommendation) {
          aiRecommendation.value = response.recommendation;
        } else if (response.fallback_recommendation) {
          aiRecommendation.value = response.fallback_recommendation;
        } else {
          // Use simple fallback
          aiRecommendation.value = generateSimpleFallback(percentage.value);
        }
      } catch (error) {
        console.error('Failed to fetch AI recommendation:', error);
        // Use simple fallback
        aiRecommendation.value = generateSimpleFallback(percentage.value);
      } finally {
        loadingAI.value = false;
      }
    };
    
    const goToDashboard = () => {
      router.push('/student/performance-analytics');
    };
    
    const goHome = () => {
      router.push('/student_dashboard');
    };
    
    onMounted(async () => {
      // Get data from route query params
      score.value = parseInt(route.query.score) || 0;
      total.value = parseInt(route.query.total) || 0;
      percentage.value = parseFloat(route.query.percentage) || 0;
      correctCount.value = parseInt(route.query.correct_count) || score.value;
      unansweredCount.value = parseInt(route.query.unanswered_count) || 0;
      attemptId.value = route.query.attemptId || null;
      
      // Get exam_id from attempt_id if available
      examId.value = route.query.examId || null;
      
      // If correct_count not provided, calculate from score
      if (!route.query.correct_count) {
        correctCount.value = score.value;
      }
      
      // Award XP for exam submission and result
      try {
        const studentId = localStorage.getItem('student_id') || localStorage.getItem('user_id');
        if (studentId && examId.value) {
          // Award XP for exam submission
          await gamificationService.awardExamSubmissionXP(examId.value);
          console.log('XP awarded for exam submission');
          
          // Award XP based on exam result
          await gamificationService.awardExamResultXP(examId.value, percentage.value);
          console.log('XP awarded for exam result:', percentage.value, '%');
        }
      } catch (xpError) {
        console.error('Failed to award XP:', xpError);
      }
      
      // Check if AI recommendation was passed from backend
      const backendAiRec = route.query.ai_recommendation;
      
      if (backendAiRec) {
        try {
          // Parse the AI recommendation from backend
          const parsedRec = JSON.parse(decodeURIComponent(backendAiRec));
          aiRecommendation.value = parsedRec;
        } catch (e) {
          console.error('Failed to parse AI recommendation:', e);
          // Try to fetch from API as fallback
          const studentId = localStorage.getItem('student_id') || localStorage.getItem('user_id');
          if (studentId && examId.value) {
            await fetchAIRecommendation(studentId, examId.value);
          } else {
            // Use simple fallback
            aiRecommendation.value = generateSimpleFallback(percentage.value);
          }
        }
      } else {
        // No AI recommendation from backend - try to fetch from API
        const studentId = localStorage.getItem('student_id') || localStorage.getItem('user_id');
        if (studentId && examId.value) {
          await fetchAIRecommendation(studentId, examId.value);
        } else {
          // Use simple fallback
          aiRecommendation.value = generateSimpleFallback(percentage.value);
        }
      }
    });
    
    return {
      score,
      total,
      percentage,
      correctCount,
      wrongCount,
      unansweredCount,
      aiRecommendation,
      loadingAI,
      resultClass,
      resultIcon,
      performanceMessage,
      goToDashboard,
      goHome
    };
  }
};
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.result-container {
  max-width: 600px;
  margin: 0 auto;
  padding-top: 2rem;
}

.result-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.result-header {
  padding: 2rem;
  text-align: center;
  color: white;
}

.result-header.excellent {
  background: linear-gradient(135deg, #10b981, #059669);
}

.result-header.good {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.result-header.average {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.result-header.needs-improvement {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.result-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.result-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.result-body {
  padding: 2rem;
}

.score-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 8px solid;
}

.score-circle.excellent {
  border-color: #10b981;
  background: #ecfdf5;
}

.score-circle.good {
  border-color: #3b82f6;
  background: #eff6ff;
}

.score-circle.average {
  border-color: #f59e0b;
  background: #fffbeb;
}

.score-circle.needs-improvement {
  border-color: #ef4444;
  background: #fef2f2;
}

.score-percentage {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
}

.score-details {
  text-align: left;
}

.score-details h2 {
  font-size: 1.25rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.score-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.score-label {
  color: #64748b;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  border-radius: 12px;
  background: #f8fafc;
}

.stat-item.correct {
  background: #ecfdf5;
}

.stat-item.wrong {
  background: #fef2f2;
}

.stat-item.unanswered {
  background: #f8fafc;
}

.stat-icon {
  display: block;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.85rem;
  color: #64748b;
}

.performance-message {
  text-align: center;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
}

.performance-message.excellent {
  background: #ecfdf5;
  color: #059669;
}

.performance-message.good {
  background: #eff6ff;
  color: #2563eb;
}

.performance-message.average {
  background: #fffbeb;
  color: #d97706;
}

.performance-message.needs-improvement {
  background: #fef2f2;
  color: #dc2626;
}

/* AI Recommendation */
.ai-recommendation {
  margin-top: 1.5rem;
  padding: 1.5rem;
  border-radius: 12px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
}

.ai-recommendation.excellent {
  background: #ecfdf5;
  border-color: #10b981;
}

.ai-recommendation.good {
  background: #eff6ff;
  border-color: #3b82f6;
}

.ai-recommendation.average {
  background: #fffbeb;
  border-color: #f59e0b;
}

.ai-recommendation.needs-improvement {
  background: #fef2f2;
  border-color: #ef4444;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.ai-icon {
  font-size: 1.5rem;
}

.ai-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.ai-content {
  color: #475569;
}

.ai-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.ai-description {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.weak-sections, .study-tips {
  margin-top: 1rem;
}

.weak-sections h4, .study-tips h4 {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.weak-sections ul, .study-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.weak-sections li, .study-tips li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.weak-sections li::before {
  content: "🎯";
  position: absolute;
  left: 0;
}

.study-tips li::before {
  content: "📚";
  position: absolute;
  left: 0;
}

.result-footer {
  padding: 2rem;
  border-top: 2px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-dashboard {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: white;
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

.btn-dashboard:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
}

.btn-home {
  width: 100%;
  padding: 1rem;
  background: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-home:hover {
  background: #e2e8f0;
  color: #475569;
}

.btn-icon {
  font-size: 1.2rem;
}

@media (max-width: 600px) {
  .result-page {
    padding: 1rem;
  }
  
  .score-display {
    flex-direction: column;
    text-align: center;
  }
  
  .score-details {
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
