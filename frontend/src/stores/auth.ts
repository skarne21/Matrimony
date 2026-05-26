import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const userId = ref<string | null>(null)
  const pendingPhone = ref<string | null>(null)

  const isLoggedIn = computed(() => !!accessToken.value)

  function setTokens(access: string, refresh: string, id: string) {
    accessToken.value = access
    refreshToken.value = refresh
    userId.value = id
  }

  function setPendingPhone(phone: string) {
    pendingPhone.value = phone
  }

  function logout() {
    accessToken.value = null
    refreshToken.value = null
    userId.value = null
  }

  return { accessToken, refreshToken, userId, pendingPhone, isLoggedIn, setTokens, setPendingPhone, logout }
}, {
  persist: { storage: localStorage },
})
