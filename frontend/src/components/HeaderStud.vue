<template>
  <header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        <!-- Left section: Logo and Mobile Menu -->
        <div class="flex items-center lg:hidden">
          <button 
            @click="toggleSidebar" 
            class="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors mr-2"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>

        <!-- Logo and Brand - Centered on mobile, left on desktop -->
        <div class="flex items-center flex-1 lg:flex-none">
          <div class="flex items-center space-x-3">
            <div class="relative">
              <img 
                src="@/assets/images/eduskill-logo.png" 
                alt="Eduskill" 
                class="h-14 w-auto object-contain"
              />
              <!-- Decorative gradient overlay for modern look -->
              <div class="absolute inset-0 bg-gradient-to-tr from-blue-600/10 to-purple-600/10 rounded-lg"></div>
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                EduSkill
              </h1>
              <p class="text-xs text-gray-500">Student Portal</p>
            </div>
          </div>
        </div>

        <!-- Right section: Notifications, Profile, and AI Icon -->
        <div class="flex items-center space-x-2 md:space-x-4">
        

          <!-- User Profile -->
          <div class="relative">
            <button 
              @click="toggleProfileMenu" 
              class="flex items-center space-x-3 p-1.5 rounded-lg hover:bg-gray-100 transition-colors group"
            >
              <div class="flex items-center space-x-3">
                <div class="text-right hidden md:block">
                  <p class="text-sm font-semibold text-gray-800">{{ student.full_name || 'Student' }}</p>
                  <p class="text-xs text-gray-500">Grade {{ student.grade || '7' }}</p>
                </div>
                <div class="relative">
                  <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-md">
                    {{ initials || 'S' }}
                  </div>
                  <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <svg class="w-4 h-4 text-gray-400 group-hover:text-gray-600 transition-colors hidden md:block" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
              </div>
            </button>
            
            <!-- Simplified Profile Dropdown - Only My Profile and Logout -->
            <div v-if="showProfileMenu" class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl py-2 z-50 border border-gray-100">
              <!-- User Info in Dropdown (Mobile) -->
              <div class="md:hidden px-4 py-3 border-b border-gray-100">
                <p class="font-semibold text-gray-800">{{ student.full_name || 'Student' }}</p>
                <p class="text-sm text-gray-500">Grade {{ student.grade || '7' }}</p>
              </div>
              
              <a href="#" @click.prevent="goToProfile" class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                <svg class="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                My Profile
              </a>
              
              <div class="border-t my-1"></div>
              
              <a href="#" @click.prevent="logout" class="flex items-center px-4 py-3 text-sm text-red-600 hover:bg-red-50 transition-colors">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                </svg>
                Logout
              </a>
            </div>
          </div>

          <!-- Separator Line -->
          <div class="h-8 w-px bg-gradient-to-b from-transparent via-gray-300 to-transparent mx-1"></div>

        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderStud',
  props: {
    showMobileMenu: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      student: {
        full_name: 'Alex Johnson',
        grade: '7',
        email: 'alex.j@eduskill.com',
        username: '',
        profile_photo: ''
      },
      unreadCount: 3,
      showProfileMenu: false,
    };
  },
  computed: {
    initials() {
      if (!this.student.full_name) return '';
      return this.student.full_name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .substring(0, 2);
    },
  },
  methods: {
    toggleProfileMenu() {
      this.showProfileMenu = !this.showProfileMenu;
    },
    toggleNotifications() {
      console.log('Toggle notifications');
    },
    toggleSidebar() {
      this.$emit('toggle-sidebar');
    },
    openAIAssistant() {
      console.log('AI Assistant opened');
      // Add your AI assistant logic here
      // For example: this.$router.push('/ai-assistant');
      // Or open a modal: this.$emit('open-ai-assistant');
    },
    goToProfile() {
      this.$router.push('/student/settings');
    },
    logout() {
      // Clear local storage
      localStorage.removeItem('username');
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      // Redirect to login
      this.$router.push('/user_login');
    },
    async loadStudentProfile() {
      const username = localStorage.getItem("username");
      if (!username) {
        this.$router.push('/login');
        return;
      }

      try {
        const res = await fetch(`http://127.0.0.1:8000/api/users/profile/${username}`);
        const data = await res.json();
        this.student = { ...this.student, ...data };
      } catch (error) {
        console.error('Error loading profile:', error);
      }
    }
  },
  mounted() {
    this.loadStudentProfile();

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.$el.contains(e.target)) {
        this.showProfileMenu = false;
      }
    });
  },
};
</script>

<style scoped>
/* Smooth transitions */
.nav-item-transition {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Profile dropdown animation */
.profile-dropdown-enter-active,
.profile-dropdown-leave-active {
  transition: all 0.2s ease;
}

.profile-dropdown-enter-from,
.profile-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* AI icon animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

.group:hover .relative .bg-gradient-to-br {
  animation: float 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.2);
  }
}

.group:hover .relative .bg-gradient-to-br {
  animation: glow 2s ease-in-out infinite;
}

/* Separator line animation */
.hover\:scale-110:hover {
  transform: scale(1.1);
}
</style>