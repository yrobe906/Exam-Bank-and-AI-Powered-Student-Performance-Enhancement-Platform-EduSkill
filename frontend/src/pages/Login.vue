<template>
  <Transition name="modal-slide">
    <div v-if="$route.path === '/login'" class="fixed inset-0 z-[50] bg-black/60 backdrop-blur-md flex items-center justify-center p-4" @click.self="closeModal">
      <div class="bg-white/20 backdrop-blur-2xl shadow-2xl p-10 rounded-3xl w-full max-w-md mx-4 border border-white/30 relative max-h-[90vh] overflow-y-auto">
        <!-- Close Button -->
        <button @click="closeModal" class="absolute top-4 right-4 w-12 h-12 bg-white/90 hover:bg-white rounded-full shadow-2xl flex items-center justify-center text-gray-800 text-xl font-bold hover:scale-110 transition-all duration-200">
          &times;
        </button>

        <h2 class="text-5xl font-extrabold text-center text-white mb-6 drop-shadow-lg">Welcome Back</h2>
        <p class="text-center text-white mb-8 text-lg">Sign in to your account to continue learning</p>
        
        <div class="bg-white/10 backdrop-blur-xl p-6 rounded-2xl shadow-xl space-y-6 border border-white/20">
          <!-- Username or Email -->
<input 
            id="usernameOrEmail" 
            name="usernameOrEmail"
            v-model="usernameOrEmail" 
            type="text" 
            placeholder="Username or Email"
            class="w-full border border-white/40 bg-white/20 text-white placeholder-white/70 rounded-xl p-3 focus:ring-2 focus:ring-white/80 outline-none transition duration-300 hover:ring-white/60"
          />

          <!-- Password with toggle -->
          <div class="relative">
<input 
              id="password" 
              name="password"
              :type="showPassword ? 'text' : 'password'" 
              v-model="password" 
              placeholder="Password"
              class="w-full border border-white/40 bg-white/20 text-white placeholder-white/70 rounded-xl p-3 focus:ring-2 focus:ring-white/80 outline-none transition duration-300 hover:ring-white/60"
            />
            <button @click="togglePassword" type="button" class="absolute top-1/2 right-3 -translate-y-1/2 text-white/80 hover:text-white">
              <span v-if="showPassword">🙈</span>
              <span v-else>👁️</span>
            </button>
          </div>

          <!-- Login Button -->
          <button @click="login" :disabled="loading"
            class="w-full bg-gradient-to-r from-cyan-400 to-purple-500 text-white font-semibold py-3 rounded-full shadow-lg text-lg transition-all hover:from-teal-400 hover:to-blue-500 disabled:opacity-50 disabled:cursor-not-allowed animate-pulse">
            {{ loading ? "Logging in..." : "Login" }}
          </button>
        </div>

        <!-- Feedback Message -->
        <p v-if="message"
           :class="isSuccess ? 'bg-green-500/70 border border-green-400/50' : 'bg-red-500/70 border border-red-400/50'"
           class="text-center mt-6 text-white text-lg font-semibold py-3 px-4 rounded-xl shadow-lg transition-all duration-300">
          {{ message }}
        </p>
      </div>
    </div>
  </Transition>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginModal',
  data() {
    return {
      usernameOrEmail: '',
      password: '',
      message: '',
      isSuccess: false,
      loading: false,
      showPassword: false
    };
  },
  methods: {
    closeModal() {
      this.$router.push('/');
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      if (!this.usernameOrEmail || !this.password) {
        this.message = "Please enter both username/email and password";
        this.isSuccess = false;
        setTimeout(() => (this.message = ""), 3000);
        return;
      }

      this.loading = true;
      this.message = '';

      try {
        const response = await axios.post("http://127.0.0.1:8000/students/login", {
          username_or_email: this.usernameOrEmail,
          password: this.password
        });

        // Save token and student info
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("student_id", response.data.user_id);
        localStorage.setItem("username", response.data.username);
        localStorage.setItem("role", response.data.role);
        localStorage.setItem("student_info", JSON.stringify({
          full_name: response.data.full_name,
          school_id: response.data.school_id,
          profile_photo_url: response.data.profile_photo_url
        }));

        this.isSuccess = true;
        this.message = "Login successful! Redirecting...";

        setTimeout(() => {
          this.$router.push('/student_dashboard');
        }, 1500);

      } catch (err) {
        this.isSuccess = false;
        this.message = err.response?.data?.detail || "Login failed. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Animations */
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(-10px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.6s ease-out forwards;
}
</style>

