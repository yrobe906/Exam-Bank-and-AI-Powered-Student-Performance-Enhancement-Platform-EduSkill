// src/services/aiService.js - UPDATED
import axios from 'axios'

// Configure axios
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with better defaults
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const aiService = {
  /**
   * Send a message to the AI assistant - SIMPLIFIED
   */
  async sendMessage(message) {
    try {
      console.log('📡 Sending to AI:', message)
      
      // Your backend expects: {"message": "your text"}
      const response = await api.post('/ai/chat', {
        message: message.trim()
      })
      
      console.log('✅ AI Response received:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ AI Service Error:', error)
      
      // Better error handling
      if (error.response) {
        console.error('Response error:', error.response.status, error.response.data)
      } else if (error.request) {
        console.error('No response received:', error.request)
      }
      
      return {
        response: "I'm having trouble connecting to the AI service. Please try again.",
        timestamp: new Date().toISOString(),
        ai_enabled: false
      }
    }
  },
  
  /**
   * Check AI health
   */
  async checkHealth() {
    try {
      const response = await api.get('/ai/health')
      return response.data
    } catch (error) {
      console.error('Health check error:', error)
      return { status: 'unhealthy', ai_enabled: false }
    }
  },
  
  /**
   * Get example questions
   */
  async getExamples() {
    try {
      const response = await api.get('/ai/example')
      return response.data
    } catch {
      return { examples: [] }
    }
  },
  
  /**
   * Simple student ID getter
   */
  getStudentId() {
    return localStorage.getItem('user_id') || 1 // Default to 1 for testing
  }
}

// Development logging
if (import.meta.env.DEV) {
  api.interceptors.request.use(request => {
    console.log('➡️ Request:', request.method?.toUpperCase(), request.url)
    return request
  })
  
  api.interceptors.response.use(response => {
    console.log('⬅️ Response:', response.status, response.config.url)
    return response
  }, error => {
    console.error('❌ API Error:', error.message)
    return Promise.reject(error)
  })
}

export default aiService