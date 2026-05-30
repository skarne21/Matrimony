<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api/index'

interface ProfileDetail {
  user_id: string
  first_name: string
  last_name: string
  age: number
  gender: string
  marital_status: string
  height_cm: number | null
  weight_kg: number | null
  profile_created_by: string
  mother_tongue: string
  religion_name: string
  caste_display: string
  sub_caste: string
  nakshatra: string
  rashi: string
  is_manglik: boolean | null
  education_level: string
  college: string
  occupation: string
  company: string
  annual_income: number | null
  work_location: string
  father_name: string
  father_occupation: string
  mother_name: string
  mother_occupation: string
  brothers_count: number
  sisters_count: number
  family_type: string
  family_status: string
  eating_habit: string
  smoking_habit: string
  drinking_habit: string
  hobbies: string[]
  bio: string
  photo_privacy: string
  profile_pic_url: string
  is_verified: boolean
  city: string
  state: string
  country: string
  postal_code: string
}

interface InterestState {
  id: number
  status: string
  direction: 'sent' | 'received'
  message: string
  conversation_id: string | null
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const profile = ref<ProfileDetail | null>(null)
const interest = ref<InterestState | null>(null)
const loading = ref(true)
const actionLoading = ref(false)
const error = ref('')
const showNoteInput = ref(false)
const connectNote = ref('')

const isOwnProfile = () => auth.userId === route.params.id

function fmt(val: string | number | null | undefined, fallback = '—') {
  if (val === null || val === undefined || val === '') return fallback
  return String(val)
}

async function loadInterestStatus() {
  if (isOwnProfile()) return
  try {
    const { data } = await api.get(`/api/interests/with/${route.params.id}/`)
    interest.value = data
  } catch { /* non-blocking */ }
}

async function sendInterest(message = '') {
  actionLoading.value = true
  try {
    const { data } = await api.post('/api/interests/', { receiver_id: route.params.id, message })
    interest.value = { id: data.id, status: data.status, direction: 'sent', message: data.message, conversation_id: null }
    showNoteInput.value = false
    connectNote.value = ''
  } catch { /* ignore */ } finally {
    actionLoading.value = false
  }
}

async function withdrawInterest() {
  if (!interest.value) return
  actionLoading.value = true
  try {
    await api.patch(`/api/interests/${interest.value.id}/`, { action: 'withdraw' })
    interest.value = null
  } catch { /* ignore */ } finally {
    actionLoading.value = false
  }
}

async function respondToInterest(action: 'accept' | 'decline') {
  if (!interest.value) return
  actionLoading.value = true
  try {
    const { data } = await api.patch(`/api/interests/${interest.value.id}/`, { action })
    interest.value = { ...interest.value, status: data.status }
    if (action === 'accept') await loadInterestStatus()
  } catch { /* ignore */ } finally {
    actionLoading.value = false
  }
}

function openChat() {
  if (interest.value?.conversation_id) {
    router.push(`/conversations/${interest.value.conversation_id}`)
  } else {
    router.push('/conversations')
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get(`/api/users/${route.params.id}/`)
    profile.value = data
  } catch {
    error.value = 'Profile not found.'
  } finally {
    loading.value = false
  }
  await loadInterestStatus()
})
</script>

