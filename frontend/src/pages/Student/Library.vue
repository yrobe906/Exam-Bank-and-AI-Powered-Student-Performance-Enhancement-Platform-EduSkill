<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-slate-100 text-slate-900">

    <!-- Animated Background Elements - Light version -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-indigo-100 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-purple-100 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-50 rounded-full blur-3xl"></div>
    </div>

    <!-- EduSkill Header -->
    <EduskillHeader />

    <!-- Global Search -->
    <section class="relative max-w-3xl mx-auto px-6 mb-12">
      <div class="relative group">
        <input 
          v-model="globalSearch"
          type="text" 
          placeholder="Search across all resources..."
          class="w-full px-6 py-4 pl-14 bg-white border border-slate-200 rounded-2xl text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition shadow-sm"
        />
        <svg class="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-400 group-focus-within:text-indigo-500 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <div class="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-2">
          <span class="text-xs text-slate-400 px-2 py-1 bg-slate-100 rounded">⌘K</span>
        </div>
      </div>
    </section>

    <!-- Featured Section -->
    <section v-if="!isLoading && !error && featuredResource" class="relative max-w-7xl mx-auto px-6 mb-16">
      <h2 class="text-2xl font-bold mb-6 flex items-center gap-2 text-slate-800">
        <svg class="w-6 h-6 text-amber-500 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
        Featured Resource
      </h2>
      <div class="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-center gap-6 hover:border-amber-300 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer shadow-sm" @click="goToFeatured">
        <div class="w-24 h-24 bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <div class="flex-1 text-center md:text-left">
          <h3 class="text-2xl font-bold text-slate-800 mb-2">{{ featuredResource.title }}</h3>
          <p class="text-slate-600 mb-4">{{ featuredResource.description }}</p>
          <div class="flex items-center justify-center md:justify-start gap-4 text-sm">
            <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full">{{ featuredResource.subject }}</span>
            <span class="text-slate-500">Grade {{ featuredResource.grade_level }}</span>
            <span v-if="featuredResource.is_premium" class="px-3 py-1 bg-amber-500 text-white rounded-full text-xs font-semibold">PREMIUM</span>
          </div>
        </div>
        <button class="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-semibold transition-all duration-300 hover:scale-105 hover:shadow-lg">
          View Now
        </button>
      </div>
    </section>

    <!-- Library Grid -->
    <section class="relative max-w-7xl mx-auto px-6 pb-16">
      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="i in 4" :key="i"
             class="bg-white rounded-2xl p-6 border border-slate-200 animate-pulse shadow-sm">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-20 h-20 bg-slate-200 rounded-xl"></div>
            <div>
              <div class="h-6 bg-slate-200 rounded mb-2 w-24"></div>
              <div class="h-4 bg-slate-200 rounded w-16"></div>
            </div>
          </div>
          <div class="h-4 bg-slate-200 rounded mb-2"></div>
          <div class="h-4 bg-slate-200 rounded w-3/4"></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-16">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
          <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-slate-800 mb-2">Failed to Load Resources</h3>
        <p class="text-slate-500 mb-4">{{ error }}</p>
        <button @click="fetchResources" class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all duration-300 hover:scale-105">
          Try Again
        </button>
      </div>

      <!-- Library Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="item in libraryItems" :key="item.id"
             @click="goExplore(item.route)"
             class="group bg-white rounded-2xl p-6 cursor-pointer
                    border border-slate-200 hover:border-indigo-300
                    transition-all duration-500 hover:-translate-y-2 hover:shadow-xl shadow-sm">

          <div class="flex items-center gap-4 mb-6">
            <div :class="[item.color, 'w-20 h-20 rounded-xl flex items-center justify-center text-white shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300']">
              <component :is="item.icon" class="w-10 h-10" />
            </div>
            <div>
              <h3 class="text-xl font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">{{ item.title }}</h3>
              <p class="text-sm text-slate-500">{{ item.count }} resources</p>
            </div>
          </div>

          <p class="text-slate-600 mb-6 group-hover:text-slate-700">{{ item.description }}</p>

          <div class="flex items-center justify-between">
            <span class="text-indigo-600 font-medium group-hover:text-indigo-500 group-hover:translate-x-1 transition-all">Explore</span>
            <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center group-hover:bg-indigo-100 group-hover:scale-110 transition-all duration-300">
              <ArrowRightIcon class="w-5 h-5 text-slate-500 group-hover:text-indigo-600 group-hover:translate-x-0.5 transition-all" />
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import EduskillHeader from "@/components/Header/EduskillHeader.vue";
import { 
  BookOpenIcon, PresentationChartBarIcon, VideoCameraIcon, 
  AcademicCapIcon, SparklesIcon, ArrowRightIcon 
} from "@heroicons/vue/24/solid";

