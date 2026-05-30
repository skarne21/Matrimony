import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/index'
import { useAuthStore } from './auth'

export interface OtherUser {
  id: string
  name: string
  photo: string | null
  city: string
}

export interface ConversationSummary {
  id: string
  other_user: OtherUser
  last_message: { text: string; created_at: string; sender_id: string } | null
  unread_count: number
  last_message_at: string | null
}

export interface Message {
  id: number
  sender_id: string
  content_text: string
  is_read: boolean
  created_at: string
}

export const useConversationsStore = defineStore('conversations', () => {
  const inbox = ref<ConversationSummary[]>([])
  const messages = ref<Record<string, Message[]>>({})
  const socket = ref<WebSocket | null>(null)
  const activeConversationId = ref<string | null>(null)

  async function fetchInbox() {
    const { data } = await api.get('/api/conversations/')
    inbox.value = data
  }

  async function fetchMessages(conversationId: string) {
    const { data } = await api.get(`/api/conversations/${conversationId}/messages/`)
    messages.value[conversationId] = data
  }

  function connectSocket(conversationId: string) {
    if (socket.value) {
      socket.value.close()
      socket.value = null
    }

    const auth = useAuthStore()
    const token = auth.accessToken
    const url = `ws://localhost:8000/ws/chat/${conversationId}/?token=${token}`

    activeConversationId.value = conversationId
    const ws = new WebSocket(url)

    ws.onmessage = (event) => {
      const msg: Message = JSON.parse(event.data)
      if (!messages.value[conversationId]) messages.value[conversationId] = []
      messages.value[conversationId].push(msg)

      const conv = inbox.value.find(c => c.id === conversationId)
      if (conv) {
        conv.last_message = { text: msg.content_text, created_at: msg.created_at, sender_id: msg.sender_id }
        conv.last_message_at = msg.created_at
      }
    }

    socket.value = ws
  }

  function sendMessage(text: string) {
    if (socket.value?.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ message: text }))
    }
  }

  function disconnectSocket() {
    socket.value?.close()
    socket.value = null
    activeConversationId.value = null
  }

  return {
    inbox, messages, activeConversationId,
    fetchInbox, fetchMessages, connectSocket, sendMessage, disconnectSocket,
  }
})
