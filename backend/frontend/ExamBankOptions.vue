<template>
  <div class="exam-bank-options">
    <EduskillHeader>
      <p>Exam Bank Options</p>
    </EduskillHeader>
    <div class="options-content">
      <h2>Exam Bank Options</h2>
      <p>Options for exam bank will be displayed here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'ExamBankOptions',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.exam-bank-options {
  padding: 20px;
}

.options-content {
  max-width: 800px;
  margin: 0 auto;
}
</style>