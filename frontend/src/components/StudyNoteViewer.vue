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
             class="group bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden border border-white/10 hover:border-cyan-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20 hover:scale-105">
          <!-- Note Preview -->
          <div class="relative h-48 overflow-hidden p-6" :class="getThemeGradient(note.theme_color)">
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

                <!-- Premium Badge -->
                <div v-if="note.access_type === 'premium'" class="px-3 py-1 bg-amber-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white flex items-center gap-1">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  {{ note.price }} Birr
                </div>
                <div v-else class="px-3 py-1 bg-teal-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
                  Free
                </div>
              </div>

              <div>
                <p class="text-xs text-cyan-400 font-medium mb-1">{{ note.subject }}</p>
                <p class="text-xs text-slate-400">{{ note.category }}</p>
              </div>
            </div>
          </div>

          <!-- Note Info -->
          <div class="p-4">
            <h3 class="text-lg font-semibold mb-2 line-clamp-2 group-hover:text-cyan-400 transition">{{ note.title }}</h3>
            <p class="text-sm text-slate-400 mb-4 line-clamp-2">{{ note.content.substring(0, 100) }}...</p>

            <!-- Action Button -->
            <button @click="openNote(note)"
                    class="w-full flex items-center justify-center gap-2 py-2 rounded-lg transition text-white font-medium"
                    :class="note.access_type === 'free' ? 'bg-teal-600 hover:bg-teal-500' : 'bg-amber-600 hover:bg-amber-500'">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
              <span class="text-sm">{{ note.access_type === 'free' ? 'Read Now' : 'Subscribe to Access' }}</span>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Reading Modal -->
    <div v-if="activeNote" class="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4" @click.self="closeReader">
      <div class="w-full max-w-4xl h-[90vh] bg-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-white/10" :class="getThemeGradient(activeNote.theme_color)">
          <div>
            <h2 class="text-xl font-bold">{{ activeNote.title }}</h2>
            <div class="flex items-center gap-2 mt-1">
              <span class="px-2 py-1 bg-white/20 rounded-full text-xs">{{ activeNote.subject }}</span>
              <span class="px-2 py-1 bg-white/20 rounded-full text-xs">{{ activeNote.category }}</span>
              <span v-if="activeNote.access_type === 'premium'" class="px-2 py-1 bg-amber-500/20 rounded-full text-xs text-amber-300">Premium</span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-sm text-slate-400">Page {{ currentPage + 1 }} of {{ totalPages }}</span>
            <button @click="closeReader"
                    class="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-auto p-6" :class="getThemeBg(activeNote.theme_color)">
          <div v-if="activeNote.access_type === 'premium' && !isSubscribed" class="relative">
            <div class="blur-sm pointer-events-none">
              <div class="max-w-3xl mx-auto space-y-4">
                <div v-for="(item, index) in paginatedContent" :key="index" 
                     :class="getContentItemClass(item.type)">
                  <div v-if="item.type === 'formula'" class="formula-box">
                    <span class="font-mono text-lg">{{ item.content }}</span>
                  </div>
                  <div v-else-if="item.type === 'number'" class="number-highlight">
                    <span class="font-bold text-xl">{{ item.content }}</span>
                  </div>
                  <div v-else-if="item.type === 'list'" class="list-item">
                    <span class="bullet">•</span>
                    <span>{{ item.content }}</span>
                  </div>
                  <div v-else class="sentence-text">
                    {{ item.content }}
                  </div>
                </div>
              </div>
            </div>
            <!-- Premium Overlay -->
            <div class="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm rounded-lg">
              <div class="text-center p-8 bg-slate-800/90 rounded-2xl border border-amber-500/30">
                <div class="w-16 h-16 bg-amber-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg class="w-8 h-8 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </div>
                <h3 class="text-2xl font-bold mb-2">Premium Content</h3>
                <p class="text-slate-400 mb-6">Subscribe to access this note for {{ activeNote.price }} Birr</p>
