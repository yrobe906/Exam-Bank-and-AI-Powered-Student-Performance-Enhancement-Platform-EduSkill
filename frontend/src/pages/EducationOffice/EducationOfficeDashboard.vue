<template>
  <DashboardLayout 
    @nav-click="handleNavClick"
    @view-change="handleViewChange"
    @scroll-sidebar-up="scrollSidebarUp"
    @scroll-sidebar-down="scrollSidebarDown"
  >
    <template #header="{ activeNav, toggleMobileMenu, handleNavClick }">
      <!-- Custom Header: With Logo on Left End and Navigation on All Screens -->
      <div class="flex items-center justify-between px-4 md:px-6 py-4 bg-white border-b border-slate-200">
        <!-- Left: Logo + Mobile Toggle + Navigation (Always visible on all screens) -->
        <div class="flex items-center gap-4 flex-1 min-w-0">
          <!-- Logo - Always on left end -->
          <img 
            src="@/assets/images/eduskill-logo.png" 
            alt="EduSkill" 
            class="h-9 w-auto lg:h-10 object-contain flex-shrink-0"
          />
          
          <!-- Mobile Toggle (visible only on mobile) -->
          <button 
            @click="toggleMobileMenu" 
            class="lg:hidden p-2 rounded-lg hover:bg-slate-100 text-slate-700 flex-shrink-0"
            :aria-label="sidebarOpen ? 'Close menu' : 'Open menu'"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!sidebarOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <!-- Navigation - Visible on all screens, scrollable on mobile -->
          <div class="flex items-center gap-1 overflow-x-auto hide-scrollbar flex-1 min-w-0">
            <button 
              v-for="(item, index) in headerNavItems.slice(0,3)" 
              :key="index"
              @click="handleNavClick(item, index)"
              :class="[
                'px-3 py-2 rounded-xl text-sm font-medium transition-all flex items-center gap-2 whitespace-nowrap flex-shrink-0',
                activeNav === index 
                  ? 'bg-[#1e3c72] text-white shadow-lg' 
                  : 'text-slate-600 hover:bg-slate-100 hover:text-[#1e3c72]'
              ]"
            >
              <component :is="item.icon" class="w-4 h-4" />
              {{ item.label }}
            </button>
          </div>
        </div>

        <!-- Right: Profile Dropdown -->
        <div class="flex items-center gap-3 relative flex-shrink-0">
          <!-- Refresh Button -->
          <button @click="refreshData" class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all">
            <svg class="w-5 h-5" :class="isRefreshing ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          <!-- Profile Dropdown -->
          <div class="flex items-center gap-3 cursor-pointer group" @click="showProfileDropdown = !showProfileDropdown">
            <!-- Profile Photo -->
            <img 
              :src="profileData.profile_photo || `https://api.dicebear.com/7.x/avataaars/svg?seed=${profileData.full_name}`" 
              :alt="profileData.full_name"
              class="w-10 h-10 rounded-2xl object-cover border-2 border-slate-200 shadow-md hover:shadow-lg transition-all group-hover:scale-105"
              @error="handleImageError"
            />
            <!-- Name (hidden on smaller screens) -->
            <div class="hidden md:block">
              <p class="font-semibold text-slate-800 text-sm truncate max-w-32">{{ profileData.full_name }}</p>
              <p class="text-xs text-slate-500">Education Office</p>
            </div>
            <!-- Chevron -->
            <svg class="w-4 h-4 text-slate-400 group-hover:text-slate-600 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :class="['transform transition-transform', showProfileDropdown ? 'rotate-180' : '']" d="M19 9l-7 7-7-7" />
            </svg>
          </div>

          <!-- Dropdown Menu -->
          <div 
            v-if="showProfileDropdown"
            class="absolute top-full right-0 mt-2 w-56 bg-white rounded-2xl shadow-2xl border border-slate-100 py-2 z-50 animate-in slide-in-from-top-2 duration-200"
          >
            <div class="px-4 py-3 border-b border-slate-100">
              <div class="flex items-center gap-3">
                <img 
                  :src="profileData.profile_photo || `https://api.dicebear.com/7.x/avataaars/svg?seed=${profileData.full_name}`" 
                  class="w-12 h-12 rounded-xl object-cover border-2 border-slate-200 shadow-md"
                  @error="handleImageError"
                />
                <div>
                  <p class="font-semibold text-slate-800">{{ profileData.full_name }}</p>
                  <p class="text-sm text-slate-500">Education Office</p>
                </div>
              </div>
            </div>
            <button 
              class="w-full text-left px-4 py-3 hover:bg-slate-50 transition-colors flex items-center gap-3 text-slate-700 hover:text-[#1e3c72]"
              @click="handleMyProfile"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              My Profile
            </button>
            <button 
              class="w-full text-left px-4 py-3 hover:bg-red-50 border-t border-slate-100 transition-colors text-slate-700 hover:text-red-600"
              @click="handleLogout"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
    </template>

    <template #sidebar="{ sidebarOpen, activeNav, handleNavClick, closeSidebar, canScrollSidebarUp, canScrollSidebarDown, scrollSidebarUp, scrollSidebarDown }">
      <EducationOfficeSidebar 
        :is-open="sidebarOpen"
        @update:is-open="closeSidebar"
        :active-nav="activeNav"
        :nav-items="navItems"
        :officer-profile="profileData"
        :can-scroll-up="canScrollSidebarUp"
        :can-scroll-down="canScrollSidebarDown"
        @nav-click="handleNavClick"
        @scroll-up="scrollSidebarUp"
        @scroll-down="scrollSidebarDown"
        @logout="handleLogout"
      />
    </template>

    <template #main="{ currentView }">
      <div class="px-4 md:px-6 py-8">
        <!-- CITY OVERVIEW DASHBOARD VIEW -->
        <template v-if="currentView === 'overview'">
          <div class="ml-0 !lg:ml-16 w-full">
            <div class="mb-8 animate-fade-in">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <h1 class="text-3xl font-bold text-[#1e293b]">School Overview Dashboard</h1>
                  <p class="text-slate-500 mt-1">Monitor student performance across Grades 9-12 in Jimma City</p>
                </div>
                <div class="flex items-center gap-3">
                  <span class="text-sm text-slate-500 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Last updated: {{ lastUpdated }}
                  </span>
                  <button @click="refreshData" class="p-2 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow text-[#1e3c72]">
                    <svg class="w-5 h-5" :class="isRefreshing ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- SECTION 1: CITY OVERVIEW METRICS -->
          <section class="mb-8">
            <h2 class="text-xl font-bold text-[#1e293b] mb-4 flex items-center gap-2">
              <span class="w-2 h-8 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full"></span>
              School Overview
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="group bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-transparent hover:border-[#1e3c72]/20 relative overflow-hidden animate-fade-in" style="animation-delay: 0.1s">
                <div class="absolute inset-0 bg-gradient-to-r from-[#1e3c72]/5 to-[#2a5298]/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div class="relative flex items-center justify-between">
                  <div>
                    <p class="text-slate-500 text-sm font-medium">Total Registered Students</p>
                    <p class="text-3xl font-bold text-[#1e293b] mt-2">{{ animatedValues.students }}</p>
                    <div class="flex items-center mt-2 text-sm">
                      <span class="text-[#10b981] flex items-center gap-1 font-medium">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
                        +12%
                      </span>
                      <span class="text-slate-400 ml-2">from last month</span>
                    </div>
                  </div>
                  <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#1e3c72] to-[#2a5298] flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">👨‍🎓</div>
                </div>
              </div>
              
              <div class="group bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-transparent hover:border-[#1e3c72]/20 relative overflow-hidden animate-fade-in" style="animation-delay: 0.2s">
                <div class="absolute inset-0 bg-gradient-to-r from-[#1e3c72]/5 to-[#2a5298]/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div class="relative flex items-center justify-between">
                  <div>
                    <p class="text-slate-500 text-sm font-medium">Registered Teachers</p>
                    <p class="text-3xl font-bold text-[#1e293b] mt-2">{{ animatedValues.teachers }}</p>
                    <div class="flex items-center mt-2 text-sm">
                      <span class="text-[#10b981] flex items-center gap-1 font-medium">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
                        +5%
                      </span>
                      <span class="text-slate-400 ml-2">new this month</span>
                    </div>
                  </div>
                  <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#0fb9b1] to-[#3b82f6] flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">👩‍🏫</div>
                </div>
              </div>
              
              <div class="group bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-transparent hover:border-[#1e3c72]/20 relative overflow-hidden animate-fade-in" style="animation-delay: 0.3s">
                <div class="absolute inset-0 bg-gradient-to-r from-[#1e3c72]/5 to-[#2a5298]/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div class="relative flex items-center justify-between">
                  <div>
                    <p class="text-slate-500 text-sm font-medium">Total Exams Added</p>
                    <p class="text-3xl font-bold text-[#1e293b] mt-2">{{ animatedValues.exams }}</p>
                    <div class="flex items-center mt-2 text-sm">
                      <span class="text-[#10b981] flex items-center gap-1 font-medium">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" /></svg>
                        +8%
                      </span>
                      <span class="text-slate-400 ml-2">since last update</span>
                    </div>
                  </div>
                  <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#f59e0b] to-[#f97316] flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">📚</div>
                </div>
              </div>
              
              <div class="group bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all duration-300 border border-transparent hover:border-[#1e3c72]/20 relative overflow-hidden animate-fade-in" style="animation-delay: 0.4s">
                <div class="absolute inset-0 bg-gradient-to-r from-[#1e3c72]/5 to-[#2a5298]/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div class="relative flex items-center justify-between">
                  <div>
                    <p class="text-slate-500 text-sm font-medium">Grade 12 Readiness</p>
                    <p class="text-3xl font-bold text-[#1e293b] mt-2">{{ animatedValues.readiness }}%</p>
                    <div class="w-full bg-slate-200 rounded-full h-2 mt-3 overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-[#1e3c72] to-[#0fb9b1] rounded-full transition-all duration-1000" :style="{ width: animatedValues.readiness + '%' }"></div>
                    </div>
                  </div>
                  <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#10b981] to-[#0fb9b1] flex items-center justify-center text-white text-2xl shadow-lg group-hover:scale-110 transition-transform">🎯</div>
                </div>
              </div>
            </div>
          </section>
        </template>

        <!-- GRADE PERFORMANCE VIEW -->
        <template v-if="currentView === 'grade-performance'">
          <div class="mb-8 animate-fade-in">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="flex items-center gap-4">
                <button 
                  @click="goBackToOverview" 
                  class="p-2 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow text-[#1e3c72] hover:bg-gray-50"
                  title="Back to Overview"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <div>
                  <h1 class="text-3xl font-bold text-[#1e293b]">Grade Performance Drill-Down</h1>
                  <p class="text-slate-500 mt-1">Detailed performance analysis by grade</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-sm text-slate-500 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Last updated: {{ lastUpdated }}
                </span>
              </div>
            </div>
          </div>
          
          <section class="mb-8">
            <div class="bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-shadow animate-fade-in">
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <h3 class="text-lg font-bold text-[#1e293b] flex items-center gap-2">
                  <span class="w-1 h-6 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full"></span>
                  Select Grade
                </h3>
                <div class="relative inline-block">
