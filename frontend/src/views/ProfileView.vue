<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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

const route = useRoute()
const router = useRouter()

const profile = ref<ProfileDetail | null>(null)
const loading = ref(true)
const error = ref('')

function fmt(val: string | number | null | undefined, fallback = '—') {
  if (val === null || val === undefined || val === '') return fallback
  return String(val)
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
})
</script>

<template>
  <div>
    <nav class="dash-nav">
      <button class="btn btn-secondary" style="padding:8px 16px; font-size:13px;" @click="router.back()">← Back</button>
      <span style="font-size:20px; font-weight:800; color:#c0392b;">Vivah</span>
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
