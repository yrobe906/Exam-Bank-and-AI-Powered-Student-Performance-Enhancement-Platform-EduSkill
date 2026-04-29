<template>
  <div class="exam-result">
    <EduskillHeader>
      <p>Exam Results</p>
    </EduskillHeader>
    <div class="result-content">
      <h2>Your Exam Results</h2>
      <p>Results will be displayed here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'ExamResult',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.exam-result {
  padding: 20px;
}

.result-content {
  max-width: 800px;
  margin: 0 auto;
}
</style>