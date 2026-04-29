<template>
  <div class="min-h-screen flex bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,1),_rgba(248,250,252,1),_rgba(226,232,240,1))] text-slate-900">
    <!-- Fixed Header -->
    <div class="fixed top-0 left-0 right-0 z-50 h-20 bg-white/95 backdrop-blur-xl border-b border-slate-200 shadow-sm">
      <MainHeader class="h-full" @toggle-sidebar="toggleSidebar" />
    </div>

    <!-- Sidebar Overlay for Mobile -->
    <div
      v-if="sidebarOpen"
      class="md:hidden fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-40"
      @click="closeSidebar"
    ></div>

    <!-- Sidebar -->
    <AdminSidebar
      :is-open="sidebarOpen"
      @logout="handleLogout"
      @close="closeSidebar"
    />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col pt-20 min-h-screen transition-all duration-300 ease-in-out" :class="sidebarOpen ? 'ml-0 md:ml-80' : 'ml-0'">
      <main class="flex-1 p-4 md:p-6 overflow-y-auto min-h-0">

        <!-- Page Title with Admin Info -->
        <div class="space-y-2 mb-6 md:mb-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Admin Dashboard
              </h1>
              <p class="text-slate-500 text-sm md:text-base">
                Welcome back, {{ adminName }} • {{ adminEmail }}
              </p>
            </div>
            <div class="bg-white/90 backdrop-blur-xl px-3 py-1.5 rounded-lg border border-white/20 shadow-sm">
              <span class="text-sm text-cyan-600 font-medium">Role: Admin</span>
            </div>
          </div>
          <p class="text-slate-400 text-sm md:text-base">
            Monitor, manage, and control EduSkill Hub from one powerful center.
          </p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
          <StatCard title="Students" value="1,245" icon="👨‍🎓" color="from-blue-500 to-cyan-500" />
          <StatCard title="Resources" :value="resourceCount.toString()" icon="📚" color="from-purple-500 to-pink-500" />
          <StatCard title="AI Requests" value="8,920" icon="🤖" color="from-amber-500 to-orange-500" />
          <StatCard title="Active Users" value="856" icon="⚡" color="from-green-500 to-emerald-500" />
        </div>

        <!-- Quick Actions Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 mb-6 md:mb-8">
          <router-link
            to="/admin/add-resource"
            class="bg-white/95 backdrop-blur-xl p-4 rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col items-center justify-center text-center hover:-translate-y-1 group"
          >
            <div class="text-2xl md:text-3xl mb-2 group-hover:scale-110 transition-transform">📤</div>
            <h3 class="font-semibold text-sm md:text-base">Add Resource</h3>
            <p class="text-xs text-slate-500 mt-1">Upload new materials</p>
          </router-link>

          <router-link
            to="/admin/library"
            class="bg-white/95 backdrop-blur-xl p-4 rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col items-center justify-center text-center hover:-translate-y-1 group"
          >
            <div class="text-2xl md:text-3xl mb-2 group-hover:scale-110 transition-transform">📚</div>
            <h3 class="font-semibold text-sm md:text-base">View Library</h3>
            <p class="text-xs text-slate-500 mt-1">Manage resources</p>
          </router-link>

          <router-link
            to="/admin/manage_forum"
            class="bg-white/95 backdrop-blur-xl p-4 rounded-2xl border border-slate-200 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col items-center justify-center text-center hover:-translate-y-1 group"
          >
            <div class="text-2xl md:text-3xl mb-2 group-hover:scale-110 transition-transform">💬</div>
            <h3 class="font-semibold text-sm md:text-base">Forum</h3>
            <p class="text-xs text-slate-500 mt-1">Manage posts</p>
          </router-link>

          <div class="bg-white/95 backdrop-blur-xl p-4 rounded-2xl border border-slate-200 shadow-sm transition-all duration-300 flex flex-col items-center justify-center text-center group">
            <div class="text-2xl md:text-3xl mb-2 group-hover:scale-110 transition-transform">👥</div>
            <h3 class="font-semibold text-sm md:text-base">Students</h3>
            <p class="text-xs text-slate-500 mt-1">Manage users</p>
          </div>
        </div>

        <!-- System Overview -->
        <div class="bg-white/95 backdrop-blur-xl shadow-xl rounded-2xl md:rounded-3xl p-4 md:p-8 border border-slate-200/50 mb-6 md:mb-8">
          <h2 class="text-xl md:text-2xl font-bold mb-4 flex items-center gap-2">
            <span class="text-cyan-400">●</span>
            System Overview
          </h2>

          <p class="text-slate-600 leading-relaxed text-sm md:text-base">
            EduSkill Hub is operating smoothly. All services are active, the AI
            learning assistant is responding efficiently, and student engagement
            continues to grow steadily across schools.
          </p>

          <div class="mt-6 flex flex-wrap gap-3">
            <span class="status-pill bg-green-500/20 text-green-700 border border-green-200">
              ✔ Database Connected
            </span>
            <span class="status-pill bg-blue-500/20 text-blue-700 border border-blue-200">
              ✔ AI Service Online
            </span>
            <span class="status-pill bg-cyan-500/20 text-cyan-700 border border-cyan-200" v-if="isAuthenticated">
              ✔ Admin Authenticated
            </span>
            <span class="status-pill bg-purple-500/20 text-purple-700 border border-purple-200">
              ✔ API Stable
            </span>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white/95 backdrop-blur-xl shadow-xl rounded-2xl md:rounded-3xl p-4 md:p-8 border border-slate-200/50">
          <h2 class="text-xl md:text-2xl font-bold mb-6 flex items-center gap-2">
            <span class="text-cyan-400">●</span>
            Recent Activity
          </h2>

          <div class="space-y-4">
            <div class="flex items-center gap-4 p-4 bg-slate-50/50 rounded-xl border border-slate-100">
              <div class="w-10 h-10 rounded-full bg-cyan-500/20 flex items-center justify-center">
                <span class="text-cyan-600">📤</span>
              </div>
              <div class="flex-1">
                <p class="font-medium text-slate-800">Resource Upload</p>
                <p class="text-sm text-slate-500">New Mathematics notes added</p>
              </div>
              <span class="text-sm text-slate-400">2 hours ago</span>
            </div>

            <div class="flex items-center gap-4 p-4 bg-slate-50/50 rounded-xl border border-slate-100">
              <div class="w-10 h-10 rounded-full bg-green-500/20 flex items-center justify-center">
                <span class="text-green-600">👤</span>
              </div>
              <div class="flex-1">
                <p class="font-medium text-slate-800">New Student</p>
                <p class="text-sm text-slate-500">Student registered from Addis Ababa</p>
              </div>
              <span class="text-sm text-slate-400">5 hours ago</span>
            </div>
          </div>
        </div>

      </main>

      <!-- Footer -->
      <MainFooter />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainHeader from "@/components/Header/MainHeader.vue"
