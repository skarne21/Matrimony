import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: '',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

let refreshing: Promise<void> | null = null

api.interceptors.response.use(
  res => res,
  async (error) => {
    const auth = useAuthStore()
    const original = error.config

    if (error.response?.status === 401 && !original._retry && auth.refreshToken) {
      original._retry = true

      if (!refreshing) {
        refreshing = axios
          .post('/api/auth/token/refresh/', { refresh: auth.refreshToken })
          .then(({ data }) => {
            auth.setTokens(data.access, auth.refreshToken!, auth.userId!)
          })
          .catch(() => {
            auth.logout()
            window.location.href = '/login'
          })
          .finally(() => { refreshing = null })
      }

      await refreshing
      if (auth.accessToken) {
        original.headers.Authorization = `Bearer ${auth.accessToken}`
        return api(original)
      }
    }

    return Promise.reject(error)
  }
)

export default api
