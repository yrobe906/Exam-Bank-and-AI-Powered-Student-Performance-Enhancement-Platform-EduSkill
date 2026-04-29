<template>
  <footer class="relative bg-gradient-to-br from-black via-gray-900 to-black border-t border-white/10 px-6 pt-16 pb-10 overflow-hidden">
    
    <!-- Glow background -->
    <div class="absolute inset-0 -z-10">
      <div class="absolute -top-20 -left-20 w-72 h-72 bg-indigo-600/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -right-20 w-72 h-72 bg-purple-600/20 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto">

      <!-- MAIN GRID -->
      <div class="grid gap-12 md:grid-cols-3 mb-12">

        <!-- BRAND -->
        <div class="space-y-5">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/40">
              <span class="text-2xl font-bold text-white">Y</span>
            </div>
            <h2 class="text-2xl font-bold tracking-wide">
              Yasin <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500">RW</span>
            </h2>
          </div>

          <p class="text-gray-400 leading-relaxed">
            Crafting scalable digital experiences with modern technology, clean design, and performance-driven solutions.
          </p>

          <!-- SOCIAL ICONS -->
          <div class="flex gap-4 pt-4">
            <a
              v-for="social in socialLinks"
              :key="social.name"
              :href="social.link"
              target="_blank"
              :aria-label="social.name"
              class="group w-11 h-11 rounded-full bg-white/5 border border-white/10 flex items-center justify-center
                     hover:bg-indigo-600/30 hover:border-indigo-400/50 hover:scale-110
                     transition-all duration-300 shadow-md hover:shadow-indigo-500/40"
            >
              <i
                :class="social.icon"
                class="text-xl text-gray-300 group-hover:text-white"
              ></i>
            </a>
          </div>
        </div>

        <!-- QUICK LINKS -->
        <div>
          <h3 class="text-xl font-semibold mb-6">Quick Links</h3>
          <ul class="space-y-4">
            <li v-for="link in quickLinks" :key="link.name">
              <a
                :href="link.href"
                class="flex items-center gap-3 text-gray-400 hover:text-indigo-400 transition duration-300"
              >
                <span class="w-2 h-2 bg-indigo-500 rounded-full"></span>
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>

        <!-- CONTACT -->
        <div>
          <h3 class="text-xl font-semibold mb-6">Get In Touch</h3>
          <ul class="space-y-4 text-gray-400">
            <li class="flex items-center gap-3">
              <i class="fas fa-envelope text-indigo-400"></i>
              yasinrw24@gmail.com
            </li>
            <li class="flex items-center gap-3">
              <i class="fas fa-phone text-indigo-400"></i>
              +251 721601263
            </li>
            <li class="flex items-center gap-3">
              <i class="fas fa-map-marker-alt text-indigo-400"></i>
              Jimma, Ethiopia
            </li>
          </ul>
        </div>

      </div>

      <!-- COPYRIGHT -->
      <div class="pt-6 border-t border-white/10 text-center text-sm text-gray-500">
        © {{ year }} <span class="text-gray-300 font-medium">Yasin RW</span>. All rights reserved.
      </div>

    </div>
  </footer>
</template>

<script>
export default {
  name: 'MyFooter',
  computed: {
    year() {
      return new Date().getFullYear()
    }
  },
  data() {
    return {
      socialLinks: [
        { name: 'GitHub', icon: 'fab fa-github', link: 'https://github.comyrobe906' },
        { name: 'LinkedIn', icon: 'fab fa-linkedin', link: 'https://linkedin.com' },
        { name: 'Twitter', icon: 'fab fa-twitter', link: 'https://twitter.com' },
        { name: 'Instagram', icon: 'fab fa-instagram', link: 'https://instagram.com' }
      ],
      quickLinks: [
        { name: 'Home', href: '#home' },
        { name: 'About', href: '#about' },
        { name: 'Skills', href: '#skills' },
        { name: 'Projects', href: '#projects' },
        { name: 'Contact', href: '#contact' }
      ]
    }
  }
}
</script>
