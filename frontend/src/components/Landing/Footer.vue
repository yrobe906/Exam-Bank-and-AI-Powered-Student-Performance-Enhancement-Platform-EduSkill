<template>
  <footer class="relative bg-gray-900 text-gray-300 overflow-hidden">
    <!-- Background decorations -->
    <div class="absolute inset-0 -z-10">
      <div class="absolute top-0 left-1/4 w-72 h-72 bg-indigo-600/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-1/4 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <!-- Main Footer Content -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
        <!-- Brand Column -->
        <div class="lg:col-span-1">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg overflow-hidden">
              <img :src="logoImage" alt="EduSkill" class="w-8 h-8 object-contain" />
            </div>
            <div>
              <span class="text-xl font-bold text-white">Edu<span class="text-indigo-400">Skill</span></span>
              <span class="block text-xs text-gray-500">Hub</span>
            </div>
          </div>
          
          <p class="text-gray-400 mb-6 leading-relaxed text-sm">
            Empowering students worldwide with AI-powered learning tools for exam success.
          </p>

          <!-- Social Links -->
          <div class="flex gap-3">
            <a 
              v-for="social in socials" 
              :key="social.name"
              :href="social.href"
              target="_blank"
              rel="noopener noreferrer"
              class="w-9 h-9 rounded-lg bg-gray-800 flex items-center justify-center text-gray-400 hover:bg-indigo-600 hover:text-white transition-all duration-200"
            >
              <span v-html="social.icon"></span>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="text-white font-semibold mb-5">Quick Links</h4>
          <ul class="space-y-3">
            <li v-for="link in quickLinks" :key="link.name">
              <a :href="link.href" class="text-gray-400 hover:text-indigo-400 transition-colors duration-200 text-sm">
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Resources -->
        <div>
          <h4 class="text-white font-semibold mb-5">Resources</h4>
          <ul class="space-y-3">
            <li v-for="link in resources" :key="link.name">
              <a :href="link.href" class="text-gray-400 hover:text-indigo-400 transition-colors duration-200 text-sm">
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Newsletter -->
        <div>
          <h4 class="text-white font-semibold mb-4">Stay Updated</h4>
          <p class="text-gray-400 mb-4 text-sm">Subscribe to our newsletter for the latest updates and offers.</p>
          
          <form @submit.prevent="subscribeNewsletter" class="space-y-3">
            <input 
              v-model="email"
              type="email" 
              placeholder="Enter your email"
              class="w-full px-4 py-2.5 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 transition-colors text-sm"
              required
            />
            <button 
              type="submit"
              class="w-full px-4 py-2.5 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition-colors text-sm"
            >
              Subscribe
            </button>
          </form>
        </div>
      </div>

      <!-- App Store Buttons -->
      <div class="border-t border-gray-800 pt-8 mb-8">
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <p class="text-gray-500 text-sm">Download our mobile app:</p>
          <div class="flex gap-3">
            <a href="#" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 hover:border-indigo-500 transition-colors">
              <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
              </svg>
              <div class="text-left">
                <p class="text-xs text-gray-500">Download on the</p>
                <p class="text-sm font-medium text-white">App Store</p>
              </div>
            </a>
            <a href="#" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 hover:border-indigo-500 transition-colors">
              <svg class="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3.609 1.814L13.792 12 3.61 22.186c-.186.185-.437.247-.656.165-.22-.082-.365-.292-.365-.527V2.176c0-.235.146-.445.365-.527.219-.082.47-.02.655.165m9.292 10.011L5.314 21.814c-.409.409-.299.75.245 1.015l4.313 2.5c.157.097.341.134.528.105.531-.078.906-.562.824-1.093l-.896-5.334 5.893-3.563c.135-.083.237-.221.237-.377v-1.372c0-.209-.167-.377-.375-.377-.139 0-.273.076-.351.196l-5.195 3.134z"/>
              </svg>
              <div class="text-left">
                <p class="text-xs text-gray-500">Get it on</p>
                <p class="text-sm font-medium text-white">Google Play</p>
              </div>
            </a>
          </div>
        </div>
      </div>

      <!-- Copyright -->
      <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-gray-500 text-sm">
          © {{ currentYear }} EduSkill Hub. All rights reserved.
        </p>
        <div class="flex gap-6">
          <a href="#" class="text-gray-500 hover:text-indigo-400 text-sm transition-colors">Privacy Policy</a>
          <a href="#" class="text-gray-500 hover:text-indigo-400 text-sm transition-colors">Terms of Service</a>
          <a href="#" class="text-gray-500 hover:text-indigo-400 text-sm transition-colors">Cookie Policy</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed } from 'vue'
import logoImage from '@/assets/images/eduskill-real.png'

const email = ref('')

const currentYear = computed(() => new Date().getFullYear())

const socials = [
  { name: 'Twitter', href: '#', icon: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"/></svg>' },
  { name: 'GitHub', href: '#', icon: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg>' },
  { name: 'LinkedIn', href: '#', icon: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>' },
  { name: 'YouTube', href: '#', icon: '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>' }
]

const quickLinks = [
  { name: 'Home', href: '#home' },
  { name: 'Features', href: '#features' },
  { name: 'Pricing', href: '#pricing' },
  { name: 'Testimonials', href: '#testimonials' },
  { name: 'FAQ', href: '#faq' }
]

const resources = [
  { name: 'Documentation', href: '#' },
  { name: 'Blog', href: '#' },
  { name: 'Support Center', href: '#' },
  { name: 'Contact Us', href: '#' }
]

const subscribeNewsletter = () => {
  alert(`Thank you for subscribing with: ${email.value}`)
  email.value = ''
}
</script>


