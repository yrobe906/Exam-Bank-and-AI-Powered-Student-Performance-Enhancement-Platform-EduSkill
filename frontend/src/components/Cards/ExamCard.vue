<template>
  <div @click="$emit('select', exam)"
       class="exam-card group"
       :class="{ 'exam-card-selected': selected }">
    
    <!-- Animated background gradient for selected state -->
    <div class="card-bg" :class="{ 'card-bg-selected': selected }"></div>
    
    <!-- Hover overlay effect -->
    <div class="hover-overlay"></div>
    
    <div class="card-content">
      <div class="card-main">
        <div class="exam-icon" :class="{ 'icon-selected': selected }">
          {{ exam.icon || '📝' }}
        </div>
        
        <div class="exam-details">
          <h4 class="exam-title" :class="{ 'title-selected': selected }">
            {{ exam.name }}
          </h4>
          
          <div class="exam-meta">
            <div class="meta-item" :class="{ 'meta-selected': selected }">
              <span class="meta-dot">●</span>
              <span class="meta-text">{{ exam.questions }} Questions</span>
            </div>
            <div class="meta-item" :class="{ 'meta-selected': selected }">
              <span class="meta-dot">●</span>
              <span class="meta-text">{{ exam.duration }} minutes</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Selected checkmark with animation -->
      <transition name="scale-pop">
        <div v-if="selected" class="checkmark-container">
          <div class="checkmark-circle">
            <svg class="checkmark-icon" viewBox="0 0 24 24" fill="none">
              <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </transition>
    </div>

    <!-- Shine effect on hover -->
    <div class="shine-effect"></div>
  </div>
</template>

<script setup>
defineProps({
  exam: {
    type: Object,
    required: true
  },
  selected: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
@reference "tailwindcss";

.exam-card {
  position: relative;
  padding: 1.25rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid #e2e8f0;
  background: white;
  overflow: hidden;
  transform: translateY(0);
}

.exam-card:hover {
  transform: translateY(-4px);
  border-color: #2563eb;
  box-shadow: 0 20px 30px -10px rgba(37, 99, 235, 0.2);
}

.exam-card-selected {
  border-color: transparent;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 20px 30px -10px rgba(37, 99, 235, 0.3);
}

/* Card background with gradient animation */
.card-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  opacity: 0;
  transition: opacity 0.4s ease;
  border-radius: 18px;
}

.card-bg-selected {
  opacity: 1;
}

/* Hover overlay */
.hover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.05), rgba(124, 58, 237, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 18px;
}

.exam-card:hover .hover-overlay {
  opacity: 1;
}

/* Card content */
.card-content {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-main {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

/* Exam icon */
.exam-icon {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  transition: all 0.3s ease;
  transform: rotate(0deg);
}

.exam-card:hover .exam-icon {
  transform: rotate(5deg) scale(1.1);
  background: #e2e8f0;
}

.icon-selected {
  background: rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(4px);
  color: white;
  transform: rotate(0deg) !important;
}

/* Exam details */
.exam-details {
  flex: 1;
}

.exam-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  transition: color 0.3s ease;
}

.exam-card:hover .exam-title {
  color: #2563eb;
}

.title-selected {
  color: white !important;
}

/* Meta information */
.exam-meta {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  transition: all 0.3s ease;
}

.meta-selected {
  color: rgba(255, 255, 255, 0.9) !important;
}

.meta-dot {
  font-size: 0.75rem;
  color: #2563eb;
  transition: color 0.3s ease;
}

.exam-card-selected .meta-dot {
  color: white;
}

.meta-text {
  font-size: 0.9rem;
  font-weight: 500;
}

/* Checkmark animation */
.checkmark-container {
  margin-left: 1rem;
  animation: scaleIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.checkmark-circle {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.2);
}

.checkmark-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  stroke-dasharray: 50;
  stroke-dashoffset: 50;
  animation: drawCheck 0.6s ease forwards 0.2s;
}

/* Shine effect on hover */
.shine-effect {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    135deg,
    transparent 30%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 70%
  );
  transform: rotate(45deg) translateX(-100%);
  transition: transform 0.6s ease;
  pointer-events: none;
  z-index: 20;
}

.exam-card:hover .shine-effect {
  transform: rotate(45deg) translateX(100%);
}

/* Animations */
@keyframes scaleIn {
  0% {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0);
    opacity: 1;
  }
}

@keyframes drawCheck {
  to {
    stroke-dashoffset: 0;
  }
}

.scale-pop-enter-active {
  animation: scaleIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-pop-leave-active {
  animation: scaleIn 0.3s reverse;
}

/* Responsive */
@media (max-width: 640px) {
  .exam-card {
    padding: 1rem;
  }
  
  .exam-icon {
    width: 40px;
    height: 40px;
    font-size: 1.25rem;
  }
  
  .exam-title {
    font-size: 1rem;
  }
  
  .exam-meta {
    gap: 1rem;
  }
  
  .meta-text {
    font-size: 0.8rem;
  }
}

/* Pulse animation for selected state */
@keyframes softPulse {
  0%, 100% {
    box-shadow: 0 20px 30px -10px rgba(37, 99, 235, 0.3);
  }
  50% {
    box-shadow: 0 25px 35px -8px rgba(37, 99, 235, 0.5);
  }
}

.exam-card-selected {
  animation: softPulse 2s infinite;
}

/* Ripple effect on click */
.exam-card:active {
  transform: scale(0.98);
}

.exam-card:active::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 18px;
  animation: ripple 0.3s ease-out;
}

@keyframes ripple {
  0% {
    opacity: 0.5;
    transform: scale(0);
  }
  100% {
    opacity: 0;
    transform: scale(1);
  }
}
</style>