<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
    
    <!-- Header -->
    <header class="pt-24 pb-8 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center gap-4 mb-4">
          <button 
            @click="$router.push('/library')"
            class="p-2 rounded-xl bg-white/10 hover:bg-white/20 transition backdrop-blur-sm">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
          </button>
          <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
            Presentation Slides
          </h1>
        </div>
        <p class="text-slate-400 text-lg">Visual learning materials and diagrams</p>
      </div>
    </header>

    <!-- Search Bar -->
    <section class="max-w-3xl mx-auto px-6 mb-8">
      <div class="relative">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search slides by title, subject, or topic..."
          class="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/50 focus:bg-white/10 transition"
        />
        <svg class="absolute right-4 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
      </div>
    </section>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 pb-16">
      
      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden animate-pulse">
          <div class="h-48 bg-slate-700"></div>
          <div class="p-4 space-y-3">
            <div class="h-6 bg-slate-700 rounded w-3/4"></div>
            <div class="h-4 bg-slate-700 rounded w-1/2"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-16">
        <div class="w-20 h-20 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-semibold mb-2">Failed to Load Slides</h3>
        <p class="text-slate-400 mb-6">{{ error }}</p>
        <button @click="fetchSlides" class="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-xl transition">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredSlides.length === 0" class="text-center py-16">
        <div class="w-20 h-20 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-semibold mb-2">No Slides Found</h3>
        <p class="text-slate-400">{{ searchQuery ? 'Try a different search term' : 'Check back later for new presentations' }}</p>
      </div>

      <!-- Slides Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="slide in filteredSlides" :key="slide.id" 
             class="group bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden border border-white/10 hover:border-purple-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20">
          
          <!-- Slide Preview -->
          <div class="relative h-48 bg-gradient-to-br from-purple-600/20 to-pink-600/20 overflow-hidden p-6">
            <div class="absolute inset-0 opacity-20">
              <div class="grid grid-cols-2 gap-2 p-4">
                <div v-for="i in 4" :key="i" class="bg-white/20 rounded h-16"></div>
              </div>
            </div>
            
            <div class="relative z-10 h-full flex flex-col justify-between">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
                  </svg>
                </div>
                
                <!-- Premium Badge - Hide for teachers -->
                <div v-if="slide.is_premium && !isTeacher" class="px-3 py-1 bg-amber-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white flex items-center gap-1">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  PREMIUM
                </div>
              </div>
              
              <div>
                <p class="text-xs text-purple-400 font-medium mb-1">{{ slide.subject }}</p>
                <p class="text-xs text-slate-400">Grade {{ slide.grade_level }}</p>
              </div>
            </div>
          </div>

          <!-- Slide Info -->
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-2 line-clamp-2 group-hover:text-purple-400 transition">{{ slide.title }}</h3>
            <p class="text-sm text-slate-400 mb-4 line-clamp-2">{{ slide.description || 'No description available' }}</p>
            
            <div class="flex items-center justify-between text-xs text-slate-500 mb-4">
              <span class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                </svg>
                {{ formatFileSize(slide.file_size) }}
              </span>
              <span class="px-2 py-1 bg-white/10 rounded">{{ slide.file_name?.split('.').pop()?.toUpperCase() || 'PPT' }}</span>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <button @click="viewSlide(slide)" 
                      class="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 transition text-white font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <span class="text-sm">View Slides</span>
              </button>

              <button @click="downloadSlide(slide)" 
                      class="flex items-center justify-center gap-2 py-2 px-3 rounded-lg bg-white/5 hover:bg-green-600/20 text-slate-300 hover:text-green-400 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Slide Viewer Modal -->
    <div v-if="activeSlide" class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-sm p-4" @click.self="closeViewer">
      <div class="w-full max-w-5xl h-[90vh] bg-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-white/10 bg-slate-900/50">
          <div>
            <h2 class="text-xl font-bold">{{ activeSlide.title }}</h2>
            <p class="text-sm text-slate-400">{{ activeSlide.subject }} • Grade {{ activeSlide.grade_level }}</p>
          </div>
          <div class="flex items-center gap-2">
            <button @click="downloadSlide(activeSlide)" 
                    class="p-2 rounded-lg bg-white/5 hover:bg-green-600/20 text-slate-300 hover:text-green-400 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
            </button>
            <button @click="closeViewer" 
                    class="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Slide Content -->
        <div class="flex-1 overflow-auto p-8 bg-slate-800 flex items-center justify-center">
          <div class="bg-white rounded-lg shadow-2xl p-8 max-w-3xl w-full aspect-video flex items-center justify-center">
            <div class="text-center text-slate-800">
              <svg class="w-20 h-20 mx-auto mb-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
              </svg>
              <h3 class="text-2xl font-bold mb-2">Slide Presentation</h3>
              <p class="text-slate-600 mb-4">This would display the actual slide content</p>
              <p class="text-sm text-slate-500">File: {{ activeSlide.file_name }}</p>
              <button @click="downloadSlide(activeSlide)" class="mt-4 px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition">
                Download to View
              </button>
            </div>
          </div>
        </div>
        
        <!-- Navigation -->
        <div class="p-4 border-t border-white/10 bg-slate-900/50 flex items-center justify-between">
          <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition text-slate-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Previous
          </button>
          <span class="text-slate-400">Slide 1 of 10</span>
          <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition text-slate-400">
            Next
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Premium Modal -->
    <div v-if="showPremiumModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-slate-800 rounded-2xl p-8 max-w-md w-full border border-amber-500/30 shadow-2xl shadow-amber-500/20">
        <div class="w-16 h-16 bg-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-center mb-2">Premium Content</h3>
        <p class="text-slate-400 text-center mb-6">This presentation requires a premium subscription to view.</p>
        <div class="space-y-3">
          <button @click="goToPremium" class="w-full py-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 rounded-xl font-semibold transition">
            Upgrade to Premium
          </button>
          <button @click="showPremiumModal = false" class="w-full py-3 bg-white/5 hover:bg-white/10 rounded-xl transition">
            Maybe Later
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const slides = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const activeSlide = ref(null);
const showPremiumModal = ref(false);
const pendingSlide = ref(null);

