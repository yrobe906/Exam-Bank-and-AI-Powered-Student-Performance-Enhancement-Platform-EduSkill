<template>
  <nav class="fixed top-0 left-0 w-full backdrop-blur-lg bg-black/30 z-50 px-6 py-4 border-b border-white/10">
    <div class="max-w-7xl mx-auto flex justify-between items-center">

      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
          <span class="text-xl font-bold">Y</span>
        </div>
        <h1 class="text-2xl font-bold tracking-wider">
          Yasin
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-500">
            RW
          </span>
        </h1>
      </div>

      <!-- Desktop Menu -->
      <ul class="hidden md:flex gap-8 text-lg">
        <li v-for="item in navItems" :key="item.name">
          <a
            :href="item.href"
            class="relative group hover:text-indigo-300 duration-300"
          >
            {{ item.name }}
            <span
              class="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-indigo-400 to-purple-500 group-hover:w-full duration-300"
            ></span>
          </a>
        </li>
      </ul>

      <!-- Actions -->
      <div class="flex items-center gap-4">
        <button
          @click="scrollToContact"
          class="px-6 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full hover:scale-105 duration-300 shadow-lg shadow-indigo-500/30"
        >
          Hire Me
        </button>

        <!-- Mobile Button -->
        <button @click="toggleMenu" class="md:hidden text-2xl">
          <i class="fas fa-bars"></i>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="isMenuOpen"
      class="md:hidden absolute top-full left-0 w-full bg-black/90 backdrop-blur-xl border-b border-white/10 px-6 py-8"
    >
      <div class="flex flex-col gap-6 text-center">
        <a
          v-for="item in navItems"
          :key="item.name"
          :href="item.href"
          class="text-xl py-3 hover:text-indigo-400 duration-300 border-b border-white/10 last:border-b-0"
          @click="toggleMenu"
        >
          {{ item.name }}
        </a>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'MyHeader',
  data() {
    return {
      isMenuOpen: false,
      navItems: [
        { name: 'Home', href: '#home' },
        { name: 'About', href: '#about' },
        { name: 'Skills', href: '#skills' },
        { name: 'Projects', href: '#projects' },
        { name: 'Contact', href: '#contact' }
      ]
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
    },
    scrollToContact() {
      this.isMenuOpen = false
      document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })
    }
  }
}
</script>
