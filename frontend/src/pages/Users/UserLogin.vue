<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-purple-900 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Animated Background Effects -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-20 left-20 w-96 h-96 bg-blue-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float"></div>
      <div class="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float animation-delay-2000"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/20 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float animation-delay-4000"></div>
      
      <!-- Grid Pattern Overlay -->
      <div class="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width%3D%2260%22 height%3D%2260%22 viewBox%3D%220 0 60 60%22 xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Cg fill%3D%22none%22 fill-rule%3D%22evenodd%22%3E%3Cg fill%3D%22%234338ca%22 fill-opacity%3D%220.05%22%3E%3Cpath d%3D%22M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')] opacity-20"></div>
    </div>

    <!-- Main Login Card -->
    <div class="relative w-full max-w-md">
      <!-- Decorative Top Bar -->
      <div class="absolute -top-3 left-1/2 transform -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-cyan-400 to-fuchsia-500 rounded-full"></div>
      
      <!-- Card Container with Premium Glassmorphism -->
      <div class="bg-white/10 backdrop-blur-xl rounded-3xl border border-white/20 shadow-2xl p-8 transition-all duration-500 hover:shadow-3xl">
        
        <!-- Logo Section with Animation -->
        <div class="text-center mb-8">
          <div class="relative inline-block">
            <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-fuchsia-500 rounded-2xl blur-xl opacity-50 animate-pulse"></div>
            <div class="relative w-20 h-20 bg-gradient-to-r from-cyan-400 to-fuchsia-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg transform transition-transform hover:scale-105 duration-300">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
          </div>
          
          <h2 class="text-4xl font-bold text-white mb-2 bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">
            Welcome Back
          </h2>
          <p class="text-white/50 text-sm">Sign in to your EduSkill Hub account</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="login" class="space-y-5">
          <!-- Username/Email Field -->
          <div class="group">
            <label class="block text-white/70 text-sm font-medium mb-2 transition-all group-focus-within:text-cyan-400">
              Username or Email
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 group-focus-within:text-cyan-400 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
              <input 
                v-model="email" 
                type="text"
                placeholder="Enter your username or email" 
                class="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/20 rounded-xl outline-none text-white placeholder-white/30 text-sm transition-all duration-300 focus:ring-2 focus:ring-cyan-400 focus:border-transparent focus:bg-white/10 backdrop-blur-sm"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div class="group">
            <label class="block text-white/70 text-sm font-medium mb-2 transition-all group-focus-within:text-cyan-400">
              Password
            </label>
            <div class="relative">
              <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 group-focus-within:text-cyan-400 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>
              <input 
                v-model="password" 
                :type="showPassword ? 'text' : 'password'" 
                placeholder="Enter your password" 
                class="w-full pl-10 pr-12 py-3 bg-white/5 border border-white/20 rounded-xl outline-none text-white placeholder-white/30 text-sm transition-all duration-300 focus:ring-2 focus:ring-cyan-400 focus:border-transparent focus:bg-white/10 backdrop-blur-sm"
              />
              <button 
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/40 hover:text-white/80 transition-all duration-200"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                </svg>
              </button>
            </div>
            <div class="text-right mt-2">
              <button 
                @click.prevent="goToContactAdmin"
                class="text-xs text-cyan-300 hover:text-cyan-200 transition-colors hover:underline"
              >
                Forgot Password?
              </button>
            </div>
          </div>

          <!-- Sign In Button - Improved realistic design -->
          <button
            type="submit"
            :disabled="loading"
            class="relative w-full bg-gradient-to-r from-cyan-500 to-fuchsia-500 hover:from-cyan-600 hover:to-fuchsia-600 text-white font-medium py-2.5 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden group mt-6"
          >
            <span class="relative z-10 flex items-center justify-center gap-2 text-[15px]">
              <span>{{ loading ? "Signing in..." : "Sign In" }}</span>
              <svg v-if="!loading" class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </span>
            
            <!-- Loading spinner -->
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white/80 absolute right-4 top-1/2 transform -translate-y-1/2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            
            <!-- Shine effect on hover -->
            <div class="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-500 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12"></div>
          </button>
        </form>

        <!-- Message Display -->
        <div v-if="message" class="mt-5">
          <div :class="[
            'rounded-xl p-3 border-l-4 transition-all duration-500 animate-slide-in',
            isSuccess ? 'bg-emerald-500/20 border-emerald-400' : 'bg-rose-500/20 border-rose-400'
          ]">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 flex-shrink-0" :class="isSuccess ? 'text-emerald-400' : 'text-rose-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="isSuccess" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-white text-sm">{{ message }}</p>
            </div>
          </div>
        </div>

       
        <!-- Footer -->
        <div class="mt-8 text-center">
          <p class="text-white/60 text-sm">
            Don't have an account? 
            <button @click="$router.push('/register')" class="text-cyan-300 hover:text-cyan-200 font-medium transition-colors hover:underline">
              Register for free
            </button>
          </p>
        </div>
      </div>
      
      <!-- Bottom Decorative Element -->
      <div class="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-gradient-to-r from-transparent via-white/30 to-transparent rounded-full"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      email: "",
      password: "",
      showPassword: false,
      loading: false,
      message: "",
      isSuccess: false
    };
  },
  methods: {
    show(msg, success) {
      this.message = msg;
      this.isSuccess = success;
      setTimeout(() => (this.message = ""), 5000);
    },

    goToContactAdmin() {
      this.$router.push('/forgot-password');
    },

    async login() {
      if (!this.email.trim() || !this.password) {
        this.show("Please enter username/email and password", false);
        return;
      }

      this.loading = true;
      this.message = '';

      try {
        const formData = new FormData();
        formData.append("username_or_email", this.email.trim());
        formData.append("password", this.password);

        const res = await fetch("http://127.0.0.1:8000/api/users/login", {
          method: "POST",
          body: formData
        });

        const data = await res.json();
        this.loading = false;

        if (data.status === "pending") {
          localStorage.setItem("pendingUser", data.username);
          this.$router.push("/user_notification");
          return;
        }

        if (res.ok) {
          console.log('✅ API Success - data:', data);
          
          const userRole = (data.role || '').toLowerCase().trim();
          console.log('🔑 Normalized userRole:', userRole);
          
          // Store all data
          localStorage.setItem("token", data.token || "");
          localStorage.setItem("user", JSON.stringify({
            full_name: data.full_name,
            username: data.username,
            role: userRole,
            user_id: data.user_id,
            profile_photo: data.profile_photo,
            school_id: data.school_id,
            email: data.email,
            phone: data.phone,
            grade: data.grade,
            subject_assigned: data.subject_assigned
          }));
          localStorage.setItem("role", userRole);
          localStorage.setItem("user_id", data.user_id || "");
          sessionStorage.setItem("user_role", userRole);
          localStorage.setItem("username", data.username);

          console.log('💾 Storage POST-SET check:');
          console.log('  token:', !!localStorage.getItem("token"));
          console.log('  role:', localStorage.getItem("role"));
          console.log('  username:', localStorage.getItem("username"));
          
          let attempts = 0;
          const maxAttempts = 10;
          const verifyStorage = () => {
            const token = localStorage.getItem("token");
            const role = localStorage.getItem("role");
            const username = localStorage.getItem("username");
            
            if (token && role && username && attempts < maxAttempts) {
              console.log('✅ Storage VERIFIED after', attempts, 'attempts. Navigating...');
              this.redirectToDashboard(userRole);
            } else {
              attempts++;
              console.log('⏳ Storage verify attempt', attempts, '- token:', !!token, 'role:', role, 'username:', !!username);
              setTimeout(verifyStorage, 100);
            }
          };
          
          verifyStorage();
          
        } else {
          this.show(data.message || "Login failed", false);
        }
      } catch (error) {
        this.loading = false;
        console.error('❌ Login error:', error);
        this.show("Network error. Please try again.", false);
      }
    },

    redirectToDashboard(userRole) {
      this.show("Login successful! Redirecting...", true);
      localStorage.removeItem('pendingUser');
      
      let dashboardPath = '/';
      if (userRole === "student") {
        dashboardPath = '/student_dashboard';
      } else if (userRole === "teacher") {
        dashboardPath = '/teacher_dashboard';
      } else if (userRole === "eduoffice") {
        dashboardPath = '/education_office_dashboard';
      } else if (userRole === "admin") {
        dashboardPath = '/admin_dashboard';
      } else {
        console.error('❌ Unknown role:', userRole);
        dashboardPath = '/';
      }
      
      console.log('🚀 FINAL REDIRECT to:', dashboardPath);
      console.log('📊 FINAL STORAGE STATE:');
      console.log('  token:', localStorage.getItem("token")?.slice(0,20) + '...');
      console.log('  role:', localStorage.getItem("role"));
      console.log('  username:', localStorage.getItem("username"));
      
      setTimeout(() => {
        this.$nextTick(() => {
          this.$router.push(dashboardPath).catch(err => {
            console.error('🚨 Router push failed:', err);
            window.location.href = dashboardPath;
          });
        });
      }, 2500);
    }
  }
}
</script>

<style scoped>
/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0px) translateX(0px); }
  50% { transform: translateY(-20px) translateX(10px); }
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-float {
  animation: float 8s ease-in-out infinite;
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

/* Loading Spinner */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Custom Focus Ring */
input:focus {
  box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.2);
}

/* Smooth Hover Transitions */
* {
  transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Card Shadow Enhancement */
.shadow-3xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
</style>