<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../api/index'

const auth = useAuthStore()
const router = useRouter()

const otp = ref('')
const loading = ref(false)
const error = ref('')

async function verify() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.post('/api/auth/verify-otp/', {
      phone_number: auth.pendingPhone,
      otp: otp.value,
    })
    auth.setTokens(data.access, data.refresh, data.user_id)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.error ?? 'Invalid OTP. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page-center">
    <div class="card">
      <div style="text-align:center; margin-bottom:28px;">
        <h1 style="font-size:26px; font-weight:800; color:#c0392b;">Verify OTP</h1>
        <p style="font-size:14px; color:#888; margin-top:4px;">
          Enter the 6-digit code sent to {{ auth.pendingPhone }}
        </p>
      </div>

      <div v-if="error" class="api-error">{{ error }}</div>

      <div class="form-group">
        <label>OTP</label>
        <input type="text" v-model="otp" maxlength="6" placeholder="6-digit code" style="letter-spacing:8px; font-size:22px; text-align:center;" @keydown.enter="verify" />
        <p class="hint-text">During development, check the Django server console for the OTP.</p>
      </div>

      <button class="btn btn-primary btn-full" :disabled="otp.length !== 6 || loading" @click="verify">
        {{ loading ? 'Verifying…' : 'Verify & Sign In' }}
      </button>

      <p style="text-align:center; margin-top:16px; font-size:14px;">
        <RouterLink to="/login" style="color:#c0392b; font-weight:600; text-decoration:none;">← Change number</RouterLink>
      </p>
    </div>
  </div>
</template>
