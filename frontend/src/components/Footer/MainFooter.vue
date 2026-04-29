<template>
  <footer class="w-full h-12 bg-slate-900 flex items-center justify-center text-slate-400 text-sm border-t border-white/10">
    © {{ year }} EduSkill Hub — All Rights Reserved
  </footer>
</template>

<script>
export default {
  name: "MainFooter",
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
