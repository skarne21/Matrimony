<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../api/index'

const auth = useAuthStore()
const router = useRouter()

const phone = ref(auth.pendingPhone ?? '')
const loading = ref(false)
const error = ref('')

async function sendOTP() {
  loading.value = true
  error.value = ''
  try {
    await api.post('/api/auth/login/', { phone_number: phone.value })
    auth.setPendingPhone(phone.value)
    router.push('/verify-otp')
  } catch (err: any) {
    error.value = err.response?.data?.error ?? 'Something went wrong.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page-center">
    <div class="card">
      <div style="text-align:center; margin-bottom:28px;">
        <h1 style="font-size:26px; font-weight:800; color:#c0392b;">Vivah</h1>
        <p style="font-size:14px; color:#888; margin-top:4px;">Sign in with your mobile number</p>
      </div>

      <div v-if="error" class="api-error">{{ error }}</div>

      <div class="form-group">
        <label>Mobile Number</label>
        <input type="tel" v-model="phone" placeholder="+91 98765 43210" @keydown.enter="sendOTP" />
      </div>

      <button class="btn btn-primary btn-full" :disabled="!phone.trim() || loading" @click="sendOTP">
        {{ loading ? 'Sending OTP…' : 'Send OTP' }}
      </button>

      <p style="text-align:center; margin-top:20px; font-size:14px; color:#888;">
        Don't have an account?
        <RouterLink to="/register" style="color:#c0392b; font-weight:600; text-decoration:none;"> Register</RouterLink>
      </p>
    </div>
  </div>
</template>
