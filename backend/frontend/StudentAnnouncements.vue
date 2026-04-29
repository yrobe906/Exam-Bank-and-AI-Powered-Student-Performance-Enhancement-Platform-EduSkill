<template>
  <div class="announcements-section">
    <h3>📢 Announcements</h3>
    <div v-if="loading" class="loading">Loading announcements...</div>
    <div v-else-if="announcements.length === 0" class="no-announcements">
      No announcements at this time.
    </div>
    <div v-else class="announcements-list">
      <div
        v-for="announcement in announcements"
        :key="announcement.id"
        class="announcement-card"
        :class="{ 'highlight': announcement.category === 'achievement' }"
      >
        <div class="announcement-header">
          <h4>{{ announcement.title }}</h4>
          <span class="category" :class="announcement.category">
            {{ announcement.category }}
          </span>
        </div>
        <p class="message">{{ announcement.message }}</p>
        <div class="announcement-footer">
          <span class="timestamp">{{ timeAgo(announcement.created_at) }}</span>
          <span class="target-info">For: {{ announcement.target_role }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentAnnouncements',
  data() {
    return {
      announcements: [],
      loading: true
    }
  },
  mounted() {
    this.fetchAnnouncements()
  },
  methods: {
    async fetchAnnouncements() {
      try {
        const response = await axios.get('/api/announcements?role=student')
        this.announcements = response.data
      } catch (error) {
        console.error('Error fetching announcements:', error)
      } finally {
        this.loading = false
      }
    },

    timeAgo(dateString) {
      const now = new Date()
      const date = new Date(dateString)
      const diffInSeconds = Math.floor((now - date) / 1000)

      if (diffInSeconds < 60) return 'Just now'
      if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`
      if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`
      if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`

      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.announcements-section {
  margin-bottom: 30px;
}

.announcements-section h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.2em;
}

.loading {
  text-align: center;
  color: #666;
  padding: 20px;
}

.no-announcements {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.announcement-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
}

.announcement-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.announcement-card.highlight {
  border-left: 4px solid #28a745;
  background: linear-gradient(90deg, #f8fff8 0%, white 10%);
}

.announcement-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.announcement-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.1em;
}

.category {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: bold;
  text-transform: uppercase;
}

.category.academic {
  background: #007bff;
  color: white;
}

.category.achievement {
  background: #28a745;
  color: white;
}

.message {
  color: #555;
  line-height: 1.5;
  margin: 10px 0;
}

.announcement-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9em;
  color: #777;
}

.timestamp {
  font-style: italic;
}

.target-info {
  text-transform: capitalize;
}
</style>