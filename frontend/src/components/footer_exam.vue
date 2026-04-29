<!-- File: footer_exam.vue -->
<template>
  <footer class="bg-white/60 dark:bg-slate-900/60 backdrop-blur border-t border-white/10 py-10 mt-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div>
        <div class="flex items-center gap-3 mb-3">
          <svg class="w-10 h-10 rounded p-1 bg-gradient-to-br from-cyan-400 to-purple-500" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <rect width="24" height="24" rx="6" fill="white" opacity="0.06"></rect>
            <path d="M6 15V9l6-4 6 4v6l-6 4-6-4z" fill="white" opacity="0.9"/>
          </svg>
          <div>
            <h4 class="font-semibold text-slate-900 dark:text-white">Exam Bank</h4>
            <p class="text-xs text-slate-600 dark:text-slate-300">Curated past exams & study resources</p>
          </div>
        </div>
        <p class="text-xs text-slate-600 dark:text-slate-300 max-w-sm">Trusted by students and tutors — a growing library of past papers, solutions, and video lessons.</p>
      </div>

      <div class="flex flex-col">
        <h5 class="font-semibold text-slate-900 dark:text-white mb-3">Quick links</h5>
        <ul class="space-y-2 text-sm text-slate-600 dark:text-slate-300">
          <li><a class="hover:underline" href="#" aria-label="Explore resources">Explore</a></li>
          <li><a class="hover:underline" href="#" aria-label="Upload resource">Upload</a></li>
          <li><a class="hover:underline" href="#" aria-label="Pricing and premium">Pricing</a></li>
          <li><a class="hover:underline" href="#" aria-label="Contact us">Contact</a></li>
        </ul>
      </div>

      <div>
        <h5 class="font-semibold text-slate-900 dark:text-white mb-3">Newsletter</h5>
        <p class="text-xs text-slate-600 dark:text-slate-300 mb-3">Get notified when new exam packs and premium bundles are released.</p>
        <form @submit.prevent="subscribe" class="flex gap-2">
          <label class="sr-only" for="newsletter-email">Email</label>
          <input id="newsletter-email" v-model="email" type="email" placeholder="you@example.com" required class="flex-1 px-3 py-2 rounded-full bg-white dark:bg-slate-800 text-sm focus:ring-2 focus:ring-cyan-400 focus:outline-none" aria-label="Newsletter email"/>
          <button type="submit" class="px-4 py-2 rounded-full bg-gradient-to-br from-cyan-500 to-purple-600 text-white text-sm focus:outline-none" aria-label="Subscribe to newsletter">Subscribe</button>
        </form>
        <p v-if="message" class="mt-2 text-xs text-emerald-500">{{ message }}</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 border-t border-white/10 pt-6 text-xs text-slate-600 dark:text-slate-300 flex items-center justify-between">
      <div>© {{ new Date().getFullYear() }} Exam Bank. All rights reserved.</div>
      <div class="flex items-center gap-4">
        <a href="#" aria-label="Twitter" class="hover:underline">Twitter</a>
        <a href="#" aria-label="Facebook" class="hover:underline">Facebook</a>
        <a href="#" aria-label="Privacy policy" class="hover:underline">Privacy</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from "vue";
const email = ref("");
const message = ref("");

function subscribe() {
  // TODO: Plug in API call to subscribe user: axios.post('/api/subscribe', { email: email.value })
  message.value = "Thanks! We'll notify you when new bundles drop.";
  email.value = "";
  setTimeout(() => (message.value = ""), 4000);
}
</script>

<style scoped>
/* small adjustments for footer */
</style>