<select id="grade-performance-select" name="selectedGrade" v-model="selectedGrade" class="appearance-none bg-white border-2 border-[#1e3c72] text-[#1e3c72] px-6 py-2.5 pr-10 rounded-xl font-bold shadow-md hover:shadow-lg hover:border-[#0fb9b1] transition-all cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#0fb9b1] focus:border-[#0fb9b1]">
                    <option value="9">Grade 9</option>
                    <option value="10">Grade 10</option>
                    <option value="11">Grade 11</option>
                    <option value="12">Grade 12</option>
                  </select>
                  <svg class="w-5 h-5 absolute right-3 top-1/2 -translate-y-1/2 text-[#1e3c72] pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
              
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
                <div class="bg-gradient-to-br from-[#f8fafc] to-[#e2e8f0] rounded-xl p-4 border border-slate-200">
                  <p class="text-slate-500 text-sm">Total Students</p>
                  <p class="text-2xl font-bold text-[#1e293b]">{{ gradeData[selectedGrade]?.totalStudents?.toLocaleString() || 0 }}</p>
                </div>
                <div class="bg-gradient-to-br from-[#f8fafc] to-[#e2e8f0] rounded-xl p-4 border border-slate-200">
                  <p class="text-slate-500 text-sm">Grade Average</p>
                  <p class="text-2xl font-bold text-[#1e293b]">{{ gradeData[selectedGrade]?.average || 0 }}%</p>
                </div>
                <div class="bg-gradient-to-br from-[#f8fafc] to-[#e2e8f0] rounded-xl p-4 border border-slate-200">
                  <p class="text-slate-500 text-sm">Pass Rate</p>
                  <p class="text-2xl font-bold text-[#10b981]">{{ gradeData[selectedGrade]?.passRate || 0 }}%</p>
                </div>
              </div>
              
              <!-- Charts Row -->
              <div class="grid grid-cols-1 lg:grid-cols-5 gap-4">
                <!-- All Grades Performance -->
                <div class="lg:col-span-2">
                  <h4 class="text-md font-semibold text-[#1e293b] mb-3">All Grades Performance</h4>
                  <div class="h-56 lg:h-64">
                    <Bar :data="allGradesPerformanceData" :options="liquidBarChartOptions" />
                  </div>
                </div>
                <!-- Performance Distribution -->
                <div class="lg:col-span-3">
                  <h4 class="text-md font-semibold text-[#1e293b] mb-3">Performance Distribution - Grade {{ selectedGrade }}</h4>
                  <div class="h-56 lg:h-64 flex items-center justify-center">
                    <Pie :data="performanceDistributionData" :options="liquidPieChartOptions" />
                  </div>
                </div>
              </div>
            </div>
          </section>
        </template>

        <!-- SUBJECT LEADERBOARD VIEW -->
        <template v-if="currentView === 'subject-leaderboard'">
          <div class="mb-8 animate-fade-in">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="flex items-center gap-4">
                <button 
                  @click="goBackToOverview" 
                  class="p-2 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow text-[#1e3c72] hover:bg-gray-50"
                  title="Back to Overview"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <div>
                  <h1 class="text-3xl font-bold text-[#1e293b]">Subject Leaderboard</h1>
                  <p class="text-slate-500 mt-1">Ranked by Sections • {{ sectionData.length }} Sections</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <!-- Visualize Data Button -->
                <button 
                  @click="showChartModal = true"
                  :disabled="!selectedSection"
                  class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-xl font-medium shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                  </svg>
                  Visualize Data
                </button>

                <span class="text-sm text-slate-500 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Last updated: {{ lastUpdated }}
                </span>
                <button @click="loadSubjectFilters" class="p-2 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow text-[#1e3c72]">
                  <svg class="w-5 h-5" :class="isSubjectLeaderboardLoading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Filter Controls -->
          <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg mb-6">
            <div class="flex flex-wrap items-center gap-4">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
                <span class="text-sm font-medium text-slate-700">Filters:</span>
              </div>
              
              <!-- Grade Level Filter -->
              <select 
                v-model="subjectSelectedGrade"
                @change="loadSubjectFilters"
                class="px-4 py-2 bg-slate-100/50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 min-w-[140px]"
              >
                <option :value="null">All Grades</option>
                <option v-for="grade in availableGrades" :key="grade" :value="grade">
                  Grade {{ grade }}
                </option>
              </select>

              <!-- Section Category Filter -->
              <select 
                v-model="subjectSelectedCategory"
                @change="loadSubjectFilters"
                class="px-4 py-2 bg-slate-100/50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 min-w-[180px]"
              >
                <option value="all">All Categories</option>
                <option v-for="cat in categories" :key="cat.name" :value="cat.name">
                  {{ cat.name }}
                </option>
              </select>

              <!-- Search -->
              <div class="flex-1 min-w-[200px]">
                <div class="relative">
                  <svg class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <input 
                    v-model="subjectSearchQuery"
                    type="text"
                    placeholder="Search sections..."
                    class="w-full pl-10 pr-4 py-2 bg-slate-100/50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Stats Summary -->
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ sectionData.length }}</p>
                  <p class="text-sm text-slate-500">Total Sections</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-green-500 to-green-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ totalAttempts }}</p>
                  <p class="text-sm text-slate-500">Total Attempts</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ totalStudents }}</p>
                  <p class="text-sm text-slate-500">Active Students</p>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-amber-500 to-amber-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ topSection?.section_name || 'N/A' }}</p>
                  <p class="text-sm text-slate-500">Top Section</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Leaderboard Cards -->
          <section class="space-y-6">
            <div class="flex items-center gap-2">
              <div class="w-1 h-6 bg-gradient-to-b from-[#1e3c72] to-[#0fb9b1] rounded-full"></div>
              <h2 class="text-lg font-bold text-[#1e293b]">Section Rankings</h2>
            </div>
            
            <div class="grid gap-4">
              <div 
                v-for="section in filteredSections" 
                :key="section.section_id"
                @click="selectSection(section)"
                class="bg-white rounded-2xl border border-slate-200/50 shadow-lg overflow-hidden hover:shadow-xl transition-all cursor-pointer"
                :class="{ 'ring-2 ring-blue-500': selectedSection?.section_id === section.section_id }"
              >
                <div class="p-5">
                  <div class="flex items-start gap-4">
                    <!-- Rank Badge -->
                    <div 
                      class="flex-shrink-0 w-14 h-14 rounded-xl flex items-center justify-center font-bold text-xl"
                      :class="getRankClass(section.rank)"
                    >
                      <span v-if="section.rank === 1">🥇</span>
                      <span v-else-if="section.rank === 2">🥈</span>
                      <span v-else-if="section.rank === 3">🥉</span>
                      <span v-else>#{{ section.rank }}</span>
                    </div>

                    <!-- Section Info -->
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2 mb-1">
                        <div 
                          class="w-3 h-3 rounded-full"
                          :style="{ backgroundColor: section.color }"
                        ></div>
                        <h3 class="text-lg font-bold text-gray-800 truncate">{{ section.section_name }}</h3>
                        <span class="px-2 py-0.5 bg-slate-100 text-slate-600 text-xs rounded-full">
                          {{ section.sector_name }}
                        </span>
                      </div>
                      
                      <div class="flex flex-wrap gap-4 text-sm text-slate-500 mb-3">
                        <div class="flex items-center gap-1">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          <span>{{ section.total_exam_attempts }} attempts</span>
                        </div>
                        <div class="flex items-center gap-1">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                          </svg>
                          <span>{{ section.unique_students }} students</span>
                        </div>
                        <div class="flex items-center gap-1">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                          </svg>
                          <span>{{ section.exams_count }} exams</span>
                        </div>
                      </div>

                      <!-- Progress Bar & Score -->
                      <div class="flex items-center gap-4">
                        <div class="flex-1">
                          <div class="flex items-center justify-between mb-1">
                            <span class="text-xs font-medium text-slate-600">Weighted Score</span>
                            <span class="text-sm font-bold" :class="getScoreClass(section.weighted_score)">
                              {{ section.weighted_score }}%
                            </span>
                          </div>
                          <div class="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                            <div 
                              class="h-full rounded-full transition-all duration-500"
                              :class="getScoreBarClass(section.weighted_score)"
                              :style="{ width: Math.min(section.weighted_score, 100) + '%' }"
                            ></div>
                          </div>
                        </div>
                        
                        <!-- Stats Grid -->
                        <div class="flex gap-4 text-center">
                          <div>
                            <p class="text-lg font-bold text-gray-800">{{ section.average_score }}%</p>
                            <p class="text-xs text-slate-500">Avg Score</p>
                          </div>
                          <div class="w-px bg-slate-200"></div>
                          <div>
                            <p class="text-lg font-bold text-gray-800">{{ section.normalized_attempts || 0 }}%</p>
                            <p class="text-xs text-slate-500">Attempts</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Actions -->
                    <div class="flex-shrink-0">
                      <button 
                        @click.stop="viewSectionDetails(section)"
                        class="p-2 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-600 transition-colors"
                        title="View Details"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredSections.length === 0 && !isSubjectLeaderboardLoading" class="bg-white rounded-2xl border border-slate-200/50 shadow-lg p-12 text-center">
              <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <p class="text-gray-500 text-lg">No sections found.</p>
              <p class="text-slate-400 text-sm mt-1">Sections will appear here once students take exams.</p>
            </div>
          </section>

          <!-- Section Details Modal -->
          <div v-if="showDetailsModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showDetailsModal = false"></div>
            <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden">
              <div class="flex items-center justify-between px-6 py-4 border-b border-slate-200">
                <div>
                  <h3 class="text-lg font-bold text-gray-800">
                    {{ selectedSection?.section_name }} - Exam Details
                  </h3>
                  <p class="text-sm text-slate-500">Performance breakdown by exam</p>
                </div>
                <button 
                  @click="showDetailsModal = false"
                  class="p-2 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
                <div v-if="sectionDetails.length > 0" class="space-y-3">
                  <div 
                    v-for="exam in sectionDetails" 
                    :key="exam.exam_id"
                    class="bg-slate-50 rounded-xl p-4 flex items-center justify-between"
                  >
                    <div>
                      <h4 class="font-medium text-gray-800">{{ exam.exam_name }}</h4>
                      <p class="text-sm text-slate-500">{{ exam.sector_name }} • {{ exam.total_questions }} questions</p>
                    </div>
                    <div class="text-right">
                      <p class="text-lg font-bold" :class="getScoreClass(exam.average_score)">
                        {{ exam.average_score }}%
                      </p>
                      <p class="text-sm text-slate-500">{{ exam.total_attempts }} attempts</p>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center py-8">
                  <p class="text-slate-500">No exam details available</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Chart Modal for Visualize Data -->
          <div v-if="showChartModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showChartModal = false"></div>
            <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden">
              <!-- Modal Header -->
              <div class="flex items-center justify-between px-6 py-4 border-b border-slate-200">
                <div>
                  <h3 class="text-lg font-bold text-gray-800">
                    {{ selectedSection?.section_name || 'Section' }} Analytics
                  </h3>
                  <p class="text-sm text-slate-500">Visualization of performance metrics</p>
                </div>
                <button 
                  @click="showChartModal = false"
                  class="p-2 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Modal Content -->
              <div class="p-6">
                <div class="h-80">
                  <Bar :data="chartData" :options="chartOptions" />
                </div>

                <!-- Summary Stats -->
                <div class="grid grid-cols-3 gap-4 mt-6">
                  <div class="bg-slate-50 rounded-xl p-4 text-center">
                    <p class="text-2xl font-bold text-blue-600">{{ selectedSection?.total_exam_attempts || 0 }}</p>
                    <p class="text-sm text-slate-500">Total Attempts</p>
                  </div>
                  <div class="bg-slate-50 rounded-xl p-4 text-center">
                    <p class="text-2xl font-bold text-green-600">{{ selectedSection?.average_score || 0 }}%</p>
                    <p class="text-sm text-slate-500">Average Score</p>
                  </div>
                  <div class="bg-slate-50 rounded-xl p-4 text-center">
                    <p class="text-2xl font-bold text-purple-600">{{ selectedSection?.weighted_score || 0 }}</p>
                    <p class="text-sm text-slate-500">Weighted Score</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- STUDENT PERFORMANCE VIEW -->
        <template v-if="currentView === 'student-performance'">
          <div class="mb-8 animate-fade-in">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div class="flex items-center gap-4">
                <button 
                  @click="goBackToOverview" 
                  class="p-2 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow text-[#1e3c72] hover:bg-gray-50"
                  title="Back to Overview"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <div>
                  <h1 class="text-3xl font-bold text-[#1e293b]">Student Performance Leaderboard</h1>
                  <p class="text-slate-500 mt-1">All Grades (9-12) • {{ studentPerformanceData.length }} Students</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-sm text-slate-500 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Last updated: {{ lastUpdated }}
                </span>
                <button @click="loadStudentPerformanceData" class="p-2 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow text-[#1e3c72]">
                  <svg class="w-5 h-5" :class="isStudentPerformanceLoading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Filter Controls -->
          <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg mb-6">
            <div class="flex flex-wrap items-center gap-4">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                </svg>
                <span class="text-sm font-medium text-slate-700">Sort by:</span>
              </div>
              <select 
                v-model="studentSortBy"
                class="px-4 py-2 bg-slate-100/50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              >
                <option value="rank">Rank</option>
                <option value="average_score">Score</option>
                <option value="total_exams">Exams Taken</option>
              </select>
            </div>
          </div>

          <!-- Performance Stats Summary -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ studentPerformanceData.length }}</p>
                  <p class="text-sm text-slate-500">Total Students</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-green-500 to-green-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ averageClassScore }}%</p>
                  <p class="text-sm text-slate-500">Class Average</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white rounded-2xl p-5 border border-slate-200/50 shadow-lg">
              <div class="flex items-center gap-3">
                <div class="p-3 bg-gradient-to-br from-amber-500 to-amber-600 rounded-xl">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                </div>
                <div>
                  <p class="text-2xl font-bold text-gray-800">{{ topPerformer?.full_name || topPerformer?.username || 'N/A' }}</p>
                  <p class="text-sm text-slate-500">Top Performer</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Leaderboard Table -->
          <div class="bg-white rounded-2xl border border-slate-200/50 shadow-lg overflow-hidden">
            <table class="w-full">
              <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
                <tr>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Rank</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Student</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Grade</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Total Exams</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Average Score</th>
                  <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Performance</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="student in sortedStudents" 
                  :key="student.id"
                  class="hover:bg-blue-50/50 transition-colors border-b border-slate-100"
                >
                  <td class="px-6 py-4">
                    <span 
                      class="inline-flex items-center justify-center w-10 h-10 rounded-full font-bold text-lg"
                      :class="getRankClass(student.rank)"
                    >
                      <span v-if="student.rank === 1">🥇</span>
                      <span v-else-if="student.rank === 2">🥈</span>
                      <span v-else-if="student.rank === 3">🥉</span>
                      <span v-else>#{{ student.rank }}</span>
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <img
                        :src="getProfilePhotoUrl(student.profile_photo, student.username)"
                        :alt="student.username"
                        class="w-12 h-12 rounded-xl object-cover border-2 border-white shadow"
                        @error="handleImageError"
                      />
                      <div>
                        <p class="font-semibold text-gray-800">{{ student.full_name || student.username }}</p>
                        <p class="text-xs text-slate-500">@{{ student.username }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                      Grade {{ student.grade }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                      <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span class="text-gray-700 font-medium">{{ student.total_exams_taken }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span 
                      class="text-lg font-bold"
                      :class="getScoreClass(student.average_score)"
                    >
                      {{ student.average_score }}%
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                      <div class="w-32 h-2.5 bg-slate-100 rounded-full overflow-hidden">
                        <div 
                          class="h-full rounded-full transition-all duration-500"
                          :class="getScoreBarClass(student.average_score)"
                          :style="{ width: student.average_score + '%' }"
                        ></div>
                      </div>
                      <span 
                        class="text-xs font-semibold px-2 py-1 rounded-full"
                        :class="getPerformanceBadgeClass(student.average_score)"
                      >
                        {{ getPerformanceLabel(student.average_score) }}
                      </span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <!-- Empty State -->
            <div v-if="studentPerformanceData.length === 0" class="p-12 text-center">
              <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
              <p class="text-gray-500 text-lg">No students found for this grade.</p>
              <p class="text-slate-400 text-sm mt-1">Students will appear here once they take exams.</p>
            </div>
          </div>
        </template>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import { Bar, Line, Pie } from 'vue-chartjs'
import { 
  ChartBarIcon, ChartPieIcon, BookOpenIcon, UserGroupIcon, 
  DocumentTextIcon, MegaphoneIcon, Cog6ToothIcon 
} from '@heroicons/vue/24/outline'

// Import layout components
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import EducationOfficeSidebar from '@/components/Sidebar/EducationOfficeSidebar.vue'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend, Filler)

const router = useRouter()

// Profile data from localStorage
const profileData = ref({
  full_name: 'Education Officer',
  profile_photo: ''
})

const showProfileDropdown = ref(false)

// Load profile on mount
watchEffect(() => {
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (user.full_name && user.profile_photo) {
      const normalizedPhoto = user.profile_photo.replace(/\\/g, '/').replace(/^\/+/, '')
      if (!normalizedPhoto.startsWith('uploads/')) {
        normalizedPhoto = 'uploads/' + normalizedPhoto
      }
      profileData.value = {
        full_name: user.full_name,
        profile_photo: user.profile_photo.startsWith('http')
          ? user.profile_photo
          : `http://127.0.0.1:8000/${normalizedPhoto}`
      }
    }
  } catch (e) {
    console.warn('Profile load error:', e)
  }
})

// State variables
const sidebarOpen = ref(false)
const activeNav = ref(0)
const currentView = ref('overview')
const selectedGrade = ref('9')
const isRefreshing = ref(false)
const isInitialLoading = ref(true)
const currentTime = ref('')
const lastUpdated = ref('')
const atRiskStudents = ref(0) // Set to 0 to remove fake data
const searchQuery = ref('')
const navRef = ref(null)
const mobileNavRef = ref(null)
const mainContentRef = ref(null)
const canScrollSidebarUp = ref(false)
const canScrollSidebarDown = ref(true)
const canScrollContentUp = ref(false)
const canScrollContentDown = ref(true)
const scrollProgress = ref(0)

// Chart data for visualization modal
const chartData = computed(() => ({
  labels: ['Total Attempts', 'Average Score', 'Weighted Score'],
  datasets: [{
    label: selectedSection.value?.section_name || 'Section',
    data: [
      selectedSection.value?.total_exam_attempts || 0,
      selectedSection.value?.average_score || 0,
      selectedSection.value?.weighted_score || 0
    ],
    backgroundColor: [
      'rgba(59, 130, 246, 0.8)',
      'rgba(16, 185, 129, 0.8)',
      'rgba(139, 92, 246, 0.8)'
    ],
    borderColor: [
      'rgb(59, 130, 246)',
      'rgb(16, 185, 129)',
      'rgb(139, 92, 246)'
    ],
    borderWidth: 2,
    borderRadius: 8
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { backgroundColor: 'rgba(0, 0, 0, 0.8)', padding: 12, cornerRadius: 8 }
  },
  scales: {
    y: { beginAtZero: true, grid: { color: 'rgba(0, 0, 0, 0.05)' } },
    x: { grid: { display: false } }
  }
}

// Subject Leaderboard state
const isSubjectLeaderboardLoading = ref(false)
const sectionData = ref([])
const availableGrades = ref([])
const categories = ref([])
const sectionDetails = ref([])
const subjectSelectedGrade = ref(null)
const subjectSelectedCategory = ref('all')
const subjectSearchQuery = ref('')
const selectedSection = ref(null)
const showChartModal = ref(false)
const showDetailsModal = ref(false)

// Student Performance state
const isStudentPerformanceLoading = ref(false)
const apiError = ref(null)
const isDataLoading = ref(true)
const studentPerformanceData = ref([])
const studentSortBy = ref('rank')

const animatedValues = ref({ students: 0, teachers: 0, exams: 0, average: 0, readiness: 0 })

// Header navigation items
const headerNavItems = [
  { icon: ChartBarIcon, label: 'Overview', view: 'overview', index: 0 },
  { icon: ChartPieIcon, label: 'Grade Performance', view: 'grade-performance', index: 1 },
  { icon: BookOpenIcon, label: 'Subject Leaderboard', view: 'subject-leaderboard', index: 2 }
]

const navItems = [
  { icon: ChartBarIcon, label: 'City Overview', view: 'overview', index: 0 },
  { icon: ChartPieIcon, label: 'Grade Performance', view: 'grade-performance', index: 1 },
  { icon: BookOpenIcon, label: 'Subject Leaderboard', view: 'subject-leaderboard', index: 2 }
]

const gradeData = ref({
  '9': { totalStudents: 0, average: 0, passRate: 0 },
  '10': { totalStudents: 0, average: 0, passRate: 0 },
  '11': { totalStudents: 0, average: 0, passRate: 0 },
  '12': { totalStudents: 0, average: 0, passRate: 0 }
})

const performanceDistribution = ref({
  '9': { top_performers: 0, average: 0, below_average: 0, failing: 0 },
  '10': { top_performers: 0, average: 0, below_average: 0, failing: 0 },
  '11': { top_performers: 0, average: 0, below_average: 0, failing: 0 },
  '12': { top_performers: 0, average: 0, below_average: 0, failing: 0 }
})

// Computed properties
const allGradesPerformanceData = computed(() => ({
  labels: ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'],
  datasets: [{
    label: 'Average Score %',
    data: [
      gradeData.value['9']?.average || 0,
      gradeData.value['10']?.average || 0,
      gradeData.value['11']?.average || 0,
      gradeData.value['12']?.average || 0
    ],
    backgroundColor: ['rgba(30, 60, 114, 0.85)', 'rgba(30, 60, 114, 0.85)', 'rgba(30, 60, 114, 0.85)', 'rgba(239, 68, 68, 0.85)'],
    borderColor: ['#1e3c72', '#1e3c72', '#1e3c72', '#ef4444'],
    borderWidth: 2,
    borderRadius: 12,
    barThickness: 28
  }]
}))

const performanceDistributionData = computed(() => {
  const grade = selectedGrade.value
  const dist = performanceDistribution.value[grade] || { top_performers: 0, average: 0, below_average: 0, failing: 0 }
  const total = dist.top_performers + dist.average + dist.below_average + dist.failing
  const getPercentage = (value) => total > 0 ? Math.round((value / total) * 100) : 0
  return {
    labels: ['Top Performers (≥85%)', 'Average (50-85%)', 'Below Average (40-50%)', 'Failing (<40%)'],
    datasets: [{
      data: [getPercentage(dist.top_performers), getPercentage(dist.average), getPercentage(dist.below_average), getPercentage(dist.failing)],
      backgroundColor: ['rgba(16, 185, 129, 0.9)', 'rgba(59, 130, 246, 0.9)', 'rgba(245, 158, 11, 0.9)', 'rgba(239, 68, 68, 0.9)'],
      borderColor: ['rgba(16, 185, 129, 1)', 'rgba(59, 130, 246, 1)', 'rgba(245, 158, 11, 1)', 'rgba(239, 68, 68, 1)'],
      borderWidth: 2
    }]
  }
})

const filteredSections = computed(() => {
  if (!subjectSearchQuery.value) return sectionData.value
  const query = subjectSearchQuery.value.toLowerCase()
  return sectionData.value.filter(section => 
    section.section_name.toLowerCase().includes(query) ||
    section.sector_name.toLowerCase().includes(query)
  )
})

const totalAttempts = computed(() => {
  return sectionData.value.reduce((sum, s) => sum + s.total_exam_attempts, 0)
})

const totalStudents = computed(() => {
  return new Set(sectionData.value.flatMap(s => s.unique_students)).size
})

const topSection = computed(() => {
  return sectionData.value.find(s => s.rank === 1) || null
})

const sortedStudents = computed(() => {
  const data = [...studentPerformanceData.value]
  if (studentSortBy.value === 'average_score') {
    return data.sort((a, b) => b.average_score - a.average_score)
      .map((student, index) => ({ ...student, rank: index + 1 }))
  } else if (studentSortBy.value === 'total_exams') {
    return data.sort((a, b) => b.total_exams_taken - a.total_exams_taken)
      .map((student, index) => ({ ...student, rank: index + 1 }))
  }
  return data.sort((a, b) => a.rank - b.rank)
})

const averageClassScore = computed(() => {
  if (studentPerformanceData.value.length === 0) return 0
  const total = studentPerformanceData.value.reduce((sum, s) => sum + s.average_score, 0)
  return Math.round(total / studentPerformanceData.value.length)
})

const topPerformer = computed(() => {
  return studentPerformanceData.value.find(s => s.rank === 1) || null
})

// Chart options
const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { backgroundColor: '#1e293b', titleColor: '#fff', bodyColor: '#fff', padding: 12, cornerRadius: 8 } },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 12 } } },
    y: { beginAtZero: true, max: 100, grid: { color: '#e2e8f0' }, ticks: { color: '#64748b', font: { size: 12 }, callback: (value) => value + '%' } }
  }
}

