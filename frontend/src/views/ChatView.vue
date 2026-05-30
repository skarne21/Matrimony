<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useConversationsStore } from '../stores/conversations'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const store = useConversationsStore()
const auth = useAuthStore()

const conversationId = route.params.id as string
const text = ref('')
const messagesEl = ref<HTMLElement | null>(null)

const conv = computed(() => store.inbox.find(c => c.id === conversationId))
const messages = computed(() => store.messages[conversationId] ?? [])

onMounted(async () => {
  if (store.inbox.length === 0) await store.fetchInbox()
  await store.fetchMessages(conversationId)
  store.connectSocket(conversationId)
  scrollToBottom()
})

onUnmounted(() => store.disconnectSocket())

watch(messages, () => nextTick(scrollToBottom), { deep: true })

function scrollToBottom() {
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

function send() {
  const msg = text.value.trim()
  if (!msg) return
  store.sendMessage(msg)
  text.value = ''
}

function formatTime(ts: string) {
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="chat-wrap">
    <!-- Header -->
    <div class="chat-header">
      <button class="back-btn" @click="router.push('/conversations')">&#8592;</button>
      <div v-if="conv" class="chat-header-info">
        <div class="chat-avatar">
          <img v-if="conv.other_user.photo" :src="conv.other_user.photo" alt="" />
          <div v-else class="avatar-placeholder-sm">{{ conv.other_user.name[0] }}</div>
        </div>
        <div>
          <div style="font-weight:700; font-size:15px;">{{ conv.other_user.name }}</div>
          <div style="font-size:12px; color:#aaa;">{{ conv.other_user.city }}</div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div class="messages-area" ref="messagesEl">
      <div v-if="messages.length === 0" style="text-align:center; color:#bbb; margin-top:40px;">
        Say hello!
      </div>

      <div
        v-for="msg in messages"
        :key="msg.id"
        class="msg-row"
        :class="msg.sender_id === auth.userId ? 'mine' : 'theirs'"
      >
        <div class="bubble">
          {{ msg.content_text }}
          <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="chat-input-bar">
      <input
        type="text"
        v-model="text"
        placeholder="Type a message…"
        @keydown.enter="send"
        class="chat-input"
      />
      <button class="send-btn" :disabled="!text.trim()" @click="send">Send</button>
    </div>
  </div>
</template>

<style scoped>
.chat-wrap {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 680px;
  margin: 0 auto;
  background: #f7f2f2;
}

.chat-header {
  background: #fff;
  border-bottom: 1px solid #eee;
  padding: 0 16px;
  height: 60px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.back-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #c0392b;
  padding: 4px 8px;
}
.chat-header-info { display: flex; align-items: center; gap: 10px; }
.chat-avatar img { width: 38px; height: 38px; border-radius: 50%; object-fit: cover; }
.avatar-placeholder-sm {
  width: 38px; height: 38px; border-radius: 50%;
  background: #f5c6c6; color: #c0392b;
  font-weight: 700; font-size: 16px;
  display: flex; align-items: center; justify-content: center;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.msg-row { display: flex; }
.msg-row.mine { justify-content: flex-end; }
.msg-row.theirs { justify-content: flex-start; }

.bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  position: relative;
}
.mine .bubble {
  background: #c0392b;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.theirs .bubble {
  background: #fff;
  color: #1a1a1a;
  border: 1px solid #eee;
  border-bottom-left-radius: 4px;
}

.msg-time {
  display: block;
  font-size: 10px;
  opacity: 0.65;
  margin-top: 4px;
  text-align: right;
}

.chat-input-bar {
  background: #fff;
  border-top: 1px solid #eee;
  padding: 12px 16px;
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}
.chat-input {
  flex: 1;
  font-family: inherit;
  font-size: 15px;
  padding: 10px 14px;
  border: 1.5px solid #ddd;
  border-radius: 24px;
  outline: none;
  background: #fafafa;
  transition: border-color 0.2s;
}
.chat-input:focus { border-color: #c0392b; background: #fff; }
.send-btn {
  background: #c0392b;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 10px 22px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.send-btn:hover:not(:disabled) { background: #a93226; }
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
