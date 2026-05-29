<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api/index'

interface InterestProfile {
  user_id: string
  first_name: string
  last_name: string
  age: number
  city: string
  state: string
  occupation: string
  profile_pic_url: string
  is_verified: boolean
}

interface InterestItem {
  id: number
  status: string
  created_at: string
  sender_profile: InterestProfile
  receiver_profile: InterestProfile
}

const router = useRouter()
const auth = useAuthStore()

const received = ref<InterestItem[]>([])
const sent = ref<InterestItem[]>([])
const activeTab = ref<'received' | 'sent'>('received')
const loading = ref(true)
const actionLoadingId = ref<number | null>(null)

async function load() {
  loading.value = true
  try {
    const [r, s] = await Promise.all([
      api.get('/api/interests/received/'),
      api.get('/api/interests/sent/'),
    ])
    received.value = r.data
    sent.value = s.data
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

async function respond(id: number, action: 'accept' | 'decline') {
  actionLoadingId.value = id
  try {
    await api.patch(`/api/interests/${id}/`, { action })
    received.value = received.value.filter(i => i.id !== id)
  } catch { /* ignore */ } finally {
    actionLoadingId.value = null
  }
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(load)
</script>

<template>
  <div>
    <nav class="dash-nav">
      <span style="font-size:20px; font-weight:800; color:#c0392b;">Veerabhadra Matrimony</span>
      <div style="display:flex; gap:12px; align-items:center;">
        <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;" @click="router.push('/dashboard')">← Dashboard</button>
        <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;" @click="logout">Logout</button>
      </div>
    </nav>

    <div class="dash-body" style="max-width:700px;">
      <h2 style="font-size:20px; font-weight:700; color:#1a1a1a; margin-bottom:20px;">Interests</h2>

      <!-- Tabs -->
      <div style="display:flex; gap:0; margin-bottom:24px; border-bottom:2px solid #eee;">
        <button
          v-for="tab in ['received','sent'] as const" :key="tab"
          @click="activeTab = tab"
          :style="{
            padding: '10px 24px',
            fontWeight: '600',
            fontSize: '14px',
            border: 'none',
            background: 'none',
            cursor: 'pointer',
            color: activeTab === tab ? '#c0392b' : '#888',
            borderBottom: activeTab === tab ? '2px solid #c0392b' : '2px solid transparent',
            marginBottom: '-2px',
          }"
        >
          {{ tab === 'received' ? `Received (${received.length})` : `Sent (${sent.length})` }}
        </button>
      </div>

      <div v-if="loading" style="text-align:center; padding:40px 0; color:#888;">Loading…</div>

      <!-- Received -->
      <template v-else-if="activeTab === 'received'">
        <div v-if="received.length === 0" style="text-align:center; padding:40px 0; color:#888;">
          No pending interest requests.
        </div>
        <div v-for="item in received" :key="item.id" class="interest-card">
          <div class="interest-avatar" @click="router.push(`/profile/${item.sender_profile.user_id}`)">
            <img v-if="item.sender_profile.profile_pic_url" :src="item.sender_profile.profile_pic_url" />
            <span v-else>{{ item.sender_profile.first_name.charAt(0) }}</span>
          </div>
          <div class="interest-info" @click="router.push(`/profile/${item.sender_profile.user_id}`)">
            <p class="interest-name">{{ item.sender_profile.first_name }} {{ item.sender_profile.last_name }}, {{ item.sender_profile.age }}</p>
            <p class="interest-meta" v-if="item.sender_profile.city || item.sender_profile.state">
              📍 {{ [item.sender_profile.city, item.sender_profile.state].filter(Boolean).join(', ') }}
            </p>
            <p class="interest-meta" v-if="item.sender_profile.occupation">💼 {{ item.sender_profile.occupation }}</p>
          </div>
          <div class="interest-actions">
            <button class="btn btn-primary" style="background:#27ae60; padding:8px 16px; font-size:13px;"
              :disabled="actionLoadingId === item.id"
              @click.stop="respond(item.id, 'accept')">
              Accept
            </button>
            <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;"
              :disabled="actionLoadingId === item.id"
              @click.stop="respond(item.id, 'decline')">
              Decline
            </button>
          </div>
        </div>
      </template>

      <!-- Sent -->
      <template v-else>
        <div v-if="sent.length === 0" style="text-align:center; padding:40px 0; color:#888;">
          You haven't sent any interests yet.
        </div>
        <div v-for="item in sent" :key="item.id" class="interest-card" @click="router.push(`/profile/${item.receiver_profile.user_id}`)">
          <div class="interest-avatar">
            <img v-if="item.receiver_profile.profile_pic_url" :src="item.receiver_profile.profile_pic_url" />
            <span v-else>{{ item.receiver_profile.first_name.charAt(0) }}</span>
          </div>
          <div class="interest-info">
            <p class="interest-name">{{ item.receiver_profile.first_name }} {{ item.receiver_profile.last_name }}, {{ item.receiver_profile.age }}</p>
            <p class="interest-meta" v-if="item.receiver_profile.city || item.receiver_profile.state">
              📍 {{ [item.receiver_profile.city, item.receiver_profile.state].filter(Boolean).join(', ') }}
            </p>
            <p class="interest-meta" v-if="item.receiver_profile.occupation">💼 {{ item.receiver_profile.occupation }}</p>
          </div>
          <span :style="{
            fontSize: '13px',
            fontWeight: '600',
            padding: '6px 12px',
            borderRadius: '20px',
            background: item.status === 'accepted' ? '#e8f5e9' : item.status === 'declined' ? '#fafafa' : '#fff8e1',
            color: item.status === 'accepted' ? '#27ae60' : item.status === 'declined' ? '#aaa' : '#f39c12',
          }">
            {{ item.status === 'accepted' ? '✓ Accepted' : item.status === 'declined' ? 'Declined' : 'Pending' }}
          </span>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.interest-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: box-shadow 0.15s;
}
.interest-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.interest-avatar {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  background: #f0e8e8;
  display: flex;
  align-items: center;
  justify-content: center;
}
.interest-avatar img { width: 100%; height: 100%; object-fit: cover; }
.interest-avatar span { font-size: 22px; font-weight: 700; color: #c0392b; opacity: 0.5; }
.interest-info { flex: 1; min-width: 0; }
.interest-name { font-size: 15px; font-weight: 700; color: #1a1a1a; }
.interest-meta { font-size: 13px; color: #666; margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.interest-actions { display: flex; gap: 8px; flex-shrink: 0; }
</style>
