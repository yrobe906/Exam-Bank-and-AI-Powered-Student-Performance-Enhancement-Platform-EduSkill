<template>
  <header class="max-w-7xl mx-auto px-6 py-6 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <div class="group w-14 h-14 rounded-full overflow-hidden bg-white/10 border border-white/20 
       shadow-xl flex items-center justify-center transition-all duration-500
       hover:scale-110 hover:-translate-y-1 hover:shadow-2xl hover:bg-white/20">

  <img 
    src="@/assets/images/logo.png" 
    alt="logo"
    class="w-full h-full object-cover transition-all duration-500 group-hover:scale-110"
  />
</div>

      <div>
        <h1 class="font-extrabold text-xl tracking-tight">KTech</h1>
        <p class="text-xs text-slate-300">Schools • Teachers • Students</p>
      </div>
    </div>

    <nav class="hidden md:flex items-center gap-6 text-sm text-slate-200">
      <a class="hover:underline" href="#features">Features</a>
      <a class="hover:underline" href="#pricing">Pricing</a>
      <a class="hover:underline" href="#demo">Demo</a>
      <button class="ml-2 px-4 py-2 rounded-full bg-white/10
      backdrop-blur-sm hover:bg-white/20 transition">Login</button>
    </nav>
  </header>
</template>
