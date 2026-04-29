<template>
  <div class="teacher-announcements-page">
    <EduskillHeader>
      <p>Teacher Announcements</p>
    </EduskillHeader>
    <!-- Teacher Announcements Component -->
    <div class="announcements-container">
      <TeacherAnnouncements />
    </div>
  </div>
</template>

<script>
import EduskillHeader from '@/components/Header/EduskillHeader.vue'
import TeacherAnnouncements from '@/components/TeacherAnnouncements.vue'

export default {
  name: 'TeacherAnnouncementsPage',
  components: {
    EduskillHeader,
    TeacherAnnouncements
  },
  mounted() {
    // Set page title
    document.title = 'Announcements - EduSkill Hub'
  }
}
</script>

<style scoped>
.teacher-announcements-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.announcements-container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}
</style>