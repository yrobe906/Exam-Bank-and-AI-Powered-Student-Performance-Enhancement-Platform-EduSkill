<template>
  <header 
    class="fixed top-0 left-0 w-full z-50 transition-all duration-300"
    :class="[
      isScrolled 
        ? 'bg-white/95 backdrop-blur-md shadow-lg py-3' 
        : 'bg-white/80 backdrop-blur-sm py-4'
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between">
        
        <!-- Logo -->
        <div class="flex items-center gap-3 group cursor-pointer" @click="scrollToTop">
          <div class="relative">
            <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300 overflow-hidden">
              <img :src="logoImage" alt="EduSkill Logo" class="w-8 h-8 object-contain" />
            </div>
          </div>
          
          <div class="flex flex-col">
            <span class="text-xl font-bold text-gray-900">
              Edu<span class="text-indigo-600">Skill</span>
            </span>
            <span class="text-xs text-gray-500 -mt-0.5">Hub</span>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden lg:flex items-center gap-1">
          <a 
            v-for="item in navItems" 
            :key="item.name"
            :href="item.href"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors duration-200"
            @click="handleNavClick"
          >
            {{ item.name }}
          </a>
        </nav>

        <!-- CTA Buttons -->
        <div class="hidden lg:flex items-center gap-3">
          <!-- Login Button -->
          <button 
            @click="navigateToLogin"
            class="px-5 py-2 text-sm font-semibold text-gray-700 hover:text-indigo-600 transition-colors duration-200"
          >
            Login
          </button>

          <!-- Get Started Button -->
          <button 
            @click="navigateToRegister"
            class="px-5 py-2.5 text-sm font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-all duration-200 hover:shadow-md"
          >
            Get Started
          </button>
        </div>

        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMobileMenu"
          class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <svg v-if="!isMobileMenuOpen" class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <Transition
        enter-active-class="transition-all duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div 
          v-if="isMobileMenuOpen"
          class="lg:hidden absolute top-full left-0 w-full bg-white shadow-xl border-t border-gray-100"
        >
          <div class="px-4 py-4 space-y-2">
            <a 
              v-for="item in navItems" 
              :key="item.name"
              :href="item.href"
              class="block px-4 py-3 text-base font-medium text-gray-700 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
              @click="closeMobileMenu"
            >
              {{ item.name }}
            </a>
            
            <div class="pt-3 flex flex-col gap-2 border-t border-gray-100">
              <button 
                @click="navigateToLogin"
                class="w-full px-4 py-3 text-center font-semibold text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Login
              </button>
              <button 
                @click="navigateToRegister"
                class="w-full px-4 py-3 text-center font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import logoImage from '@/assets/images/eduskill-real.png'

const router = useRouter()

const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

const navItems = [
  { name: 'Home', href: '#home' },
  { name: 'Features', href: '#features' },
  { name: 'Testimonials', href: '#testimonials' },
  { name: 'Pricing', href: '#pricing' },
  { name: 'FAQ', href: '#faq' },
]

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleNavClick = (e) => {
  const href = e.currentTarget.getAttribute('href')
  if (href.startsWith('#')) {
    e.preventDefault()
    const element = document.querySelector(href)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
    closeMobileMenu()
  }
}

const navigateToLogin = () => {
  router.push('/user_login')
  closeMobileMenu()
}

const navigateToRegister = () => {
  router.push('/register')
  closeMobileMenu()
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>


