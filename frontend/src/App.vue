<template>
  <div id="app">
    <!-- Home page always visible as background -->
    <Home v-if="showHomeBackground" :overlay-active="overlayActive" class="fixed inset-0 z-0 transition-all duration-500" :class="{ 'backdrop-blur-md brightness-75 pointer-events-none': overlayActive }" />
    
    <!-- Router view for other pages (login, register, etc.) shown as overlays -->
    <router-view v-slot="{ Component }">
      <transition name="modal-slide">
        <component :is="Component" class="relative z-10" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import Home from '@/pages/Home.vue'

const route = useRoute()

// Routes that should show as overlay on top of Home background
const overlayRoutes = []

// Show Home as background for overlay routes
const overlayActive = computed(() => overlayRoutes.includes(route.path))
const showHomeBackground = computed(() => overlayActive.value)

</script>

<style>
#app {
  font-family: Arial, sans-serif;
  background: #f5f5f5;
  min-height: 100vh;
  margin: 0;
}

/* Fade transition for overlay pages */
/* Modal slide transition */
.modal-slide-enter-active,
.modal-slide-leave-active {
  transition: all 0.8s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.modal-slide-enter-from {
  opacity: 0;
  transform: translateY(-50px) scale(0.95);
}
.modal-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(1.05);
}
.modal-slide-enter-to,
.modal-slide-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>

