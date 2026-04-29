<template>
  <header class="exam-header">
    <div class="header-left">
      <h1 class="logo">MockSensei</h1>
      <div class="difficulty-badge" :class="examData.difficulty?.toLowerCase()">
        {{ examData.difficulty }} {{ examData.subjects }}
      </div>
    </div>
    
    <div class="header-right">
      <div class="timer" :class="{ 'timer-warning': timeLeft < 300, 'timer-danger': timeLeft < 60 }">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ formatTime(timeLeft) }}</span>
      </div>
      
      <button @click="$emit('submit')" class="btn-submit">Submit</button>
      <button @click="$emit('exit')" class="btn-exit">Exit</button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'ExamHeader',
  props: {
    examData: Object,
    timeLeft: Number
  },
  methods: {
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
  }
}
</script>

<style scoped>

.exam-header {
  background: white;
  border-bottom: 2px solid #e2e8f0;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.difficulty-badge {
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  border-radius: 30px;
  font-size: 0.9rem;
  font-weight: 500;
}

.difficulty-badge.hard {
  background: #fee2e2;
  color: #dc2626;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.timer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  border-radius: 30px;
  font-weight: 600;
  color: #1e293b;
  transition: all 0.3s ease;
}

.timer-warning {
  background: #fef3c7;
  color: #d97706;
  animation: pulse 1s infinite;
}

.timer-danger {
  background: #fee2e2;
  color: #dc2626;
  animation: pulse 0.5s infinite;
}

.btn-submit {
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
}

.btn-exit {
  padding: 0.5rem 1.5rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 30px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-exit:hover {
  border-color: #ef4444;
  color: #ef4444;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
</style>