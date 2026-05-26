<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="page-center">
    <div class="card" style="text-align:center;">
      <h1 style="font-size:26px; font-weight:800; color:#c0392b; margin-bottom:8px;">Vivah</h1>
      <p style="color:#444; margin-bottom:24px;">Welcome! You are logged in.</p>
      <p style="font-size:13px; color:#888; margin-bottom:24px;">Dashboard — Phase 4 (coming soon)</p>
      <button class="btn btn-secondary" @click="logout">Logout</button>
    </div>
  </div>
</template>
