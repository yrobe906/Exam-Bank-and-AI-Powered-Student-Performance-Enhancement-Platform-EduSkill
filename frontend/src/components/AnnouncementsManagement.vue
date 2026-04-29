<template>
  <div class="announcements-container">
    <div class="header">
      <h2>Announcements Management</h2>
      <button @click="showCreateForm = !showCreateForm" class="create-btn">
        {{ showCreateForm ? 'Cancel' : 'Create Announcement' }}
      </button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="showCreateForm" class="form-container">
      <form @submit.prevent="submitAnnouncement" class="announcement-form">
        <h3>{{ editingAnnouncement ? 'Edit Announcement' : 'Create New Announcement' }}</h3>

        <div class="form-group">
          <label for="title">Title</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            placeholder="Enter announcement title"
          >
        </div>

        <div class="form-group">
          <label for="message">Message</label>
          <textarea
            id="message"
            v-model="form.message"
            required
            placeholder="Enter announcement message"
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="file">Attach PDF File (Optional)</label>
          <input
            id="file"
            type="file"
            accept=".pdf"
            @change="handleFileChange"
            ref="fileInput"
          >
          <small class="file-help">Only PDF files are allowed. Max file size: 10MB</small>
          <div v-if="selectedFile" class="file-info">
            <span>Selected: {{ selectedFile.name }}</span>
            <button type="button" @click="clearFile" class="clear-file-btn">×</button>
          </div>
        </div>

        <div class="form-group">
          <label for="category">Category</label>
          <select id="category" v-model="form.category" required>
            <option value="academic">Academic</option>
            <option value="achievement">Achievement</option>
          </select>
        </div>

        <div class="form-group">
          <label>Target Audience</label>
          <div class="target-options">
            <label class="target-card">
              <input type="radio" value="student" v-model="form.target_role">
              <span class="card-content">
                <i class="fas fa-user-graduate"></i>
                <strong>Students</strong>
                <small>Send to students only</small>
              </span>
            </label>
            <label class="target-card">
              <input type="radio" value="teacher" v-model="form.target_role">
              <span class="card-content">
                <i class="fas fa-chalkboard-teacher"></i>
                <strong>Teachers</strong>
                <small>Send to teachers only</small>
              </span>
            </label>
            <label class="target-card">
              <input type="radio" value="both" v-model="form.target_role">
              <span class="card-content">
                <i class="fas fa-users"></i>
                <strong>Both</strong>
                <small>Send to everyone</small>
              </span>
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-btn">
            {{ editingAnnouncement ? 'Update' : 'Create' }} Announcement
          </button>
          <button type="button" @click="resetForm" class="cancel-btn">Cancel</button>
        </div>
      </form>
    </div>

    <!-- Announcements List -->
    <div class="announcements-list">
      <h3>Sent Announcements</h3>
      <div v-if="announcements.length === 0" class="no-announcements">
        No announcements created yet.
      </div>
      <div v-else class="announcement-item" v-for="announcement in announcements" :key="announcement.id">
        <div class="announcement-header">
          <h4>{{ announcement.title }}</h4>
          <div class="actions">
            <button @click="editAnnouncement(announcement)" class="edit-btn">
              <i class="fas fa-edit"></i>
            </button>
            <button @click="deleteAnnouncement(announcement.id)" class="delete-btn">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
        <p class="message">{{ announcement.message }}</p>
        <div class="meta">
          <span class="category">{{ announcement.category }}</span>
          <span class="target">Target: {{ announcement.target_role }}</span>
          <span class="date">{{ formatDate(announcement.created_at) }}</span>
          <span class="status" :class="{ active: announcement.is_active }">
            {{ announcement.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AnnouncementsManagement',
  data() {
    return {
      showCreateForm: false,
      editingAnnouncement: null,
      announcements: [],
      selectedFile: null,
      form: {
        title: '',
        message: '',
        category: 'academic',
        target_role: 'student'
      }
    }
  },
  mounted() {
    this.fetchAnnouncements()
  },
  methods: {
    getAuthHeaders() {
      const token = sessionStorage.getItem('admin_token') || localStorage.getItem('admin_token')
      return token ? { 'Authorization': `Bearer ${token}` } : {}
    },

    async fetchAnnouncements() {
      try {
        const response = await axios.get('/api/announcements/', {
          headers: this.getAuthHeaders()
        })
        this.announcements = response.data
      } catch (error) {
        console.error('Error fetching announcements:', error)
        alert('Failed to load announcements')
      }
    },

    async submitAnnouncement() {
      try {
        const formData = new FormData()
        formData.append('title', this.form.title)
        formData.append('message', this.form.message)
        formData.append('category', this.form.category)
        formData.append('target_role', this.form.target_role)

        if (this.selectedFile) {
          formData.append('file', this.selectedFile)
        }

        let response
        if (this.editingAnnouncement) {
          response = await axios.put(`/api/announcements/${this.editingAnnouncement.id}`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              ...this.getAuthHeaders()
            }
          })
        } else {
          response = await axios.post('/api/announcements/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              ...this.getAuthHeaders()
            }
          })
        }
        this.resetForm()
        this.fetchAnnouncements()
        alert('Announcement saved successfully!')
      } catch (error) {
        console.error('Error saving announcement:', error)
        alert('Failed to save announcement')
      }
    },

    editAnnouncement(announcement) {
      this.editingAnnouncement = announcement
      this.form = {
        title: announcement.title,
        message: announcement.message,
        category: announcement.category,
        target_role: announcement.target_role
      }
      this.showCreateForm = true
    },

    async deleteAnnouncement(id) {
      if (!confirm('Are you sure you want to delete this announcement?')) return

      try {
        await axios.delete(`/api/announcements/${id}`, {
          headers: this.getAuthHeaders()
        })
        this.fetchAnnouncements()
        alert('Announcement deleted successfully!')
      } catch (error) {
        console.error('Error deleting announcement:', error)
        alert('Failed to delete announcement')
      }
    },

    resetForm() {
      this.form = {
        title: '',
        message: '',
        category: 'academic',
        target_role: 'student'
      }
      this.editingAnnouncement = null
      this.showCreateForm = false
      this.clearFile()
    },

    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    },

    handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        // Validate file type
        if (file.type !== 'application/pdf') {
          alert('Only PDF files are allowed')
          this.clearFile()
          return
        }
        // Validate file size (10MB max)
        if (file.size > 10 * 1024 * 1024) {
          alert('File size must be less than 10MB')
          this.clearFile()
          return
        }
        this.selectedFile = file
      }
    },

    clearFile() {
      this.selectedFile = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    }
  }
}
</script>

