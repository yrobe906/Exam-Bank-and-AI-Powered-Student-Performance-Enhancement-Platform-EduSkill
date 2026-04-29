<template>
  <footer class="max-w-7xl mx-auto px-6 py-12 text-slate-300">
    <div class="flex flex-col md:flex-row justify-between items-start gap-6">
      <div>
        <h4 class="font-bold">EduSphere</h4>
        <p class="text-sm mt-2 text-slate-400 max-w-xs">
          Built for modern schools. Manage exams, classes and video tutors.
        </p>
      </div>

      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <h5 class="font-semibold">Product</h5>
          <ul class="mt-2 space-y-2">
            <li>Features</li>
            <li>Pricing</li>
            <li>Demo</li>
          </ul>
        </div>
        <div>
          <h5 class="font-semibold">Company</h5>
          <ul class="mt-2 space-y-2">
            <li>About</li>
            <li>Contact</li>
            <li>Privacy</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="mt-8 text-xs text-slate-500">
      © {{ new Date().getFullYear() }} — All rights reserved.
    </div>
  </footer>
</template>
