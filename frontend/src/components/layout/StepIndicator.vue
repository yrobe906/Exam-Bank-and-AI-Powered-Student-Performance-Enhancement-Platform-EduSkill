<template>
  <div class="steps-container">
    <div v-for="(step, index) in steps" :key="index" class="step-wrapper">
      <!-- Step Item - Made clickable -->
      <div class="step-item" :class="getStepClass(index + 1)" @click="$emit('update:currentStep', index + 1)">
        <div class="step-number" :class="getStepNumberClass(index + 1)">
          <span v-if="index + 1 < currentStep" class="check-icon">✓</span>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <div class="step-label-container">
          <span class="step-label" :class="getStepLabelClass(index + 1)">{{ step }}</span>
          <span v-if="index + 1 === currentStep" class="step-status">Current</span>
          <span v-else-if="index + 1 < currentStep" class="step-status completed-status">Completed</span>
        </div>
      </div>
      
      <!-- Connector Line -->
      <div v-if="index < steps.length - 1" class="step-connector">
        <div class="connector-line" :class="{ 'connector-active': index + 1 < currentStep }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  steps: {
    type: Array,
    required: true
  },
  currentStep: {
    type: Number,
    required: true
  }
})

defineEmits(['update:currentStep'])

// Step classes
const getStepClass = (stepNumber) => {
  return {
    'step-active': stepNumber === props.currentStep,
    'step-completed': stepNumber < props.currentStep,
    'step-upcoming': stepNumber > props.currentStep,
    'clickable': true
  }
}

const getStepNumberClass = (stepNumber) => {
  return {
    'number-active': stepNumber === props.currentStep,
    'number-completed': stepNumber < props.currentStep,
    'number-upcoming': stepNumber > props.currentStep
  }
}

const getStepLabelClass = (stepNumber) => {
  return {
    'label-active': stepNumber === props.currentStep,
    'label-completed': stepNumber < props.currentStep,
    'label-upcoming': stepNumber > props.currentStep
  }
}
</script>

<style scoped>

.steps-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 1.5rem 2rem;
  border-radius: 60px;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.step-wrapper {
  display: flex;
  align-items: center;
  flex: 1;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 40px;
  transition: all 0.3s ease;
}

.step-item:hover {
  background: rgba(37, 99, 235, 0.05);
}

.step-item.step-active:hover {
  background: rgba(37, 99, 235, 0.1);
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.number-active {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.3);
}

.number-completed {
  background: #10b981;
  color: white;
}

.number-upcoming {
  background: #f1f5f9;
  color: #64748b;
}

.check-icon {
  font-size: 1.2rem;
  font-weight: bold;
  animation: popIn 0.3s ease;
}

.step-label-container {
  display: flex;
  flex-direction: column;
}

.step-label {
  font-size: 0.95rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.label-active {
  color: #2563eb;
  font-weight: 600;
}

.label-completed {
  color: #10b981;
}

.label-upcoming {
  color: #64748b;
}

.step-status {
  font-size: 0.7rem;
  color: #94a3b8;
  margin-top: 0.1rem;
}

.completed-status {
  color: #10b981;
}

.step-connector {
  flex: 1;
  display: flex;
  align-items: center;
  margin: 0 1rem;
}

.connector-line {
  height: 3px;
  width: 100%;
  background: #e2e8f0;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.connector-active {
  background: linear-gradient(90deg, #2563eb, #7c3aed);
}

/* Animations */
@keyframes popIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Hover effects */
.step-item:hover .step-number {
  transform: scale(1.05);
}

.step-item.step-active:hover .step-number {
  transform: scale(1.15);
}

.step-item:hover .step-label {
  color: #2563eb;
}

/* Responsive */
@media (max-width: 768px) {
  .steps-container {
    padding: 1rem;
    border-radius: 30px;
  }
  
  .step-label-container {
    display: none;
  }
  
  .step-number {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
  
  .step-connector {
    margin: 0 0.5rem;
  }
}

/* Click ripple effect */
.step-item:active {
  transform: scale(0.98);
}

/* Pulse animation for active step */
@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(37, 99, 235, 0);
  }
}

.step-active .step-number {
  animation: pulse 2s infinite;
}
</style>