const verticalBarOptions = { ...barChartOptions }

const liquidBarChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 2000, easing: 'easeOutQuart' },
  plugins: { legend: { display: false }, tooltip: { backgroundColor: '#1e293b', titleColor: '#fff', bodyColor: '#fff', padding: 12, cornerRadius: 8, callbacks: { label: (context) => `Average: ${context.raw}%` } } },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 11 } } },
    y: { beginAtZero: true, max: 100, grid: { color: '#e2e8f0' }, ticks: { color: '#64748b', font: { size: 11 }, callback: (value) => value + '%' } }
  }
}

const liquidPieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: { animateRotate: true, animateScale: true, duration: 2000, easing: 'easeOutQuart' },
  plugins: {
    legend: { position: 'right', labels: { color: '#64748b', font: { size: 11 }, padding: 10, usePointStyle: true, pointStyle: 'circle' } },
    tooltip: { backgroundColor: '#1e293b', titleColor: '#fff', bodyColor: '#fff', padding: 12, cornerRadius: 8, callbacks: { label: (context) => ` ${context.label}: ${context.raw}%` } }
  }
}

// Functions
const fetchGradePerformance = async () => {
  try {
    isDataLoading.value = true
    apiError.value = null
    const response = await api.get('/api/eduoffice/grade-performance')
    if (response) {
      const grades = ['9', '10', '11', '12']
      grades.forEach(grade => {
        const key = `grade_${grade}`
        if (response[key]) {
          gradeData.value[grade] = {
            totalStudents: response[key].total_students || 0,
            average: response[key].average_score || 0,
            passRate: response[key].pass_rate || 0
          }
        }
      })
    }
  } catch (error) { 
    console.error('Error fetching grade performance:', error)
    apiError.value = 'Failed to load grade data. Using mock data.'
    // Mock fallback data
    const mockData = { '9': {totalStudents: 3200, average: 68, passRate: 82}, '10': {totalStudents: 2950, average: 71, passRate: 85}, '11': {totalStudents: 2800, average: 65, passRate: 78}, '12': {totalStudents: 2500, average: 58, passRate: 72} }
    Object.keys(mockData).forEach(grade => {
      gradeData.value[grade] = mockData[grade]
    })
  } finally {
    isDataLoading.value = false
  }
}

