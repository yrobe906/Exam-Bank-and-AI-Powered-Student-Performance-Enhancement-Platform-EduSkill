<template>
  <div class="practice-8">
    <EduskillHeader>
      <p>Flashcards Practice - Set 8</p>
    </EduskillHeader>
    <div class="practice-content">
      <h2>Flashcards Practice Set 8</h2>
      <p>Practice flashcards will be displayed here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from '../EduskillHeader.vue'

export default {
  name: 'Practice8',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.practice-8 {
  padding: 20px;
}

.practice-content {
  max-width: 800px;
  margin: 0 auto;
}
</style>