<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRegistrationStore } from '../../../stores/registration'
import { useAuthStore } from '../../../stores/auth'
import api from '../../../api/index'

const reg = useRegistrationStore()
const auth = useAuthStore()
const router = useRouter()

const submitting = ref(false)
const apiError = ref('')
const uploadingPhoto = ref(false)
const photoPreview = ref<string | null>(null)

const hobbyInput = ref('')

function addHobby() {
  const h = hobbyInput.value.trim()
  if (h && !reg.hobbies.includes(h)) reg.hobbies.push(h)
  hobbyInput.value = ''
}

function removeHobby(h: string) {
  reg.hobbies = reg.hobbies.filter(x => x !== h)
}

async function handlePhotoSelect(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) {
    apiError.value = 'Photo must be under 5 MB.'
    return
  }

  photoPreview.value = URL.createObjectURL(file)
  uploadingPhoto.value = true
  apiError.value = ''

  try {
    // Get presigned URL from backend
    const { data } = await api.post('/api/upload/presigned-url/', { filename: file.name, content_type: file.type })
    // Upload directly to S3
    await fetch(data.url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    reg.profile_pic_url = data.public_url
  } catch {
    apiError.value = 'Photo upload failed. You can add it later from your profile.'
  } finally {
    uploadingPhoto.value = false
  }
}

async function submit() {
  submitting.value = true
  apiError.value = ''
  try {
    await api.post('/api/auth/register/', reg.toPayload())
    auth.setPendingPhone(reg.phone_number)
    reg.reset()
    router.push('/login')
  } catch (err: any) {
    const data = err.response?.data
    if (typeof data === 'object') {
      apiError.value = Object.values(data).flat().join(' ')
    } else {
      apiError.value = 'Registration failed. Please try again.'
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div>
    <p class="card-title">Lifestyle, Photos & Verification</p>
    <p class="card-subtitle">Almost done — just a few last details</p>

    <!-- Lifestyle -->
    <div class="row">
      <div class="form-group">
        <label>Eating Habits</label>
        <select v-model="reg.eating_habit">
          <option value="">Select</option>
          <option value="veg">Vegetarian</option>
          <option value="non_veg">Non-Vegetarian</option>
          <option value="vegan">Vegan</option>
        </select>
      </div>
      <div class="form-group">
        <label>Smoking</label>
        <select v-model="reg.smoking_habit">
          <option value="">Select</option>
          <option value="no">No</option>
          <option value="occasionally">Occasionally</option>
          <option value="yes">Yes</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label>Drinking</label>
      <div class="radio-group">
        <label v-for="opt in ['no','occasionally','regular','daily']" :key="opt"
          class="radio-option" :class="{ selected: reg.drinking_habit === opt }"
          @click="reg.drinking_habit = opt">
          {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
        </label>
      </div>
    </div>

    <div class="form-group">
      <label>Hobbies <span class="optional-tag">optional</span></label>
      <div style="display:flex; gap:8px; margin-bottom:8px;">
        <input type="text" v-model="hobbyInput" placeholder="e.g. Cricket, Reading" @keydown.enter.prevent="addHobby" style="flex:1;" />
        <button type="button" class="btn btn-secondary" style="padding:10px 16px;" @click="addHobby">Add</button>
      </div>
      <div style="display:flex; flex-wrap:wrap; gap:8px;">
        <span v-for="h in reg.hobbies" :key="h"
          style="background:#fff5f5; border:1px solid #f5c6c6; color:#c0392b; padding:4px 10px; border-radius:20px; font-size:13px; display:flex; align-items:center; gap:6px;">
          {{ h }}
          <button @click="removeHobby(h)" style="background:none;border:none;cursor:pointer;color:#c0392b;font-size:15px;line-height:1;">×</button>
        </span>
      </div>
    </div>

    <!-- Location -->
    <hr style="border:none; border-top:1px solid #eee; margin: 16px 0;" />

    <div class="row">
      <div class="form-group">
        <label>City</label>
        <input type="text" v-model="reg.city" placeholder="e.g. Hyderabad" />
      </div>
      <div class="form-group">
        <label>State</label>
        <input type="text" v-model="reg.state" placeholder="e.g. Telangana" />
      </div>
    </div>

    <div class="row">
      <div class="form-group">
        <label>Country</label>
        <input type="text" v-model="reg.country" />
      </div>
      <div class="form-group">
        <label>Postal Code <span class="optional-tag">optional</span></label>
        <input type="text" v-model="reg.postal_code" placeholder="e.g. 500001" />
      </div>
    </div>

    <!-- Bio -->
    <div class="form-group">
      <label>About Me <span class="optional-tag">optional</span></label>
      <textarea v-model="reg.bio" placeholder="Write a short bio about yourself..." rows="3" />
    </div>

    <!-- Photo upload -->
    <hr style="border:none; border-top:1px solid #eee; margin: 16px 0;" />

    <div class="form-group">
      <label>Profile Photo <span class="optional-tag">optional — max 5 MB</span></label>
      <div style="display:flex; align-items:center; gap:16px; margin-top:6px;">
        <div v-if="photoPreview"
          style="width:72px; height:72px; border-radius:50%; overflow:hidden; border:2px solid #c0392b; flex-shrink:0;">
          <img :src="photoPreview" style="width:100%; height:100%; object-fit:cover;" />
        </div>
        <div>
          <label class="btn btn-secondary" style="cursor:pointer; font-size:14px; padding:10px 16px;">
            {{ uploadingPhoto ? 'Uploading…' : 'Choose Photo' }}
            <input type="file" accept="image/*" style="display:none;" @change="handlePhotoSelect" :disabled="uploadingPhoto" />
          </label>
          <p class="hint-text" style="margin-top:6px;">JPG, PNG, or WEBP. Max 5 MB.</p>
        </div>
      </div>
    </div>

    <!-- Photo privacy -->
    <div class="form-group">
      <label>Who can see my photos?</label>
      <div class="radio-group">
        <label class="radio-option" :class="{ selected: reg.photo_privacy === 'public' }" @click="reg.photo_privacy = 'public'">
          Everyone
        </label>
        <label class="radio-option" :class="{ selected: reg.photo_privacy === 'locked' }" @click="reg.photo_privacy = 'locked'">
          Only with my permission
        </label>
      </div>
    </div>

    <div v-if="apiError" class="api-error">{{ apiError }}</div>

    <div class="step-actions">
      <button class="btn btn-secondary" @click="reg.prevStep()">← Back</button>
      <button class="btn btn-primary" :disabled="submitting" @click="submit">
        {{ submitting ? 'Creating profile…' : 'Create Profile' }}
      </button>
    </div>
  </div>
</template>