const fetchPerformanceDistribution = async () => {
  try {
    apiError.value = null
    const response = await api.get('/api/eduoffice/grade-performance-distribution')
    if (response) {
      const grades = ['9', '10', '11', '12']
      grades.forEach(grade => {
        const key = `grade_${grade}`
        if (response[key]) {
          performanceDistribution.value[grade] = {
            top_performers: response[key].top_performers || 0,
            average: response[key].average || 0,
            below_average: response[key].below_average || 0,
            failing: response[key].failing || 0
          }
        }
      })
    }
  } catch (error) { 
    console.error('Error fetching performance distribution:', error)
    apiError.value = 'Using mock distribution data.'
    // Mock fallback
    const mockDist = { top_performers: 25, average: 45, below_average: 20, failing: 10 }
    const grades = ['9', '10', '11', '12']
    grades.forEach(grade => performanceDistribution.value[grade] = {...mockDist})
  }
}

const fetchSectionLeaderboard = async () => {
  isSubjectLeaderboardLoading.value = true
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    let url = 'http://127.0.0.1:8000/api/analytics/section-leaderboard?'
    if (subjectSelectedGrade.value) {
      url += `grade_level=${subjectSelectedGrade.value}&`
    }
    if (subjectSelectedCategory.value && subjectSelectedCategory.value !== 'all') {
      url += `section_category=${encodeURIComponent(subjectSelectedCategory.value)}`
    }
    
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const data = await response.json()
      sectionData.value = data.sections || []
    }
  } catch (error) { console.error('Error fetching section leaderboard:', error) }
  
  isSubjectLeaderboardLoading.value = false
}

