<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/40 font-sans">
    <!-- EduSkill Header -->
    <EduskillHeader />

    <div class="max-w-4xl mx-auto px-4 py-8 md:py-12">
      <!-- Main Card with depth -->
      <div class="bg-white rounded-2xl shadow-xl shadow-indigo-100/30 border border-gray-100 overflow-hidden transition-all duration-300">
        
        <!-- Hero Banner with modern wave pattern -->
        <div class="relative bg-gradient-to-r from-indigo-600 via-blue-600 to-indigo-700 px-6 py-10 text-center overflow-hidden">
          <div class="absolute inset-0 opacity-20">
            <svg class="absolute bottom-0 left-0 w-full h-24" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
              <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="currentColor" class="fill-white"></path>
            </svg>
          </div>
          <div class="relative z-2">
            <div class="relative inline-block group">
              <div class="absolute inset-0 rounded-full bg-gradient-to-tr from-indigo-300 to-blue-300 blur-md opacity-60 group-hover:opacity-80 transition-all"></div>
              <img 
                :src="previewUrl || getProfilePhotoUrl(userData.profile_photo)" 
                class="relative w-32 h-32 rounded-full border-4 border-white shadow-xl object-cover bg-gray-100 transition-all duration-300 group-hover:scale-105"
                @error="handleImageError"
                alt="profile"
              />
              <label for="profile-upload" class="absolute bottom-1 right-1 bg-white p-2.5 rounded-full shadow-lg text-indigo-600 hover:bg-indigo-50 hover:scale-110 transition-all cursor-pointer border border-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </label>
              <input id="profile-upload" type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleFileChange" />
            </div>
            <h2 class="text-white text-2xl md:text-3xl font-bold mt-5 tracking-tight">{{ userData.full_name || 'User' }}</h2>
            <div class="inline-flex items-center gap-1.5 mt-1.5 bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold text-white uppercase tracking-wide">
              <span class="w-1.5 h-1.5 bg-green-300 rounded-full animate-pulse"></span>
              {{ userRoleLabel }}
            </div>
          </div>
        </div>

        <!-- Form Sections with cards inside card -->
        <form @submit.prevent="updateProfile" class="p-6 md:p-8 space-y-8">
          <!-- Personal details card -->
          <div class="bg-gray-50/80 rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-800 flex items-center gap-2 mb-5">
              <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              Basic Information
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Full Name</label>
                <input v-model="formData.full_name" type="text" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 outline-none transition-all bg-white" placeholder="Your full name" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Username</label>
                <input v-model="formData.username" type="text" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 outline-none transition-all bg-white" placeholder="username" />
              </div>
            </div>
          </div>

          <!-- Role Specific Card (dynamic fields) -->
          <div v-if="userRole === 'student'" class="bg-gradient-to-r from-amber-50 to-orange-50/60 rounded-xl p-5 border border-amber-100 shadow-sm">
            <div class="flex items-center gap-2 mb-4">
              <div class="p-1.5 bg-amber-100 rounded-lg"><svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg></div>
                  <h3 class="text-lg font-semibold text-gray-800">Academic Info</h3>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Grade Level</label>
              <select v-model="formData.grade" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white">
                <option v-for="g in [9, 10, 11, 12]" :key="g" :value="g">Grade {{ g }}</option>
              </select>
            </div>
          </div>

          <div v-if="userRole === 'teacher'" class="bg-gradient-to-r from-emerald-50 to-teal-50/60 rounded-xl p-5 border border-emerald-100 shadow-sm">
            <div class="flex items-center gap-2 mb-4">
              <div class="p-1.5 bg-emerald-100 rounded-lg"><svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg></div>
              <h3 class="text-lg font-semibold text-gray-800">Teaching Details</h3>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1.5">Subject Expertise</label>
              <input v-model="formData.subject_assigned" type="text" placeholder="e.g. Mathematics, Physics, Literature" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white" />
            </div>
          </div>

          <!-- Contact Card (for teacher/office/admin) -->
          <div v-if="['teacher', 'eduoffice', 'admin'].includes(userRole)" class="bg-blue-50/40 rounded-xl p-5 border border-blue-100 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-800 flex items-center gap-2 mb-4">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              Contact Information
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Email Address</label>
                <input v-model="formData.email" type="email" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white" placeholder="professional@example.com" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">Phone Number</label>
                <input v-model="formData.phone" type="tel" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white" placeholder="+1 234 567 890" />
              </div>
            </div>
          </div>

          <!-- Security Card -->
          <div class="bg-gray-50/70 rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 class="text-lg font-semibold text-gray-800 flex items-center gap-2 mb-4">
              <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              Security & Password
            </h3>
            <div class="space-y-4">
              <input v-model="formData.current_password" type="password" placeholder="Current Password (required for any change)" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white" />
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input v-model="formData.new_password" type="password" placeholder="New Password" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white" />
                <input v-model="formData.confirm_password" type="password" placeholder="Confirm New Password" class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-400 outline-none bg-white" />
              </div>
              <p class="text-xs text-gray-500 mt-1">* Leave password fields empty if you don't want to change password.</p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="pt-2">
            <button 
              type="submit" 
              :disabled="loading"
              class="w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-bold py-3.5 rounded-xl hover:from-indigo-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-base"
            >
              <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              {{ loading ? 'Saving Changes...' : 'Save Profile & Update' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Extra tip card (optional) -->
      <div class="mt-6 text-center text-sm text-gray-500 flex items-center justify-center gap-2">
        <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span>Your data is securely encrypted. Changes reflect immediately across the platform.</span>
      </div>
    </div>

    <!-- Toast Notifications (modern) -->
    <transition name="toast-fade">
      <div v-if="message" :class="isSuccess ? 'bg-emerald-600 shadow-emerald-500/20' : 'bg-rose-600 shadow-rose-500/20'" class="fixed bottom-8 left-1/2 transform -translate-x-1/2 text-white px-6 py-3 rounded-2xl shadow-2xl z-50 flex items-center gap-3 backdrop-blur-md bg-opacity-95 font-medium">
        <svg v-if="isSuccess" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ message }}
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import EduskillHeader from '@/components/Header/EduskillHeader.vue'

