<template>
  <div class="time-warning">
    ⚠️ Less than 1 minute remaining! Your test will auto-submit.
  </div>
</template>

<script>
export default {
  name: 'TimeWarning'
}
</script>

<style scoped>
@reference "tailwindcss";

.time-warning {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: #ef4444;
  color: white;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  box-shadow: 0 10px 20px -5px rgba(239, 68, 68, 0.4);
  animation: slideUp 0.3s ease;
  z-index: 100;
}

@keyframes slideUp {
  from { transform: translate(-50%, 20px); opacity: 0; }
  to { transform: translate(-50%, 0); opacity: 1; }
}
</style>