<button @click="$router.push('/premium')" class="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 rounded-xl font-semibold transition">
                  Subscribe Now
                </button>
              </div>
            </div>
          </div>
          
          <!-- Structured Content Display -->
          <div v-else class="max-w-3xl mx-auto space-y-4" :style="getFontStyle(activeNote.font_style)">
            <div v-for="(item, index) in paginatedContent" :key="index" 
                 :class="getContentItemClass(item.type)"
                 class="animate-fade-in"
                 :style="{ animationDelay: `${index * 100}ms` }">
              
              <!-- Formula Box -->
              <div v-if="item.type === 'formula'" class="formula-container">
                <div class="formula-box rounded-xl p-4 bg-gradient-to-r from-purple-600/30 to-blue-600/30 border-2 border-purple-400/50">
                  <span class="font-mono text-lg text-purple-200">{{ item.content }}</span>
                </div>
              </div>
              
              <!-- Number Highlight -->
              <div v-else-if="item.type === 'number'" class="number-container">
                <div class="number-highlight inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-amber-500/20 border border-amber-400/50">
                  <span class="text-amber-400 font-bold text-2xl">{{ item.content }}</span>
                </div>
              </div>
              
              <!-- List Item -->
              <div v-else-if="item.type === 'list'" class="list-container flex items-start gap-3 p-3 rounded-lg bg-white/5">
                <span class="bullet w-6 h-6 rounded-full bg-cyan-500/30 flex items-center justify-center text-cyan-400 text-sm font-bold flex-shrink-0">•</span>
                <span class="text-slate-200">{{ item.content }}</span>
              </div>
              
              <!-- Definition/Term -->
              <div v-else-if="item.type === 'definition'" class="definition-container p-4 rounded-xl bg-emerald-500/10 border-l-4 border-emerald-400">
                <span class="text-emerald-300 font-semibold text-sm uppercase tracking-wide">Definition</span>
                <p class="text-emerald-100 mt-1">{{ item.content }}</p>
              </div>
              
              <!-- Regular Sentence -->
              <div v-else class="sentence-container py-2">
                <p class="text-slate-200 leading-relaxed text-lg">{{ item.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination Controls -->
        <div class="flex items-center justify-between p-4 border-t border-white/10 bg-slate-800/50">
          <button @click="prevPage" :disabled="currentPage === 0" 
                  class="flex items-center gap-2 px-4 py-2 rounded-xl transition"
                  :class="currentPage > 0 ? 'bg-cyan-600 hover:bg-cyan-500 text-white' : 'bg-white/5 text-slate-500 cursor-not-allowed'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Previous
          </button>
          
          <div class="flex items-center gap-2">
            <span class="text-sm text-slate-400">Page</span>
            <div class="flex gap-1">
              <button v-for="page in totalPages" :key="page" @click="goToPage(page - 1)"
                      :class="[
                        'w-8 h-8 rounded-lg text-sm font-medium transition',
                        currentPage === page - 1 
                          ? 'bg-cyan-500 text-white' 
                          : 'bg-white/10 text-slate-400 hover:bg-white/20'
                      ]">
                {{ page }}
              </button>
            </div>
          </div>
          
          <button @click="nextPage" :disabled="currentPage >= totalPages - 1" 
                  class="flex items-center gap-2 px-4 py-2 rounded-xl transition"
                  :class="currentPage < totalPages - 1 ? 'bg-cyan-600 hover:bg-cyan-500 text-white' : 'bg-white/5 text-slate-500 cursor-not-allowed'">
            Next
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>

        <!-- Note Navigation -->
        <div class="flex items-center justify-between p-4 border-t border-white/10">
          <button @click="previousNote" :disabled="!hasPrevious" class="flex items-center gap-2 px-4 py-2 rounded-xl transition" :class="hasPrevious ? 'bg-slate-700 hover:bg-slate-600 text-white' : 'bg-white/5 text-slate-500 cursor-not-allowed'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Previous Note
          </button>
          <button @click="nextNote" :disabled="!hasNext" class="flex items-center gap-2 px-4 py-2 rounded-xl transition" :class="hasNext ? 'bg-slate-700 hover:bg-slate-600 text-white' : 'bg-white/5 text-slate-500 cursor-not-allowed'">
            Next Note
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  isSubscribed: {
    type: Boolean,
    default: false
  }
});

const router = useRouter();
const notes = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const activeNote = ref(null);
const currentNoteIndex = ref(0);
const currentPage = ref(0);
const ITEMS_PER_PAGE = 7;

// Content parsing
const parsedContent = ref([]);

// Filtered notes based on search
const filteredNotes = computed(() => {
  if (!searchQuery.value) return notes.value;
  const query = searchQuery.value.toLowerCase();
  return notes.value.filter(note =>
    note.title.toLowerCase().includes(query) ||
    note.subject.toLowerCase().includes(query) ||
    note.category.toLowerCase().includes(query)
  );
});

// Navigation computed
const hasPrevious = computed(() => currentNoteIndex.value > 0);
const hasNext = computed(() => currentNoteIndex.value < filteredNotes.value.length - 1);

// Pagination computed
const totalPages = computed(() => Math.ceil(parsedContent.value.length / ITEMS_PER_PAGE));
const paginatedContent = computed(() => {
  const start = currentPage.value * ITEMS_PER_PAGE;
  return parsedContent.value.slice(start, start + ITEMS_PER_PAGE);
});

