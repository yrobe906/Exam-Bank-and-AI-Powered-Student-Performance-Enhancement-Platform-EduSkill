import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import axios from 'axios'

// Configure axios
axios.defaults.baseURL = 'http://localhost:8000'

// Add JWT token to requests if available
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const app = createApp(App)

// Use router
app.use(router)

// Mount the app
app.mount('#app')

// Optional: Development helper
if (import.meta.env.DEV) {
  window.vueApp = app
}