# Frontend Integration Steps for Announcement System

## Prerequisites
- Vue.js application with Vue Router
- Axios for API calls
- Existing EduOffice, Student, and Teacher dashboards
- Font Awesome icons (for the UI components)

## Step 1: Component Registration

### Global Component Registration (main.js or app.js)
```javascript
// In your main Vue app file
import AnnouncementsManagement from './components/AnnouncementsManagement.vue'
import StudentAnnouncements from './components/StudentAnnouncements.vue'
import TeacherAnnouncements from './components/TeacherAnnouncements.vue'

Vue.component('AnnouncementsManagement', AnnouncementsManagement)
Vue.component('StudentAnnouncements', StudentAnnouncements)
Vue.component('TeacherAnnouncements', TeacherAnnouncements)
```

### Or Per-Component Import
Import components directly in the pages that use them.

## Step 2: EduOffice Integration

### 2.1 Add to EduOffice Sidebar
Locate your EduOffice sidebar component (likely `EduOfficeSidebar.vue` or similar):

```vue
<template>
  <div class="sidebar">
    <!-- ... existing menu items ... -->
    <router-link to="/eduoffice/announcements" class="menu-item">
      <i class="fas fa-bullhorn"></i>
      <span>Announcements</span>
    </router-link>
    <!-- ... rest of sidebar ... -->
  </div>
</template>
```

### 2.2 Create Announcements Page
Create `/eduoffice/announcements` route that renders the management component:

```vue
<!-- EduOfficeAnnouncements.vue -->
<template>
  <div class="eduoffice-announcements-page">
    <AnnouncementsManagement />
  </div>
</template>

<script>
export default {
  name: 'EduOfficeAnnouncements'
}
</script>

<style scoped>
.eduoffice-announcements-page {
  padding: 20px;
}
</style>
```

### 2.3 Add Route to Router
In your `router.js` or `router/index.js`:

```javascript
{
  path: '/eduoffice/announcements',
  name: 'EduOfficeAnnouncements',
  component: () => import('@/views/eduoffice/EduOfficeAnnouncements.vue'),
  meta: { requiresAuth: true, role: 'eduoffice' }
}
```

## Step 3: Student Dashboard Integration

### 3.1 Add to Student Dashboard
Locate your main student dashboard component (`StudentDashboard.vue`):

```vue
<template>
  <div class="student-dashboard">
    <!-- ... existing dashboard content ... -->

    <!-- Add announcements section -->
    <div class="dashboard-section">
      <StudentAnnouncements />
    </div>

    <!-- ... rest of dashboard ... -->
  </div>
</template>

<script>
import StudentAnnouncements from '@/components/StudentAnnouncements.vue'

export default {
  name: 'StudentDashboard',
  components: {
    StudentAnnouncements
    // ... other components
  }
}
</script>
```

### 3.2 Styling Integration
Ensure the announcements fit well with your existing dashboard design. You may need to adjust CSS classes.

## Step 4: Teacher Dashboard Integration

### 4.1 Add to Teacher Sidebar
Locate your teacher sidebar component (`TeacherSidebar.vue`):

```vue
<template>
  <nav class="teacher-sidebar">
    <!-- ... existing menu items ... -->

    <!-- Add below "Feedback & Actions" -->
    <router-link to="/teacher/announcements" class="menu-item">
      <i class="fas fa-bell"></i>
      <span>Notifications</span>
    </router-link>

    <!-- ... rest of sidebar ... -->
  </nav>
</template>
```

### 4.2 Create Teacher Announcements Page
Create `/teacher/announcements` route:

```vue
<!-- TeacherAnnouncementsPage.vue -->
<template>
  <div class="teacher-announcements-page">
    <div class="page-header">
      <h2>Announcements & Notifications</h2>
    </div>
    <TeacherAnnouncements />
  </div>
</template>

<script>
import TeacherAnnouncements from '@/components/TeacherAnnouncements.vue'

export default {
  name: 'TeacherAnnouncementsPage',
  components: {
    TeacherAnnouncements
  }
}
</script>

<style scoped>
.teacher-announcements-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h2 {
  color: #333;
  font-size: 1.5em;
}
</style>
```

