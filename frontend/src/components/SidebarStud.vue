<template>
  <aside class="w-64 bg-gradient-to-b from-gray-50 to-white border-r border-gray-200 min-h-screen lg:min-h-0 overflow-y-auto scroll-smooth" style="max-height: calc(100vh - 80px);">
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="absolute inset-0 bg-white/90 backdrop-blur-sm z-50 flex flex-col items-center justify-center rounded-l-2xl">
      <div class="relative">
        <div class="w-16 h-16 border-4 border-blue-100 border-t-blue-500 rounded-full animate-spin"></div>
        <div class="absolute inset-0 w-16 h-16 border-4 border-purple-100 border-t-purple-500 rounded-full animate-spin" style="animation-delay: 0.2s"></div>
        <div class="absolute inset-1 w-14 h-14 border-4 border-indigo-100 border-t-indigo-500 rounded-full animate-spin" style="animation-delay: 0.4s"></div>
      </div>
      <p class="mt-4 text-gray-700 font-semibold">loading...</p>
    </div>
    
    <div class="p-4 lg:p-6">
      <!-- Mobile Close Button -->
      <button 
        @click="closeSidebar" 
        class="lg:hidden absolute top-4 right-4 p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>

      <!-- User Profile Summary -->
      <div class="flex items-center space-x-3 lg:space-x-4 mb-6 lg:mb-8">
        <!-- Profile Picture -->
        <div v-if="student.profile_photo" class="w-12 h-12 lg:w-16 lg:h-16 rounded-full overflow-hidden border-2 border-blue-400 flex-shrink-0">
          <img :src="getProfilePhotoUrl(student.profile_photo)" alt="Profile Picture" class="w-full h-full object-cover" />
        </div>
        <div v-else class="w-12 h-12 lg:w-16 lg:h-16 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center border-2 border-blue-400 flex-shrink-0">
          <span class="text-white font-bold text-lg lg:text-xl">{{ initials }}</span>
        </div>

        <!-- Name, Grade, School ID -->
        <div class="min-w-0">
          <h3 class="text-base lg:text-lg font-semibold text-gray-800 truncate">@:{{ student.username }}</h3>
          <p class="text-xs lg:text-sm text-gray-500">Grade {{ student.grade }} Student</p>
          <p class="text-xs text-gray-400 hidden lg:block">School ID: {{ student.school_id }}</p>
        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="space-y-1 lg:space-y-2">
        <router-link 
          v-for="item in menuItems" 
          :key="item.name"
          :to="item.path"
          @click="closeOnNavigate"
          :class="[ 
            'flex items-center space-x-3 px-3 lg:px-4 py-2.5 lg:py-3 rounded-lg transition-all duration-200',
            isActive(item.path) ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-md' : 'text-gray-700 hover:bg-blue-50 hover:text-blue-600'
          ]"
        >
          <div :class="isActive(item.path) ? 'text-white' : 'text-blue-500'">
            <component :is="item.icon" class="w-5 h-5" />
          </div>
          <span class="font-medium text-sm lg:text-base">{{ item.name }}</span>
          <span v-if="item.badge" class="ml-auto bg-red-500 text-white text-xs px-2 py-0.5 lg:py-1 rounded-full">
            {{ item.badge }}
          </span>
        </router-link>
      </nav>

      <!-- Gamification Section -->
      <div class="mt-4 lg:mt-6">
        <div class="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl p-3 lg:p-4">
          <h4 class="font-semibold text-gray-800 mb-3 text-sm lg:text-base flex items-center gap-2">
            <span>🎮</span> Gamification
          </h4>
          
          <!-- XP Points Display -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs">💎</span>
              </div>
              <div>
                <div class="text-xs text-gray-500">Points</div>
                <div class="font-bold text-gray-800 text-sm">{{ profile?.xp_points || 0 }} XP</div>
              </div>
            </div>
            <div class="text-xs px-2 py-1 rounded-full font-semibold" :class="getTierClass(profile?.tier)">
              {{ profile?.tier?.toUpperCase() || 'BRONZE' }}
            </div>
          </div>
          
          <!-- Streak Display -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-gradient-to-br from-red-400 to-orange-500 rounded-full flex items-center justify-center">
                <span class="text-white text-xs">🔥</span>
              </div>
              <div>
                <div class="text-xs text-gray-500">Streak</div>
                <div class="font-bold text-gray-800 text-sm">{{ profile?.current_streak || 0 }} days</div>
              </div>
            </div>
          </div>

          <!-- Badges Grid -->
          <div class="mt-3 pt-3 border-t border-gray-200">
            <div class="text-xs text-gray-500 mb-2">Badges Earned</div>
            <div class="flex flex-wrap gap-2">
              <div v-for="badge in earnedBadges" :key="badge.id" class="relative group">
                <div class="w-10 h-10 rounded-full flex items-center justify-center transform transition-all duration-300 hover:scale-110 hover:-translate-y-1 cursor-pointer" :class="getBadgeClass(badge.tier_required)">
                  <span class="text-white text-sm">{{ badge.icon || '🏆' }}</span>
                </div>
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block z-50">
                  <div class="bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">{{ badge.name }}</div>
                </div>
              </div>
              <div v-if="earnedBadges.length === 0" class="text-xs text-gray-500">No badges yet</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
