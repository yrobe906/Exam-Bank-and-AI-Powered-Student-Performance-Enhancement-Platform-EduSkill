<template>
  <div class="admin-add-practice-mock">
    <EduskillHeader>
      <p>Admin - Add Practice Mock</p>
    </EduskillHeader>
    <div class="content">
      <h2>Add Practice Mock Test</h2>
      <p>Form to add practice mock tests will be here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'AdminAddPracticeMock',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.admin-add-practice-mock {
  padding: 20px;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}
</style>