const fetchStudentPerformance = async () => {
  isStudentPerformanceLoading.value = true
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/users/teacher/student-performance', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const data = await response.json()
      const studentsArray = data.students || data
      const sortedData = studentsArray.sort((a, b) => b.average_score - a.average_score)
      studentPerformanceData.value = sortedData.map((student, index) => ({
        ...student,
        rank: index + 1
      }))
    }
  } catch (error) { console.error('Error fetching student performance:', error) }
  
  isStudentPerformanceLoading.value = false
}

const fetchAvailableGrades = async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/analytics/section-leaderboard/grades', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const data = await response.json()
      availableGrades.value = data.grades || []
    }
  } catch (error) { console.error('Error fetching grades:', error) }
}

const fetchCategories = async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/analytics/section-leaderboard/categories', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const data = await response.json()
      categories.value = data.categories || []
    }
  } catch (error) { console.error('Error fetching categories:', error) }
}

const loadSectionDetails = async (sectionName) => {
  const token = localStorage.getItem('token')
  if (!token) return
  
  try {
    let url = `http://127.0.0.1:8000/api/analytics/section-leaderboard/${encodeURIComponent(sectionName)}/details`
    if (subjectSelectedGrade.value) {
      url += `?grade_level=${subjectSelectedGrade.value}`
    }
    
    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    if (response.ok) {
      const data = await response.json()
      sectionDetails.value = data.exams || []
    }
  } catch (error) { console.error('Error loading section details:', error) }
}

