<!-- File: components/HeroSearch.vue -->
<template>
  <section class="relative pt-24 pb-12 overflow-hidden">
    <!-- Animated gradient background -->
    <div aria-hidden="true" class="absolute inset-0 -z-10">
      <div class="absolute -left-40 -top-40 w-[720px] h-[720px] rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 opacity-20 blur-3xl transform-gpu animate-blob"></div>
      <div class="absolute -right-40 -bottom-40 w-[520px] h-[520px] rounded-full bg-gradient-to-tr from-rose-400 to-yellow-300 opacity-10 blur-2xl transform-gpu animate-blob animation-delay-2000"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bg-white/60 dark:bg-slate-800/60 backdrop-blur-lg rounded-2xl p-8 shadow-xl border border-white/10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
          <!-- Text -->
          <div>
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold leading-tight text-slate-900 dark:text-white">
              Exam Bank & Study Hub
            </h1>
            <p class="mt-3 text-slate-700 dark:text-slate-300 max-w-xl">
              Thousands of past exams, curated notes, and tutor videos — free and premium. Find, preview, and practice with resources tailored for your class and exam.
            </p>

            <!-- Search field (large) -->
            <div class="mt-6">
              <label class="sr-only" for="hero-search">Search resources</label>
              <div class="flex gap-3">
                <input
                  id="hero-search"
                  v-model="query"
                  @keyup.enter="doSearch"
                  type="search"
                  placeholder="Search by subject, exam, topic or keyword..."
                  class="flex-1 px-4 py-3 rounded-full focus:outline-none focus:ring-2 focus:ring-cyan-400 bg-white dark:bg-slate-900 text-sm shadow"
                  aria-label="Search study resources"
                />
                <button
                  @click="doSearch"
                  class="rounded-full px-4 py-2 bg-gradient-to-br from-cyan-500 to-purple-600 text-white font-semibold shadow hover:scale-105 focus:outline-none"
                  aria-label="Search resources"
                >
                  Search
                </button>
              </div>
              <p class="mt-2 text-xs text-slate-500">Try: "Grade 12 physics past paper", "calculus solutions", "entrance exam 2019".</p>
            </div>

            <!-- CTAs -->
            <div class="mt-6 flex flex-wrap gap-3">
              <button @click="$emit('explore')" class="px-5 py-2 rounded-full bg-white/80 dark:bg-slate-700/70 shadow hover:scale-105 focus:outline-none" aria-label="Explore resources">
                Explore Resources
              </button>
              <button @click="$emit('upload')" class="px-5 py-2 rounded-full border border-white/20 bg-transparent text-sm text-slate-900 dark:text-white focus:outline-none" aria-label="Upload resource">
                Upload (Teachers)
              </button>
            </div>
          </div>

          <!-- Right side: feature cards -->
          <div class="space-y-3">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div class="p-4 rounded-xl bg-white/80 dark:bg-slate-900/50 backdrop-blur shadow hover:translate-y-1 transition-transform">
                <h3 class="font-semibold text-slate-900 dark:text-white">Curated Past Papers</h3>
                <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Past questions & model answers categorized by year and subject.</p>
              </div>
              <div class="p-4 rounded-xl bg-white/80 dark:bg-slate-900/50 backdrop-blur shadow hover:translate-y-1 transition-transform">
                <h3 class="font-semibold text-slate-900 dark:text-white">Video Tutors</h3>
                <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Short lessons and walkthroughs from experienced tutors.</p>
              </div>
              <div class="p-4 rounded-xl bg-white/80 dark:bg-slate-900/50 backdrop-blur shadow hover:translate-y-1 transition-transform">
                <h3 class="font-semibold text-slate-900 dark:text-white">Practice Quizzes</h3>
                <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Timed mock exams to help you prepare.</p>
              </div>
              <div class="p-4 rounded-xl bg-white/80 dark:bg-slate-900/50 backdrop-blur shadow hover:translate-y-1 transition-transform">
                <h3 class="font-semibold text-slate-900 dark:text-white">Premium Bundles</h3>
                <p class="text-sm text-slate-600 dark:text-slate-300 mt-1">Specialized packs for entrance exams and final reviews.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
const emit = defineEmits(["search", "explore", "upload"]);

const query = ref("");

function doSearch() {
  emit("search", query.value.trim());
}
</script>

<style scoped>
@keyframes blob {
  0% { transform: translateY(0px) scale(1) }
  33% { transform: translateY(-20px) scale(1.05) }
  66% { transform: translateY(10px) scale(0.95) }
  100% { transform: translateY(0px) scale(1) }
}
.animate-blob {
  animation: blob 8s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