export default {
  name: 'EditProfile',
  components: {
    EduskillHeader
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const message = ref('')
    const isSuccess = ref(false)
    const previewUrl = ref(null)
    const fileInput = ref(null)

    // Role label mapping for display
    const userRoleLabel = computed(() => {
      const roleMap = {
        student: '🎓 STUDENT',
        teacher: '👩‍🏫 TEACHER',
        eduoffice: '🏛️ EDUCATION OFFICE',
        admin: '⚙️ ADMIN'
      }
      return roleMap[userRole.value] || 'MEMBER'
    })

    const userRole = computed(() => {
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      return user.role || 'student'
    })

    const userData = ref({
      full_name: '',
      username: '',
      email: '',
      phone: '',
      grade: '',
      subject_assigned: '',
      profile_photo: null,
      role: 'student'
    })

    const formData = ref({
      full_name: '',
      username: '',
      email: '',
      phone: '',
      grade: '',
      subject_assigned: '',
      current_password: '',
      new_password: '',
      confirm_password: '',
      profile_photo: null
    })

    onMounted(() => {
      const storedUser = localStorage.getItem('user')
      if (!storedUser) {
        router.push('/login')
        return
      }
      const user = JSON.parse(storedUser)
      if (!user.username) {
        router.push('/login')
        return
      }
      userData.value = { ...user }
      
      // Populate formData with existing user data
      formData.value.full_name = user.full_name || ''
      formData.value.username = user.username || ''
      formData.value.email = user.email || ''
      formData.value.phone = user.phone || ''
      formData.value.grade = user.grade || ''
      formData.value.subject_assigned = user.subject_assigned || ''
      // Keep password fields empty
    })

    const handleFileChange = (e) => {
      const file = e.target.files[0]
      if (file) {
        // Validate file size & type (optional)
        if (file.size > 2 * 1024 * 1024) {
          message.value = "Image size must be less than 2MB"
          isSuccess.value = false
          setTimeout(() => message.value = "", 3000)
          return
        }
        formData.value.profile_photo = file
        previewUrl.value = URL.createObjectURL(file)
      }
    }

    const handleImageError = (event) => {
      // fallback to dicebear if image fails to load
      event.target.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${userData.value.username || 'user'}`
    }

    const getProfilePhotoUrl = (path) => {
      if (!path || typeof path !== 'string' || path.trim().length === 0) {
        return `https://api.dicebear.com/7.x/avataaars/svg?seed=${userData.value.username || 'avatar'}`
      }
      const cleaned = path.trim()
      if (cleaned.startsWith('http')) return cleaned
      // Remove leading slashes and handle various formats
      let normalized = cleaned.replace(/^\/+/, '')
      // Remove all leading 'uploads/' prefixes
      while (normalized.startsWith('uploads/')) {
        normalized = normalized.substring(8)
      }
      return `http://127.0.0.1:8000/uploads/${normalized}`
    }

    const updateProfile = async () => {
      // validation
      if (formData.value.new_password && formData.value.new_password !== formData.value.confirm_password) {
        message.value = "❌ New passwords do not match!"
        isSuccess.value = false
        setTimeout(() => message.value = "", 3000)
        return
      }
      
      if (formData.value.new_password && (!formData.value.current_password || formData.value.current_password.trim() === '')) {
        message.value = "⚠️ Please enter your current password to set a new password."
        isSuccess.value = false
        setTimeout(() => message.value = "", 3000)
        return
      }

      loading.value = true
      const data = new FormData()
      
      // Base fields
      data.append('full_name', formData.value.full_name || '')
      data.append('username', formData.value.username || '')
      
      // Always send current password if provided, else send as empty but backend may handle
      if (formData.value.current_password) {
        data.append('current_password', formData.value.current_password)
      } else {
        // if no password change, we still need to pass something to not break backend? we send blank but backend might ignore if no new password.
        data.append('current_password', '')
      }

      // Role specific
      if (userRole.value === 'student') {
        data.append('grade', formData.value.grade || '')
      }
      if (userRole.value === 'teacher') {
        data.append('subject_assigned', formData.value.subject_assigned || '')
      }
      if (['teacher', 'eduoffice', 'admin'].includes(userRole.value)) {
        data.append('email', formData.value.email || '')
        data.append('phone', formData.value.phone || '')
      }

      if (formData.value.new_password) {
        data.append('new_password', formData.value.new_password)
      }
      
      if (formData.value.profile_photo && formData.value.profile_photo instanceof File) {
        data.append('profile_photo', formData.value.profile_photo)
      }

      try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No auth token')
        
        const res = await axios.put('/api/users/profile', data, {
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        
        // Merge updated user data into localStorage
        const updatedUserPayload = res.data?.user || {}
        const updatedUser = { ...userData.value, ...updatedUserPayload }
        localStorage.setItem('user', JSON.stringify(updatedUser))
        userData.value = updatedUser
        
        // sync formData's text fields (except password)
        formData.value.full_name = updatedUser.full_name || ''
        formData.value.username = updatedUser.username || ''
        if (['teacher', 'eduoffice', 'admin'].includes(userRole.value)) {
          formData.value.email = updatedUser.email || ''
          formData.value.phone = updatedUser.phone || ''
        }
        if (userRole.value === 'student') formData.value.grade = updatedUser.grade || ''
        if (userRole.value === 'teacher') formData.value.subject_assigned = updatedUser.subject_assigned || ''
        
        // Clear password fields after success
        formData.value.current_password = ''
        formData.value.new_password = ''
        formData.value.confirm_password = ''
        
        isSuccess.value = true
        message.value = "✨ Profile updated successfully!"
        setTimeout(() => message.value = "", 3500)
        
        // optional: clear preview url but keep avatar (no need)
      } catch (err) {
        console.error('Update error:', err)
        isSuccess.value = false
        const errorMsg = err.response?.data?.message || err.response?.data?.error || "Update failed. Please check your credentials."
        message.value = `❌ ${errorMsg}`
        setTimeout(() => message.value = "", 4000)
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      const role = userRole.value
      let dashboardPath = '/student_dashboard' // default
      
      if (role === 'teacher') {
        dashboardPath = '/teacher_dashboard'
      } else if (role === 'eduoffice') {
        dashboardPath = '/education_office_dashboard'
      } else if (role === 'admin') {
        dashboardPath = '/admin_dashboard'
      }
      
      router.push(dashboardPath)
    }

    return {
      userRole,
      userRoleLabel,
      userData,
      formData,
      loading,
      message,
      isSuccess,
      previewUrl,
      fileInput,
      handleFileChange,
      updateProfile,
      getProfilePhotoUrl,
      goBack,
      handleImageError
    }
  }
}
</script>

<style scoped>
/* Smooth toast transitions */
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast-fade-enter-from {
  opacity: 0;
  transform: translate(-50%, 20px);
}
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}

/* Custom scrollbar for inputs */
input, select {
  transition: all 0.2s ease;
}
input:focus, select:focus {
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* card hover enhancements */
.bg-white.rounded-2xl {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.bg-white.rounded-2xl:hover {
  box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.15);
}

/* role badges subtle */
.relative.z-2 .inline-flex {
  backdrop-filter: blur(4px);
}
</style>