// Content parser
const parseContent = (content) => {
  if (!content) return [];
  
  const items = [];
  const lines = content.split('\n').filter(line => line.trim());
  
  lines.forEach(line => {
    const trimmed = line.trim();
    
    // Check for formula (contains =, +, -, *, /, ^, or math symbols)
    if (/[=\+\-\*\/\^]/.test(trimmed) && /[a-zA-Z0-9]/.test(trimmed)) {
      items.push({ type: 'formula', content: trimmed });
    }
    // Check for numbered list (starts with number and dot or parenthesis)
    else if (/^\d+[\.\)]\s/.test(trimmed)) {
      items.push({ type: 'number', content: trimmed });
    }
    // Check for bullet list
    else if (/^[\-\*•]\s/.test(trimmed)) {
      items.push({ type: 'list', content: trimmed.replace(/^[\-\*•]\s/, '') });
    }
    // Check for definition (contains "is defined as", "refers to", "means")
    else if (/is defined as|refers to|means|is a|are/i.test(trimmed) && trimmed.length < 200) {
      items.push({ type: 'definition', content: trimmed });
    }
    // Regular sentence
    else {
      items.push({ type: 'sentence', content: trimmed });
    }
  });
  
  return items;
};

// Get content item styling
const getContentItemClass = (type) => {
  const classes = {
    formula: 'my-4',
    number: 'my-3',
    list: 'my-2',
    definition: 'my-3',
    sentence: 'my-2'
  };
  return classes[type] || 'my-2';
};

// Theme helpers
const getThemeGradient = (color) => {
  const gradients = {
    blue: 'bg-gradient-to-br from-blue-600/20 to-cyan-600/20',
    purple: 'bg-gradient-to-br from-purple-600/20 to-pink-600/20',
    emerald: 'bg-gradient-to-br from-emerald-600/20 to-teal-600/20',
    orange: 'bg-gradient-to-br from-orange-600/20 to-red-600/20',
    rose: 'bg-gradient-to-br from-rose-600/20 to-pink-600/20'
  };
  return gradients[color] || gradients.blue;
};

const getThemeBg = (color) => {
  const bgs = {
    blue: 'bg-gradient-to-br from-blue-50/5 to-cyan-50/5',
    purple: 'bg-gradient-to-br from-purple-50/5 to-pink-50/5',
    emerald: 'bg-gradient-to-br from-emerald-50/5 to-teal-50/5',
    orange: 'bg-gradient-to-br from-orange-50/5 to-red-50/5',
    rose: 'bg-gradient-to-br from-rose-50/5 to-pink-50/5'
  };
  return bgs[color] || bgs.blue;
};

const getFontStyle = (font) => {
  const fonts = {
    'sans-serif': 'font-family: system-ui, -apple-system, sans-serif',
    'serif': 'font-family: Georgia, Cambria, serif',
    'monospace': 'font-family: Consolas, Monaco, monospace'
  };
  return fonts[font] || fonts['sans-serif'];
};

// Pagination controls
const prevPage = () => {
  if (currentPage.value > 0) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value - 1) currentPage.value++;
};

const goToPage = (page) => {
  currentPage.value = page;
};

// Fetch notes from API
const fetchNotes = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/notes/`);
    if (!response.ok) {
      throw new Error('Failed to fetch notes');
    }
    const data = await response.json();
    notes.value = data;
  } catch (err) {
    console.error('Error fetching notes:', err);
    error.value = err.message || 'Failed to load notes. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Open note
const openNote = (note) => {
  activeNote.value = note;
  currentNoteIndex.value = filteredNotes.value.findIndex(n => n.id === note.id);
  currentPage.value = 0;
  parsedContent.value = parseContent(note.content);
};

// Close reader
const closeReader = () => {
  activeNote.value = null;
  currentNoteIndex.value = 0;
  currentPage.value = 0;
  parsedContent.value = [];
};

// Navigation
const previousNote = () => {
  if (hasPrevious.value) {
    currentNoteIndex.value--;
    activeNote.value = filteredNotes.value[currentNoteIndex.value];
    currentPage.value = 0;
    parsedContent.value = parseContent(activeNote.value.content);
  }
};

const nextNote = () => {
  if (hasNext.value) {
    currentNoteIndex.value++;
    activeNote.value = filteredNotes.value[currentNoteIndex.value];
    currentPage.value = 0;
    parsedContent.value = parseContent(activeNote.value.content);
  }
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

/* Formula Box Styling */
.formula-box {
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
  border: 2px solid rgba(147, 51, 234, 0.5);
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  display: inline-block;
  box-shadow: 0 4px 15px rgba(147, 51, 234, 0.3);
}

/* Number Highlight Styling */
.number-highlight {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(251, 191, 36, 0.2) 100%);
  border: 2px solid rgba(245, 158, 11, 0.5);
  color: #fbbf24;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
}

/* List Item Styling */
.list-container {
  background: rgba(255, 255, 255, 0.05);
  border-left: 3px solid #06b6d4;
  transition: all 0.3s ease;
}

.list-container:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

/* Definition Styling */
.definition-container {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%);
  border-left: 4px solid #34d399;
}

/* Sentence Styling */
.sentence-container {
  text-align: justify;
  hyphens: auto;
}

/* Animation */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out forwards;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
