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
            Study Notes
          </h1>
        </div>
        <p class="text-slate-400 text-lg">Comprehensive notes for effective learning</p>
      </div>
    </header>

    <!-- Search Bar -->
    <section class="max-w-3xl mx-auto px-6 mb-8">
      <div class="relative">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search notes by title, subject, or topic..."
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
        <h3 class="text-2xl font-semibold mb-2">Failed to Load Notes</h3>
        <p class="text-slate-400 mb-6">{{ error }}</p>
        <button @click="fetchNotes" class="px-6 py-3 bg-cyan-600 hover:bg-cyan-700 rounded-xl transition">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredNotes.length === 0" class="text-center py-16">

        <div class="w-20 h-20 bg-cyan-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-semibold mb-2">No Notes Available</h3>
        <p class="text-slate-400">Check back later for new study notes</p>
      </div>

      <!-- Notes Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="note in filteredNotes" :key="note.id" 

             class="group bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden border border-white/10 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20">
          
          <!-- Note Preview -->
          <div class="relative h-48 bg-gradient-to-br from-blue-600/20 to-cyan-600/20 overflow-hidden p-6">
            <div class="absolute inset-0 opacity-30">
              <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                  <path d="M 10 0 L 0 0 0 10" fill="none" stroke="currentColor" stroke-width="0.5"/>
                </pattern>
                <rect width="100" height="100" fill="url(#grid)"/>
              </svg>
            </div>
            
            <div class="relative z-10 h-full flex flex-col justify-between">
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                
                <!-- Premium Badge - Hide for teachers -->
                <div v-if="note.is_premium && !isTeacher" class="px-3 py-1 bg-amber-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white flex items-center gap-1">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  PREMIUM
                </div>
              </div>
              
              <div>
                <p class="text-xs text-cyan-400 font-medium mb-1">{{ note.subject }}</p>
                <p class="text-xs text-slate-400">Grade {{ note.grade_level }}</p>
              </div>
            </div>
          </div>

          <!-- Note Info -->
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-2 line-clamp-2 group-hover:text-cyan-400 transition">{{ note.title }}</h3>
            <p class="text-sm text-slate-400 mb-4 line-clamp-2">{{ note.description || 'No description available' }}</p>
            
            <div class="flex items-center justify-between text-xs text-slate-500 mb-4">
              <span class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                </svg>
                {{ formatFileSize(note.file_size) }}
              </span>
              <span class="px-2 py-1 bg-white/10 rounded">{{ note.file_name?.split('.').pop()?.toUpperCase() || 'PDF' }}</span>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <button @click="readNote(note)" 
                      class="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 transition text-white font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
                <span class="text-sm">Read Now</span>
              </button>

              <button @click="downloadNote(note)" 
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

    <!-- Note Reader Modal -->
    <div v-if="activeNote" class="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4" @click.self="closeReader">
      <div class="w-full max-w-4xl h-[90vh] bg-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-white/10 bg-slate-900/50">
          <div>
            <h2 class="text-xl font-bold">{{ activeNote.title }}</h2>
            <p class="text-sm text-slate-400">{{ activeNote.subject }} • Grade {{ activeNote.grade_level }}</p>
          </div>
          <div class="flex items-center gap-2">
            <button @click="downloadNote(activeNote)" 
                    class="p-2 rounded-lg bg-white/5 hover:bg-green-600/20 text-slate-300 hover:text-green-400 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
            </button>
            <button @click="closeReader" 
                    class="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Content -->
        <div class="flex-1 overflow-auto p-6 bg-slate-800">
          <div v-if="noteContent" class="prose prose-invert max-w-none">
            <div v-html="noteContent"></div>
          </div>
          <div v-else class="flex items-center justify-center h-full">
            <div class="text-center">
              <svg class="w-16 h-16 text-slate-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p class="text-slate-400">Loading note content...</p>
            </div>
          </div>
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
        <p class="text-slate-400 text-center mb-6">This note requires a premium subscription to read.</p>
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
const notes = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const activeNote = ref(null);
const noteContent = ref('');
const showPremiumModal = ref(false);
const pendingNote = ref(null);

// Check if user is a teacher - teachers don't see premium badges
const isTeacher = computed(() => {
  return localStorage.getItem('role') === 'teacher';
});

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Filtered notes based on search
const filteredNotes = computed(() => {
  if (!searchQuery.value) return notes.value;
  const query = searchQuery.value.toLowerCase();
  return notes.value.filter(note => 
    note.title.toLowerCase().includes(query) ||
    note.subject.toLowerCase().includes(query) ||
    note.description?.toLowerCase().includes(query)
  );
});

// Fetch notes from database
const fetchNotes = async () => {

  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/resources/`);
    if (!response.ok) {
      throw new Error('Failed to fetch notes');
    }
    const data = await response.json();
    // Filter only notes type resources
    notes.value = data.filter(r => r.type === 'notes' && r.is_active);
  } catch (err) {
    console.error('Error fetching notes:', err);
    error.value = err.message || 'Failed to load notes. Please try again.';
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

// Format file size
const formatFileSize = (bytes) => {
  if (!bytes) return 'Unknown size';
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Read note (check premium access)
const readNote = (note) => {
  if (note.is_premium) {
    // Check if user has premium access
    const hasPremium = localStorage.getItem('has_premium') === 'true';
    if (!hasPremium) {
      pendingNote.value = note;
      showPremiumModal.value = true;
      return;
    }
  }
  
  activeNote.value = note;
  // In a real app, you would fetch and parse the note content here
  // For now, we'll show a placeholder
  noteContent.value = `
    <div class="space-y-4">
      <p class="text-lg leading-relaxed">This is a preview of the note content. In a production environment, this would display the actual note content parsed from the file.</p>
      <div class="bg-slate-700/50 p-4 rounded-lg">
        <h4 class="font-semibold mb-2">Key Points:</h4>
        <ul class="list-disc list-inside space-y-1 text-slate-300">
          <li>Important concept explained clearly</li>
          <li>Step-by-step breakdown of the topic</li>
          <li>Examples and practice problems included</li>
          <li>Summary at the end for quick revision</li>
        </ul>
      </div>
      <p class="text-slate-400 italic">Note: Full content would be loaded from: ${note.file_path}</p>
    </div>
  `;
};

// Close reader
const closeReader = () => {
  activeNote.value = null;
  noteContent.value = '';
};

// Download note
const downloadNote = (note) => {
  const link = document.createElement('a');
  link.href = getFileUrl(note.file_path);
  link.download = note.file_name || `${note.title}.pdf`;
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

// Fetch notes on mount
onMounted(() => {
  fetchNotes();
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prose {
  color: #e2e8f0;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
  color: #fff;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.prose p {
  margin-bottom: 1em;
  line-height: 1.75;
}

.prose ul {
  list-style-type: disc;
  padding-left: 1.5em;
}

.prose li {
  margin-bottom: 0.5em;
}
</style>
