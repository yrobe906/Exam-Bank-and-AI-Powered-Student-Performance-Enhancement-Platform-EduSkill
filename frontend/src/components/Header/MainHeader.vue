<template>
  <header class="w-full h-full bg-white/95 backdrop-blur-xl border-b border-slate-200 shadow-sm flex items-center justify-between px-4 md:px-6">
    <!-- Left Section -->
    <div class="flex items-center gap-3">
      <!-- Mobile Menu Toggle -->
      <button
        @click="$emit('toggle-sidebar')"
        class="md:hidden inline-flex flex-col items-center justify-center w-10 h-10 rounded-xl bg-slate-100 text-slate-700 shadow-sm border border-slate-200 transition hover:bg-slate-200 p-2"
        aria-label="Toggle sidebar"
      >
        <span class="block w-5 h-0.5 bg-slate-700 mb-1"></span>
        <span class="block w-5 h-0.5 bg-slate-700 mb-1"></span>
        <span class="block w-5 h-0.5 bg-slate-700"></span>
      </button>

      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 md:w-12 md:h-12 rounded-2xl bg-white shadow-sm overflow-hidden flex items-center justify-center">
          <img src="/eduSkill-logo.png" alt="EduSkill Logo" class="h-full w-full object-contain" />
        </div>
        <div class="leading-tight">
          <p class="text-slate-900 text-sm md:text-base font-semibold">EduSkill Hub</p>
          <p class="text-slate-500 text-xs">Admin Portal</p>
        </div>
      </div>
    </div>

    <!-- Right Section -->
    <div class="flex items-center gap-4">
      <span class="text-slate-500 text-sm hidden md:block">Admin Panel</span>
      <button
        @click="logout"
        class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 md:px-4 py-2 rounded-2xl text-sm transition shadow-sm"
      >
        Logout
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: "MainHeader",
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    }
  }
};
</script>
