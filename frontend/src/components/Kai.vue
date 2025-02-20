<template>
  <div>
    <!-- Floating Chat Icon -->
    <div class="chat-floating-btn" v-if="!chatOpen" @click="toggleChat">
      <i class="bi bi-chat-dots"></i>
    </div>

    <!-- Chat Panel -->
    <transition name="fade">
      <div v-if="chatOpen" class="offcanvas-chat">
        <!-- Chat Header (Sky Blue) -->
        <div class="chat-header d-flex justify-content-between align-items-center">
          <h5 class="offcanvas-title">Kai</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="toggleChat"
            aria-label="Close"
          ></button>
        </div>
        <!-- Chat Body -->
        <div class="chat-body d-flex flex-column">
          <!-- Chat Messages (scrollable) -->
          <div class="chat-messages flex-grow-1" ref="messagesContainer">
            <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="['message-bubble', { 'message-user': msg.sender === 'user' }]"
            >
              <strong>{{ msg.sender === 'bot' ? 'Kai:' : 'You:' }}</strong> {{ msg.text }}
            </div>
          </div>
          <!-- Chat Input Box -->
          <div class="chat-input border-top p-2">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Type your message..."
                v-model="newMessage"
                @keyup.enter="sendMessage"
              />
              <button class="btn btn-primary" @click="sendMessage">
                <i class="bi bi-send"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, nextTick, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'Chatbot',
  setup() {
    const route = useRoute()
    const chatOpen = ref(false)
    const messages = ref([{ sender: 'bot', text: 'Hello I am Kai! How can I help you?' }])
    const newMessage = ref('')

    const toggleChat = () => {
      chatOpen.value = !chatOpen.value
      if (chatOpen.value) {
        nextTick(() => {
          scrollToBottom()
        })
      }
    }

    const sendMessage = () => {
      if (newMessage.value.trim() !== '') {
        messages.value.push({ sender: 'user', text: newMessage.value.trim() })
        newMessage.value = ''
        nextTick(() => {
          scrollToBottom()
        })
        // Simulate Kai response
        setTimeout(() => {
          messages.value.push({ sender: 'bot', text: 'I am here to help you!' })
          nextTick(() => {
            scrollToBottom()
          })
        }, 500)
      }
    }

    const scrollToBottom = () => {
      nextTick(() => {
        const container = messagesContainer.value
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }

    // Reference for the messages container
    const messagesContainer = ref(null)

    // Watch for route changes: close chat when route changes
    watch(
      () => route.fullPath,
      () => {
        chatOpen.value = false
      },
    )

    return {
      chatOpen,
      messages,
      newMessage,
      toggleChat,
      sendMessage,
      scrollToBottom,
      messagesContainer,
      route,
    }
  },
}
</script>

<style scoped>
/* Floating Chat Icon */
.chat-floating-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background-color: #87ceeb; /* Sky Blue */
  color: #fff;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  z-index: 1000;
  transition:
    transform 0.3s,
    background-color 0.3s;
}
.chat-floating-btn:hover {
  transform: scale(1.05);
  background-color: #00bfff; /* DeepSkyBlue */
}

/* Chat Panel Container */
.offcanvas-chat {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 320px;
  height: 400px; /* Fixed height */
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Chat Header */
.chat-header {
  background-color: #87ceeb; /* Sky Blue */
  color: #fff;
  padding: 0.75rem;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Chat Body */
.chat-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Allow inner flex items to scroll */
}

/* Chat Messages */
.chat-messages {
  flex: 1;
  min-height: 0; /* Critical for nested flex scrolling */
  overflow-y: auto;
  padding: 1rem;
  background-color: #fff;
}

/* Message Bubbles */
.message-bubble {
  margin-bottom: 0.75rem;
  max-width: 80%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  background-color: #f1f1f1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.message-user {
  background-color: #d1e7dd;
  margin-left: auto;
  text-align: right;
}

/* Chat Input */
.chat-input {
  border-top: 1px solid #ccc;
  padding: 0.5rem;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
