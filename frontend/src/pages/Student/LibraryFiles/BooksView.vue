<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
    
    <!-- EduSkill Header -->
    <EduskillHeader />

    <!-- Search Bar -->
    <section class="max-w-3xl mx-auto px-6 mb-8">
      <div class="relative">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search books by title, author, or subject..."
          class="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-2xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500/50 focus:bg-white/10 transition"
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
          <div class="h-56 bg-slate-700"></div>
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
        <h3 class="text-2xl font-semibold mb-2">Failed to Load Books</h3>
        <p class="text-slate-400 mb-6">{{ error }}</p>
        <button @click="fetchBooks" class="px-6 py-3 bg-amber-600 hover:bg-amber-700 rounded-xl transition">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredBooks.length === 0" class="text-center py-16">
        <div class="w-20 h-20 bg-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-10 h-10 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <h3 class="text-2xl font-semibold mb-2">No Books Found</h3>
        <p class="text-slate-400">{{ searchQuery ? 'Try a different search term' : 'Check back later for new books' }}</p>
      </div>

      <!-- Books Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="book in filteredBooks" :key="book.id" 
             class="group bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden border border-white/10 hover:border-amber-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-500/20">
          
          <!-- Book Cover -->
          <div class="relative h-56 bg-gradient-to-br from-amber-600/20 to-orange-600/20 overflow-hidden">
            <!-- Book Cover Design -->
            <div class="absolute inset-0 flex items-center justify-center p-8">
              <div class="w-32 h-44 bg-gradient-to-br from-amber-700 to-amber-900 rounded-r-lg shadow-2xl transform group-hover:scale-105 transition-transform duration-300 flex flex-col items-center justify-center p-4 text-center border-l-4 border-amber-500">
                <svg class="w-12 h-12 text-amber-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
                <p class="text-xs text-amber-300 font-medium line-clamp-2">{{ book.subject }}</p>
              </div>
            </div>
            
            <!-- Premium Badge -->
            <div v-if="book.is_premium && !isTeacher" class="absolute top-3 right-3 px-3 py-1 bg-amber-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white flex items-center gap-1">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              PREMIUM
            </div>

            <!-- Price Tag -->
            <div v-if="book.price > 0 && !book.is_premium" class="absolute top-3 left-3 px-3 py-1 bg-green-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
              ${{ book.price }}
            </div>
          </div>

          <!-- Book Info -->
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-2 line-clamp-2 group-hover:text-amber-400 transition">{{ book.title }}</h3>
            <p class="text-sm text-slate-400 mb-3 line-clamp-2">{{ book.description || 'No description available' }}</p>
            
            <div class="flex items-center justify-between text-xs text-slate-500 mb-4">
              <span class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                </svg>
                {{ formatFileSize(book.file_size) }}
              </span>
              <span class="px-2 py-1 bg-white/10 rounded">{{ book.file_name?.split('.').pop()?.toUpperCase() || 'PDF' }}</span>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <button @click="readBook(book)" 
                      class="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 transition text-white font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
                <span class="text-sm">Read Now</span>
              </button>

              <button @click="downloadBook(book)" 
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

    <!-- Book Reader Modal -->
    <div v-if="activeBook" class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-sm p-4" @click.self="closeReader">
      <div class="w-full max-w-4xl h-[90vh] bg-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-white/10 bg-slate-900/50">
          <div class="flex items-center gap-4">
            <div class="w-12 h-16 bg-gradient-to-br from-amber-700 to-amber-900 rounded-r border-l-2 border-amber-500 flex items-center justify-center">
              <svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-bold">{{ activeBook.title }}</h2>
              <p class="text-sm text-slate-400">{{ activeBook.subject }} • Grade {{ activeBook.grade_level }}</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button @click="downloadBook(activeBook)" 
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
        
        <!-- Book Content -->
        <div class="flex-1 overflow-auto p-8 bg-slate-800">
          <div class="max-w-2xl mx-auto bg-white text-slate-900 rounded-lg shadow-2xl p-8 min-h-[60vh]">
            <div class="text-center mb-8">
              <h1 class="text-3xl font-bold mb-2">{{ activeBook.title }}</h1>
              <p class="text-slate-600">{{ activeBook.subject }} Textbook</p>
              <div class="w-24 h-1 bg-amber-500 mx-auto mt-4"></div>
            </div>
            
            <div class="prose prose-slate max-w-none">
              <p class="text-lg leading-relaxed mb-4">This is a preview of the book content. In a production environment, this would display the actual PDF or e-book content with full navigation, search, and annotation features.</p>
              
              <h3 class="text-xl font-semibold mt-6 mb-3">Table of Contents</h3>
              <ul class="space-y-2 text-slate-700">
                <li class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center text-sm font-medium">1</span>
                  <span>Introduction to {{ activeBook.subject }}</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center text-sm font-medium">2</span>
                  <span>Core Concepts and Principles</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center text-sm font-medium">3</span>
                  <span>Advanced Topics</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center text-sm font-medium">4</span>
                  <span>Practice Problems</span>
                </li>
                <li class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center text-sm font-medium">5</span>
                  <span>Summary and Review</span>
                </li>
              </ul>
              
              <div class="mt-8 p-4 bg-amber-50 rounded-lg border border-amber-200">
                <p class="text-sm text-amber-800 italic">Full book content would be loaded from: {{ activeBook.file_path }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Navigation -->
        <div class="p-4 border-t border-white/10 bg-slate-900/50 flex items-center justify-between">
          <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition text-slate-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Previous Chapter
          </button>
          <span class="text-slate-400">Page 1 of 250</span>
          <button class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition text-slate-400">
            Next Chapter
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
        <h3 class="text-2xl font-bold text-center mb-2">Premium Book</h3>
        <p class="text-slate-400 text-center mb-6">This book requires a premium subscription to read.</p>
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
import EduskillHeader from '@/components/Header/EduskillHeader.vue';

const router = useRouter();
const books = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const activeBook = ref(null);
const showPremiumModal = ref(false);
const pendingBook = ref(null);

// Check if user is a teacher - teachers don't see premium badges
const isTeacher = computed(() => {
  return localStorage.getItem('role') === 'teacher';
});

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Fetch books from database
const fetchBooks = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/resources/`);
    if (!response.ok) {
      throw new Error('Failed to fetch books');
    }
    const data = await response.json();
    // Filter only books type resources
    books.value = data.filter(r => r.type === 'books' && r.is_active);
  } catch (err) {
    console.error('Error fetching books:', err);
    error.value = err.message || 'Failed to load books. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Filtered books based on search
const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value;
  const query = searchQuery.value.toLowerCase();
  return books.value.filter(book => 
    book.title.toLowerCase().includes(query) ||
    book.subject.toLowerCase().includes(query) ||
    book.description?.toLowerCase().includes(query)
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

// Read book (check premium access)
const readBook = (book) => {
  if (book.is_premium) {
    const hasPremium = localStorage.getItem('has_premium') === 'true';
    if (!hasPremium) {
      pendingBook.value = book;
      showPremiumModal.value = true;
      return;
    }
  }
  activeBook.value = book;
};

// Close reader
const closeReader = () => {
  activeBook.value = null;
};

// Download book
const downloadBook = (book) => {
  const link = document.createElement('a');
  link.href = getFileUrl(book.file_path);
  link.download = book.file_name || `${book.title}.pdf`;
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

// Fetch books on mount
onMounted(() => {
  fetchBooks();
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
