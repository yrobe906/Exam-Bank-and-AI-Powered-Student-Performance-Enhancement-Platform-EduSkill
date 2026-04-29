<template>
  <div class="forgot-password-container">
    <div class="forgot-password-card">
      <h2>Forgot Password</h2>
      <p>Enter your email address and we'll send you a link to reset your password.</p>

      <form @submit.prevent="handleSubmit" class="forgot-password-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="Enter your email"
            class="form-input"
          />
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="submit-btn"
        >
          {{ isLoading ? 'Sending...' : 'Send Reset Link' }}
        </button>
      </form>

      <div v-if="message" class="message" :class="{ 'success': !error, 'error': error }">
        {{ message }}
      </div>

      <div class="back-to-login">
        <router-link to="/login">Back to Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      message: '',
      error: false,
      isLoading: false
    }
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true
      this.message = ''
      this.error = false

      try {
        const response = await fetch('/api/auth/forgot-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: this.email })
        })

        const data = await response.json()

        if (response.ok) {
          this.message = data.message
          this.error = false
        } else {
          this.message = data.detail || 'An error occurred'
          this.error = true
        }
      } catch (error) {
        this.message = 'Network error. Please try again.'
        this.error = true
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.forgot-password-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.forgot-password-card h2 {
  text-align: center;
  margin-bottom: 1rem;
  color: #333;
}

.forgot-password-card p {
  text-align: center;
  margin-bottom: 2rem;
  color: #666;
  line-height: 1.5;
}

.forgot-password-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
}

.submit-btn {
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.back-to-login {
  text-align: center;
  margin-top: 1.5rem;
}

.back-to-login a {
  color: #007bff;
  text-decoration: none;
}

.back-to-login a:hover {
  text-decoration: underline;
}
</style>