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
          <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            Video Lessons
          </h1>
        </div>
        <p class="text-slate-400 text-lg">Learn through engaging video content</p>
      </div>
    </header>

    <!-- Search Bar -->
    <section class="max-w-3xl mx-auto px-6 mb-8">
      <div class="relative">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search videos by title, subject, or topic..."
          class="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 focus:bg-white/10 transition"
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
          <div class="aspect-video bg-slate-700"></div>
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
        <h3 class="text-2xl font-semibold mb-2">Failed to Load Videos</h3>
        <p class="text-slate-400 mb-6">{{ error }}</p>
        <button @click="fetchVideos" class="px-6 py-3 bg-cyan-600 hover:bg-cyan-700 rounded-xl transition">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredVideos.length === 0" class="text-center py-16">
        <div class="w-20 h-20 bg-cyan-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-semibold mb-2">No Videos Available</h3>
        <p class="text-slate-400">Check back later for new video content</p>
      </div>

      <!-- Videos Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="video in filteredVideos" :key="video.id" 
             class="group bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden border border-white/10 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20">
          
          <!-- Video Thumbnail / Player -->
          <div class="relative aspect-video bg-slate-800 overflow-hidden">
            <!-- Thumbnail View -->
            <div v-if="currentPlayingVideoId !== video.id" class="absolute inset-0 cursor-pointer" @click="playVideo(video)">
              <img v-if="video.preview_path" :src="getFileUrl(video.preview_path)" 
                   class="w-full h-full object-cover" :alt="video.title">
              <div v-else class="w-full h-full bg-gradient-to-br from-cyan-600/20 to-purple-600/20 flex items-center justify-center">
                <svg class="w-16 h-16 text-cyan-400/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
              </div>
              
              <!-- Play Button Overlay -->
              <div class="absolute inset-0 bg-black/40 group-hover:bg-black/30 transition-all duration-300 flex items-center justify-center">
                <div class="w-20 h-20 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 rounded-full flex items-center justify-center transform group-hover:scale-110 transition-all duration-300 shadow-xl shadow-cyan-500/50">
                  <svg class="w-10 h-10 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </div>
              </div>

              <!-- Premium Badge -->
              <div v-if="video.is_premium && !isTeacher" class="absolute top-3 right-3 px-3 py-1 bg-amber-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white flex items-center gap-1 z-10">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                PREMIUM
              </div>
            </div>

            <!-- Video Player View -->
            <div v-else class="absolute inset-0">
              <video 
                :ref="el => { if (el && currentPlayingVideoId === video.id) videoPlayerRefs[video.id] = el }"
                class="w-full h-full"
                controls
                autoplay
                @ended="stopVideo(video.id)">
                <source :src="getFileUrl(video.file_path)" type="video/mp4">
                <track v-if="video.subtitle_path" kind="subtitles" :src="getFileUrl(video.subtitle_path)" label="English" default>
                Your browser does not support the video tag.
              </video>
            </div>
          </div>

          <!-- Video Info -->
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-1 line-clamp-2 group-hover:text-cyan-400 transition">{{ video.title }}</h3>
            <p class="text-sm text-slate-400 mb-3 line-clamp-2">{{ video.description || 'No description available' }}</p>
            
            <div class="flex items-center justify-between text-xs text-slate-500 mb-3">
              <span class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                {{ formatDuration(video.duration) }}
              </span>
              <span class="px-2 py-1 bg-white/10 rounded">{{ video.subject }}</span>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2 pt-3 border-t border-white/10">
              <button @click="likeVideo(video)" 
                      :class="['flex-1 flex items-center justify-center gap-2 py-2 rounded-lg transition', video.userLiked ? 'bg-blue-600 text-white' : 'bg-white/5 hover:bg-white/10 text-slate-300']">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"/>
                </svg>
                <span class="text-sm">{{ video.likes || 0 }}</span>
              </button>

              <button @click="dislikeVideo(video)" 
                      :class="['flex-1 flex items-center justify-center gap-2 py-2 rounded-lg transition', video.userDisliked ? 'bg-red-600 text-white' : 'bg-white/5 hover:bg-white/10 text-slate-300']">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z"/>
                </svg>
                <span class="text-sm">{{ video.dislikes || 0 }}</span>
              </button>

              <button @click="downloadVideo(video)" 
                      class="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-white/5 hover:bg-green-600/20 text-slate-300 hover:text-green-400 transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                <span class="text-sm">Download</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Premium Modal -->
    <div v-if="showPremiumModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="showPremiumModal = false">
      <div class="bg-slate-800 rounded-2xl p-8 max-w-md w-full border border-amber-500/30 shadow-2xl shadow-amber-500/20">
        <div class="w-16 h-16 bg-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-center mb-2">Premium Content</h3>
        <p class="text-slate-400 text-center mb-6">This video requires a premium subscription to watch.</p>
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
import { ref, onMounted, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const videos = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const showPremiumModal = ref(false);
const selectedVideo = ref(null);
const currentPlayingVideoId = ref(null);
const videoPlayerRefs = ref({});

// Check if user is a teacher
const isTeacher = computed(() => {
  return localStorage.getItem('role') === 'teacher';
});

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Filtered videos based on search
const filteredVideos = computed(() => {
  if (!searchQuery.value) return videos.value;
  const query = searchQuery.value.toLowerCase();
  return videos.value.filter(video => 
    video.title.toLowerCase().includes(query) ||
    video.subject?.toLowerCase().includes(query) ||
    video.description?.toLowerCase().includes(query)
  );
});

// Fetch videos from database
const fetchVideos = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/resources/`);
    if (!response.ok) {
      throw new Error('Failed to fetch videos');
    }
    const data = await response.json();
    videos.value = data
      .filter(r => r.type === 'videos' && r.is_active)
      .map(v => ({
        ...v,
        isPlaying: false,
        userLiked: false,
        userDisliked: false,
        likes: Math.floor(Math.random() * 100),
        dislikes: Math.floor(Math.random() * 10),
      }));
  } catch (err) {
    console.error('Error fetching videos:', err);
    error.value = err.message || 'Failed to load videos. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Get full file URL
const getFileUrl = (filePath) => {
  if (!filePath) return '';
  if (filePath.startsWith('http')) return filePath;
  return `${API_BASE_URL}/${filePath}`;
};

// Format duration
const formatDuration = (duration) => {
  if (!duration) return '10:00';
  const minutes = Math.floor(duration / 60);
  const seconds = duration % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

// Play video
const playVideo = async (video) => {
  // Check premium access
  if (video.is_premium) {
    const hasPremium = localStorage.getItem('has_premium') === 'true';
    if (!hasPremium) {
      selectedVideo.value = video;
      showPremiumModal.value = true;
      return;
    }
  }
  
  // Stop any currently playing video
  if (currentPlayingVideoId.value) {
    const currentPlayer = videoPlayerRefs.value[currentPlayingVideoId.value];
    if (currentPlayer) {
      currentPlayer.pause();
    }
  }
  
  // Set current playing video
  currentPlayingVideoId.value = video.id;
  
  // Wait for DOM update and play
  await nextTick();
  const player = videoPlayerRefs.value[video.id];
  if (player) {
    player.play().catch(error => {
      console.error('Error playing video:', error);
    });
  }
};

// Stop video
const stopVideo = (videoId) => {
  if (currentPlayingVideoId.value === videoId) {
    currentPlayingVideoId.value = null;
  }
};

// Like video
const likeVideo = (video) => {
  if (video.userDisliked) {
    video.userDisliked = false;
    video.dislikes--;
  }
  if (!video.userLiked) {
    video.userLiked = true;
    video.likes++;
  } else {
    video.userLiked = false;
    video.likes--;
  }
};

// Dislike video
const dislikeVideo = (video) => {
  if (video.userLiked) {
    video.userLiked = false;
    video.likes--;
  }
  if (!video.userDisliked) {
    video.userDisliked = true;
    video.dislikes++;
  } else {
    video.userDisliked = false;
    video.dislikes--;
  }
};

// Download video
const downloadVideo = (video) => {
  const link = document.createElement('a');
  link.href = getFileUrl(video.file_path);
  link.download = video.file_name || `${video.title}.mp4`;
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

// Fetch videos on mount
onMounted(() => {
  fetchVideos();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

video {
  outline: none;
}

video::-webkit-media-controls {
  cursor: pointer;
}
</style>