<template>
  <nav
    class="w-full fixed top-0 z-40 backdrop-blur bg-white/30 dark:bg-slate-900/40 border-b border-white/10"
    role="navigation"
    aria-label="Main Navigation"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Brand -->
        <div class="flex items-center gap-3">
          <button
            class="flex items-center gap-2 focus:outline-none group hover-animate"
            aria-label="Go to home"
            @click="$emit('go-home')"
          >
            <img 
              src="@/assets/images/logo.png" 
              alt="logo"
              class="w-10 h-10 object-cover rounded-xl transition-transform duration-500 group-hover:rotate-45"
            />
            <span class="font-semibold text-lg text-slate-900 dark:text-slate-100">KTech</span>
          </button>
          <span class="font-semibold text-lg text-slate-900 dark:text-slate-100 hover-animate">Exam Bank</span>
        </div>

        <!-- Search (desktop) -->
        <div class="hidden md:flex md:items-center md:w-1/3">
          <label class="sr-only" for="nav-search">Search resources</label>
          <div class="w-full">
            <div class="relative">
              <input
                id="nav-search"
                type="search"
                v-model="localQuery"
                @keyup.enter="emitSearch"
                placeholder="Search exams, notes, videos..."
                class="w-full rounded-full bg-white/60 dark:bg-slate-800/50 backdrop-blur px-4 py-2 text-sm focus:outline-none shadow-sm border-2 border-transparent search-animate"
                aria-label="Search resources"
              />
              <button
                @click="emitSearch"
                class="absolute right-1 top-1/2 -translate-y-1/2 px-3 py-1 rounded-full hover:bg-white/30 focus:outline-none"
                aria-label="Search"
              >
                <svg class="w-5 h-5 text-slate-700 dark:text-slate-200" viewBox="0 0 24 24" fill="none">
                  <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.5"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center gap-3">
          <!-- Dark mode toggle -->
          <button
            @click="toggleTheme"
            :aria-pressed="isDark.toString()"
            class="p-2 rounded-full hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-cyan-400"
            aria-label="Toggle dark mode"
          >
            <svg v-if="!isDark" class="w-5 h-5 text-slate-800" viewBox="0 0 24 24" fill="none">
              <path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            <svg v-else class="w-5 h-5 text-yellow-300" viewBox="0 0 24 24" fill="none">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="currentColor"/>
            </svg>
          </button>

          <!-- Auth Buttons -->
          <button class="hidden sm:inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-white/70 dark:bg-slate-800/60 focus:outline-none hover-animate" aria-label="Login">
            Login
          </button>
          <button @click="goRegister" class="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-gradient-to-br from-cyan-500 to-purple-600 text-white shadow focus:outline-none hover-animate" aria-label="Sign up">
            Sign Up
          </button>

          <!-- Mobile search button -->
          <button class="md:hidden p-2 rounded-full hover:bg-white/20 focus:outline-none" @click="$emit('open-search')" aria-label="Open search">
            <svg class="w-5 h-5 text-slate-700 dark:text-slate-200" viewBox="0 0 24 24" fill="none">
              <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const emit = defineEmits(["search", "toggle-theme", "go-home", "open-search"]);
const localQuery = ref("");
const isDark = ref(false);
const router = useRouter();

onMounted(() => {
  const stored = localStorage.getItem("eb_theme");
  if (stored === "dark") {
    isDark.value = true;
    document.documentElement.classList.add("dark");
  } else {
    isDark.value = false;
    document.documentElement.classList.remove("dark");
  }
});

function emitSearch() {
  emit("search", localQuery.value.trim());
}

function toggleTheme() {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add("dark");
    localStorage.setItem("eb_theme", "dark");
  } else {
    document.documentElement.classList.remove("dark");
    localStorage.setItem("eb_theme", "light");
  }
  emit("toggle-theme", isDark.value);
}

// Navigate to register page
function goRegister() {
  router.push("/register");
}
</script>

<style scoped>
:focus { outline: none; }

/* Simple animated hover effect */
.hover-animate {
  transition: transform 0.3s ease, filter 0.3s ease;
}
.hover-animate:hover {
  transform: scale(1.05);
  filter: brightness(1.2);
}

/* Keep search bar animation separate if needed */
.search-animate {
  border: 2px solid transparent;
  border-radius: 9999px;
  background-clip: padding-box;
  transition: all 0.5s ease;
}
.search-animate:hover {
  border-image-slice: 1;
  border-width: 2px;
  border-image-source: linear-gradient(270deg, #06b6d4, #8b5cf6, #06b6d4);
  animation: borderShift 2s linear infinite;
}

@keyframes borderShift {
  0% { border-image-source: linear-gradient(270deg, #06b6d4, #8b5cf6, #06b6d4); }
  50% { border-image-source: linear-gradient(450deg, #8b5cf6, #06b6d4, #8b5cf6); }
  100% { border-image-source: linear-gradient(270deg, #06b6d4, #8b5cf6, #06b6d4); }
}
</style>
