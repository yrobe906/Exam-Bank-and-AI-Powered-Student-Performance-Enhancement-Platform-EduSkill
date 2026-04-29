<template>
  <div class="premium-fixed">
    <EduskillHeader>
      <p>Premium Features</p>
    </EduskillHeader>
    <div class="premium-content">
      <h2>Premium Features</h2>
      <p>Premium content will be displayed here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'PremiumFixed',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.premium-fixed {
  padding: 20px;
}

.premium-content {
  max-width: 800px;
  margin: 0 auto;
}
</style>