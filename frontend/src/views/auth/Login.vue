<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../api/index'
import PhoneInput from '../../components/PhoneInput.vue'

const auth = useAuthStore()
const router = useRouter()

const phone = ref(auth.pendingPhone ?? '')
const loading = ref(false)
const error = ref('')

async function quickLogin(testPhone: string) {
  phone.value = testPhone
  await sendOTP()
}

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
        <h1 style="font-size:26px; font-weight:800; color:#c0392b;">Veerabhadra Matrimony</h1>
        <p style="font-size:14px; color:#888; margin-top:4px;">Sign in with your mobile number</p>
      </div>

      <div v-if="error" class="api-error">{{ error }}</div>

      <div class="form-group">
        <label>Mobile Number</label>
        <PhoneInput v-model="phone" />
      </div>

      <button class="btn btn-primary btn-full" :disabled="!phone.trim() || loading" @click="sendOTP">
        {{ loading ? 'Sending OTP…' : 'Send OTP' }}
      </button>

      <p style="text-align:center; margin-top:20px; font-size:14px; color:#888;">
        Don't have an account?
        <RouterLink to="/register" style="color:#c0392b; font-weight:600; text-decoration:none;"> Register</RouterLink>
      </p>

      <!-- Dev quick-login -->
      <div style="margin-top:24px; padding-top:20px; border-top:1px solid #eee;">
        <p style="font-size:12px; color:#bbb; text-align:center; margin-bottom:10px; text-transform:uppercase; letter-spacing:1px;">Dev Quick Login</p>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-secondary btn-full" style="font-size:13px;" @click="quickLogin('+911111111111')">
            Arjun (Male)
          </button>
          <button class="btn btn-secondary btn-full" style="font-size:13px;" @click="quickLogin('+912222222222')">
            Priya (Female)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