const getRankClass = (rank) => {
  if (rank === 1) return 'bg-yellow-100 text-yellow-700 border-2 border-yellow-300'
  if (rank === 2) return 'bg-gray-100 text-gray-700 border-2 border-gray-300'
  if (rank === 3) return 'bg-orange-100 text-orange-700 border-2 border-orange-300'
  return 'bg-slate-100 text-slate-600'
}

const getScoreClass = (score) => {
  if (score >= 70) return 'text-green-600'
  if (score >= 50) return 'text-amber-600'
  return 'text-red-600'
}

const getScoreBarClass = (score) => {
  if (score >= 70) return 'bg-gradient-to-r from-green-500 to-green-600'
  if (score >= 50) return 'bg-gradient-to-r from-amber-500 to-amber-600'
  return 'bg-gradient-to-r from-red-500 to-red-600'
}

const getPerformanceBadgeClass = (score) => {
  if (score >= 70) return 'bg-green-100 text-green-700'
  if (score >= 50) return 'bg-amber-100 text-amber-700'
  return 'bg-red-100 text-red-700'
}

const getPerformanceLabel = (score) => {
  if (score >= 80) return 'Excellent'
  if (score >= 70) return 'Good'
  if (score >= 50) return 'Average'
  return 'Needs Improvement'
}

