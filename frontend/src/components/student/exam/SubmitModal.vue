<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Submit Test?</h3>
        <button @click="$emit('close')" class="modal-close">✕</button>
      </div>
      
      <div class="modal-body">
        <p>You are about to finish the test. You cannot change answers after this.</p>
        
        <div class="summary-stats">
          <div class="stat">
            <span class="stat-label">Answered</span>
            <span class="stat-value">{{ answeredCount }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Not Answered</span>
            <span class="stat-value">{{ notAnsweredCount }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Marked</span>
            <span class="stat-value">{{ markedCount }}</span>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="$emit('close')" class="btn-cancel">Cancel</button>
        <button @click="$emit('submit')" class="btn-submit-test" :disabled="submitting">
          {{ submitting ? 'Submitting...' : 'Submit' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SubmitModal',
  props: {
    show: Boolean,
    answeredCount: Number,
    notAnsweredCount: Number,
    markedCount: Number,
    submitting: Boolean
  }
}
</script>

<style scoped>
@reference "tailwindcss";

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 24px;
  width: 90%;
  max-width: 400px;
  animation: slideUp 0.3s ease;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.2s ease;
}

.modal-close:hover {
  color: #ef4444;
}

.modal-body {
  padding: 1.5rem;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}

.stat {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2563eb;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 2px solid #e2e8f0;
  display: flex;
  gap: 1rem;
}

.btn-cancel {
  flex: 1;
  padding: 0.75rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-submit-test {
  flex: 1;
  padding: 0.75rem;
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  border-radius: 12px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit-test:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
}

.btn-submit-test:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>