<template>
  <div @mouseenter="open = true" @mouseleave="open = false" class="relative">
    <!-- Main Item (no subitems) -->
    <router-link
      v-if="!subItems || subItems.length === 0"
      :to="to"
      class="group flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-400 hover:bg-gray-800/50 hover:text-gray-200 transition-all duration-200"
      active-class="bg-gradient-to-r from-blue-600/20 to-indigo-600/20 text-white border-l-2 border-blue-400"
      @click="handleClick(to, $event)"
    >
      <component :is="icon" class="w-5 h-5 text-gray-500 group-hover:text-blue-400 transition-all duration-200 group-hover:scale-110" />
      <span class="font-medium text-sm">{{ label }}</span>
      
      <!-- Active indicator dot -->
      <span class="ml-auto w-1.5 h-1.5 bg-blue-400 rounded-full opacity-0 router-link-active:opacity-100 transition-opacity duration-200"></span>
    </router-link>

    <!-- Item with SubItems (dropdown trigger) -->
    <div 
      v-else 
      class="group flex items-center justify-between px-3 py-2.5 rounded-lg text-gray-400 hover:bg-gray-800/50 hover:text-gray-200 transition-all duration-200 cursor-pointer"
      :class="{ 'bg-gradient-to-r from-gray-800/50 to-gray-700/50 text-white': open }"
    >
      <div class="flex items-center gap-3">
        <component :is="icon" class="w-5 h-5 text-gray-500 transition-all duration-200" 
                   :class="{
                     'group-hover:text-blue-400 group-hover:scale-110': true,
                     'text-blue-400': open
                   }" />
        <span class="font-medium text-sm">{{ label }}</span>
      </div>
      
      <!-- Chevron icon with rotation -->
      <svg class="w-4 h-4 transition-transform duration-300" 
           :class="{ 'rotate-180 text-blue-400': open }" 
           fill="none" 
           stroke="currentColor" 
           viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>

    <!-- SubItems Dropdown - Different background from parent -->
    <transition name="dropdown">
      <div
        v-if="subItems && subItems.length > 0 && open"
        class="relative mt-1 w-full rounded-lg shadow-xl border py-1 z-50"
        :class="submenuBgClass"
      >
        <!-- Submenu items -->
        <div class="py-1 max-h-80 overflow-y-auto custom-scrollbar">
          <router-link
            v-for="(sub, index) in subItems"
            :key="index"
            :to="sub.to"
            class="block px-4 py-2.5 text-sm transition-all duration-200"
            :class="submenuItemClass"
            active-class="bg-gradient-to-r from-blue-600/30 to-indigo-600/30 text-white border-l-2 border-blue-400"            @click="handleClick(sub.to, $event)"          >
            <div class="flex items-center">
              <!-- Bullet point -->
              <span class="w-1.5 h-1.5 rounded-full mr-3 transition-all duration-200" 
                    :class="bulletClass"></span>
              <!-- Label -->
              {{ sub.label }}
            </div>
          </router-link>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "SidebarItem",
  props: {
    icon: [Object, Function],
    label: String,
    subItems: Array,
    to: String,
    click: Function
  },
  emits: ['navigate'],
  data() {
    return {
      open: false
    };
  },
  methods: {
    handleClick(path, e) {
      if (this.click) {
        e.preventDefault();
        this.click(path);
      }
      this.$emit('navigate', path);
    }
  },
  computed: {
    // Different background colors based on parent item for variety
    submenuBgClass() {
      const bgClasses = {
        'Exclusive Content Management': 'bg-slate-800 border-slate-600/50',
        'User Management': 'bg-slate-800/90 border-slate-600/50',
        'Financial / Premium Controls': 'bg-slate-800 border-slate-600/50',
        'Communication': 'bg-slate-800 border-slate-600/50'
      };
      
      // Default background if not found
      return bgClasses[this.label] || 'bg-slate-800 border-slate-600/50';
    },
    
    // Different hover effects for submenu items
    submenuItemClass() {
      const hoverClasses = {
        'Exclusive Content Management': 'text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/80 hover:to-indigo-600/80 hover:text-white',
        'User Management': 'text-gray-300 hover:bg-gradient-to-r hover:from-purple-600/80 hover:to-pink-600/80 hover:text-white',
        'Financial / Premium Controls': 'text-gray-300 hover:bg-gradient-to-r hover:from-green-600/80 hover:to-emerald-600/80 hover:text-white',
        'Communication': 'text-gray-300 hover:bg-gradient-to-r hover:from-cyan-600/80 hover:to-sky-600/80 hover:text-white'
      };
      
      return hoverClasses[this.label] || 'text-gray-300 hover:bg-gradient-to-r hover:from-blue-600/80 hover:to-indigo-600/80 hover:text-white';
    },
    
    // Different bullet colors
    bulletClass() {
      const bulletColors = {
        'Exclusive Content Management': 'bg-blue-400',
        'User Management': 'bg-purple-400',
        'Financial / Premium Controls': 'bg-green-400',
        'Communication': 'bg-cyan-400'
      };
      
      return bulletColors[this.label] || 'bg-gray-500';
    }
  }
};
</script>

<style scoped>
/* Dropdown animations - now vertical */
.dropdown-enter-active {
  transition: all 0.2s ease-out;
}

.dropdown-leave-active {
  transition: all 0.15s ease-in;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Custom scrollbar for submenu */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #1e293b;
  border-radius: 0 0 8px 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

/* Firefox scrollbar */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #475569 #1e293b;
}

/* Active item styles */
.router-link-active {
  position: relative;
}

.router-link-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10%;
  height: 80%;
  width: 2px;
  background: linear-gradient(to bottom, #60A5FA, #818CF8);
  border-radius: 0 2px 2px 0;
}

/* Chevron rotation */
.rotate-180 {
  transform: rotate(180deg);
}

/* Pulse animation for active dot */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

.router-link-active .w-1\.5.h-1\.5 {
  animation: pulse 2s ease infinite;
}

/* Smooth hover transitions */
a, div[role="button"] {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Submenu container - different from parent */
.relative.mt-1 {
  position: relative;
  margin-top: 0.25rem;
  width: 100%;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
}

/* Bullet point hover effect */
.router-link:hover .bg-blue-400,
.router-link:hover .bg-purple-400,
.router-link:hover .bg-amber-400,
.router-link:hover .bg-emerald-400,
.router-link:hover .bg-green-400,
.router-link:hover .bg-red-400,
.router-link:hover .bg-cyan-400 {
  background-color: white;
  transform: scale(1.2);
}

/* Custom background classes */
.bg-slate-800 {
  background-color: #1e293b;
}

.bg-slate-800\/90 {
  background-color: rgba(30, 41, 59, 0.9);
}

/* Border colors */
.border-slate-600\/50 {
  border-color: rgba(71, 85, 105, 0.5);
}
</style>