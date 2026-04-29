<template>
  <div class="student-announcements-page">
    <!-- EduSkill Header -->
    <EduskillHeader />

    <div class="page-header">
      <h1 class="text-2xl font-bold text-gray-800 mb-2">Announcements & Notifications</h1>
      <p class="text-gray-600">Stay updated with the latest announcements and notifications</p>
    </div>

    <!-- Student Announcements Component -->
    <div class="announcements-container">
      <StudentAnnouncements />
    </div>
  </div>
</template>

<script>
import EduskillHeader from '@/components/Header/EduskillHeader.vue'
import StudentAnnouncements from '@/components/StudentAnnouncements.vue'

export default {
  name: 'StudentAnnouncementsPage',
  components: {
    EduskillHeader,
    StudentAnnouncements
  },
  mounted() {
    // Set page title
    document.title = 'Announcements - EduSkill Hub'
  }
}
</script>

<style scoped>
.student-announcements-page {
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