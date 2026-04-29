<template>
  <div class="mock-test-subject">
    <EduskillHeader>
      <p>Mock Test Subject</p>
    </EduskillHeader>
    <div class="test-content">
      <h2>Mock Test Subject</h2>
      <p>Mock test content will be displayed here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'MockTestSubject',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.mock-test-subject {
  padding: 20px;
}

.test-content {
  max-width: 800px;
  margin: 0 auto;
}
</style>