<template>
  <div class="teacher-room">
    <EduskillHeader>
      <p>Teacher Room</p>
    </EduskillHeader>
    <div class="content">
      <h2>Teacher Dashboard</h2>
      <p>Teacher room content will be here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'TeacherRoom',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.teacher-room {
  padding: 20px;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}
</style>