<style scoped>
.announcements-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.create-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.form-container {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group input[type="file"] {
  padding: 4px;
}

.file-help {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 0.9em;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 5px;
  padding: 5px 10px;
  background: #e9ecef;
  border-radius: 4px;
}

.clear-file-btn {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.target-options {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.target-card {
  flex: 1;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
}

.target-card:hover {
  border-color: #007bff;
}

.target-card input[type="radio"] {
  display: none;
}

.target-card input[type="radio"]:checked + .card-content {
  background: #007bff;
  color: white;
}

.card-content {
  display: block;
  text-align: center;
  padding: 10px;
  border-radius: 6px;
}

.card-content i {
  font-size: 24px;
  margin-bottom: 8px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.submit-btn,
.cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn {
  background: #28a745;
  color: white;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.announcements-list h3 {
  margin-bottom: 15px;
}

.announcement-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background: white;
}

.announcement-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.announcement-header h4 {
  margin: 0;
  flex-grow: 1;
}

.actions {
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 3px;
}

.edit-btn {
  color: #007bff;
}

.delete-btn {
  color: #dc3545;
}

.message {
  margin: 10px 0;
  line-height: 1.5;
}

.meta {
  display: flex;
  gap: 15px;
  font-size: 0.9em;
  color: #666;
}

.category {
  background: #e9ecef;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: capitalize;
}

.target {
  text-transform: capitalize;
}

.status {
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: bold;
}

.status.active {
  background: #d4edda;
  color: #155724;
}

.no-announcements {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 40px;
}
</style>