const getProfilePhotoUrl = (profilePhoto, username) => {
  if (!profilePhoto) return `https://api.dicebear.com/7.x/avataaars/svg?seed=${username}`
  if (profilePhoto.startsWith('http')) return profilePhoto
  
  // Normalize path separators
  let normalizedPath = profilePhoto.replace(/\\/g, '/').replace(/^\/+/, '')
  if (!normalizedPath.startsWith('uploads/')) {
    normalizedPath = 'uploads/' + normalizedPath
  }
  
  return `http://127.0.0.1:8000/${normalizedPath}`
}

const handleImageError = (event) => {
  event.target.src = `https://api.dicebear.com/7.x/avataaars/svg?seed=${event.target.alt}`
}

const selectSection = (section) => {
  selectedSection.value = section
}

const viewSectionDetails = async (section) => {
  selectedSection.value = section
  showDetailsModal.value = true
  await loadSectionDetails(section.section_name)
}

const loadSubjectFilters = () => {
  Promise.all([fetchSectionLeaderboard(), fetchAvailableGrades(), fetchCategories()])
}

const loadStudentPerformanceData = () => {
  fetchStudentPerformance()
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
  lastUpdated.value = now.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true })
}

const fetchDashboardOverview = async () => {
  try {
    const response = await api.get('/api/eduoffice/dashboard-overview')
    if (response) {
      // Animate the counters with real data
      const duration = 2000, steps = 60, interval = duration / steps
      const targets = {
        students: response.total_students || 0,
        teachers: response.total_teachers || 0,
        exams: response.total_exams || 0,
        average: 64.5, // Keep this as it's not part of the overview
        readiness: response.grade_12_readiness || 0
      }
      let step = 0
      const timer = setInterval(() => {
        step++
        const progress = step / steps
        const easeOut = 1 - Math.pow(1 - progress, 3)
        animatedValues.value.students = Math.round(targets.students * easeOut).toLocaleString()
        animatedValues.value.teachers = Math.round(targets.teachers * easeOut)
        animatedValues.value.exams = Math.round(targets.exams * easeOut).toLocaleString()
        animatedValues.value.average = (targets.average * easeOut).toFixed(1)
        animatedValues.value.readiness = Math.round(targets.readiness * easeOut)
        if (step >= steps) {
          clearInterval(timer)
          animatedValues.value = {
            students: targets.students.toLocaleString(),
            teachers: targets.teachers,
            exams: targets.exams.toLocaleString(),
            average: targets.average.toFixed(1),
            readiness: targets.readiness
          }
        }
      }, interval)
    }
  } catch (error) {
    console.error('Error fetching dashboard overview:', error)
    // Fallback to zeros if API fails
    animatedValues.value = { students: '0', teachers: 0, exams: '0', average: '0.0', readiness: 0 }
  }
}

