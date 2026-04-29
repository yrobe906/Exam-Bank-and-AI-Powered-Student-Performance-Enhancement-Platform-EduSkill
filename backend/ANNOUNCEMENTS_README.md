# Announcement & Notification System

This document describes the newly implemented role-based Announcement & Notification System for the EduSkill Hub project.

## Overview

The system allows educational officers to create announcements targeted at specific audiences (students, teachers, or both) with different categories (academic, achievement).

## Backend Implementation

### Database Model
- **Table**: `announcements`
- **Fields**:
  - `id`: Primary key
  - `title`: Announcement title
  - `message`: Announcement content
  - `category`: "academic" or "achievement"
  - `target_role`: "student", "teacher", or "both"
  - `created_at`: Timestamp
  - `is_active`: Boolean flag

### API Endpoints

All endpoints are prefixed with `/api/announcements/`

#### Public Endpoints (require authentication)
- `GET /` - Get announcements filtered by user role
  - Query params: `role` (student/teacher), `skip`, `limit`
  - Returns announcements where `target_role` matches the user's role or "both"

#### EduOffice/Admin Only Endpoints
- `POST /` - Create new announcement
- `PUT /{announcement_id}` - Update announcement
- `DELETE /{announcement_id}` - Delete announcement

### Authentication
- Reading announcements requires user authentication
- Creating/updating/deleting requires eduoffice or admin role

## Frontend Implementation

### Components Created

1. **AnnouncementsManagement.vue** - For EduOffice dashboard
   - Form to create/edit announcements
   - List of sent announcements with edit/delete buttons
   - Category and target audience selection

2. **StudentAnnouncements.vue** - For Student dashboard
   - Displays announcements targeted at students
   - Shows relative timestamps ("2 hours ago")
   - Highlights achievement announcements

3. **TeacherAnnouncements.vue** - For Teacher dashboard
   - Similar to student component but for teachers

### Integration Steps

#### 1. EduOffice Sidebar
Add to the EduOffice sidebar navigation:
```vue
<!-- In EduOffice sidebar component -->
<router-link to="/eduoffice/announcements">
  <i class="fas fa-bullhorn"></i> Announcements
</router-link>
```

#### 2. Student Dashboard
Add the StudentAnnouncements component:
```vue
<!-- In StudentDashboard.vue -->
<template>
  <!-- ... existing content ... -->
  <StudentAnnouncements />
  <!-- ... rest of content ... -->
</template>

<script>
import StudentAnnouncements from '@/components/StudentAnnouncements.vue'

export default {
  components: {
    StudentAnnouncements,
    // ... other components
  }
}
</script>
```

#### 3. Teacher Dashboard
Add the TeacherAnnouncements component and update navigation:
```vue
<!-- In TeacherSidebar.vue -->
<!-- Add below Feedback & Actions -->
<li>
  <router-link to="/teacher/announcements">
    <i class="fas fa-bell"></i> Notifications
  </router-link>
</li>

<!-- In TeacherDashboard.vue or relevant component -->
<template>
  <!-- ... existing content ... -->
  <TeacherAnnouncements />
  <!-- ... rest of content ... -->
</template>

<script>
import TeacherAnnouncements from '@/components/TeacherAnnouncements.vue'

export default {
  components: {
    TeacherAnnouncements,
    // ... other components
  }
}
</script>
```

## Usage Examples

### Creating an Announcement
```javascript
const announcement = {
  title: "New Exam Schedule",
  message: "The final exam schedule has been updated. Please check your dashboard.",
  category: "academic",
  target_role: "student"
}

axios.post('/api/announcements/', announcement)
```

### Fetching Announcements for Students
```javascript
axios.get('/api/announcements/?role=student')
  .then(response => {
    // Display announcements
  })
```

## Features

- ✅ Role-based filtering
- ✅ Category-based styling
- ✅ Real-time timestamps
- ✅ Edit/Delete functionality for EduOffice
- ✅ Responsive design
- ✅ Highlight important announcements
- ✅ Active/Inactive status management

## Testing

Run the test script to verify API functionality:
```bash
python test_announcements_api.py
```

Make sure to:
1. Start the FastAPI server
2. Update the test script with a valid JWT token from an eduoffice/admin user
3. Run the test

## Database Migration

The announcements table has been created automatically. If you need to recreate it:
```bash
python create_announcements_table.py
```

## Security Notes

- Only eduoffice and admin users can create/manage announcements
- All endpoints require authentication
- Announcements are filtered based on user roles
- Input validation is handled by Pydantic schemas