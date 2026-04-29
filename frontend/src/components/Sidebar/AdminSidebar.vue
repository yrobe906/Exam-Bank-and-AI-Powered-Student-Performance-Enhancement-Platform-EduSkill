<template>
  <aside
    :class="[
      'bg-white/95 backdrop-blur-xl border-r border-slate-200/50 shadow-xl flex flex-col min-h-0 overflow-hidden',
      'fixed top-20 left-0 h-[calc(100vh-5rem)] w-80 z-45 transition-all duration-300 ease-in-out',
      // Mobile: toggle visibility
      isOpen ? 'translate-x-0' : '-translate-x-full',
      // Desktop: always visible
      'md:translate-x-0'
    ]"
  >
    <!-- Decorative gradient overlay -->
    <div class="absolute inset-0 bg-gradient-to-br from-indigo-50/30 via-white/20 to-purple-50/30 pointer-events-none"></div>
    
    <!-- Navigation -->
    <nav class="relative flex-1 min-h-0 px-4 py-8 space-y-2 overflow-y-auto custom-scrollbar">
      <SidebarItem
        :icon="icons.ChartBarIcon"
        label="Dashboard"
        to="/admin_dashboard"
        :click="handleNavigation"
        class="sidebar-item"
      />

      <SidebarItem
        :icon="icons.DocumentPlusIcon"
        label="Exclusive Content Management"
        :subItems="[
          { label: 'Add Library Items', to: 'AdminAddLibrary' },
          { label: 'Add Mock Exams', to: '/exam_builder' },
          { label: 'Add Flashcards', to: '/admin_add_flashcards' },
          { label: 'Add Practice Tests', to: '/admin_add_practice_mock' },
        ]"
        :click="handleNavigation"
        class="sidebar-item"
      />

      <SidebarItem
        :icon="icons.UserGroupIcon"
        label="User Management"
        :subItems="[
          { label: 'Create Accounts', to: '/register' },
          { label: 'Approve Registrations', to: '/pending_users' },
        ]"
        :click="handleNavigation"
        class="sidebar-item"
      />

      <SidebarItem
        :icon="icons.CreditCardIcon"
        label="Financial / Premium Controls"
        :subItems="[
          { label: 'Manage Premium Access', to: '/admin/unlock-requests' },
        ]"
        :click="handleNavigation"
        class="sidebar-item"
      />

      <SidebarItem
        :icon="icons.ChatBubbleLeftRightIcon"
        label="Communication"
        :subItems="[
          { label: 'Send Notifications', to: '/eduoffice/announcements' },
          { label: 'Manage Forum Posts', to: '/admin/manage_forum' }
        ]"
        :click="handleNavigation"
        class="sidebar-item"
      />

      <SidebarItem
        :icon="icons.Cog6ToothIcon"
        label="Settings"
        to="/admin/settings"
        :click="handleNavigation"
        class="sidebar-item"
      />

      <!-- Decorative divider -->
      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-slate-200/60"></div>
        </div>
        <div class="relative flex justify-center text-xs">
          <span class="px-3 bg-white text-slate-400">Quick Access</span>
        </div>
      </div>

      <!-- Quick stats cards -->
      <div class="grid grid-cols-2 gap-3 mt-4">
        <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-3 border border-indigo-100/50 hover:shadow-lg transition-all duration-300 hover:scale-105">
          <div class="text-indigo-600 text-xs font-semibold">Total Users</div>
          <div class="text-slate-800 text-xl font-bold mt-1">{{ totalUsers.toLocaleString() }}</div>
        </div>
        <div class="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-3 border border-emerald-100/50 hover:shadow-lg transition-all duration-300 hover:scale-105">
          <div class="text-emerald-600 text-xs font-semibold">Active</div>
          <div class="text-slate-800 text-xl font-bold mt-1">{{ activeUsers.toLocaleString() }}</div>
        </div>
      </div>
    </nav>

    <!-- Footer -->
    <div class="relative p-5 border-t border-slate-200/60 bg-gradient-to-r from-slate-50 to-gray-50">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-sm"></div>
          <span class="text-slate-600 text-xs font-medium">System Online</span>
        </div>
        <div class="text-slate-400 text-xs flex items-center gap-2">
          <span>v2.0.0</span>
          <span class="w-1 h-1 bg-slate-300 rounded-full"></span>
          <span class="text-indigo-600 font-bold">Pro</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