### 4.3 Add Route to Router
```javascript
{
  path: '/teacher/announcements',
  name: 'TeacherAnnouncements',
  component: () => import('@/views/teacher/TeacherAnnouncementsPage.vue'),
  meta: { requiresAuth: true, role: 'teacher' }
}
```

## Step 5: Authentication & Authorization

### 5.1 Ensure JWT Token is Available
The components expect the JWT token to be available. Make sure your axios instance includes the authorization header:

```javascript
// In your axios configuration
import axios from 'axios'

const token = localStorage.getItem('token') // or however you store the token
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}
```

### 5.2 Role-Based Access
Ensure your route guards check for proper roles:

```javascript
// In router guards
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiredRole = to.matched.some(record => record.meta.role)

  if (requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }

    // Verify token and role
    // ... your auth logic ...
  }

  next()
})
```

## Step 6: API Base URL Configuration

### 6.1 Update API Calls
The components use relative URLs like `/api/announcements/`. Ensure your axios base URL is configured:

```javascript
// In your axios config
axios.defaults.baseURL = 'http://localhost:8000' // or your API URL
```

## Step 7: Styling & Theming

### 7.1 Font Awesome Icons
Ensure Font Awesome is included in your project:

```html
<!-- In index.html -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

### 7.2 CSS Integration
The components include scoped styles, but you may need to adjust colors and spacing to match your theme. Key classes to customize:

- `.announcements-container` - Main container
- `.announcement-card` - Individual announcement cards
- `.target-card` - Role selection cards
- `.category` - Category badges

## Step 8: Testing Integration

### 8.1 Test EduOffice Features
1. Login as EduOffice user
2. Navigate to Announcements
3. Create a new announcement
4. Edit and delete announcements

### 8.2 Test Student Features
1. Login as Student
2. Check dashboard for announcements
3. Verify filtering works

### 8.3 Test Teacher Features
1. Login as Teacher
2. Navigate to Notifications
3. Check announcements display

## Step 9: Error Handling

### 9.1 Add Global Error Handling
```javascript
// In main.js
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)
```

## Step 10: Production Deployment

### 10.1 Build Components
Ensure the Vue components are included in your build process:

```javascript
// In vue.config.js or similar
module.exports = {
  // ... other config ...
  components: [
    '@/components/AnnouncementsManagement.vue',
    '@/components/StudentAnnouncements.vue',
    '@/components/TeacherAnnouncements.vue'
  ]
}
```

### 10.2 API URL Environment Variables
Use environment variables for API URLs:

```javascript
// .env
VUE_APP_API_URL=http://your-api-domain.com
```

Then update axios config:
```javascript
axios.defaults.baseURL = process.env.VUE_APP_API_URL
```

## Troubleshooting

### Common Issues:

1. **401 Unauthorized**: Check JWT token validity and role permissions
2. **CORS Errors**: Ensure backend CORS is configured for your frontend domain
3. **Component Not Found**: Verify import paths and component registration
4. **Styling Issues**: Check CSS conflicts with existing styles

### Debug Steps:
1. Check browser console for errors
2. Verify API endpoints are accessible
3. Test with different user roles
4. Check network tab for failed requests

## File Structure After Integration

```
src/
├── components/
│   ├── AnnouncementsManagement.vue
│   ├── StudentAnnouncements.vue
│   └── TeacherAnnouncements.vue
├── views/
│   ├── eduoffice/
│   │   └── EduOfficeAnnouncements.vue
│   └── teacher/
│       └── TeacherAnnouncementsPage.vue
├── router/
│   └── index.js (updated with new routes)
└── main.js (updated with component registration)
```

This completes the integration of the Announcement & Notification System into your existing Vue.js application! 🎉