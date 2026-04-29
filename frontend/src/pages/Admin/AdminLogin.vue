<template>
  <div class="login-container">
    <!-- Animated Background with 3D organic shapes -->
    <div class="fixed inset-0 overflow-hidden -z-10">
      <div class="absolute -top-40 -right-32 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style="animation-delay: 0s;"></div>
      <div class="absolute top-60 -left-32 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-20 right-20 w-80 h-80 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-25 animate-float" style="animation-delay: 4s;"></div>
      <div class="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-indigo-50/30"></div>
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zMCAzMG0tMjkgMGEyOSAyOSAwIDEgMCA1OCAwIDI5IDI5IDAgMSAwLTU4IDB6IiBzdHJva2U9IiNjY2NjY2MvMTIiIHN0cm9rZS13aWR0aD0iMSIvPjwvZz48L3N2Zz4=')] opacity-20"></div>
    </div>

    <!-- Main Content -->
    <div class="login-wrapper relative z-10">
      <!-- Login Card - premium glassmorphism with logo inside -->
      <div class="login-card backdrop-blur-xl bg-white/90 rounded-2xl shadow-2xl border border-white/50 p-6 transition-all duration-300 hover:shadow-indigo-100/40">
        
        <!-- Logo & Title inside card (compact) -->
        <div class="logo-section text-center mb-5">
          <div class="logo-icon mx-auto w-14 h-14 bg-gradient-to-br from-indigo-600 via-blue-600 to-purple-700 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 class="text-2xl font-extrabold mt-3 bg-clip-text text-transparent bg-gradient-to-r from-gray-800 to-gray-600 tracking-tight">Admin Portal</h1>
          <p class="text-slate-500 text-xs font-medium mt-0.5">Secure Access Dashboard</p>
        </div>

        <!-- Card Header Welcome -->
        <div class="card-header text-center mb-5">
          <h2 class="text-xl font-bold text-gray-800">Welcome Back</h2>
          <p class="text-slate-400 text-xs mt-1">Enter your credentials to access the admin panel</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form space-y-4">
          <!-- Username Field -->
          <div class="form-group space-y-1.5">
            <label class="form-label text-[11px] font-semibold text-gray-600 uppercase tracking-wider">Username</label>
            <div class="input-wrapper relative">
              <svg class="input-icon absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <input 
                v-model="form.username"
                type="text" 
                required
                placeholder="Enter your username"
                class="form-input w-full pl-9 pr-3 py-2.5 rounded-lg border border-gray-200 bg-white/70 focus:bg-white focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition-all duration-200 outline-none text-sm"
                :disabled="isLoading"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div class="form-group space-y-1.5">
            <label class="form-label text-[11px] font-semibold text-gray-600 uppercase tracking-wider">Password</label>
            <div class="input-wrapper relative">
              <svg class="input-icon absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input 
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="Enter your password"
                class="form-input w-full pl-9 pr-9 py-2.5 rounded-lg border border-gray-200 bg-white/70 focus:bg-white focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition-all duration-200 outline-none text-sm"
                :disabled="isLoading"
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="password-toggle absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                :disabled="isLoading"
              >
                <svg v-if="!showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
              </button>
            </div>
          </div>

          <!-- Submit Button with modern animation -->
          <button 
            type="submit"
            :disabled="isLoading"
            class="submit-btn w-full py-2.5 rounded-lg font-bold text-white bg-gradient-to-r from-indigo-600 via-blue-600 to-indigo-700 hover:scale-[1.01] transition-all duration-300 shadow-md shadow-indigo-500/30 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed disabled:hover:scale-100 text-sm"
            :class="{ 'loading': isLoading }"
          >
            <svg v-if="isLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <span v-else>Sign In</span>
            <svg v-if="!isLoading" class="w-4 h-4 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </form>

        <!-- Back Link -->
        <div class="back-link mt-4 text-center">
          <router-link to="/" class="back-btn inline-flex items-center gap-1.5 text-slate-400 hover:text-indigo-600 transition-colors text-xs">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Home
          </router-link>
        </div>

        <!-- Status & Messages Section at the bottom of card -->
        <div class="mt-5 pt-3 border-t border-gray-100">
          <!-- Status Indicator inside card -->
          <div class="status-bar text-center mb-2">
            <div class="status-indicator inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-50/80 rounded-full shadow-sm text-xs font-medium" :class="serverStatus">
              <span class="status-dot w-1.5 h-1.5 rounded-full" :class="serverStatus === 'online' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'"></span>
              <span class="status-text text-gray-600">{{ serverStatus === 'online' ? 'System Online' : 'System Offline' }}</span>
            </div>
          </div>

          <!-- Success Message (Green, at bottom of card) -->
          <div v-if="showSuccess" class="mt-2 p-2 bg-emerald-50 border border-emerald-200 rounded-lg flex items-center justify-center gap-2">
            <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span class="text-emerald-700 text-xs font-medium">Login Successful! Redirecting...</span>
          </div>

          <!-- Error Message (Red, at bottom of card) -->
          <div v-if="showError" class="mt-2 p-2 bg-rose-50 border border-rose-200 rounded-lg flex items-center justify-between">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-rose-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span class="text-rose-700 text-xs font-medium">{{ errorMessage }}</span>
            </div>
            <button @click="showError = false" class="text-rose-400 hover:text-rose-600 transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating toasts removed - messages now inside card -->
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const showPassword = ref(false)
const isLoading = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const serverStatus = ref('checking')
const apiBaseUrl = ref('http://localhost:8000')

