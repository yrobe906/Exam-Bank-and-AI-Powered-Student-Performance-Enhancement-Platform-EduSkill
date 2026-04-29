<template>
  <div 
    class="min-h-screen relative overflow-x-hidden transition-all duration-500"
    :class="[
      isDark ? 'dark' : '',
      overlayActive ? 'backdrop-blur-xl brightness-75 saturate-50 pointer-events-none' : ''
    ]"
    ref="mainContainer"
    @mousemove="!overlayActive && handleMouseMove"
  >
    <!-- ==================== PARTICLE BACKGROUND ==================== -->
    <canvas 
      ref="particleCanvas" 
      class="fixed inset-0 z-0 pointer-events-none"
    ></canvas>

    <!-- ==================== NAVIGATION ==================== -->
    <header 
      class="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
      :class="[
        scrolled ? 'bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl shadow-lg' : 'bg-transparent',
        scrolled ? 'py-3' : 'py-5'
      ]"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <!-- Logo -->
          <div class="flex items-center space-x-3 cursor-pointer" @click="scrollToTop">
            <div class="relative w-12 h-12 rounded-xl overflow-hidden">
              <img 
                src="@/assets/images/eduskill-logo.png" 
                alt="EduSkill Hub Logo"
                class="w-full h-full object-contain"
              />
            </div>
            <span class="text-2xl font-bold bg-gradient-to-r from-purple-600 via-blue-500 to-cyan-400 bg-clip-text text-transparent">
              EduSkill Hub
            </span>
          </div>

          <!-- Mobile Menu Button -->
          <button 
            class="md:hidden relative w-10 h-10 flex flex-col justify-center items-center gap-1.5"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <span 
              class="w-6 h-0.5 bg-gray-700 dark:bg-white transition-all duration-300"
              :class="mobileMenuOpen ? 'rotate-45 translate-y-2' : ''"
            ></span>
            <span 
              class="w-6 h-0.5 bg-gray-700 dark:bg-white transition-all duration-300"
              :class="mobileMenuOpen ? 'opacity-0' : ''"
            ></span>
            <span 
              class="w-6 h-0.5 bg-gray-700 dark:bg-white transition-all duration-300"
              :class="mobileMenuOpen ? '-rotate-45 -translate-y-2' : ''"
            ></span>
          </button>

          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center space-x-1">
            <a 
              v-for="(item, index) in navItems" 
              :key="index"
              href="#" 
              @click.prevent="scrollToSection(item.section)"
              class="nav-link relative px-4 py-2 text-gray-800 dark:text-gray-200 font-medium hover:text-purple-600 dark:hover:text-cyan-400 transition-all duration-300"
            >
              <span class="relative z-10">{{ item.name }}</span>
              <span class="absolute inset-0 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 rounded-lg opacity-0 hover:opacity-100 transition-opacity"></span>
            </a>
          </nav>

          <!-- Auth Buttons -->
          <div class="hidden md:flex items-center space-x-4">
            <!-- Dark/Light Toggle -->
            <button 
              @click="toggleDarkMode"
              class="relative w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center hover:scale-110 transition-transform"
            >
              <span v-if="isDark" class="text-xl">☀️</span>
              <span v-else class="text-xl">🌙</span>
            </button>
            
            <button 
              @click="goToLogin"
              class="px-5 py-2.5 text-gray-800 dark:text-gray-200 font-semibold hover:text-purple-600 dark:hover:text-cyan-400 transition-all duration-300 relative overflow-hidden group cursor-pointer"
            >
              <span class="relative z-10">Sign In</span>
              <span class="absolute inset-0 bg-purple-100 dark:bg-purple-900/30 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"></span>
            </button>
            
            <button 
              @click="goToRegister"
              class="px-6 py-2.5 bg-gradient-to-r from-purple-600 via-blue-500 to-cyan-500 text-white rounded-xl font-semibold shadow-lg hover:shadow-purple-500/30 transition-all duration-300 transform hover:-translate-y-1 hover:scale-105 cursor-pointer"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div 
        class="md:hidden absolute top-full left-0 right-0 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl shadow-xl transition-all duration-500 overflow-hidden"
        :class="mobileMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'"
      >
        <div class="px-4 py-4 space-y-2">
          <a 
            v-for="(item, index) in navItems" 
            :key="index"
            href="#" 
            @click.prevent="scrollToSection(item.section); mobileMenuOpen = false"
            class="block px-4 py-3 text-gray-800 dark:text-gray-200 font-medium hover:bg-purple-50 dark:hover:bg-purple-900/30 rounded-lg transition-colors"
          >
            {{ item.name }}
          </a>
          <div class="pt-4 space-y-2 border-t border-gray-200 dark:border-gray-700">
            <button 
              @click="goToLogin; mobileMenuOpen = false"
              class="w-full px-4 py-3 text-center text-gray-800 dark:text-gray-200 font-medium border border-gray-300 dark:border-gray-600 rounded-xl hover:bg-purple-50 dark:hover:bg-purple-900/30 transition-colors cursor-pointer"
            >
              Sign In
            </button>
            <button 
              @click="goToRegister; mobileMenuOpen = false"
              class="w-full px-4 py-3 text-center bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-semibold cursor-pointer"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- ==================== HERO SECTION ==================== -->
    <section 
      id="hero"
      class="relative min-h-screen flex items-center justify-center overflow-hidden pt-20 bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900"
    >
      <!-- Animated Background -->
      <div class="absolute inset-0 z-0">
        <!-- Gradient Orbs - Adjusted colors for blue-black theme -->
        <div class="absolute top-20 left-20 w-96 h-96 bg-blue-600/20 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-float"></div>
        <div class="absolute bottom-20 right-20 w-96 h-96 bg-purple-600/20 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-float animation-delay-2000"></div>
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-600/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float animation-delay-4000"></div>
        
        <!-- Grid Pattern with blue tint -->
        <div class="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%233b82f6%22%20fill-opacity%3D%220.1%22%3E%3Cpath%20d%3D%22M36%2034v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6%2034v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6%204V0H4v4H0v2h4v4h2V6h4V4H6z%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-30"></div>
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Hero Content -->
          <div class="text-center lg:text-left" ref="heroContent">
            <!-- Animated Badge -->
            <div 
              class="inline-flex items-center px-5 py-2.5 rounded-full bg-blue-900/40 border border-blue-500/30 mb-8 animate-float"
            >
              <span class="w-2.5 h-2.5 bg-blue-400 rounded-full mr-2 animate-pulse"></span>
              <span class="text-sm font-semibold text-blue-300">🎯 AI-Powered Learning Platform</span>
            </div>

            <!-- Main Heading with Typewriter -->
            <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              <span class="block text-white">Transform Your</span>
              <span class="bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
                {{ typedText }}
                <span class="animate-pulse">|</span>
              </span>
            </h1>

            <!-- Subtitle -->
            <p class="text-xl text-blue-100 max-w-2xl mx-auto lg:mx-0 mb-10 leading-relaxed">
              Ethiopia's first AI-powered educational platform that combines exam preparation, 
              personalized learning, and performance analytics for Grade 9-12 students.
            </p>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row justify-center lg:justify-start gap-4 mb-12">
              <button 
                @click="goToRegister"
                class="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-2xl font-bold text-lg shadow-lg hover:shadow-xl hover:shadow-blue-500/30 transition-all duration-300 transform hover:-translate-y-2 hover:scale-105 group cursor-pointer"
              >
                <span class="relative z-10 flex items-center justify-center gap-2">
                  🚀 Start Learning Free
                  <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                  </svg>
                </span>
              </button>
              <button 
                @click="scrollToSection('features')"
                class="px-8 py-4 bg-gray-800/80 backdrop-blur-sm text-white rounded-2xl font-bold text-lg border-2 border-blue-500/50 hover:border-blue-400 hover:bg-gray-800/90 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
              >
                📚 Explore Features
              </button>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto lg:mx-0">
              <div 
                v-for="(stat, index) in heroStats" 
                :key="index"
                class="bg-gray-800/60 backdrop-blur-sm p-4 rounded-2xl border border-blue-500/30 hover:border-blue-400 hover:scale-105 transition-all duration-300 cursor-pointer"
                @click="goToRegister"
              >
                <div class="text-2xl md:text-3xl font-bold" :class="stat.color">{{ stat.value }}</div>
                <div class="text-xs md:text-sm text-blue-200">{{ stat.label }}</div>
              </div>
            </div>
          </div>

          <!-- 3D Visual Element -->
          <div class="relative hidden lg:block" ref="heroVisual">
            <div class="relative w-full aspect-square">
              <!-- Rotating Globe with blue tint -->
              <div class="globe-container">
                <div class="globe">
                  <div class="globe-inner">
                    <div class="globe-line lat" v-for="i in 5" :key="'lat'+i" style="border-color: rgba(59, 130, 246, 0.3);"></div>
                    <div class="globe-line lon" v-for="i in 5" :key="'lon'+i" style="border-color: rgba(59, 130, 246, 0.3);"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div class="w-6 h-10 border-2 border-blue-400 rounded-full flex justify-center pt-2">
          <div class="w-1.5 h-3 bg-blue-400 rounded-full animate-scroll"></div>
        </div>
      </div>
    </section>

    <!-- ==================== FEATURES SECTION ==================== -->
    <section 
      id="features" 
      class="py-24 relative overflow-hidden"
      :class="isDark ? 'bg-gray-900' : 'bg-gray-800'"
    >
      <!-- Section Background -->
      <div class="absolute inset-0">
        <div class="absolute top-0 left-1/4 w-96 h-96 bg-purple-200 dark:bg-purple-900/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30"></div>
        <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-200 dark:bg-blue-900/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30"></div>
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 text-white dark:text-white">
            Everything You Need to <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">Succeed</span>
          </h2>
          <p class="text-xl text-gray-300 dark:text-gray-300 max-w-2xl mx-auto">
            All-in-one platform for modern education with cutting-edge features
          </p>
        </div>

        <!-- Feature Cards Grid with Images -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="group relative bg-gray-800 dark:bg-gray-800 rounded-3xl overflow-hidden border border-gray-700 hover:border-purple-400 dark:hover:border-purple-500 transition-all duration-500 hover:shadow-2xl hover:shadow-purple-500/20 cursor-pointer"
            @click="handleFeatureClick(feature.cta)"
          >
            <!-- Feature Image -->
            <div class="h-48 overflow-hidden">
              <img 
                :src="feature.image" 
                :alt="feature.title"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
              />
              <!-- Overlay Gradient -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
            </div>
            
            <div class="p-6 relative z-10">
              <!-- Icon -->
              <div 
                class="absolute -top-12 right-6 w-16 h-16 rounded-2xl flex items-center justify-center text-3xl shadow-xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300"
                :class="feature.iconBg"
              >
                {{ feature.icon }}
              </div>

              <!-- Title -->
              <h3 class="text-xl font-bold mb-3 text-white dark:text-white group-hover:text-purple-400 dark:group-hover:text-cyan-400 transition-colors">
                {{ feature.title }}
              </h3>

              <!-- Description -->
              <p class="text-gray-300 dark:text-gray-300 mb-4 leading-relaxed">
                {{ feature.description }}
              </p>

              <!-- CTA Link -->
              <div class="flex items-center text-purple-400 dark:text-cyan-400 font-semibold group-hover:translate-x-2 transition-transform">
                <span>{{ feature.cta }}</span>
                <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== DASHBOARD PREVIEW SECTION ==================== -->
    <section 
      id="dashboard" 
      class="py-24 relative overflow-hidden"
      :class="isDark ? 'bg-gray-800' : 'bg-gradient-to-br from-gray-900 to-gray-800'"
    >
      <!-- Animated Background -->
      <div class="absolute inset-0">
        <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div class="absolute bottom-1/4 right-1/4 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 text-white">
            Smart Dashboards for <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">Everyone</span>
          </h2>
          <p class="text-xl text-gray-300 max-w-2xl mx-auto">
            Different interfaces for different educational roles
          </p>
        </div>

        <!-- Role Tabs -->
        <div class="flex flex-wrap justify-center gap-4 mb-12">
          <button 
            v-for="(role, index) in roles" 
            :key="index"
            @click="activeRole = role.id"
            :class="[
              'px-6 py-3 rounded-full font-semibold transition-all duration-300 transform hover:scale-105 cursor-pointer',
              activeRole === role.id 
                ? 'bg-white text-gray-900 shadow-lg shadow-purple-500/30' 
                : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700 border border-gray-600'
            ]"
          >
            <span class="mr-2">{{ role.icon }}</span>
            {{ role.name }}
          </button>
        </div>

        <!-- Dashboard Preview Carousel -->
        <div class="relative">
          <div 
            class="bg-gray-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-gray-700 cursor-pointer"
            :style="{ perspective: '1000px' }"
            @click="goToRegister"
          >
            <div class="grid lg:grid-cols-2 gap-8 items-center">
              <!-- Dashboard Visual -->
              <div class="relative" :style="{ transform: `rotateY(${rotateY}deg)`, transition: 'transform 0.5s ease' }">
                <div class="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-6 shadow-inner border border-gray-700">
                  <!-- Window Controls -->
                  <div class="flex space-x-2 mb-6">
                    <div class="w-3.5 h-3.5 bg-red-500 rounded-full"></div>
                    <div class="w-3.5 h-3.5 bg-yellow-500 rounded-full"></div>
                    <div class="w-3.5 h-3.5 bg-green-500 rounded-full"></div>
                  </div>
                  
                  <!-- Dashboard Content -->
                  <div class="space-y-4">
                    <div 
                      v-for="(item, idx) in activeDashboard.features" 
                      :key="idx"
                      class="bg-gray-800/50 rounded-xl p-4 border border-gray-700 hover:border-purple-500 transition-colors"
                    >
                      <div class="flex items-center justify-between mb-2">
                        <div class="h-4 bg-gray-700 rounded w-1/2 shimmer"></div>
                        <div class="h-4 bg-green-500/30 rounded-full px-3 py-1">
                          <div class="h-1.5 bg-green-500 rounded w-8"></div>
                        </div>
                      </div>
                      <div class="h-3 bg-gray-700/50 rounded w-3/4"></div>
                    </div>
                  </div>

                  <!-- Chart Animation -->
                  <div class="mt-6 p-4 bg-gray-800/50 rounded-xl border border-gray-700">
                    <div class="flex items-end justify-between h-24">
                      <div 
                        v-for="(bar, idx) in chartBars" 
                        :key="idx"
                        class="flex-1 mx-1 bg-gradient-to-t rounded-t"
                        :class="bar.gradient"
                        :style="{ height: bar.height, animationDelay: `${idx * 0.1}s` }"
                        @mouseenter="bar.height = bar.hoverHeight"
                        @mouseleave="bar.height = bar.originalHeight"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Dashboard Info -->
              <div>
                <h3 class="text-3xl font-bold mb-4 text-white">
                  {{ activeDashboard.title }}
                </h3>
                <p class="text-gray-300 mb-6 leading-relaxed">
                  {{ activeDashboard.description }}
                </p>
                
                <div class="space-y-4 mb-8">
                  <div 
                    v-for="(feature, idx) in activeDashboard.keyFeatures" 
                    :key="idx"
                    class="flex items-center"
                  >
                    <div class="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center mr-3">
                      <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                    </div>
                    <span class="text-gray-200">{{ feature }}</span>
                  </div>
                </div>

                <button 
                  @click.stop="goToRegister"
                  class="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl font-bold hover:shadow-xl hover:shadow-purple-500/30 transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
                >
                  Explore {{ activeDashboard.name }} Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== HOW IT WORKS SECTION ==================== -->
    <section 
      id="how-it-works" 
      class="py-24 relative"
      :class="isDark ? 'bg-gray-900' : 'bg-gray-800'"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 text-white dark:text-white">
            How <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">EduSkill Hub</span> Works
          </h2>
          <p class="text-xl text-gray-300 dark:text-gray-300 max-w-2xl mx-auto">
            Three simple steps to transform your learning journey
          </p>
        </div>

        <div class="relative">
          <!-- Progress Line -->
          <div class="hidden md:block absolute top-1/2 left-0 right-0 h-1 bg-gray-700 dark:bg-gray-700 -translate-y-1/2 z-0">
            <div 
              class="h-full bg-gradient-to-r from-purple-600 to-blue-600 transition-all duration-1000"
              :style="{ width: progressWidth }"
            ></div>
          </div>

          <div class="grid md:grid-cols-3 gap-8 relative z-10">
            <div 
              v-for="(step, index) in steps" 
              :key="index"
              class="text-center cursor-pointer"
              @click="goToRegister"
            >
              <!-- Step Circle -->
              <div 
                class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br flex items-center justify-center text-4xl shadow-lg transition-all duration-500 transform hover:scale-110"
                :class="[
                  step.completed || index < currentStep 
                    ? 'from-purple-600 to-blue-600 text-white' 
                    : 'from-gray-700 to-gray-800 dark:from-gray-700 dark:to-gray-800 text-gray-400',
                  index === currentStep ? 'animate-pulse ring-4 ring-purple-300' : ''
                ]"
                @mouseenter="step.completed = true"
              >
                {{ step.icon }}
              </div>

              <!-- Step Number -->
              <div 
                class="text-2xl font-bold mb-2"
                :class="index <= currentStep ? 'text-purple-400' : 'text-gray-500'"
              >
                {{ String(index + 1).padStart(2, '0') }}
              </div>

              <!-- Step Content -->
              <h3 class="text-xl font-bold mb-3 text-white dark:text-white">
                {{ step.title }}
              </h3>
              <p class="text-gray-300 dark:text-gray-300 leading-relaxed">
                {{ step.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== STATS SECTION ==================== -->
    <section 
      id="stats" 
      class="py-24 relative overflow-hidden"
      :class="isDark ? 'bg-gray-800' : 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900'"
    >
      <!-- Animated Background -->
      <div class="absolute inset-0">
        <div class="absolute top-0 left-0 w-full h-full bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%23ffffff%22%20fill-opacity%3D%220.03%22%3E%3Cpath%20d%3D%22M36%2034v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6%2034v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6%204V0H4v4H0v2h4v4h2V6h4V4H6z%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')]"></div>
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div 
            v-for="(stat, index) in stats" 
            :key="index"
            class="text-center cursor-pointer"
            @click="goToRegister"
          >
            <!-- Circular Progress -->
            <div class="relative w-32 h-32 mx-auto mb-6">
              <svg class="w-32 h-32 transform -rotate-90">
                <circle 
                  cx="64" cy="64" r="56" 
                  stroke="currentColor" 
                  stroke-width="8" 
                  fill="none" 
                  class="text-white/10"
                ></circle>
                <circle 
                  cx="64" cy="64" r="56" 
                  stroke="url(#gradient)" 
                  stroke-width="8" 
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="351"
                  :stroke-dashoffset="351 - (351 * stat.percentage / 100)"
                  class="transition-all duration-1000"
                ></circle>
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#8b5cf6"></stop>
                    <stop offset="100%" stop-color="#06b6d4"></stop>
                  </linearGradient>
                </defs>
              </svg>
              <!-- Stat Value -->
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-3xl font-bold text-white">
                  {{ stat.prefix }}{{ animatedStats[index] }}{{ stat.suffix }}
                </span>
              </div>
            </div>

            <!-- Stat Label -->
            <div class="text-xl font-semibold text-white mb-2">{{ stat.label }}</div>
            <div class="text-purple-300 text-sm">{{ stat.sublabel }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TESTIMONIALS SECTION ==================== -->
    <section 
      id="testimonials" 
      class="py-24 relative overflow-hidden"
      :class="isDark ? 'bg-gray-900' : 'bg-gray-800'"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 text-white dark:text-white">
            What Students <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">Say</span>
          </h2>
          <p class="text-xl text-gray-300 dark:text-gray-300">
            Hear from our successful learners
          </p>
        </div>

        <!-- Testimonials Carousel -->
        <div class="relative">
          <div class="overflow-hidden">
            <div 
              class="flex transition-transform duration-500"
              :style="{ transform: `translateX(-${currentTestimonial * 100}%)` }"
            >
              <div 
                v-for="(testimonial, index) in testimonials" 
                :key="index"
                class="w-full flex-shrink-0 px-4"
              >
                <div class="max-w-3xl mx-auto">
                  <div 
                    class="bg-gray-800 dark:bg-gray-800 rounded-3xl p-8 md:p-12 shadow-xl border border-gray-700 cursor-pointer"
                    @click="goToRegister"
                  >
                    <!-- Quote -->
                    <div class="text-6xl text-purple-400 mb-4">"</div>
                    <p class="text-xl md:text-2xl text-gray-200 dark:text-gray-200 leading-relaxed mb-8 text-center">
                      {{ testimonial.quote }}
                    </p>
                    
                    <!-- Author -->
                    <div class="flex items-center justify-center">
                      <div class="w-16 h-16 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 flex items-center justify-center text-2xl font-bold text-white mr-4">
                        {{ testimonial.initials }}
                      </div>
                      <div class="text-left">
                        <div class="font-bold text-white dark:text-white">{{ testimonial.name }}</div>
                        <div class="text-gray-400 dark:text-gray-400">{{ testimonial.role }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Navigation Dots -->
          <div class="flex justify-center mt-8 gap-2">
            <button 
              v-for="(t, index) in testimonials" 
              :key="index"
              @click="currentTestimonial = index"
              :class="[
                'w-3 h-3 rounded-full transition-all duration-300 cursor-pointer',
                currentTestimonial === index ? 'bg-purple-600 w-8' : 'bg-gray-600'
              ]"
            ></button>
          </div>

          <!-- Arrow Navigation -->
          <button 
            @click="prevTestimonial"
            class="absolute top-1/2 -left-4 transform -translate-y-1/2 w-12 h-12 bg-gray-700 dark:bg-gray-700 rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform cursor-pointer"
          >
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <button 
            @click="nextTestimonial"
            class="absolute top-1/2 -right-4 transform -translate-y-1/2 w-12 h-12 bg-gray-700 dark:bg-gray-700 rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform cursor-pointer"
          >
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- ==================== CTA SECTION ==================== -->
    <section 
      class="py-24 relative overflow-hidden"
      :class="isDark ? 'bg-gray-800' : 'bg-gradient-to-r from-purple-800 via-blue-800 to-cyan-800'"
    >
      <!-- Confetti Canvas -->
      <canvas ref="confettiCanvas" class="fixed inset-0 pointer-events-none z-50"></canvas>

      <!-- Animated Background -->
      <div class="absolute inset-0">
        <div class="absolute top-0 left-1/4 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
        <div class="absolute bottom-0 right-1/4 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <!-- Countdown Timer -->
        <div class="mb-8">
          <p class="text-purple-200 mb-4">Next Exam Season Starts In:</p>
          <div class="flex justify-center gap-4">
            <div 
              v-for="(unit, index) in countdown" 
              :key="index"
              class="bg-white/20 backdrop-blur-sm rounded-xl p-4 min-w-[80px]"
            >
              <div class="text-3xl font-bold text-white">{{ unit.value }}</div>
              <div class="text-xs text-purple-200 uppercase">{{ unit.label }}</div>
            </div>
          </div>
        </div>

        <h2 class="text-4xl md:text-5xl font-bold text-white mb-6">
          Ready to Transform Your Learning?
        </h2>
        <p class="text-xl text-purple-100 mb-10 max-w-2xl mx-auto">
          Join thousands of Ethiopian students already succeeding with EduSkill Hub
        </p>
        
        <div class="flex flex-col sm:flex-row justify-center gap-4">
          <button 
            @click="goToRegister"
            class="px-10 py-5 bg-white text-purple-800 rounded-2xl font-bold text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 group cursor-pointer"
          >
            <span class="flex items-center justify-center gap-2">
              🎓 Start Free Trial
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
              </svg>
            </span>
          </button>
          <button 
            @click="scrollToSection('features')"
            class="px-10 py-5 bg-transparent border-3 border-white text-white rounded-2xl font-bold text-lg hover:bg-white/10 transition-all duration-300 cursor-pointer"
          >
            📚 Learn More
          </button>
        </div>

        <p class="text-purple-200 mt-8">
          No credit card required • Free for first 100 students
        </p>
      </div>
    </section>

    <!-- ==================== FOOTER ==================== -->
    <footer 
      class="bg-gray-900 text-white py-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-4 gap-12">
          <!-- Logo & Description -->
          <div>
            <div class="flex items-center space-x-3 mb-6">
              <div class="relative w-12 h-12 rounded-xl overflow-hidden bg-white/10 p-2">
                <img 
                  src="@/assets/images/logo.png" 
                  alt="EduSkill Hub Logo"
                  class="w-full h-full object-contain"
                />
              </div>
              <span class="text-2xl font-bold">EduSkill Hub</span>
            </div>
            <p class="text-gray-400 leading-relaxed">
              Ethiopia's premier AI-powered educational platform for Grade 9-12 students.
            </p>
          </div>

          <!-- Quick Links -->
          <div>
            <h3 class="text-lg font-bold mb-4">Quick Links</h3>
            <ul class="space-y-3">
              <li><a href="#hero" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Home</a></li>
              <li><a href="#features" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Features</a></li>
              <li><a href="#dashboard" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Dashboard</a></li>
              <li><a href="#testimonials" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Testimonials</a></li>
            </ul>
          </div>

          <!-- Products -->
          <div>
            <h3 class="text-lg font-bold mb-4">Products</h3>
            <ul class="space-y-3">
              <li><a @click.prevent="goToRegister" class="text-gray-400 hover:text-white transition-colors cursor-pointer">AI Tutor</a></li>
              <li><a @click.prevent="goToRegister" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Exam Bank</a></li>
              <li><a @click.prevent="goToRegister" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Mock Tests</a></li>
              <li><a @click.prevent="goToRegister" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Analytics</a></li>
            </ul>
          </div>

          <!-- Contact -->
          <div>
            <h3 class="text-lg font-bold mb-4">Contact Us</h3>
            <ul class="space-y-3">
              <li class="flex items-center text-gray-400">
                <span class="mr-2">📧</span> support@eduskillhub.com
              </li>
              <li class="flex items-center text-gray-400">
                <span class="mr-2">📞</span> +251 952 405 391
              </li>
              <li class="flex items-center text-gray-400">
                <span class="mr-2">📍</span> Jimma, Ethiopia
              </li>
            </ul>
          </div>
        </div>

        <div class="border-t border-gray-800 mt-12 pt-8 text-center text-gray-500">
          <p>© 2026 EduSkill Hub. All rights reserved. Designed with ❤️ for Ethiopian Students.</p>
        </div>
      </div>
    </footer>

    <!-- ==================== FLOATING AI CHATBOT ==================== -->
    <button 
      @click="showChatbot = !showChatbot"
      class="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-transform z-50 group cursor-pointer"
    >
      <span class="text-2xl">🤖</span>
      <span class="absolute -top-14 right-0 bg-gray-900 text-white px-4 py-2 rounded-xl text-sm opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap shadow-lg">
        Ask AI Tutor
      </span>
      <span v-if="!showChatbot" class="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full animate-pulse"></span>
    </button>

    <!-- AUTH MODAL - World Class Premium -->
    <AuthModal 
:model-value="isModalOpen" @update:model-value="isModalOpen = $event"
      :type="modalType"
      @close="closeModal"
      @switch-to-login="modalType = 'login'"
      class="z-[1005]"
    />
    
    <!-- Chatbot Panel -->
    <Transition name="slide-up">
      <div 
        v-if="showChatbot"
        class="fixed bottom-24 right-6 w-96 h-[500px] bg-gray-800 dark:bg-gray-800 rounded-3xl shadow-2xl z-[999] overflow-hidden border border-gray-700"
      >
        <!-- Chat Header -->
        <div class="bg-gradient-to-r from-purple-600 to-blue-600 p-4 flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center mr-3">
              <span class="text-xl">🤖</span>
            </div>
            <div>
              <div class="font-bold text-white">AI Tutor</div>
              <div class="text-xs text-purple-200">Online • Ready to help</div>
            </div>
          </div>
          <button @click="showChatbot = false" class="text-white/80 hover:text-white cursor-pointer">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Chat Messages -->
        <div class="p-4 h-[340px] overflow-y-auto">
          <div v-for="(msg, index) in chatMessages" :key="index" class="mb-4">
            <div 
              :class="[
                'max-w-[80%] p-3 rounded-2xl',
                msg.isUser ? 'ml-auto bg-purple-600 text-white rounded-br-md' : 'bg-gray-700 text-white rounded-bl-md'
              ]"
            >
              {{ msg.text }}
            </div>
          </div>
        </div>

        <!-- Chat Input -->
        <div class="p-4 border-t border-gray-700">
          <div class="flex gap-2">
            <input 
              v-model="chatInput" 
              @keyup.enter="sendMessage"
              type="text" 
              placeholder="Ask a question..."
              class="flex-1 px-4 py-2 bg-gray-700 rounded-xl outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
            />
            <button 
              @click="sendMessage"
              class="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl hover:scale-105 transition-transform cursor-pointer"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import AuthModal from '@/components/AuthModal.vue'
import UserLogin from '@/pages/Users/UserLogin.vue'
import RegisterModal from '@/pages/RegisterModal.vue'

export default {
  name: 'HomePage',
  props: {
    overlayActive: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
    // UI State
      scrolled: false,
      isDark: false,
      mobileMenuOpen: false,
      showChatbot: false,
      
      // Auth Modal State
      isModalOpen: false,
      modalType: null, // 'login' | 'register'
      
      // Mouse tracking
      mouseX: 0,
      mouseY: 0,
      
      // Navigation
      navItems: [
        { name: 'Home', section: 'hero' },
        { name: 'Features', section: 'features' },
        { name: 'Dashboard', section: 'dashboard' },
        { name: 'How It Works', section: 'how-it-works' },
        { name: 'Testimonials', section: 'testimonials' }
      ],
      
      // Hero
      typedText: '',
      typewriterWords: ['Learning Experience', 'Exam Success', 'Future Goals', 'Knowledge'],
      typewriterIndex: 0,
      typewriterCharIndex: 0,
      typewriterDeleting: false,
      
      // Hero Stats
      heroStats: [
        { value: '5,000+', label: 'Active Students', color: 'text-blue-400' },
        { value: '10,000+', label: 'Exam Questions', color: 'text-cyan-400' },
        { value: '85%', label: 'Success Rate', color: 'text-green-400' },
        { value: '24/7', label: 'AI Tutor Support', color: 'text-purple-400' }
      ],
      
      // Features with high-quality images
      features: [
        {
          icon: '🤖',
          iconBg: 'bg-purple-900/30 text-purple-400',
          title: 'AI-Powered Tutor',
          description: '24/7 personalized learning assistance with instant answers to study questions.',
          cta: 'Try AI Chat',
          image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          icon: '📚',
          iconBg: 'bg-blue-900/30 text-blue-400',
          title: 'Comprehensive Exam Bank',
          description: 'Access thousands of past national exam papers with model answers and explanations.',
          cta: 'Browse Exams',
          image: 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          icon: '📊',
          iconBg: 'bg-green-900/30 text-green-400',
          title: 'Smart Analytics',
          description: 'Track your progress, identify weak areas, and get personalized study recommendations.',
          cta: 'View Analytics',
          image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          icon: '🏆',
          iconBg: 'bg-yellow-900/30 text-yellow-400',
          title: 'Gamified Learning',
          description: 'Earn badges, level up, and compete on leaderboards to make studying fun and engaging.',
          cta: 'See Leaderboard',
          image: 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          icon: '⏱️',
          iconBg: 'bg-red-900/30 text-red-400',
          title: 'Timed Mock Exams',
          description: 'Practice with realistic exam simulations and get instant feedback on your performance.',
          cta: 'Take Mock Test',
          image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          icon: '👥',
          iconBg: 'bg-indigo-900/30 text-indigo-400',
          title: 'Multi-Role Platform',
          description: 'Separate dashboards for Students, Teachers, Admins, and Education Offices.',
          cta: 'Explore Roles',
          image: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        }
      ],
      
      // Dashboard
      activeRole: 'student',
      roles: [
        { id: 'student', name: 'Student', icon: '📚' },
        { id: 'teacher', name: 'Teacher', icon: '👨‍🏫' },
        { id: 'admin', name: 'Admin', icon: '⚙️' },
        { id: 'education_office', name: 'Education Office', icon: '🏢' }
      ],
      dashboards: {
        student: {
          title: 'Student Dashboard',
          name: 'Student',
          description: 'Personalized learning environment with AI assistance, progress tracking, and exam preparation tools.',
          keyFeatures: [
            'AI-Powered Study Assistant',
            'Personalized Learning Path',
            'Real-time Progress Analytics',
            'Gamified Learning Experience',
            '24/7 Mock Test Access'
          ],
          features: ['Performance Chart', 'Upcoming Exams', 'Recent Activities', 'AI Recommendations']
        },
        teacher: {
          title: 'Teacher Dashboard',
          name: 'Teacher',
          description: 'Complete classroom management with student monitoring, content creation, and assessment tools.',
          keyFeatures: [
            'Class Performance Analytics',
            'Exam Creation & Management',
            'Student Progress Tracking',
            'Resource Library Management',
            'Communication Tools'
          ],
          features: ['Class Overview', 'Student Grades', 'Assignment Queue', 'Resource Library']
        },
        admin: {
          title: 'Admin Dashboard',
          name: 'Admin',
          description: 'Full platform management with user administration, system analytics, and content moderation.',
          keyFeatures: [
            'User & Role Management',
            'Platform Analytics',
            'Content Moderation',
            'System Configuration',
            'Billing & Subscription'
          ],
          features: ['User Statistics', 'System Health', 'Content Reports', 'Financial Overview']
        },
        education_office: {
          title: 'Education Officer Dashboard',
          name: 'Education Office',
          description: 'School level education monitoring with school comparison, performance analytics, and intervention planning.',
          keyFeatures: [
            'Multi-School Comparison',
            'Regional Performance Analytics',
            'Intervention Planning Tools',
            'Compliance Monitoring',
            'Report Generation'
          ],
          features: ['School Rankings', 'Regional Stats', 'Intervention Alerts', 'Report Templates']
        }
      },
      chartBars: [
        { height: '40%', hoverHeight: '70%', originalHeight: '40%', gradient: 'from-purple-500 to-purple-600' },
        { height: '60%', hoverHeight: '90%', originalHeight: '60%', gradient: 'from-blue-500 to-blue-600' },
        { height: '45%', hoverHeight: '80%', originalHeight: '45%', gradient: 'from-cyan-500 to-cyan-600' },
        { height: '75%', hoverHeight: '95%', originalHeight: '75%', gradient: 'from-green-500 to-green-600' },
        { height: '55%', hoverHeight: '85%', originalHeight: '55%', gradient: 'from-yellow-500 to-yellow-600' },
        { height: '80%', hoverHeight: '100%', originalHeight: '80%', gradient: 'from-red-500 to-red-600' },
        { height: '65%', hoverHeight: '90%', originalHeight: '65%', gradient: 'from-pink-500 to-pink-600' }
      ],
      rotateY: 0,
      
      // How It Works
      currentStep: 0,
      steps: [
        {
          icon: '📝',
          title: 'Sign Up & Set Goals',
          description: 'Create your account, select your grade and subjects, and set your academic goals.',
          completed: false
        },
        {
          icon: '🧠',
          title: 'Learn & Practice',
          description: 'Access study materials, take practice tests, and get help from AI tutor 24/7.',
          completed: false
        },
        {
          icon: '📈',
          title: 'Track & Improve',
          description: 'Monitor your progress, get personalized recommendations, and achieve better results.',
          completed: false
        }
      ],
      
      // Stats
      stats: [
        { value: 5000, prefix: '', suffix: '+', label: 'Active Students', sublabel: 'Growing daily', percentage: 85 },
        { value: 10000, prefix: '', suffix: '+', label: 'Exam Questions', sublabel: 'Updated regularly', percentage: 95 },
        { value: 85, prefix: '', suffix: '%', label: 'Success Rate', sublabel: 'Proven results', percentage: 85 },
        { value: 24, prefix: '', suffix: '/7', label: 'AI Tutor Support', sublabel: 'Always available', percentage: 100 }
      ],
      animatedStats: [0, 0, 0, 0],
      statsAnimated: false,
      
      // Testimonials
      currentTestimonial: 0,
      testimonials: [
        {
          quote: "EduSkill Hub transformed my exam preparation. The AI tutor helped me understand complex topics instantly, and I improved my scores by 40% in just 3 months!",
          name: 'Abebe Bekele',
          role: 'Grade 12 Student, Addis Ababa',
          initials: 'AB'
        },
        {
          quote: "As a teacher, this platform has made monitoring student progress so much easier. The analytics dashboard gives real insights into each student's performance.",
          name: 'Tigist Haile',
          role: 'Physics Teacher, Jimma',
          initials: 'TH'
        },
        {
          quote: "The mock exams are incredibly realistic. I felt fully prepared for my national exams and achieved outstanding results thanks to EduSkill Hub.",
          name: 'Dagmawi Negash',
          role: 'Grade 12 Student, Hawassa',
          initials: 'DN'
        }
      ],
      
      // Countdown
      countdown: [
        { label: 'Days', value: '00' },
        { label: 'Hours', value: '00' },
        { label: 'Minutes', value: '00' },
        { label: 'Seconds', value: '00' }
      ],
      countdownDate: new Date('2025-06-01'),
      
      // Chatbot
      chatInput: '',
      chatMessages: [
        { text: "Hello! I'm your AI tutor. How can I help you today?", isUser: false }
      ],
      
      // Refs
      particleCanvas: null,
      confettiCanvas: null,
      mainContainer: null,
      heroContent: null,
      heroVisual: null
    }
  },
  computed: {
    activeDashboard() {
      return this.dashboards[this.activeRole]
    },
    progressWidth() {
      return `${(this.currentStep / 2) * 100}%`
    }
  },
  watch: {
    isDark(newVal) {
      if (newVal) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      localStorage.setItem('darkMode', newVal)
    }
  },
    handleEsc(event) {
      if (event.key === 'Escape' && this.isModalOpen) {
        this.closeModal()
      }
    },
    mounted() {
      // Check dark mode
      this.isDark = localStorage.getItem('darkMode') === 'true'
      
      // ESC handler for modal
      document.addEventListener('keydown', this.handleEsc)
      
      // Initialize
      this.initParticles()
      this.initConfetti()
      this.initScrollHandler()
      this.initTypewriter()
      this.initCountdown()
      this.initStatsAnimation()
      this.initCarouselAutoRotate()
    },
    beforeUnmount() {
      document.removeEventListener('keydown', this.handleEsc)
      this.cleanup()
    },
  beforeUnmount() {
    this.cleanup()
  },
  methods: {
    // ==================== REDIRECTION METHODS ====================
    openModal(type) {
      this.modalType = type
      this.isModalOpen = true
      document.body.style.overflow = 'hidden'
    },
    closeModal() {
      this.isModalOpen = false
      this.modalType = null
      document.body.style.overflow = ''
    },
    goToLogin() {
      window.open(window.location.origin + '/user_login', '_blank');
    },
    
    goToRegister() {
      window.open(window.location.origin + '/register', '_blank');
    },
    
    handleFeatureClick(cta) {
      // Map feature CTAs to register page
      const registerTriggers = [
        'Try AI Chat',
        'Browse Exams',
        'View Analytics',
        'See Leaderboard',
        'Take Mock Test',
        'Explore Roles'
      ]
      
      if (registerTriggers.includes(cta)) {
        this.goToRegister()
      }
    },
    
    // ==================== INITIALIZATION ====================
    initScrollHandler() {
      window.addEventListener('scroll', () => {
        this.scrolled = window.scrollY > 50
      })
    },
    
    initParticles() {
      this.particleCanvas = this.$refs.particleCanvas
      if (!this.particleCanvas) return
      
      const ctx = this.particleCanvas.getContext('2d')
      let particles = []
      let animationId
      
      const resize = () => {
        this.particleCanvas.width = window.innerWidth
        this.particleCanvas.height = window.innerHeight
      }
      
      const createParticles = () => {
        particles = []
        const count = Math.floor((window.innerWidth * window.innerHeight) / 15000)
        for (let i = 0; i < count; i++) {
          particles.push({
            x: Math.random() * this.particleCanvas.width,
            y: Math.random() * this.particleCanvas.height,
            radius: Math.random() * 2 + 0.5,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            alpha: Math.random() * 0.5 + 0.2,
            color: `hsl(${Math.random() * 60 + 200}, 80%, 60%)`
          })
        }
      }
      
      const animate = () => {
        ctx.clearRect(0, 0, this.particleCanvas.width, this.particleCanvas.height)
        
        particles.forEach((p, i) => {
          // Move
          p.x += p.vx
          p.y += p.vy
          
          // Mouse interaction
          const dx = this.mouseX - p.x
          const dy = this.mouseY - p.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < 150) {
            p.x -= dx * 0.01
            p.y -= dy * 0.01
          }
          
          // Wrap around
          if (p.x < 0) p.x = this.particleCanvas.width
          if (p.x > this.particleCanvas.width) p.x = 0
          if (p.y < 0) p.y = this.particleCanvas.height
          if (p.y > this.particleCanvas.height) p.y = 0
          
          // Draw
          ctx.beginPath()
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
          ctx.fillStyle = p.color
          ctx.globalAlpha = p.alpha
          ctx.fill()
          
          // Connect nearby particles
          particles.slice(i + 1).forEach(p2 => {
            const dx = p.x - p2.x
            const dy = p.y - p2.y
            const dist = Math.sqrt(dx * dx + dy * dy)
            if (dist < 100) {
              ctx.beginPath()
              ctx.moveTo(p.x, p.y)
              ctx.lineTo(p2.x, p2.y)
              ctx.strokeStyle = `rgba(59, 130, 246, ${0.15 * (1 - dist / 100)})`
              ctx.stroke()
            }
          })
        })
        
        animationId = requestAnimationFrame(animate)
      }
      
      resize()
      createParticles()
      animate()
      
      window.addEventListener('resize', () => {
        resize()
        createParticles()
      })
    },
    
    initConfetti() {
      this.confettiCanvas = this.$refs.confettiCanvas
      if (!this.confettiCanvas) return
      
      this.confettiCanvas.width = window.innerWidth
      this.confettiCanvas.height = window.innerHeight
    },
    
    initTypewriter() {
      const type = () => {
        const currentWord = this.typewriterWords[this.typewriterIndex]
        
        if (!this.typewriterDeleting) {
          this.typedText = currentWord.substring(0, this.typewriterCharIndex + 1)
          this.typewriterCharIndex++
          
          if (this.typewriterCharIndex === currentWord.length) {
            setTimeout(() => {
              this.typewriterDeleting = true
            }, 2000)
          }
        } else {
          this.typedText = currentWord.substring(0, this.typewriterCharIndex - 1)
          this.typewriterCharIndex--
          
          if (this.typewriterCharIndex === 0) {
            this.typewriterDeleting = false
            this.typewriterIndex = (this.typewriterIndex + 1) % this.typewriterWords.length
          }
        }
        
        setTimeout(type, this.typewriterDeleting ? 50 : 100)
      }
      
      type()
    },
    
    initCountdown() {
      const update = () => {
        const now = new Date()
        const diff = this.countdownDate - now
        
        if (diff > 0) {
          const days = Math.floor(diff / (1000 * 60 * 60 * 24))
          const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
          const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
          const seconds = Math.floor((diff % (1000 * 60)) / 1000)
          
          this.countdown[0].value = String(days).padStart(2, '0')
          this.countdown[1].value = String(hours).padStart(2, '0')
          this.countdown[2].value = String(minutes).padStart(2, '0')
          this.countdown[3].value = String(seconds).padStart(2, '0')
        }
      }
      
      update()
      setInterval(update, 1000)
    },
    
    initStatsAnimation() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !this.statsAnimated) {
            this.statsAnimated = true
            this.animateStats()
          }
        })
      }, { threshold: 0.5 })
      
      setTimeout(() => {
        const statsSection = document.getElementById('stats')
        if (statsSection) observer.observe(statsSection)
      }, 100)
    },
    
    animateStats() {
      this.stats.forEach((stat, index) => {
        let current = 0
        const increment = stat.value / 50
        const timer = setInterval(() => {
          current += increment
          if (current >= stat.value) {
            current = stat.value
            clearInterval(timer)
          }
          this.animatedStats[index] = Math.floor(current)
        }, 30 + index * 10)
      })
    },
    
    initCarouselAutoRotate() {
      setInterval(() => {
        this.currentTestimonial = (this.currentTestimonial + 1) % this.testimonials.length
      }, 5000)
    },
    
    // ==================== EVENT HANDLERS ====================
    handleMouseMove(e) {
      this.mouseX = e.clientX
      this.mouseY = e.clientY
      
      // Update 3D tilt on cards
      this.updateCardTilt(e)
    },
    
    updateCardTilt(e) {
      const cards = document.querySelectorAll('.card-tilt')
      cards.forEach(card => {
        const rect = card.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
        const centerX = rect.width / 2
        const centerY = rect.height / 2
        
        const rotateX = (y - centerY) / 20
        const rotateY = (centerX - x) / 20
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`
      })
    },
    
    cleanup() {
      const cards = document.querySelectorAll('.card-tilt')
      cards.forEach(card => {
        card.style.transform = ''
      })
    },
    
    scrollToSection(sectionId) {
      const element = document.getElementById(sectionId)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    },
    
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    },
    
    toggleDarkMode() {
      this.isDark = !this.isDark
    },
    
    prevTestimonial() {
      this.currentTestimonial = (this.currentTestimonial - 1 + this.testimonials.length) % this.testimonials.length
    },
    
    nextTestimonial() {
      this.currentTestimonial = (this.currentTestimonial + 1) % this.testimonials.length
    },
    
    sendMessage() {
      if (!this.chatInput.trim()) return
      
      this.chatMessages.push({ text: this.chatInput, isUser: true })
      this.chatInput = ''
      
      // Simulate AI response
      setTimeout(() => {
        this.chatMessages.push({ 
          text: "I'm here to help! What would you like to know about our platform?", 
          isUser: false 
        })
      }, 1000)
    }
  }
}
</script>

<style scoped>
/* ==================== ANIMATIONS ==================== */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes scroll {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(15px); opacity: 0; }
}

.animate-scroll {
  animation: scroll 2s ease-in-out infinite;
}

/* ==================== SLIDE UP TRANSITION ==================== */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* ==================== FADE TRANSITION ==================== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ==================== GLOBE ANIMATION ==================== */
.globe-container {
  perspective: 1000px;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.globe {
  width: 300px;
  height: 300px;
  position: relative;
  transform-style: preserve-3d;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotateY(0deg) rotateX(20deg); }
  to { transform: rotateY(360deg) rotateX(20deg); }
}

.globe-inner {
  position: absolute;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.globe-line {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
}

.globe-line.lat {
  width: 200px;
  height: 200px;
  transform: translate(-50%, -50%) rotateX(90deg);
}

.globe-line.lon {
  width: 200px;
  height: 200px;
  transform: translate(-50%, -50%) rotateY(90deg);
}

/* ==================== SHIMMER EFFECT ==================== */
.shimmer {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* ==================== RESPONSIVE ADJUSTMENTS ==================== */
@media (max-width: 768px) {
  .globe {
    width: 200px;
    height: 200px;
  }
  
  .globe-line.lat,
  .globe-line.lon {
    width: 150px;
    height: 150px;
  }
}
</style>