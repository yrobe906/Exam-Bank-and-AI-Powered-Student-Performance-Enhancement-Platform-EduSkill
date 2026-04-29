<template>
  <!-- Register Modal - Premium SaaS Style -->
  <Transition name="modal">
    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-[1001] flex items-center justify-center p-4"
      @click.self="$emit('close')"
    >
      <!-- Glass Overlay -->
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>
      
      <!-- Centered Card - max-w-md -->
      <div class="relative w-full max-w-md mx-auto bg-[#141b2b]/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/10 overflow-hidden">
        
        <!-- Mini Background Effects -->
        <div class="absolute inset-0 opacity-50">
          <div class="absolute top-4 -left-20 w-32 h-32 bg-gradient-to-r from-violet-600/20 to-fuchsia-600/20 rounded-full blur-xl animate-pulse-slow"></div>
          <div class="absolute bottom-4 -right-20 w-32 h-32 bg-gradient-to-r from-blue-600/20 to-cyan-600/20 rounded-full blur-xl animate-pulse-slow" style="animation-delay: 2s;"></div>
        </div>
        
        <!-- Gradient Border -->
        <div class="absolute inset-0 rounded-3xl p-[2px] bg-gradient-to-r from-violet-500/40 via-fuchsia-500/40 to-cyan-500/40 animate-gradient-x"></div>
        
        <div class="relative z-10">
          <!-- Close Button -->
          <button 
            @click="$emit('close')"
            class="absolute top-4 right-4 w-10 h-10 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl flex items-center justify-center text-white hover:text-white text-lg font-bold shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300"
          >
            ✕
          </button>

          <!-- Stepper (Simplified for modal) -->
          <div class="flex items-center justify-center mb-6 pt-4">
            <div class="flex items-center space-x-2">
              <div :class="['w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shadow-lg transition-all',
                currentStep >= 1 ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white' : 'bg-white/10 text-white/50']">
                1
              </div>
              <div class="w-8 h-1 rounded-full" :class="currentStep >= 2 ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500' : 'bg-white/10'"></div>
              <div :class="['w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shadow-lg transition-all',
                currentStep >= 2 ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white' : 'bg-white/10 text-white/50']">
                2
              </div>
            </div>
          </div>

          <!-- Content -->
          <div class="p-6 space-y-4">
            <!-- Header -->
            <div class="text-center mb-4">
              <h2 class="text-xl font-bold text-white mb-1">Join EduSkill Hub</h2>
              <p class="text-white/60 text-sm">Create your account in 2 steps</p>
            </div>

            <!-- Step 1: Role Selection (compact) -->
            <div v-if="currentStep === 1" class="grid grid-cols-3 gap-2">
              <button 
                @click="selectRole('student')"
                :class="['group p-3 rounded-xl border-2 transition-all hover:scale-105 hover:shadow-xl',
                  role === 'student' ? 'border-violet-400 bg-violet-500/20 shadow-violet-500/25' : 'border-white/10 bg-white/5 hover:border-white/20']">
                <div class="flex flex-col items-center">
                  <span class="text-lg mb-1 group-hover:scale-110">📚</span>
                  <span class="text-xs font-medium text-white">Student</span>
                </div>
              </button>
              <button 
                @click="selectRole('teacher')"
                :class="['group p-3 rounded-xl border-2 transition-all hover:scale-105 hover:shadow-xl',
                  role === 'teacher' ? 'border-violet-400 bg-violet-500/20 shadow-violet-500/25' : 'border-white/10 bg-white/5 hover:border-white/20']">
                <div class="flex flex-col items-center">
                  <span class="text-lg mb-1 group-hover:scale-110">👨‍🏫</span>
                  <span class="text-xs font-medium text-white">Teacher</span>
                </div>
              </button>
              <button 
                @click="selectRole('eduoffice')"
                :class="['group p-3 rounded-xl border-2 transition-all hover:scale-105 hover:shadow-xl',
                  role === 'eduoffice' ? 'border-violet-400 bg-violet-500/20 shadow-violet-500/25' : 'border-white/10 bg-white/5 hover:border-white/20']">
                <div class="flex flex-col items-center">
                  <span class="text-lg mb-1 group-hover:scale-110">🏢</span>
                  <span class="text-xs font-medium text-white">Office</span>
                </div>
              </button>
            </div>

            <!-- Step 2: Form Fields (compact for modal) -->
            <form v-if="currentStep === 2" @submit.prevent="signup" class="space-y-3">
              
              <!-- Photo (compact) -->
              <div class="flex items-center space-x-3">
                <label class="cursor-pointer relative group">
                  <input type="file" accept="image/*" class="hidden" @change="handlePhoto" />
                  <div class="w-14 h-14 rounded-xl border-2 flex items-center justify-center overflow-hidden transition-all group-hover:scale-105"
                       :class="photoPreview ? 'border-emerald-400 shadow-md' : 'border-white/20 bg-white/5'">
                    <img v-if="photoPreview" :src="photoPreview" class="w-full h-full object-cover" />
                    <span v-else class="text-white/40 text-lg">📷</span>
                  </div>
                </label>
                <div class="text-xs">
                  <p class="text-white/70 font-medium">Photo</p>
                  <p class="text-white/40">Optional</p>
                </div>
              </div>

              <!-- Compact Form Fields -->
              <div class="space-y-2">
                <div class="relative">
                  <input v-model="name" @input="validateName" placeholder="Full name" 
                    class="w-full px-3 py-2.5 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-white/40 text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all" />
                </div>
                
                <div class="relative">
                  <input v-model="username" @input="validateUsername" placeholder="Username" 
                    class="w-full px-3 py-2.5 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-white/40 text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all" />
                </div>
                
                <div class="relative">
                  <input v-model="email" @input="validateEmail" type="email" placeholder="Email" 
                    class="w-full px-3 py-2.5 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-white/40 text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all" />
                </div>
                
                <div class="relative">
                  <input v-model="password" @input="validatePassword" :type="showPassword ? 'text' : 'password'" placeholder="Password" 
                    class="w-full px-3 py-2.5 pr-10 bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg text-white placeholder-white/40 text-sm focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all" />
                  <button @click="showPassword = !showPassword" type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white">
                    {{ showPassword ? '🙈' : '👁️' }}
                  </button>
                </div>

                <!-- Role-specific compact fields -->
                <template v-if="role === 'student'">
                  <div class="grid grid-cols-2 gap-2">
                    <input v-model="school_id" @input="validateSchool" placeholder="School ID" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm" />
                    <select v-model="grade" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm">
                      <option value="">Grade</option>
                      <option v-for="g in [9,10,11,12]" :key="g" :value="g">Grade {{g}}</option>
                    </select>
                  </div>
                  <select v-model="gender" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm">
                    <option value="">Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </template>

                <template v-else-if="role === 'teacher'">
                  <div class="grid grid-cols-2 gap-2">
                    <input v-model="phone" @input="validatePhone" placeholder="Phone" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm" />
                    <input v-model="school_name" placeholder="School" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm" />
                  </div>
                  <select v-model="subject_assigned" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm">
                    <option value="">Subject</option>
                    <option>Math</option><option>Physics</option><option>Chemistry</option><option>Biology</option><option>English</option>
                  </select>
                </template>

                <template v-else-if="role === 'eduoffice'">
                  <input v-model="phone" @input="validatePhone" placeholder="Phone" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm" />
                  <select v-model="gender" class="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-sm">
                    <option value="">Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </template>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-2 pt-2">
                <button 
                  type="button"
                  @click="currentStep = 1"
                  class="flex-1 px-4 py-2.5 text-sm font-medium text-white/70 bg-white/5 backdrop-blur-sm rounded-xl border border-white/20 hover:bg-white/10 transition-all"
                >
                  Back
                </button>
                <button 
                  type="submit"
                  :disabled="!formValid || loading"
                  class="flex-1 px-4 py-2.5 bg-gradient-to-r from-violet-500 to-fuchsia-500 hover:from-violet-600 hover:to-fuchsia-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  {{ loading ? 'Creating...' : 'Create Account' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Footer Link -->
          <div class="px-6 pb-4 text-center">
            <p class="text-white/40 text-xs">
              Already have account? 
              <button @click="$emit('switch-to-login')" class="text-violet-400 hover:text-violet-300 font-medium underline">Sign in</button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'RegisterModal',
  props: {
    isOpen: Boolean
  },
  emits: ['close', 'switch-to-login'],
  data() {
    return {
      role: '',
      currentStep: 1,
      showPassword: false,
      name: '', username: '', email: '', password: '',
      school_id: '', grade: '', gender: '',
      phone: '', school_name: '', subject_assigned: '',
      photo: null, photoPreview: null,
      loading: false,
      // Validation states (simplified)
      formValid: false
    }
  },
  methods: {
    selectRole(role) {
      this.role = role
      this.currentStep = 2
    },
    handlePhoto(e) {
      this.photo = e.target.files[0]
      this.photoPreview = URL.createObjectURL(this.photo)
    },
    validateName() { /* impl */ },
    validateUsername() { /* impl */ },
    validateEmail() { /* impl */ },
    validatePassword() { /* impl */ },
    validatePhone() { /* impl */ },
    validateSchool() { /* impl */ },
    signup() {
      // Same backend logic as original register.vue
      console.log('Register:', this.role, this.name)
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.6; }
}
@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animate-pulse-slow { animation: pulse-slow 3s ease-in-out infinite; }
.animate-gradient-x { 
  background-size: 200% 200%; 
  animation: gradient-x 2s ease infinite; 
}

.modal-enter-active, .modal-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>