import MainFooter from "@/components/Footer/MainFooter.vue"
import AdminSidebar from "@/components/Sidebar/AdminSidebar.vue"

const StatCard = {
  props: ["title", "value", "icon", "color"],
  template: `
    <div
      class="group bg-white/95 backdrop-blur-xl p-4 md:p-6 rounded-2xl border border-slate-200/50 shadow-lg relative overflow-hidden
             transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
    >
      <!-- Gradient overlay -->
      <div
        class="absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-500 rounded-2xl"
        :class="'bg-gradient-to-br ' + (color || 'from-cyan-500 to-blue-500')"
      ></div>

      <div class="flex items-center justify-between relative z-10">
        <div class="flex-1">
          <p class="text-slate-500 text-xs md:text-sm font-medium uppercase tracking-wide mb-1">
            {{ title }}
          </p>
          <h3 class="text-2xl md:text-3xl font-extrabold text-slate-800 transition-colors duration-300 group-hover:text-slate-900">
            {{ value }}
          </h3>
        </div>

        <div class="text-2xl md:text-3xl group-hover:scale-110 transition-transform duration-300 ml-3">
          {{ icon }}
        </div>
      </div>
    </div>
  `
};

export default {
  name: "AdminDashboard",
  components: {
    MainHeader,
    MainFooter,
    AdminSidebar,
    StatCard
  },
  setup() {
    const router = useRouter()
    const sidebarOpen = ref(false) // Start closed on mobile, will auto-open on desktop
    const isAuthenticated = ref(false)
    const adminName = ref('')
    const adminEmail = ref('')
    const resourceCount = ref(0)

    // Check authentication on component mount
    onMounted(() => {
      checkAuthentication()
      fetchResourceCount()
      handleResponsiveSidebar()
      window.addEventListener('resize', handleResponsiveSidebar)
    })

    const handleResponsiveSidebar = () => {
      // Auto-open sidebar on desktop, keep user's preference on mobile
      if (window.innerWidth >= 768) { // md breakpoint
        sidebarOpen.value = true
      } else {
        sidebarOpen.value = false
      }
    }

    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value
    }

    const closeSidebar = () => {
      sidebarOpen.value = false
    }

    const checkAuthentication = () => {
      const adminToken = sessionStorage.getItem('admin_token')
      const adminUser = sessionStorage.getItem('admin_user')
      
      if (!adminToken || !adminUser) {
        console.log('❌ No admin session - redirecting to login')
        router.push('/admin_login')
        return
      }
      
      try {
        const user = JSON.parse(adminUser)
        adminName.value = user.full_name || user.email?.split('@')[0] || 'Admin'
        adminEmail.value = user.email || 'No email'
        isAuthenticated.value = true
        console.log('✅ Admin authenticated:', user.email)
      } catch (error) {
        console.error('❌ Error parsing admin user:', error)
        sessionStorage.removeItem('admin_token')
        sessionStorage.removeItem('admin_user')
        router.push('/admin_login')
      }
    }

    const fetchResourceCount = async () => {
      try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
        const response = await fetch(`${API_BASE_URL}/api/resources`)
        if (response.ok) {
          const resources = await response.json()
          resourceCount.value = resources.length || 0
        }
      } catch (error) {
        console.error('Error fetching resources:', error)
      }
    }

    const handleLogout = () => {
      // Clear all admin session data using sessionStorage
      sessionStorage.removeItem('admin_token')
      sessionStorage.removeItem('admin_user')
      sessionStorage.removeItem('admin_email')
      
      // Redirect to admin login
      router.push('/admin_login')
      
      // Optional: Show logout message
      console.log('✅ Admin logged out successfully')
    }

    return {
      sidebarOpen,
      isAuthenticated,
      adminName,
      adminEmail,
      resourceCount,
      toggleSidebar,
      closeSidebar,
      handleLogout
    }
  }
}
</script>

<style scoped>
/* Soft fade-in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

/* Status pills */
.status-pill {
  padding: 0.5rem 0.875rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(8px);
  border: 1px solid transparent;
}
</style>