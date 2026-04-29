<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-950 text-slate-900 dark:text-slate-100">
    <NavBar @search="onSearch" @toggle-theme="onToggleTheme" @go-home="goHome" @open-search="openMobileSearch" />

    <main class="pt-20">
      <HeroSearch @search="onSearch" @explore="goExplore" @upload="goUpload" class="search-animate" />

      <!-- Categories -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <h2 class="text-lg font-semibold mb-3">Subjects</h2>
        <div class="flex gap-3 overflow-x-auto pb-2">
          <button
            v-for="(cat, idx) in categories"
            :key="cat"
            @click="selectCategory(cat)"
            :class="['whitespace-nowrap px-4 py-2 rounded-full text-sm font-medium focus:outline-none transition-all duration-300 hover:shadow-md hover:scale-[1.03] hover:border-cyan-500 hover:border', selectedCategory === cat ? 'bg-gradient-to-br from-cyan-500 to-purple-600 text-white' : 'bg-white/60 dark:bg-slate-800/60 text-slate-700 dark:text-slate-200']"
            :aria-pressed="(selectedCategory===cat).toString()"
          >
            {{ cat }}
          </button>
        </div>
      </section>

      <!-- Featured resources -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold">Featured Resources</h2>
          <div class="text-sm text-slate-500 dark:text-slate-300">Showing {{ filteredResources.length }} results</div>
        </div>

        <div class="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <ResourceCard
            v-for="res in pagedResources"
            :key="res.id"
            :resource="res"
            @view="goRegister"
            @download="goRegister"
            @buy="goRegister"
            class="resource-animate"
          />
        </div>

        <div class="mt-6 flex justify-center">
          <button v-if="hasMore" @click="loadMore" class="px-4 py-2 rounded-full bg-white/80 dark:bg-slate-800/60 focus:outline-none hover:scale-105 transition duration-300">Load more</button>
          <div v-else class="text-sm text-slate-500 dark:text-slate-300">End of results</div>
        </div>
      </section>

      <!-- Stats strip -->
      <section class="mt-12 bg-gradient-to-r from-white/60 dark:from-slate-800/40 backdrop-blur py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
          <div>
            <div class="text-3xl font-extrabold">{{ stats.users }}</div>
            <div class="text-sm text-slate-500 dark:text-slate-300">Students</div>
          </div>
          <div>
            <div class="text-3xl font-extrabold">{{ stats.resources }}</div>
            <div class="text-sm text-slate-500 dark:text-slate-300">Resources</div>
          </div>
          <div>
            <div class="text-3xl font-extrabold">{{ stats.exams }}</div>
            <div class="text-sm text-slate-500 dark:text-slate-300">Exam Papers</div>
          </div>
        </div>
      </section>

      <!-- Testimonials slider -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12">
        <h3 class="text-xl font-semibold mb-4">What learners say</h3>
        <div class="bg-white/60 dark:bg-slate-800/60 backdrop-blur p-6 rounded-2xl shadow testimonial-3d">
          <div class="flex items-center gap-4">
            <button class="p-2 rounded-full hover:bg-white/20 focus:outline-none" @click="prevTestimonial">‹</button>
            <div class="flex-1 flex items-center gap-4">
              <img :src="learnerImage" class="w-14 h-14 rounded-full shadow-lg" />
              <div>
                <p class="text-sm">"{{ currentTestimonial.text }}"</p>
                <div class="mt-3 text-xs text-slate-500 dark:text-slate-400">— {{ currentTestimonial.author }}</div>
              </div>
            </div>
            <button class="p-2 rounded-full hover:bg-white/20 focus:outline-none" @click="nextTestimonial">›</button>
          </div>
        </div>
      </section>

      <FooterExam />
    </main>

    <!-- Mobile search modal -->
    <div v-if="mobileSearchOpen" class="fixed inset-0 z-50 flex items-start pt-24 px-4">
      <div class="w-full max-w-3xl mx-auto">
        <div class="bg-white/90 dark:bg-slate-900/80 backdrop-blur rounded-xl p-4 shadow animate-pulse">
          <div class="flex gap-3">
            <input v-model="mobileQuery" @keyup.enter="doMobileSearch" class="flex-1 px-4 py-2 rounded-full focus:outline-none search-animate" placeholder="Search resources..." aria-label="Mobile search" />
            <button @click="doMobileSearch" class="px-4 py-2 rounded-full bg-gradient-to-br from-cyan-500 to-purple-600 text-white hover:scale-105 transition-all">Search</button>
          </div>
        </div>
      </div>
      <button class="absolute right-6 top-28 p-2 rounded-full bg-white/30" @click="mobileSearchOpen=false" aria-label="Close search">✕</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue"
