<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-600 via-cyan-500 to-fuchsia-600 p-4 relative overflow-hidden">
    <!-- Floating particles background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-purple-400/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-80 h-80 bg-cyan-400/10 rounded-full blur-3xl"></div>
      <div v-for="i in 15" :key="i" 
           class="absolute w-1 h-1 bg-white/20 rounded-full animate-float"
           :style="`
             left: ${Math.random() * 100}%;
             top: ${Math.random() * 100}%;
             animation-delay: ${i * 0.2}s;
           `"></div>
    </div>

    <!-- Notification Card -->
    <div class="relative bg-gradient-to-br from-white/15 to-white/5 backdrop-blur-2xl shadow-2xl p-8 rounded-3xl w-full max-w-md text-center border border-white/30 animate-fade-in hover:shadow-3xl transition-shadow duration-500">
      
      <!-- Decorative corners -->
      <div class="absolute -top-2 -left-2 w-6 h-6 border-t-2 border-l-2 border-white/40 rounded-tl-lg"></div>
      <div class="absolute -top-2 -right-2 w-6 h-6 border-t-2 border-r-2 border-white/40 rounded-tr-lg"></div>
      <div class="absolute -bottom-2 -left-2 w-6 h-6 border-b-2 border-l-2 border-white/40 rounded-bl-lg"></div>
      <div class="absolute -bottom-2 -right-2 w-6 h-6 border-b-2 border-r-2 border-white/40 rounded-br-lg"></div>
      
      <!-- Status Icon -->
      <div class="relative mb-6 flex justify-center">
        <div class="relative">
          <!-- Outer glow -->
          <div class="absolute inset-0 animate-ping bg-gradient-to-r from-cyan-400/40 to-purple-400/40 rounded-full"></div>
          <!-- Inner pulse -->
          <div :class="isApproved ? 'animate-pulse-success' : (isRejected ? 'animate-pulse-reject' : 'animate-pulse-pending')" 
               class="absolute inset-[-5px] rounded-full border-2 border-white/30"></div>
          <!-- Icon container -->
          <div class="relative w-20 h-20 bg-gradient-to-br from-white/30 to-white/10 backdrop-blur-sm rounded-full flex items-center justify-center border-2 border-white/50 shadow-lg hover:scale-105 transition-transform duration-300">
            <div class="relative">
              <svg v-if="!isApproved && !isRejected" class="w-10 h-10 text-white drop-shadow-lg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <svg v-else-if="isApproved" class="w-10 h-10 text-green-300 drop-shadow-lg animate-bounce-in" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <svg v-else class="w-10 h-10 text-red-400 drop-shadow-lg animate-bounce-in" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Status Header -->
      <h2 class="text-3xl font-bold text-white mb-4 drop-shadow-lg bg-gradient-to-r from-white via-white/90 to-white/80 bg-clip-text text-transparent">
        Registration Status
      </h2>
      
      <!-- Status Indicator -->
      <div class="flex items-center justify-center mb-4">
        <div class="flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-white/15 to-white/5 backdrop-blur-sm border border-white/20 shadow-inner hover:from-white/20 hover:to-white/10 transition-all duration-300">
          <div :class="statusDotClass" class="w-3 h-3 rounded-full animate-pulse mr-2 shadow-lg"></div>
          <span :class="statusTextClass" class="text-sm font-semibold tracking-wide drop-shadow-sm">
            {{ statusText }}
          </span>
        </div>
      </div>
      
      <!-- Message -->
      <div class="relative mb-8 group">
        <div :class="messageBackgroundClass" class="absolute -inset-0.5 rounded-2xl blur opacity-0 group-hover:opacity-100 transition duration-500"></div>
        <p class="relative text-white/90 text-sm leading-relaxed bg-gradient-to-br from-white/15 to-white/5 p-4 rounded-2xl backdrop-blur-sm border border-white/10">
          {{ message }}
        </p>
      </div>

      <!-- Loading Bar for Pending -->
      <div v-if="!isApproved && !isRejected" class="mb-8">
        <div class="relative h-2 bg-gradient-to-r from-white/10 to-white/5 rounded-full overflow-hidden border border-white/10">
          <div class="absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-cyan-300 via-purple-400 to-fuchsia-400 rounded-full animate-loading shadow-lg"></div>
        </div>
        <p class="text-white/70 text-xs mt-2 flex items-center justify-center">
          <svg class="w-4 h-4 mr-2 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Checking status every 5 seconds...
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="space-y-4">
        <button v-if="isApproved"
                @click="goToLogin"
                class="group relative bg-gradient-to-r from-green-500 via-emerald-500 to-green-600 text-white font-bold py-3 px-8 rounded-full shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 w-full overflow-hidden">
          
          <!-- Shine effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
          
          <span class="relative flex items-center justify-center space-x-2 cursor-pointer">
            <span class="drop-shadow-sm">Proceed to Login</span>
            <svg class="w-5 h-5 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
            </svg>
          </span>
        </button>

        <button v-else-if="isRejected"
                @click="goToSupport"
                class="group relative bg-gradient-to-r from-red-500 via-rose-500 to-pink-500 text-white font-bold py-3 px-8 rounded-full shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 w-full overflow-hidden">
          
          <!-- Shine effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
          
          <span class="relative flex items-center justify-center space-x-2">
            <span class="drop-shadow-sm">Contact Support</span>
            <svg class="w-5 h-5 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"></path>
            </svg>
          </span>
        </button>

        <!-- Pending Message -->
        <div v-else class="text-center">
          <p class="text-white/60 text-xs italic animate-fade-in-out">You'll be redirected automatically once approved</p>
          <div class="mt-2 flex justify-center space-x-1">
            <div v-for="i in 3" :key="i" 
                 :style="`animation-delay: ${i * 0.2}s`"
                 class="w-1 h-1 bg-white/40 rounded-full animate-bounce"></div>
          </div>
        </div>
      </div>

      <!-- Footer note -->
      <div class="mt-6 pt-4 border-t border-white/10">
        <p class="text-white/40 text-xs">Auto-refresh enabled • Secure verification</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "Pending approval. Your account will be approved by admin within 48 hours.",
      isApproved: false,
      isRejected: false,
      checkInterval: null,
      username: "",
    };
  },
  computed: {
    statusText() {
      if (this.isApproved) return "APPROVED";
      if (this.isRejected) return "REJECTED";
      return "PENDING";
    },
    statusDotClass() {
      if (this.isApproved) return "bg-green-400 shadow-green-400/50";
      if (this.isRejected) return "bg-red-400 shadow-red-400/50";
      return "bg-amber-400 shadow-amber-400/50";
    },
    statusTextClass() {
      if (this.isApproved) return "text-green-200";
      if (this.isRejected) return "text-red-200";
      return "text-amber-200";
    },
    messageBackgroundClass() {
      if (this.isApproved) return "bg-gradient-to-r from-green-400/20 to-emerald-400/20";
      if (this.isRejected) return "bg-gradient-to-r from-red-400/20 to-pink-400/20";
      return "bg-gradient-to-r from-cyan-400/20 to-purple-400/20";
    },
  },
  mounted() {
  // Get username from localStorage (set after registration)
  this.username = localStorage.getItem("pendingUser");
  localStorage.removeItem("pendingUser"); // optional cleanup

  if (this.username) {
    this.startStatusCheck();
  } else {
    this.isRejected = true;
    this.message = "No username provided. Please contact support.";
  }
},


beforeUnmount() {
  if (this.checkInterval) clearInterval(this.checkInterval);
},

methods: {
  async startStatusCheck() {
    if (!this.username) return;

    // Track how long we've been polling (max 24 hours)
    let elapsedSeconds = 0;
    const maxSeconds = 86400; // 24 hours

    this.checkInterval = setInterval(async () => {
      if (elapsedSeconds >= maxSeconds) {
        clearInterval(this.checkInterval);
        this.message = "Status check expired. Please contact support.";
        this.isRejected = true;
        return;
      }

      try {
        const res = await fetch(`http://127.0.0.1:8000/api/users/status/${this.username}`);
        
        if (res.status === 404) {
          // User not found → rejected
          this.isRejected = true;
          this.message = "Your registration was rejected by admin or no longer exists. Please contact support.";
          clearInterval(this.checkInterval);
          return;
        }

        const data = await res.json();

        if (data.status === "approved") {
          this.isApproved = true;
          this.message = "Your account has been approved! You can now login.";
          clearInterval(this.checkInterval);
        } else if (data.status === "rejected") {
          this.isRejected = true;
          this.message = "Your registration was rejected by admin. Please contact support.";
          clearInterval(this.checkInterval);
        } 
        // else: still pending → keep polling

      } catch (err) {
        console.error("Failed to fetch status:", err);
      }

      elapsedSeconds += 5; // interval is 5 seconds
    }, 5000);
  },

  goToLogin() {
    this.$router.push('/user_login');
  },

  goToSupport() {
    this.$router.push({ name: "Support" });
  }
}
};
</script>

<style scoped>
@keyframes loading {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  50% { transform: translateY(-20px) translateX(10px); }
}

@keyframes fade-in-out {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@keyframes bounce-in {
  0% { transform: scale(0.3); opacity: 0; }
  50% { transform: scale(1.1); opacity: 1; }
  70% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

@keyframes pulse-pending {
  0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
}

@keyframes pulse-success {
  0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
}

@keyframes pulse-reject {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
}

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-loading {
  animation: loading 2s ease-in-out infinite;
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}

.animate-float {
  animation: float 8s ease-in-out infinite;
}

.animate-fade-in-out {
  animation: fade-in-out 2s ease-in-out infinite;
}

.animate-bounce-in {
  animation: bounce-in 0.6s ease-out;
}

.animate-pulse-pending {
  animation: pulse-pending 2s ease-in-out infinite;
}

.animate-pulse-success {
  animation: pulse-success 2s ease-in-out infinite;
}

.animate-pulse-reject {
  animation: pulse-reject 2s ease-in-out infinite;
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}

button:active {
  transform: scale(0.98);
}

@media (max-width: 640px) {
  .p-8 { padding: 1.5rem; }
  .text-3xl { font-size: 1.75rem; }
}
</style>