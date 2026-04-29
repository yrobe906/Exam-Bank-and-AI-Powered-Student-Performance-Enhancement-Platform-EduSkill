<template>
  <Transition 
    name="modal-auth" 
    @before-enter="beforeEnter" 
    @enter="enter" 
    @after-enter="afterEnter"
    @before-leave="beforeLeave"
    @leave="leave"
    @after-leave="afterLeave"
  >
    <div 
      v-if="isOpen"
      class="fixed inset-0 z-[1000] flex items-center justify-center p-4"
      @click.self="$emit('update:isOpen', false)"
      @keyup.esc="$emit('update:isOpen', false)"
      tabindex="0"
    >
      <!-- Premium Dark Overlay -->
      <div class="absolute inset-0 bg-black/40 backdrop-blur-md transition-opacity duration-300"></div>
      
      <!-- Centered Modal Card -->
      <div 
        ref="modalContent"
        class="relative w-full max-w-md mx-auto"
        :class="{ 'pointer-events-none': !isOpen }"
      >
        <!-- Close Button -->
        <button
          @click="$emit('update:isOpen', false)"
          class="absolute -top-4 -right-4 w-12 h-12 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-2xl flex items-center justify-center text-white/90 hover:text-white text-xl font-bold shadow-xl hover:shadow-2xl hover:scale-110 transition-all duration-300 z-10"
          aria-label="Close modal"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- Content Switcher -->
        <div v-if="type === 'login'">
          <UserLogin 
            :is-open="isOpen" 
            @close="$emit('update:isOpen', false)"
            class="!fixed !z-[1001] !max-w-none"
          />
        </div>
        
        <div v-else-if="type === 'register'">
          <RegisterModal 
            :is-open="isOpen" 
            @close="$emit('update:isOpen', false)"
            class="!fixed !z-[1001] !max-w-none"
          />
        </div>

        <!-- Tab Focus Trap -->
        <div class="sr-only" ref="focusEnd" tabindex="0" @focus="$refs.focusStart?.focus()"></div>
      </div>
    </div>
  </Transition>
</template>

<script>
import UserLogin from '@/pages/Users/UserLogin.vue'
import RegisterModal from '@/pages/RegisterModal.vue'

export default {
  name: 'AuthModal',
  components: {
    UserLogin,
    RegisterModal
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'login',
      validator: (value) => ['login', 'register'].includes(value)
    }
  },
  emits: ['update:modelValue', 'close'],
  directives: {
    trapFocus: {
      mounted(el) {
        el.setAttribute('tabindex', '-1')
        el.focus()
      }
    }
  },
  data() {
    return {
      transitioning: false
    }
  },
  computed: {
    isOpen: {
      get() { return this.modelValue },
      set(value) { this.$emit('update:modelValue', value) }
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        // Delay to ensure DOM rendered
        this.$nextTick(() => {
          this.$refs.focusStart?.focus()
          document.body.style.overflow = 'hidden'
        })
      } else {
        document.body.style.overflow = ''
      }
    }
  },
  mounted() {
    document.addEventListener('keydown', this.handleEsc)
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEsc)
    document.body.style.overflow = ''
  },
  methods: {
    handleEsc(event) {
      if (event.key === 'Escape' && this.isOpen) {
        this.$emit('update:modelValue', false)
      }
    },
    // Custom transition hooks for scale + fade
    beforeEnter(el) {
      this.transitioning = true
      el.style.opacity = '0'
      el.style.transform = 'scale(0.95)'
    },
    enter(el) {
      // GSAP-like animation with pure CSS
      requestAnimationFrame(() => {
        el.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)'
        el.style.opacity = '1'
        el.style.transform = 'scale(1)'
      })
    },
    afterEnter(el) {
      this.transitioning = false
      el.style.transition = ''
    },
    beforeLeave(el) {
      el.style.opacity = '1'
      el.style.transform = 'scale(1)'
    },
    leave(el) {
      requestAnimationFrame(() => {
        el.style.transition = 'all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)'
        el.style.opacity = '0'
        el.style.transform = 'scale(0.95)'
      })
    },
    afterLeave(el) {
      this.transitioning = false
      el.style.transition = ''
    }
  }
}
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Custom Modal Animation */
.modal-auth-enter-active,
.modal-auth-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-auth-enter-from,
.modal-auth-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.modal-auth-enter-to,
.modal-auth-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Prevent body scroll */
body.modal-open {
  overflow: hidden;
}

/* Responsive */
@media (max-width: 640px) {
  .max-w-md {
    max-width: 90vw;
    margin: 2rem;
  }
}
</style>