const form = reactive({
  username: '',
  password: ''
})

const testConnection = async () => {
  try {
    const response = await fetch(apiBaseUrl.value)
    serverStatus.value = response.ok ? 'online' : 'offline'
  } catch {
    serverStatus.value = 'offline'
  }
}

const handleLogin = async () => {
  isLoading.value = true
  showError.value = false
  showSuccess.value = false

  try {
    const formData = new URLSearchParams()
    formData.append('username', form.username)
    formData.append('password', form.password)

    const response = await fetch(`${apiBaseUrl.value}/api/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData
    })

    if (response.ok) {
      const data = await response.json()
      // Save to BOTH sessionStorage AND localStorage
      sessionStorage.setItem('admin_token', data.access_token)
      sessionStorage.setItem('admin_user', JSON.stringify({ username: form.username, admin_id: data.admin_id, full_name: data.full_name, email: data.email }))
      localStorage.setItem('admin_token', data.access_token)
      localStorage.setItem('admin_user', JSON.stringify({ username: form.username, admin_id: data.admin_id, full_name: data.full_name, email: data.email }))
      
      showSuccess.value = true
      setTimeout(() => router.push('/admin_dashboard'), 1200)

    } else {
      const err = await response.text()
      errorMessage.value = err || 'Invalid credentials'
      showError.value = true
      // Auto-hide error after 4 seconds
      setTimeout(() => { showError.value = false }, 4000)
    }
  } catch (error) {
    errorMessage.value = error.message || 'Connection error'
    showError.value = true
    setTimeout(() => { showError.value = false }, 4000)
  } finally {
    isLoading.value = false
  }
}

onMounted(testConnection)
</script>

<style scoped>
/* Custom Animations */
@keyframes float {
  0%, 100% { transform: translateY(0px) translateX(0px); }
  50% { transform: translateY(-10px) translateX(5px); }
}

.animate-float {
  animation: float 8s ease-in-out infinite;
}

/* Container Styles */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.login-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}

/* Button Hover Effect */
.submit-btn {
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.5s, height 0.5s;
}

.submit-btn:hover::before {
  width: 300px;
  height: 300px;
}

/* Input Focus Enhancements */
.form-input:focus {
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

/* Status indicator pulse */
.status-dot.bg-emerald-500 {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}

/* Responsive */
@media (max-width: 480px) {
  .login-wrapper {
    padding: 0.75rem;
  }
  
  .login-card {
    padding: 1.25rem;
  }
}
</style>