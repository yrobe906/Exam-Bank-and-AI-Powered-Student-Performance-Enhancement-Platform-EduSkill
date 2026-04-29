<template>
  <div class="eduoffice-announcements">
    <EduskillHeader>
      <p>EduOffice Announcements</p>
    </EduskillHeader>
    <div class="content">
      <h2>EduOffice Announcements</h2>
      <p>EduOffice announcements will be displayed here.</p>
    </div>
  </div>
</template>

<script>
import EduskillHeader from './EduskillHeader.vue'

export default {
  name: 'EduofficeAnnouncements',
  components: {
    EduskillHeader
  }
}
</script>

<style scoped>
.eduoffice-announcements {
  padding: 20px;
}

.content {
  max-width: 800px;
  margin: 0 auto;
}
</style>