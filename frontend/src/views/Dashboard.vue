<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ProfileCard from '../components/ProfileCard.vue'
import api from '../api/index'

interface ProfileCardData {
  user_id: string
  first_name: string
  last_name: string
  age: number
  city: string
  state: string
  occupation: string
  religion_name: string
  profile_pic_url: string
  is_verified: boolean
}

const auth = useAuthStore()
const router = useRouter()

const profiles = ref<ProfileCardData[]>([])
const page = ref(1)
const hasNext = ref(false)
const total = ref(0)
const loading = ref(false)
const error = ref('')

async function loadPage(p: number) {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/matches/', { params: { page: p } })
    if (p === 1) {
      profiles.value = data.results
    } else {
      profiles.value.push(...data.results)
    }
    page.value = p
    hasNext.value = data.has_next
    total.value = data.total
  } catch {
    error.value = 'Could not load matches. Please try again.'
  } finally {
    loading.value = false
  }
}

function loadMore() {
  loadPage(page.value + 1)
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(() => loadPage(1))
</script>

<template>
  <div>
    <nav class="dash-nav">
      <span style="font-size:20px; font-weight:800; color:#c0392b;">Veerabhadra Matrimony</span>
      <div style="display:flex; gap:12px; align-items:center;">
        <span style="font-size:14px; color:#888;">{{ total }} matches found</span>
        <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;" @click="router.push('/interests')">Interests</button>
        <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;" @click="logout">Logout</button>
      </div>
    </nav>

    <div class="dash-body">
      <div v-if="error" class="api-error" style="margin-bottom:16px;">{{ error }}</div>

      <div v-if="profiles.length === 0 && !loading" style="text-align:center; padding:60px 0; color:#888;">
        <p style="font-size:18px; font-weight:600; margin-bottom:8px;">No matches yet</p>
        <p style="font-size:14px;">Try widening your partner preferences.</p>
      </div>

      <div class="profile-grid">
        <ProfileCard
          v-for="p in profiles"
          :key="p.user_id"
          :userId="p.user_id"
          :firstName="p.first_name"
          :lastName="p.last_name"
          :age="p.age"
          :city="p.city"
          :state="p.state"
          :occupation="p.occupation"
          :religionName="p.religion_name"
          :profilePicUrl="p.profile_pic_url"
          :isVerified="p.is_verified"
        />
      </div>

      <div v-if="loading" style="text-align:center; padding:32px 0; color:#888;">Loading…</div>

      <div v-if="hasNext && !loading" style="text-align:center; margin-top:24px;">
        <button class="btn btn-secondary" @click="loadMore">Load more</button>
      </div>
    </div>
  </div>
</template>