import SidebarItem from "./SidebarItem.vue";
import { useRouter } from "vue-router";
import {
  ChartBarIcon,
  DocumentPlusIcon,
  UserGroupIcon,
  ChartPieIcon,
  BuildingLibraryIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  ChatBubbleLeftRightIcon,
  Cog6ToothIcon
} from "@heroicons/vue/24/outline";

export default {
  name: "AdminSidebar",
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  components: { SidebarItem },
  emits: ['close'],
  setup(props, { emit }) {
    const router = useRouter();
    
    return {
      router,
      emit
    };
  },
  data() {
    return {
      icons: {
        ChartBarIcon,
        DocumentPlusIcon,
        UserGroupIcon,
        ChartPieIcon,
        BuildingLibraryIcon,
        CreditCardIcon,
        ShieldCheckIcon,
        ChatBubbleLeftRightIcon,
        Cog6ToothIcon
      },
      totalUsers: 0,
      activeUsers: 0
    };
  },
  mounted() {
    this.fetchUserSummary();
  },
  methods: {
    async fetchUserSummary() {
      try {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
        const response = await fetch(`${API_BASE_URL}/api/users/summary`);
        if (!response.ok) {
          throw new Error(`Summary request failed: ${response.status}`);
        }
        const data = await response.json();
        this.totalUsers = data.totalUsers ?? 0;
        this.activeUsers = data.activeUsers ?? 0;
      } catch (error) {
        console.error('Failed to load user summary:', error);
      }
    },
    handleNavigation(path) {
      if (!path) return;
      this.$router.push(path);
      // Close sidebar on mobile after navigation
      if (this.isOpen && window.innerWidth < 768) {
        this.$emit('close');
      }
    }
  }
};
</script>

<style scoped>
/* Custom scrollbar - modern gradient style */
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #cbd5e1, #94a3b8);
  border-radius: 10px;
  transition: all 0.3s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #818cf8, #a855f7);
}

/* Firefox scrollbar */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

/* Sidebar item base styles */
.sidebar-item {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Pulse animation for status indicator */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.95);
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Sidebar container shadow and hover effects */
aside {
  box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(0, 0, 0, 0.02);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

aside:hover {
  box-shadow: 0 25px 40px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.02);
}

/* Ensure the nav allows overflow for submenus */
.overflow-y-auto {
  overflow-y: auto !important;
  overflow-x: visible !important;
}

/* Make sure the sidebar items container doesn't clip submenus */
nav.overflow-y-auto {
  overflow-x: visible !important;
}

/* Ensure proper stacking context */
.relative {
  isolation: isolate;
}

/* Smooth transition for all interactive elements */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Active link styling - will work with SidebarItem component */
:deep(.sidebar-item.active) {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
  border-left: 3px solid #818cf8;
}

/* Hover effects for sidebar items */
:deep(.sidebar-item:hover) {
  background: rgba(99, 102, 241, 0.05);
  transform: translateX(4px);
}

/* Icon styling within sidebar items */
:deep(.sidebar-item svg) {
  stroke: #64748b;
  transition: all 0.3s ease;
}

:deep(.sidebar-item:hover svg) {
  stroke: #6366f1;
  transform: scale(1.05);
}

/* Label styling */
:deep(.sidebar-item span) {
  color: #334155;
  font-weight: 500;
}

:deep(.sidebar-item:hover span) {
  color: #4f46e5;
}

/* Submenu item styling */
:deep(.submenu-item) {
  color: #475569;
  transition: all 0.2s ease;
}

:deep(.submenu-item:hover) {
  color: #6366f1;
  transform: translateX(4px);
}

/* Glass morphism effect for header */
.bg-white\/95 {
  backdrop-filter: blur(10px);
}

/* Gradient text animation */
@keyframes textShine {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}

.bg-gradient-to-r.bg-clip-text {
  background-size: 200% auto;
  animation: textShine 3s linear infinite;
}
</style>