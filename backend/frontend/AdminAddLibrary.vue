<template>
  <div class="admin-add-library">
    <EduskillHeader>
      <p>Admin - Add Library</p>
    </EduskillHeader>
    <div class="content">
      <h2>Add Library Resources</h2>
      <p>Form to add library resources will be here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'AdminAddLibrary',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.admin-add-library {
  padding: 20px;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}
</style>