<template>
  <div>
    <nav class="dash-nav">
      <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;" @click="router.back()">← Back</button>
      <span style="font-size:20px; font-weight:800; color:#c0392b;">Veerabhadra Matrimony</span>
      <span />
    </nav>

    <div class="profile-detail-wrap">
      <div v-if="loading" style="text-align:center; padding:60px 0; color:#888;">Loading…</div>
      <div v-else-if="error" class="api-error">{{ error }}</div>

      <template v-else-if="profile">
        <!-- Header card -->
        <div class="detail-section" style="display:flex; gap:24px; align-items:flex-start;">
          <div style="flex-shrink:0; width:120px; height:120px; border-radius:12px; overflow:hidden; background:#f0e8e8; display:flex; align-items:center; justify-content:center;">
            <img v-if="profile.profile_pic_url" :src="profile.profile_pic_url" style="width:100%;height:100%;object-fit:cover;" />
            <span v-else style="font-size:48px; font-weight:700; color:#c0392b; opacity:0.4;">{{ profile.first_name.charAt(0) }}</span>
          </div>
          <div style="flex:1;">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <h1 style="font-size:22px; font-weight:800; color:#1a1a1a;">{{ profile.first_name }} {{ profile.last_name }}, {{ profile.age }}</h1>
              <span v-if="profile.is_verified" style="background:#27ae60; color:#fff; font-size:12px; font-weight:700; padding:3px 10px; border-radius:20px;">✓ Verified</span>
            </div>
            <p style="font-size:15px; color:#555; margin-top:6px;" v-if="profile.city || profile.state">
              📍 {{ [profile.city, profile.state, profile.country].filter(Boolean).join(', ') }}
            </p>
            <p style="font-size:15px; color:#555; margin-top:4px;" v-if="profile.occupation">
              💼 {{ profile.occupation }}<span v-if="profile.company"> · {{ profile.company }}</span>
            </p>
            <p style="font-size:14px; color:#888; margin-top:8px; line-height:1.5;" v-if="profile.bio">{{ profile.bio }}</p>

            <!-- Interest actions -->
            <div v-if="!isOwnProfile()" style="margin-top:16px;">
              <!-- No relationship — Connect + optional note -->
              <template v-if="!interest">
                <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
                  <button class="btn btn-primary" :disabled="actionLoading" @click="sendInterest()">
                    {{ actionLoading ? '…' : 'Connect' }}
                  </button>
                  <button class="btn btn-secondary" style="font-size:13px;" @click="showNoteInput = !showNoteInput">
                    {{ showNoteInput ? 'Cancel' : 'Add a note' }}
                  </button>
                </div>
                <div v-if="showNoteInput" style="margin-top:12px;">
                  <textarea
                    v-model="connectNote"
                    placeholder="Write a short note with your request… (optional)"
                    maxlength="300"
                    style="width:100%; padding:10px 12px; border:1.5px solid #ddd; border-radius:8px; font-family:inherit; font-size:14px; resize:vertical; min-height:80px; outline:none;"
                  />
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                    <span style="font-size:12px; color:#aaa;">{{ connectNote.length }}/300</span>
                    <button class="btn btn-primary" style="padding:8px 20px; font-size:13px;" :disabled="actionLoading" @click="sendInterest(connectNote)">
                      {{ actionLoading ? '…' : 'Send with note' }}
                    </button>
                  </div>
                </div>
              </template>

              <!-- I sent, pending -->
              <template v-else-if="interest.direction === 'sent' && interest.status === 'pending'">
                <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                  <span style="font-size:14px; color:#888;">Request sent</span>
                  <button class="btn btn-secondary" style="font-size:13px;" :disabled="actionLoading" @click="withdrawInterest">
                    {{ actionLoading ? '…' : 'Withdraw' }}
                  </button>
                </div>
                <p v-if="interest.message" style="font-size:13px; color:#aaa; margin-top:8px; font-style:italic;">"{{ interest.message }}"</p>
              </template>

              <!-- Connected (either direction) -->
              <template v-else-if="interest.status === 'accepted'">
                <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                  <span style="background:#e8f5e9; color:#27ae60; font-size:14px; font-weight:700; padding:10px 18px; border-radius:8px;">✓ Connected</span>
                  <button class="btn btn-primary" @click="openChat">Message</button>
                </div>
              </template>

              <!-- I sent, declined -->
              <template v-else-if="interest.direction === 'sent' && interest.status === 'declined'">
                <span style="color:#aaa; font-size:14px;">Request was declined</span>
              </template>

              <!-- They sent me, pending -->
              <template v-else-if="interest.direction === 'received' && interest.status === 'pending'">
                <div v-if="interest.message" style="background:#fff8f0; border:1px solid #f0e0c0; border-radius:8px; padding:12px; margin-bottom:12px; font-size:14px; color:#555; font-style:italic;">
                  "{{ interest.message }}"
                </div>
                <div style="display:flex; gap:10px; flex-wrap:wrap;">
                  <button class="btn btn-primary" :disabled="actionLoading" @click="respondToInterest('accept')" style="background:#27ae60;">
                    {{ actionLoading ? '…' : '✓ Accept' }}
                  </button>
                  <button class="btn btn-secondary" :disabled="actionLoading" @click="respondToInterest('decline')">
                    Decline
                  </button>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- Personal & Religion -->
        <div class="detail-section">
          <h3>Personal & Religion</h3>
          <div class="detail-grid">
            <div class="detail-item"><label>Religion</label><p>{{ fmt(profile.religion_name) }}</p></div>
            <div class="detail-item"><label>Caste</label><p>{{ fmt(profile.caste_display) }}</p></div>
            <div class="detail-item" v-if="profile.sub_caste"><label>Sub-caste</label><p>{{ profile.sub_caste }}</p></div>
            <div class="detail-item"><label>Mother Tongue</label><p>{{ fmt(profile.mother_tongue) }}</p></div>
            <div class="detail-item"><label>Marital Status</label><p>{{ fmt(profile.marital_status)?.replace('_', ' ') }}</p></div>
            <div class="detail-item" v-if="profile.height_cm"><label>Height</label><p>{{ profile.height_cm }} cm</p></div>
            <div class="detail-item" v-if="profile.nakshatra"><label>Nakshatra</label><p>{{ profile.nakshatra }}</p></div>
            <div class="detail-item" v-if="profile.rashi"><label>Rashi</label><p>{{ profile.rashi }}</p></div>
            <div class="detail-item" v-if="profile.is_manglik !== null"><label>Manglik</label><p>{{ profile.is_manglik ? 'Yes' : 'No' }}</p></div>
          </div>
        </div>

        <!-- Education & Career -->
        <div class="detail-section">
          <h3>Education & Career</h3>
          <div class="detail-grid">
            <div class="detail-item"><label>Education</label><p>{{ fmt(profile.education_level) }}</p></div>
            <div class="detail-item" v-if="profile.college"><label>College</label><p>{{ profile.college }}</p></div>
            <div class="detail-item"><label>Occupation</label><p>{{ fmt(profile.occupation) }}</p></div>
            <div class="detail-item" v-if="profile.company"><label>Company</label><p>{{ profile.company }}</p></div>
            <div class="detail-item" v-if="profile.annual_income"><label>Annual Income</label><p>₹{{ profile.annual_income.toLocaleString('en-IN') }}</p></div>
            <div class="detail-item" v-if="profile.work_location"><label>Work Location</label><p>{{ profile.work_location }}</p></div>
          </div>
        </div>

        <!-- Family -->
        <div class="detail-section">
          <h3>Family</h3>
          <div class="detail-grid">
            <div class="detail-item" v-if="profile.father_name"><label>Father</label><p>{{ profile.father_name }}<span v-if="profile.father_occupation"> ({{ profile.father_occupation }})</span></p></div>
            <div class="detail-item" v-if="profile.mother_name"><label>Mother</label><p>{{ profile.mother_name }}<span v-if="profile.mother_occupation"> ({{ profile.mother_occupation }})</span></p></div>
            <div class="detail-item"><label>Siblings</label><p>{{ profile.brothers_count }}B / {{ profile.sisters_count }}S</p></div>
            <div class="detail-item" v-if="profile.family_type"><label>Family Type</label><p style="text-transform:capitalize;">{{ profile.family_type }}</p></div>
            <div class="detail-item" v-if="profile.family_status"><label>Family Status</label><p>{{ profile.family_status }}</p></div>
          </div>
        </div>

        <!-- Lifestyle -->
        <div class="detail-section">
          <h3>Lifestyle</h3>
          <div class="detail-grid">
            <div class="detail-item" v-if="profile.eating_habit"><label>Diet</label><p style="text-transform:capitalize;">{{ profile.eating_habit.replace('_', '-') }}</p></div>
            <div class="detail-item" v-if="profile.smoking_habit"><label>Smoking</label><p style="text-transform:capitalize;">{{ profile.smoking_habit }}</p></div>
            <div class="detail-item" v-if="profile.drinking_habit"><label>Drinking</label><p style="text-transform:capitalize;">{{ profile.drinking_habit }}</p></div>
          </div>
          <div v-if="profile.hobbies.length" style="margin-top:12px;">
            <label style="font-size:12px; color:#aaa; font-weight:600; text-transform:uppercase; letter-spacing:0.4px;">Hobbies</label>
            <div style="margin-top:6px;">
              <span v-for="h in profile.hobbies" :key="h" class="tag">{{ h }}</span>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