const refreshData = () => {
  isRefreshing.value = true
  fetchDashboardOverview().finally(() => {
    isRefreshing.value = false
    updateTime()
  })
}

const handleNavClick = (item, index) => {
  sidebarOpen.value = false
  
  if (item.to) {
    isRefreshing.value = true
    setTimeout(() => {
      isRefreshing.value = false
      router.push(item.to)
    }, 300)
  } else if (item.view) {
    activeNav.value = item.index || index
    currentView.value = item.view
    
    if (item.view === 'grade-performance') {
      Promise.all([fetchGradePerformance(), fetchPerformanceDistribution()])
    } else if (item.view === 'subject-leaderboard') {
      loadSubjectFilters()
    } else if (item.view === 'student-performance') {
      loadStudentPerformanceData()
    }
  } else {
    activeNav.value = index
    currentView.value = 'overview'
  }
}

const goBackToOverview = () => { 
  console.log('Going back to overview');
  currentView.value = 'overview'; 
  activeNav.value = 0;
}

const handleViewChange = (view) => {
  currentView.value = view;
  const viewToNavMap = {
    'overview': 0,
    'grade-performance': 1,
    'subject-leaderboard': 2,
    'student-performance': 3,
    'announcements': 5,
    'settings': 6
  };
  activeNav.value = viewToNavMap[view] || 0;
}

const checkSidebarScrollPosition = () => {
  if (navRef.value) {
    const { scrollTop, scrollHeight, clientHeight } = navRef.value
    canScrollSidebarUp.value = scrollTop > 0
    canScrollSidebarDown.value = scrollTop + clientHeight < scrollHeight
  }
  if (mobileNavRef.value) {
    const { scrollTop, scrollHeight, clientHeight } = mobileNavRef.value
    canScrollSidebarUp.value = scrollTop > 0
    canScrollSidebarDown.value = scrollTop + clientHeight < scrollHeight
  }
}

const scrollSidebarUp = () => {
  if (navRef.value && canScrollSidebarUp.value) {
    navRef.value.scrollBy({ top: -150, behavior: 'smooth' })
  }
  if (mobileNavRef.value && canScrollSidebarUp.value) {
    mobileNavRef.value.scrollBy({ top: -150, behavior: 'smooth' })
  }
}

const scrollSidebarDown = () => {
  if (navRef.value && canScrollSidebarDown.value) {
    navRef.value.scrollBy({ top: 150, behavior: 'smooth' })
  }
  if (mobileNavRef.value && canScrollSidebarDown.value) {
    mobileNavRef.value.scrollBy({ top: 150, behavior: 'smooth' })
  }
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/user_login')
  showProfileDropdown.value = false
}

const handleMyProfile = () => {
  router.push('/eduoffice/settings')
  showProfileDropdown.value = false
}

const toggleMobileMenu = () => {
  sidebarOpen.value = !sidebarOpen.value
}

onMounted(() => {
  setTimeout(() => {
    isInitialLoading.value = false
  }, 1000)
  
  updateTime()
  setInterval(updateTime, 1000)
  fetchDashboardOverview()
  Promise.all([fetchGradePerformance(), fetchPerformanceDistribution()]).finally(() => {
    isDataLoading.value = false
  })
})
</script>

<style scoped>
/* Hide scrollbar for navigation on mobile */
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.6s ease-out forwards; opacity: 0; }
.animate-spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>