import { 
  HomeIcon,
  BookOpenIcon,
  ChartBarIcon,
  ChatBubbleLeftRightIcon,
  BuildingLibraryIcon,
  Cog6ToothIcon,
  BellIcon,
  AcademicCapIcon,
  RectangleStackIcon,
  StarIcon 
} from '@heroicons/vue/24/outline';

export default {
  name: 'SidebarStud',
  components: {
    HomeIcon,
    BookOpenIcon,
    ChartBarIcon,
    ChatBubbleLeftRightIcon,
    BuildingLibraryIcon,
    Cog6ToothIcon,
    BellIcon,
    AcademicCapIcon,
    RectangleStackIcon,
    StarIcon,
  },
  data() {
    return {
      isLoading: false,
      student: {
        grade: '',
        school_id: '',
        username: '',
        profile_photo: ''
      },
      menuItems: [
        { name: 'Dashboard', path: '/student_dashboard', icon: 'HomeIcon', active: false },
        { name: 'Exam Bank', path: '/exam-bank-options', icon: 'BookOpenIcon', active: false },
        { name: 'Mock Tests', path: '/student/available-tests', icon: 'AcademicCapIcon', active: false, badge: '3' },
        { name: 'Flashcards', path: '/flashcards', icon: 'RectangleStackIcon', active: false },
        { name: 'Student Room', path: '/student/forum', icon: 'ChatBubbleLeftRightIcon', active: false, badge: '5' },
        { name: 'Library', path: '/library', icon: 'BuildingLibraryIcon', active: false },
        { name: 'Gamification', path: '/student/gamification', icon: 'StarIcon', active: false },
        { name: 'Section Feedback', path: '/student/section-feedback', icon: 'ChartBarIcon', active: false },
        { name: 'Notifications', path: '/student/announcements', icon: 'BellIcon', active: false },
        { name: 'Settings', path: '/student/settings', icon: 'Cog6ToothIcon', active: false },
      ],
      earnedBadges: [],
      profile: null,
    };
  },
  computed: {
    initials() {
      if (!this.student.full_name) return '';
      return this.student.full_name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase();
    }
  },
  methods: {
    isActive(path) {
      return this.$route.path === path;
    },
    closeSidebar() {
      this.$emit('close-sidebar');
    },
    closeOnNavigate() {
      // Trigger loading state before navigation
      this.isLoading = true;
      this.$emit('close-sidebar');
      
      // Navigate after a short delay to show loading
      setTimeout(() => {
        // Let the parent handle navigation through router-link
        // The loading will be cleared when component remounts
      }, 600);
    },
    getBadgeClass(tier) {
      const tierClasses = {
        bronze: 'bg-gradient-to-br from-yellow-600 to-yellow-700',
        silver: 'bg-gradient-to-br from-gray-300 to-gray-400',
        gold: 'bg-gradient-to-br from-yellow-400 to-orange-500',
        diamond: 'bg-gradient-to-br from-cyan-400 to-blue-500'
      };
      return tierClasses[tier] || 'bg-gradient-to-br from-yellow-400 to-orange-500';
    },
    getTierClass(tier) {
      const tierClasses = {
        bronze: 'bg-yellow-100 text-yellow-800',
        silver: 'bg-gray-100 text-gray-800',
        gold: 'bg-yellow-100 text-yellow-800',
        diamond: 'bg-blue-100 text-blue-800'
      };
      return tierClasses[tier] || 'bg-yellow-100 text-yellow-800';
    },
    async loadGamificationData() {
      try {
        const userToken = localStorage.getItem('token');
        if (!userToken) return;
        
        const profileResponse = await fetch('http://127.0.0.1:8000/api/gamification/profile', {
          headers: { 'Authorization': `Bearer ${userToken}` }
        });
        
        if (profileResponse.ok) {
          this.profile = await profileResponse.json();
        }
        
        const summaryResponse = await fetch('http://127.0.0.1:8000/api/gamification/summary', {
          headers: { 'Authorization': `Bearer ${userToken}` }
        });
        
        if (summaryResponse.ok) {
          const data = await summaryResponse.json();
          this.earnedBadges = data.earned_badges || [];
        }
      } catch (err) {
        console.error('Error loading gamification data:', err);
      }
    },
    async loadStudentProfile() {
      const username = localStorage.getItem("username");
      if (!username) {
        this.$router.push('user_login');
        return;
      }
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/users/profile/${username}`);
        if (!res.ok) throw new Error('Failed to fetch profile');
        const data = await res.json();
        this.student = data;
      } catch (err) {
        console.error(err);
        this.$router.push('user_login');
      }
    },
    getProfilePhotoUrl(profilePhoto) {
      if (!profilePhoto) return `https://api.dicebear.com/7.x/avataaars/svg?seed=${this.student.username}`;
      
      // Normalize path separators
      let normalizedPath = profilePhoto.replace(/\\/g, '/').replace(/^\/+/, '');
      if (!normalizedPath.startsWith('uploads/')) {
        normalizedPath = 'uploads/' + normalizedPath;
      }
      
      return `http://127.0.0.1:8000/${normalizedPath}`;
    }
  },
  mounted() {
    this.loadStudentProfile();
    this.loadGamificationData();
  }
};
</script>
