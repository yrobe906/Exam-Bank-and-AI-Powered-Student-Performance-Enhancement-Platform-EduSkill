<template>
  <div class="ai-chat-container">
    <!-- Floating AI Button -->
    <button 
      v-if="!chatOpen"
      @click="openChat"
      class="ai-floating-btn"
      :class="{ 'has-notification': unreadCount > 0 }"
    >
      <span class="ai-icon">🤖</span>
      <span class="ai-text">AI Tutor</span>
      <span v-if="unreadCount > 0" class="notification-badge">
        {{ unreadCount }}
      </span>
    </button>

    <!-- Chat Window -->
    <div v-if="chatOpen" class="ai-chat-window">
      <!-- Header -->
      <div class="chat-header">
        <div class="header-left">
          <span class="avatar">🤖</span>
          <div>
            <h3>EduSkill AI Assistant</h3>
            <p class="status">{{ aiStatus }}</p>
          </div>
        </div>
        <button @click="closeChat" class="close-btn">✕</button>
      </div>

      <!-- Messages -->
      <div class="messages-container" ref="messagesRef">
        <div v-for="(msg, index) in messages" :key="index" 
             :class="['message', msg.type]">
          <div class="message-avatar">
            {{ msg.type === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <p>{{ msg.content }}</p>
            <small class="timestamp">{{ formatTime(msg.timestamp) }}</small>
          </div>
        </div>
        
        <!-- Typing Indicator -->
        <div v-if="loading" class="typing-indicator">
          <div class="dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>AI is thinking...</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <button 
          v-for="(action, idx) in quickActions" 
          :key="idx"
          @click="sendQuickMessage(action)"
          class="quick-btn"
        >
          {{ action }}
        </button>
      </div>

      <!-- Input Area -->
      <div class="input-area">
        <textarea
          v-model="userInput"
          @keyup.enter.prevent="sendMessage"
          placeholder="Ask me anything about your studies..."
          rows="2"
          :disabled="loading"
          ref="textareaRef"
        ></textarea>
        <button 
          @click="sendMessage" 
          :disabled="!userInput.trim() || loading"
          class="send-btn"
        >
          {{ loading ? '...' : 'Send' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { aiService } from '@/services/aiService'

export default {
  name: 'AIChat',
  data() {
    return {
      chatOpen: false,
      userInput: '',
      messages: [
        {
          type: 'ai',
          content: 'Hello! I\'m your AI study assistant. How can I help you today?',
          timestamp: new Date()
        }
      ],
      loading: false,
      aiStatus: 'Connecting...',
      unreadCount: 0,
      quickActions: [
        'Help with homework',
        'Explain a concept',
        'Exam preparation tips',
        'Practice questions',
        'Study schedule'
      ]
    }
  },
  mounted() {
    this.checkAIHealth()
    
    // Auto-focus textarea when chat opens
    this.$watch('chatOpen', (newVal) => {
      if (newVal) {
        this.$nextTick(() => {
          this.$refs.textareaRef?.focus()
        })
      }
    })
    
    // Check for new messages when chat is closed
    setInterval(() => {
      if (!this.chatOpen && this.messages.length > 1) {
        this.unreadCount++
      }
    }, 60000) // Every minute
  },
  methods: {
    openChat() {
      this.chatOpen = true
      this.unreadCount = 0
      this.$nextTick(() => this.scrollToBottom())
    },
    
    closeChat() {
      this.chatOpen = false
    },
    
    async sendMessage() {
      const message = this.userInput.trim()
      if (!message || this.loading) return

      // Add user message
      this.messages.push({
        type: 'user',
        content: message,
        timestamp: new Date()
      })
      
      this.userInput = ''
      this.loading = true
      this.scrollToBottom()

      try {
        console.log('🟡 Sending message to AI:', message)
        
        // Call AI service
        const response = await aiService.sendMessage(message)
        console.log('🟢 AI Response:', response)
        
        // Handle different response formats
        let aiResponse
        if (typeof response === 'string') {
          aiResponse = response
        } else if (response?.response) {
          aiResponse = response.response
        } else if (response?.content) {
          aiResponse = response.content
        } else {
          aiResponse = 'I received your message. How can I help further?'
        }
        
        // Add AI response
        this.messages.push({
          type: 'ai',
          content: aiResponse,
          timestamp: new Date()
        })
        
      } catch (error) {
        console.error('🔴 Error sending message:', error)
        this.messages.push({
          type: 'ai',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date()
        })
      } finally {
        this.loading = false
        this.scrollToBottom()
      }
    },
    
    sendQuickMessage(action) {
      this.userInput = action
      this.sendMessage()
    },
    
    async checkAIHealth() {
      try {
        const health = await aiService.checkHealth()
        this.aiStatus = health.status === 'healthy' 
          ? 'Online • Ready to help' 
          : 'Offline • Check connection'
      } catch {
        this.aiStatus = 'Offline • Check connection'
      }
    },
    
    formatTime(date) {
      return new Date(date).toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesRef
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
.ai-chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.ai-floating-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  font-weight: bold;
  transition: all 0.3s ease;
  position: relative;
}

.ai-floating-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.ai-floating-btn.has-notification {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
  100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
}

.ai-icon {
  font-size: 20px;
}

.ai-text {
  font-size: 16px;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ef4444;
  color: white;
  font-size: 12px;
  font-weight: bold;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ai-chat-window {
  width: 380px;
  height: 500px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  font-size: 24px;
}

.header-left h3 {
  margin: 0;
  font-size: 16px;
}

.status {
  margin: 0;
  font-size: 12px;
  opacity: 0.8;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.messages-container {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f8fafc;
}

.message {
  display: flex;
  margin-bottom: 15px;
  gap: 10px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 18px;
  margin-top: 5px;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 18px;
  background: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.message.ai .message-content {
  background: #e0e7ff;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.timestamp {
  display: block;
  font-size: 11px;
  opacity: 0.6;
  margin-top: 5px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
}

.dots {
  display: flex;
  gap: 4px;
}

.dots span {
  width: 8px;
  height: 8px;
  background: #9ca3af;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-5px); }
}

.quick-actions {
  padding: 10px 15px;
  background: white;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
  overflow-x: auto;
}

.quick-btn {
  padding: 6px 12px;
  background: #f3f4f6;
  border: none;
  border-radius: 15px;
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
  transition: background 0.2s;
}

.quick-btn:hover {
  background: #e5e7eb;
}

.input-area {
  padding: 15px;
  background: white;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.input-area textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  min-height: 44px;
  max-height: 100px;
  transition: border-color 0.2s;
}

.input-area textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.send-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  transition: opacity 0.2s;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 640px) {
  .ai-chat-container {
    bottom: 10px;
    right: 10px;
  }
  
  .ai-chat-window {
    width: calc(100vw - 40px);
    height: 70vh;
    right: 10px;
    bottom: 70px;
  }
  
  .ai-floating-btn {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>