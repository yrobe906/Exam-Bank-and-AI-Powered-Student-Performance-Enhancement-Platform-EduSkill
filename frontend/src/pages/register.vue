<template>
  <Transition name="modal">
    <div v-if="$route.path === '/register'" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click.self="$router.push('/')">
      <!-- Background Overlay - Darker to match login -->
      <div class="absolute inset-0 bg-black/70 backdrop-blur-md"></div>
      
      <!-- Main Modal Container -->
      <div class="relative w-full max-w-6xl mx-auto rounded-3xl shadow-2xl overflow-hidden font-sans">
        
        <!-- Animated Gradient Border -->
        <div class="absolute inset-0 rounded-3xl p-[1px] bg-gradient-to-r from-cyan-500 via-indigo-500 to-fuchsia-500 animate-gradient-x z-0"></div>
        
        <!-- Main Content Wrapper with Glassmorphism -->
        <div class="relative bg-gradient-to-br from-slate-900/95 via-indigo-900/95 to-purple-900/95 backdrop-blur-xl rounded-3xl">
          
          <!-- Decorative top bar -->
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan-400 via-indigo-400 to-fuchsia-400 z-20"></div>
          
          <!-- Close Button -->
          <button @click="$router.push('/')" class="absolute top-4 right-4 w-10 h-10 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white/60 hover:text-white text-2xl transition-all z-30 backdrop-blur-sm border border-white/10">
            ×
          </button>
          
          <!-- Main Flex Container -->
          <div class="flex flex-col lg:flex-row">
            
            <!-- Left Side - Premium Student Image -->
            <div class="lg:w-5/12 relative overflow-hidden min-h-[550px]">
              <img 
                src="https://cdn.pixabay.com/photo/2015/07/17/22/43/student-849825_1280.jpg"
                alt="Students learning together"
                class="absolute inset-0 w-full h-full object-cover"
                loading="eager"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
              
              <!-- Overlay Content -->
              <div class="absolute bottom-0 left-0 right-0 p-8 text-white">
                <div class="flex items-center space-x-2 mb-4">
                  <div class="w-8 h-8 bg-white/20 rounded-lg backdrop-blur-sm flex items-center justify-center">
                    <span class="text-lg">🎓</span>
                  </div>
                  <span class="text-lg font-semibold tracking-tight">EduSkill Hub</span>
                </div>
                <h2 class="text-3xl lg:text-4xl font-bold mb-3 leading-tight">Start your<br>learning journey</h2>
                <p class="text-white/80 text-sm mb-6 leading-relaxed">Join thousands of students and teachers on Ethiopia's premier educational platform.</p>
                <div class="space-y-2">
                  <div class="flex items-center space-x-2 text-sm text-white/70">
                    <svg class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
                    <span>Free access to all features</span>
                  </div>
                  <div class="flex items-center space-x-2 text-sm text-white/70">
                    <svg class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
                    <span>AI-powered personalized learning</span>
                  </div>
                  <div class="flex items-center space-x-2 text-sm text-white/70">
                    <svg class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
                    <span>10,000+ exam questions</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Right Side - Registration Form with Premium Styling -->
            <div class="lg:w-7/12 p-6 lg:p-8 overflow-y-auto max-h-[90vh]">
              
              <!-- Header -->
              <div class="mb-6">
                <h1 class="text-3xl font-bold text-white mb-1">Create account</h1>
                <p class="text-white/50 text-sm">Fill in your details to get started</p>
              </div>
              
              <!-- Stepper - Modern Style -->
              <div class="flex items-center justify-between mb-8">
                <div v-for="(step, idx) in [1,2,3]" :key="idx" class="flex items-center">
                  <div :class="['w-9 h-9 rounded-full flex items-center justify-center text-xs font-semibold transition-all duration-300',
                    currentStep >= step ? 'bg-gradient-to-r from-cyan-500 to-fuchsia-500 text-white shadow-lg' : 'bg-white/10 text-white/40 border border-white/10']">
                    {{ step }}
                  </div>
                  <span :class="['ml-2 text-xs font-medium transition-all', currentStep >= step ? 'text-white' : 'text-white/40']">
                    {{ step === 1 ? 'Role' : step === 2 ? 'Profile' : 'Details' }}
                  </span>
                  <div v-if="step < 3" :class="['w-12 h-0.5 mx-3 transition-all', currentStep > step ? 'bg-gradient-to-r from-cyan-500 to-fuchsia-500' : 'bg-white/10']"></div>
                </div>
              </div>
              
              <!-- Role Selection - Glass Cards -->
              <div class="grid grid-cols-3 gap-3 mb-6">
                <button v-for="r in ['student', 'teacher', 'eduoffice']" :key="r"
                  @click="role = r; currentStep = 2"
                  :class="['relative py-3 rounded-xl border transition-all duration-300 transform hover:scale-105',
                    role === r ? 'border-cyan-400 bg-gradient-to-br from-cyan-500/20 to-fuchsia-500/20 shadow-lg shadow-cyan-500/20' : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10']">
                  <div class="flex flex-col items-center">
                    <span class="text-2xl mb-1">{{ r === 'student' ? '📚' : r === 'teacher' ? '👨‍🏫' : '🏢' }}</span>
                    <span class="text-sm font-medium capitalize" :class="role === r ? 'text-cyan-300' : 'text-white/60'">{{ r === 'eduoffice' ? 'Edu. Officer' : r }}</span>
                    <span v-if="role === r" class="absolute -top-1 -right-1 w-4 h-4 bg-emerald-400 rounded-full border-2 border-slate-900 animate-pulse"></span>
                  </div>
                </button>
              </div>
              
              <!-- Photo Upload - Centered Premium -->
              <div class="flex flex-col items-center justify-center mb-8 pb-4 border-b border-white/10">
                <label class="cursor-pointer group">
                  <input type="file" accept="image/*" class="hidden" @change="handlePhoto" />
                  <div class="relative w-24 h-24 rounded-full flex items-center justify-center overflow-hidden transition-all duration-300 group-hover:scale-105 group-hover:shadow-2xl cursor-pointer"
                    :class="photo ? 'shadow-lg shadow-cyan-500/30' : 'bg-white/5 border-2 border-dashed border-white/20 group-hover:border-cyan-400'">
                    <img v-if="photoPreview" :src="photoPreview" class="w-full h-full object-cover" />
                    <svg v-else class="w-8 h-8 text-white/40 group-hover:text-cyan-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    <div class="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-full">
                      <span class="text-white text-xs font-medium">Change</span>
                    </div>
                  </div>
                </label>
                <p class="text-white text-sm font-medium mt-3">Profile photo</p>
                <p class="text-white/40 text-xs">Click to upload (JPG, PNG, max 5MB)</p>
                <div v-if="photo" class="mt-2 text-emerald-400 text-xs flex items-center gap-1">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
                  Photo selected
                </div>
              </div>
              
              <!-- Form Fields - Premium Styling -->
              <div class="space-y-4">
                <!-- Full Name -->
                <div class="group">
                  <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5 transition-all group-focus-within:text-cyan-400">Full name</label>
                  <div class="relative">
                    <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 group-focus-within:text-cyan-400 transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                    </div>
                    <input v-model="name" @input="validateName" type="text"
                      class="w-full pl-10 pr-4 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent focus:bg-white/10"
                      :class="name ? (nameValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                      placeholder="John Doe">
                  </div>
                  <p v-if="name && !nameValid" class="text-rose-400 text-xs mt-1">Only letters and spaces, min 3 characters</p>
                </div>
                
                <!-- Username -->
                <div class="group">
                  <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5 transition-all group-focus-within:text-cyan-400">Username</label>
                  <div class="relative">
                    <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 group-focus-within:text-cyan-400 transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </div>
                    <input v-model="username" @input="validateUsername" type="text"
                      class="w-full pl-10 pr-4 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent focus:bg-white/10"
                      :class="username ? (usernameValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                      placeholder="johndoe123">
                  </div>
                  <p v-if="username && !usernameValid" class="text-rose-400 text-xs mt-1">Min 4 characters</p>
                </div>
                
                <!-- Email -->
                <div class="group">
                  <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5 transition-all group-focus-within:text-cyan-400">Email address</label>
                  <div class="relative">
                    <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 group-focus-within:text-cyan-400 transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                    </div>
                    <input v-model="email" @input="validateEmail" type="email"
                      class="w-full pl-10 pr-4 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent focus:bg-white/10"
                      :class="email ? (emailValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                      placeholder="john@example.com">
                  </div>
                </div>
                
                <!-- Password -->
                <div class="group">
                  <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5 transition-all group-focus-within:text-cyan-400">Password</label>
                  <div class="relative">
                    <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 group-focus-within:text-cyan-400 transition-colors">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                    </div>
                    <input v-model="password" @input="validatePassword" :type="showPassword ? 'text' : 'password'"
                      class="w-full pl-10 pr-12 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent focus:bg-white/10"
                      :class="password ? (passwordValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                      placeholder="••••••••">
                    <button @click="showPassword = !showPassword" type="button" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/40 hover:text-white/80 transition-colors">
                      {{ showPassword ? '👁️' : '👁️‍🗨️' }}
                    </button>
                  </div>
                  <p v-if="password && !passwordValid" class="text-rose-400 text-xs mt-1">8+ chars, 1 number, 1 special char (@$!%*?&)</p>
                  <p v-else-if="password && passwordValid" class="text-emerald-400 text-xs mt-1">Strong password ✓</p>
                </div>
                
                <!-- Role-specific fields with same styling -->
                <template v-if="role === 'student'">
                  <div class="grid grid-cols-2 gap-3">
                    <div class="group">
                      <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5">School ID</label>
                      <input v-model="school_id" @input="validateSchool" type="text"
                        class="w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
                        :class="school_id ? (schoolValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                        placeholder="SCH-12345">
                    </div>
                    <div>
                      <label class="block text-blue-400/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Grade</label>
                      <select v-model="grade" class="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-blue-400 text-sm outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent">
                        <option value="" class="text-gray-800">Select grade</option>
                        <option v-for="g in [9,10,11,12]" :key="g" :value="g">Grade {{ g }}</option>
                      </select>
                    </div>
                  </div>
                  <div>
                    <label class="block text-blue-400/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Gender</label>
                    <select v-model="gender" class="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-blue-400 text-sm outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent">
                      <option value="" class="text-gray-800">Select gender</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </div>
                </template>
                
                <template v-if="role === 'teacher'">
                  <div class="grid grid-cols-2 gap-3">
                    <div class="group">
                      <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Phone</label>
                      <input v-model="phone" @input="validatePhone" @keypress="onlyDigits" maxlength="10"
                        class="w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
                        :class="phone ? (phoneValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                        placeholder="09XXXXXXXX">
                    </div>

                  </div>
                  <div class="grid grid-cols-3 gap-3">
                    <div>
                      <label class="block text-blue-400/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Subject</label>
                      <select v-model="subject_assigned" class="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-xl text-blue-400 text-sm outline-none focus:ring-2 focus:ring-cyan-400">
                        <option value="" class="text-gray-800">Select</option>
                        <option v-for="s in subjects" :key="s" :value="s">{{ s }}</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-blue-400/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Grade</label>
                      <select v-model="teaching_grade" class="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-xl text-blue-400 text-sm outline-none focus:ring-2 focus:ring-cyan-400">
                        <option value="" class="text-gray-800">Select</option>
                        <option v-for="g in [9,10,11,12]" :key="g" :value="g">Grade {{ g }}</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-blue-400 text-xs font-semibold uppercase tracking-wide mb-1.5">Gender</label>
                      <select v-model="gender" class="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-xl text-blue-400 text-sm outline-none focus:ring-2 focus:ring-cyan-400">
                        <option value="" class="text-gray-800">Select</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                      </select>
                    </div>
                  </div>
                </template>
                
                <template v-if="role === 'eduoffice'">
                  <div class="grid grid-cols-2 gap-3">
                    <div class="group">
                      <label class="block text-white/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Phone</label>
                      <input v-model="phone" @input="validatePhone" @keypress="onlyDigits" maxlength="10"
                        class="w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white text-sm outline-none transition-all focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
                        :class="phone ? (phoneValid ? 'border-emerald-500' : 'border-rose-500') : 'border-white/10'"
                        placeholder="09XXXXXXXX">
                    </div>
                    <div>
                      <label class="block text-blue-400/70 text-xs font-semibold uppercase tracking-wide mb-1.5">Gender</label>
                      <select v-model="gender" class="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-blue-400 text-sm outline-none focus:ring-2 focus:ring-cyan-400">
                        <option value="" class="text-gray-800">Select</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                      </select>
                    </div>
                  </div>
                  <div class="grid grid-cols-2 gap-3">
                    
                    
                  </div>
                </template>
              </div>

              <!-- Register Button - Premium Gradient -->
              <button @click="signup" :disabled="!formValid || loading"
                class="relative w-full bg-gradient-to-r from-cyan-500 to-fuchsia-500 hover:from-cyan-600 hover:to-fuchsia-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] text-base mt-6 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden group">
                <span class="relative z-10 flex items-center justify-center gap-2">
                  <span>{{ loading ? 'Creating account...' : 'Create account' }}</span>
                  <svg v-if="!loading" class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                  </svg>
                </span>
                <svg v-if="loading" class="animate-spin h-5 w-5 text-white absolute right-4 top-1/2 transform -translate-y-1/2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </button>

              <!-- Login Link -->
              <div class="text-center mt-5">
                <p class="text-white/50 text-sm">
                  Already have an account? 
                  <button @click="$router.push('/login')" class="text-cyan-400 hover:text-cyan-300 font-semibold transition-colors hover:underline">Sign in</button>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Toast Message -->
      <div v-if="message" :class="isSuccess ? 'bg-emerald-500' : 'bg-rose-500'" class="fixed bottom-8 left-1/2 -translate-x-1/2 text-white px-6 py-3 rounded-xl shadow-2xl z-50 text-sm font-medium backdrop-blur-sm">
        {{ message }}
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  data() {
    return {
      role: "",
      currentStep: 1,
      showPassword: false,
      name: "",
      username: "",
      email: "",
      password: "",
      school_id: "",
      grade: "",
      gender: "",
      phone: "",
      school_name: "",
      subject_assigned: "",
      teaching_grade: "",
      woreda: "",
      school_supervising: "",
      photo: null,
      photoPreview: null,
      subjects: ["Chemistry","Biology","English","History","Math","Physics","Geography","Civics","Economics","IT","Art","Physical Education"],
      nameValid: false,
      usernameValid: false,
      emailValid: false,
      passwordValid: false,
      schoolValid: false,
      phoneValid: false,
      schoolNameValid: false,
      loading: false,
      message: "",
      isSuccess: false,
    };
  },

  computed: {
    formValid() {
      if (!this.photo || !this.nameValid || !this.usernameValid || !this.emailValid || !this.passwordValid) return false;
      if (this.role === "student") return this.schoolValid && this.grade && this.gender;
      if (this.role === "teacher") return this.phoneValid && this.schoolNameValid && this.subject_assigned && this.teaching_grade && this.gender;
      if (this.role === "eduoffice") return this.phoneValid && this.woreda && this.school_supervising && this.gender;
      return false;
    },
  },

  methods: {
    onlyDigits(e) { if (!/[0-9]/.test(e.key)) e.preventDefault(); },
    
    validateName() { 
      const alphaRegex = /^[A-Za-z\s]*$/;
      if (!alphaRegex.test(this.name)) {
        this.name = this.name.replace(/[^A-Za-z\s]/g, '');
      }
      this.nameValid = this.name.length >= 3 && /^[A-Za-z\s]+$/.test(this.name);
    },
    
    validateUsername() { this.usernameValid = this.username.length >= 4; },
    validateEmail() { this.emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email); },
    validatePassword() { this.passwordValid = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/.test(this.password); },
    validatePhone() { this.phoneValid = /^[0-9]{10}$/.test(this.phone); },
    validateSchool() { this.schoolValid = this.school_id.length >= 3; },
    validateSchoolName() { this.schoolNameValid = this.school_name.length >= 2; },

    handlePhoto(e) {
      this.photo = e.target.files[0];
      this.photoPreview = URL.createObjectURL(this.photo);
    },

    show(msg, success) {
      this.message = msg;
      this.isSuccess = success;
      setTimeout(() => this.message = "", 4000);
    },

    signup() {
      if (!this.role) { this.show("⚠️ Please select a role", false); return; }
      if (!this.formValid) { this.show("⚠️ Please fill all required fields correctly", false); return; }
      this.loading = true;

      const formData = new FormData();
      formData.append("full_name", this.name);
      formData.append("username", this.username);
      formData.append("email", this.email);
      formData.append("password", this.password);
      formData.append("role", this.role);
      formData.append("gender", this.gender);

      if (this.role === "student") {
        formData.append("school_id", this.school_id);
        formData.append("grade", this.grade);
      }
      if (this.role === "teacher") {
        formData.append("phone", this.phone);
        formData.append("school_name", this.school_name);
        formData.append("subject_assigned", this.subject_assigned);
        formData.append("teaching_grade", this.teaching_grade);
      }
      if (this.role === "eduoffice") {
        formData.append("phone", this.phone);
        formData.append("woreda", this.woreda);
        formData.append("school_supervising", this.school_supervising);
      }
      formData.append("profile_photo", this.photo);

      fetch("http://127.0.0.1:8000/api/users/register", { method: "POST", body: formData })
        .then(async res => {
          this.loading = false;
          if (res.ok) {
            this.show("Registration submitted. Waiting for admin approval.", true);
            localStorage.setItem("pendingUser", this.username);
            this.$router.push('/user_notification');
          } else {
            const data = await res.json();
            this.show(`Error: ${data.detail || "Unknown error"}`, false);
          }
        })
        .catch(err => { this.loading = false; this.show(`Network error: ${err}`, false); });
    }
  }
};
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }

/* Premium Animations */
@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animate-gradient-x {
  background-size: 200% 200%;
  animation: gradient-x 3s ease infinite;
}

input, select, button { transition: all 0.2s ease; }
input:focus, select:focus { transform: translateY(-1px); }

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}
.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}
.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(34, 211, 238, 0.3);
  border-radius: 10px;
}
.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(34, 211, 238, 0.5);
}

@media (max-width: 768px) {
  .grid.grid-cols-3 { gap: 0.5rem; }
  .grid.grid-cols-2 { gap: 0.75rem; }
}
</style>