import { useRouter } from "vue-router"
import NavBar from "@/components/NavBar.vue"
import HeroSearch from "@/components/HeroSearch.vue"
import ResourceCard from "@/components/ResourceCard.vue"
import FooterExam from "@/components/Footer_exam.vue"

/* IMPORT IMAGES HERE */
import maths from '@/assets/images/logo.png'
import physics  from '@/assets/images/physics.png'
import chemistry from '@/assets/images/chemistry.png'
import biology from '@/assets/images/biology.png'
import english from '@/assets/images/english.png'
import entrance from '@/assets/images/videotutor1.png'
import learnerImage from '@/assets/images/learner1.jpg'

const router = useRouter()

// Sample resources with some premium
const sampleResources = ref([
  { id: 1, title: "Grade 12 Physics — Past Paper 2019", description: "Complete past paper with model answers.", subject: "Physics", class_level: "Grade 12", type: "pdf", thumbnail: physics, price: 0 },
  { id: 2, title: "Calculus — Quick Revision Video", description: "Short tutorial on integrals and techniques.", subject: "Mathematics", class_level: "Grade 12", type: "video", thumbnail: maths, price: 250 },
  { id: 3, title: "Entrance Exam — Biology 2018 + Solutions", description: "Model answers included for quick review.", subject: "Biology", class_level: "University Entrance", type: "pdf", thumbnail: biology, price: 0 },
  { id: 4, title: "Chemistry — Final Revision Pack", description: "Comprehensive notes with practice questions.", subject: "Chemistry", class_level: "Grade 11", type: "note", thumbnail: chemistry, price: 100 },
  { id: 5, title: "Mathematics — Mock Exam (Timed)", description: "10-question mock exam with timer and answers.", subject: "Mathematics", class_level: "Grade 12", type: "exam", thumbnail: maths, price: 0 },
  { id: 6, title: "English — Essay Samples & Tips", description: "Model essays and marking tips.", subject: "English", class_level: "Grade 10", type: "note", thumbnail: english, price: 50 }
])

const categories = ref(["All", "Mathematics", "Physics", "Biology", "Chemistry", "English", "Entrance"])
const selectedCategory = ref("All")
const searchQuery = ref("")
const pageSize = ref(6)
const page = ref(1)
const mobileSearchOpen = ref(false)
const mobileQuery = ref("")
const stats = reactive({ users: 12400, resources: sampleResources.value.length, exams: 870 })
const testimonials = ref([
  { author: "Lina - Grade 12", text: "Found the exact entrance papers I needed. Highly recommended!" },
  { author: "Samuel - University", text: "The video tutors made difficult topics so simple." },
  { author: "Aisha - Tutor", text: "I upload bundles and students love them." }
])
const tIndex = ref(0)

const filteredResources = computed(() => {
  let list = sampleResources.value
  if (selectedCategory.value && selectedCategory.value !== "All") {
    list = list.filter(r => r.subject === selectedCategory.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(r => (r.title + " " + r.description + " " + r.subject).toLowerCase().includes(q))
  }
  return list
})

const pagedResources = computed(() => filteredResources.value.slice(0, page.value * pageSize.value))
const hasMore = computed(() => filteredResources.value.length > pagedResources.value.length)
const currentTestimonial = computed(() => testimonials.value[tIndex.value])

function goRegister() { router.push('/register') }
function selectCategory(cat) { selectedCategory.value = cat; page.value = 1 }
function onSearch(q) { searchQuery.value = q || ""; selectedCategory.value = "All"; page.value = 1 }
function loadMore() { page.value++ }
function goExplore() { window.scrollTo({ top: 600, behavior: "smooth" }) }
function goUpload() { router.push('/register') }
function goHome() { window.scrollTo({ top: 0, behavior: "smooth" }) }
function openMobileSearch() { mobileSearchOpen.value = true }
function doMobileSearch() { onSearch(mobileQuery.value); mobileSearchOpen.value = false; mobileQuery.value = "" }
function prevTestimonial() { tIndex.value = (tIndex.value - 1 + testimonials.value.length) % testimonials.value.length }
function nextTestimonial() { tIndex.value = (tIndex.value + 1) % testimonials.value.length }
function onToggleTheme(isDark) {}
</script>

<style>
:root { --card-radius: 16px; }
.search-animate {
  transition: 0.35s;
  border: 2px solid transparent;
}
.search-animate:hover {
  border-color: cyan;
  box-shadow: 0 0 6px cyan;
}
.testimonial-3d {
  transform: perspective(900px) rotateX(3deg);
  transition: 0.3s;
}
.testimonial-3d:hover {
  transform: perspective(900px) rotateX(0deg) scale(1.02);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}
@keyframes floatIn {
  from { opacity: 0; transform: translateY(8px) scale(0.995); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.resource-animate { animation: floatIn 420ms cubic-bezier(.2,.8,.2,1); }
</style>