// Check if user is a teacher - teachers don't see premium badges
const isTeacher = computed(() => {
  return localStorage.getItem('role') === 'teacher';
});

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Fetch slides from database
const fetchSlides = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/resources/`);
    if (!response.ok) {
      throw new Error('Failed to fetch slides');
    }
    const data = await response.json();
    // Filter only slides type resources
    slides.value = data.filter(r => r.type === 'slides' && r.is_active);
  } catch (err) {
    console.error('Error fetching slides:', err);
    error.value = err.message || 'Failed to load slides. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Filtered slides based on search
const filteredSlides = computed(() => {
  if (!searchQuery.value) return slides.value;
  const query = searchQuery.value.toLowerCase();
  return slides.value.filter(slide => 
    slide.title.toLowerCase().includes(query) ||
    slide.subject.toLowerCase().includes(query) ||
    slide.description?.toLowerCase().includes(query)
  );
});

// Get full file URL
const getFileUrl = (filePath) => {
  if (!filePath) return '';
  if (filePath.startsWith('http')) return filePath;
  return `${API_BASE_URL}/${filePath}`;
};

// Format file size
const formatFileSize = (bytes) => {
  if (!bytes) return 'Unknown size';
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// View slide (check premium access)
const viewSlide = (slide) => {
  if (slide.is_premium) {
    const hasPremium = localStorage.getItem('has_premium') === 'true';
    if (!hasPremium) {
      pendingSlide.value = slide;
      showPremiumModal.value = true;
      return;
    }
  }
  activeSlide.value = slide;
};

// Close viewer
const closeViewer = () => {
  activeSlide.value = null;
};

// Download slide
const downloadSlide = (slide) => {
  const link = document.createElement('a');
  link.href = getFileUrl(slide.file_path);
  link.download = slide.file_name || `${slide.title}.pptx`;
  link.target = '_blank';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Go to premium page
const goToPremium = () => {
  showPremiumModal.value = false;
  router.push('/premium');
};

// Fetch slides on mount
onMounted(() => {
  fetchSlides();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