const router = useRouter();
const currentTip = ref(0);
const isLoading = ref(true);
const error = ref(null);
const resources = ref([]);
const globalSearch = ref('');

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const aiTips = [
  "Start with notes before videos for better understanding.",
  "Use slides to visualize complex concepts effectively.",
  "Daily revision with summaries boosts retention.",
  "Watch short videos for difficult topics.",
  "Teach others to master any subject completely."
];

// Store library counts from API
const libraryCounts = ref(null);

// Fetch resources from database
const fetchResources = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/notes/library-counts`);
    if (!response.ok) {
      throw new Error('Failed to fetch library counts');
    }
    const data = await response.json();
    // Store the counts in a format compatible with the existing code
    resources.value = [];
    
    // Create resource-like objects from the counts for compatibility
    if (data.notes_count > 0) {
      for (let i = 0; i < data.notes_count; i++) {
        resources.value.push({ type: 'notes', is_active: true, is_premium: false });
      }
    }
    if (data.slides_count > 0) {
      for (let i = 0; i < data.slides_count; i++) {
        resources.value.push({ type: 'slides', is_active: true, is_premium: false });
      }
    }
    if (data.videos_count > 0) {
      for (let i = 0; i < data.videos_count; i++) {
        resources.value.push({ type: 'videos', is_active: true, is_premium: false });
      }
    }
    if (data.books_count > 0) {
      for (let i = 0; i < data.books_count; i++) {
        resources.value.push({ type: 'books', is_active: true, is_premium: false });
      }
    }
    
    // Store the actual counts for the cards
    libraryCounts.value = data;
  } catch (err) {
    console.error('Error fetching resources:', err);
    error.value = err.message || 'Failed to load resources. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Compute library items with real counts from database
const libraryItems = computed(() => {
  const counts = {
    notes: resources.value.filter(r => r.type === 'notes' && r.is_active).length,
    slides: resources.value.filter(r => r.type === 'slides' && r.is_active).length,
    videos: resources.value.filter(r => r.type === 'videos' && r.is_active).length,
    books: resources.value.filter(r => r.type === 'books' && r.is_active).length,
  };

  return [
    { 
      id: 1, 
      title: "Study Notes", 
      description: "Exam-focused notes with key highlights and summaries.", 
      icon: BookOpenIcon, 
      color: "bg-gradient-to-br from-blue-500 to-cyan-500", 
      count: counts.notes > 0 ? counts.notes : "Coming soon", 
      route: "notes" 
    },
    { 
      id: 2, 
      title: "Reference Books & Slides", 
      description: "Visual presentations and diagrams for better understanding.", 
      icon: PresentationChartBarIcon, 
      color: "bg-gradient-to-br from-purple-500 to-pink-500", 
      count: counts.slides > 0 ? counts.slides : "Coming soon", 
      route: "slides" 
    },
    { 
      id: 3, 
      title: "Video Lessons", 
      description: "Short engaging video explanations by expert teachers.", 
      icon: VideoCameraIcon, 
      color: "bg-gradient-to-br from-pink-500 to-rose-500", 
      count: counts.videos > 0 ? counts.videos : "Coming soon", 
      route: "videos" 
    },
    { 
      id: 4, 
      title: "Exam Papers and Worksheets", 
      description: "Comprehensive textbooks and reference materials.", 
      icon: AcademicCapIcon, 
      color: "bg-gradient-to-br from-amber-500 to-orange-500", 
      count: counts.books > 0 ? counts.books : "Coming soon", 
      route: "books" 
    },
  ];
});

// Stats computed properties
const totalResources = computed(() => resources.value.filter(r => r.is_active).length);
const freeResources = computed(() => resources.value.filter(r => r.is_active && !r.is_premium).length);
const premiumResources = computed(() => resources.value.filter(r => r.is_active && r.is_premium).length);

// Featured resource (first premium or first active)
const featuredResource = computed(() => {
  const premium = resources.value.find(r => r.is_active && r.is_premium);
  return premium || resources.value.find(r => r.is_active);
});

const goExplore = (route) => router.push(`/library/${route}`);
const cycleTip = () => currentTip.value = (currentTip.value + 1) % aiTips.length;

const goToFeatured = () => {
  if (featuredResource.value) {
    const type = featuredResource.value.type;
    router.push(`/library/${type}`);
  }
};

// Keyboard shortcut for search
onMounted(() => {
  fetchResources();
  
  const handleKeydown = (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      document.querySelector('input[type="text"]')?.focus();
    }
  };
  window.addEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 8s ease infinite;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Interactive hover effects */
.group:hover {
  transform: translateY(-8px);
}

/* Smooth transitions for all interactive elements */
*, .group, button, a {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Pulse animation for featured star */
@keyframes softPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.animate-pulse {
  animation: softPulse 2s ease-in-out infinite;
}
</style>