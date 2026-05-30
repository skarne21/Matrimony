<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConversationsStore } from '../stores/conversations'
import { useAuthStore } from '../stores/auth'

const store = useConversationsStore()
const auth = useAuthStore()
const router = useRouter()

onMounted(() => store.fetchInbox())

function openChat(id: string) {
  router.push(`/conversations/${id}`)
}

function timeAgo(ts: string | null) {
  if (!ts) return ''
  const diff = (Date.now() - new Date(ts).getTime()) / 1000
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}
</script>

<template>
  <div class="dash-body" style="max-width: 680px;">
    <h2 style="font-size:20px; font-weight:700; margin-bottom:20px;">Messages</h2>

    <div v-if="store.inbox.length === 0" style="text-align:center; color:#aaa; padding:60px 0;">
      No conversations yet. Accept an interest to start chatting.
    </div>

    <div
      v-for="conv in store.inbox"
      :key="conv.id"
      class="conv-row"
      @click="openChat(conv.id)"
    >
      <div class="conv-avatar">
        <img v-if="conv.other_user.photo" :src="conv.other_user.photo" alt="" />
        <div v-else class="avatar-placeholder">{{ conv.other_user.name[0] }}</div>
      </div>
      <div class="conv-body">
        <div class="conv-top">
          <span class="conv-name">{{ conv.other_user.name }}</span>
          <span class="conv-time">{{ timeAgo(conv.last_message_at) }}</span>
        </div>
        <div class="conv-preview">
          <span v-if="conv.last_message">
            <span v-if="conv.last_message.sender_id === auth.userId">You: </span>
            {{ conv.last_message.text }}
          </span>
          <span v-else style="color:#bbb;">No messages yet</span>
          <span v-if="conv.unread_count" class="unread-badge">{{ conv.unread_count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.conv-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: #fff;
  border-radius: 10px;
  margin-bottom: 8px;
  cursor: pointer;
  border: 1px solid #eee;
  transition: background 0.15s;
}
.conv-row:hover { background: #fff5f5; }

.conv-avatar { flex-shrink: 0; }
.conv-avatar img {
  width: 48px; height: 48px;
  border-radius: 50%;
  object-fit: cover;
}
.avatar-placeholder {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: #f5c6c6;
  color: #c0392b;
  font-size: 20px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

.conv-body { flex: 1; min-width: 0; }
.conv-top { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
.conv-name { font-weight: 700; font-size: 15px; color: #1a1a1a; }
.conv-time { font-size: 12px; color: #aaa; flex-shrink: 0; margin-left: 8px; }
.conv-preview {
  font-size: 14px; color: #888;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  display: flex; align-items: center; gap: 8px;
}
.unread-badge {
  background: #c0392b; color: #fff;
  border-radius: 10px; padding: 1px 7px;
  font-size: 12px; font-weight: 700;
  flex-shrink: 0;
}
</style>
