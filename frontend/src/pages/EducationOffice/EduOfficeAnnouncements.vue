<template>
  <div class="eduoffice-announcements-page">
    <EduskillHeader>
      <p>Managers' Announcements</p>
    </EduskillHeader>
    <!-- Announcements Management Component -->
    <div class="announcements-container">
      <AnnouncementsManagement />
    </div>
  </div>
</template>

<script>
import EduskillHeader from '@/components/Header/EduskillHeader.vue'
import AnnouncementsManagement from '@/components/AnnouncementsManagement.vue'

export default {
  name: 'EduOfficeAnnouncements',
  components: {
    EduskillHeader,
    AnnouncementsManagement
  },
  mounted() {
    // Set page title
    document.title = 'Announcements Management - EduSkill Hub'
  }
}
</script>

<style scoped>
.eduoffice-announcements-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #dcdde1 0%, #f0eff1 50%, #515052 100%);
  padding: 1rem 2rem 3rem 2rem;
  position: relative;
}

/* Animated background effect */
.eduoffice-announcements-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgdmlld0JveD0iMCAwIDYwIDYwIj48cGF0aCBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMDUiIGQ9Ik0zMCAzMGwxMC0xMCAxMCAxMC0xMCAxMHpNMzAgMzBsLTEwLTEwLTEwIDEwIDEwIDEweiIvPjwvc3ZnPg==') repeat;
  opacity: 0.4;
  pointer-events: none;
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
  max-width: 1200px;
  margin: 2.5rem auto 0 auto;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1);
  overflow: hidden;
  backdrop-filter: blur(2px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.announcements-container:hover {
  transform: translateY(-4px);
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .eduoffice-announcements-page {
    padding: 0.5rem 1rem 2rem 1rem;
  }
  
  .announcements-container {
    margin-top: 1.5rem;
    border-radius: 20px;
  }
}

/* Custom scrollbar for the container */
.announcements-container::-webkit-scrollbar {
  width: 8px;
}

.announcements-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.announcements-container::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
}

.announcements-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b46a0 100%);
}
</style>