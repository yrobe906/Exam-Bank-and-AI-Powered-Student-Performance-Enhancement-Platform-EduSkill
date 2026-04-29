<template>
  <div class="admin-add-note">
    <EduskillHeader>
      <p>Admin - Add Note</p>
    </EduskillHeader>
    <div class="content">
      <h2>Add Notes</h2>
      <p>Form to add notes will be here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'AdminAddNote',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.admin-add-note {
  padding: 20px;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}
</style>