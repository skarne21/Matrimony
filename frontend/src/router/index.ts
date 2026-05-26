import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/register',
    },
    {
      path: '/register',
      component: () => import('../views/auth/Register.vue'),
      meta: { guest: true },
    },
    {
      path: '/login',
      component: () => import('../views/auth/Login.vue'),
      meta: { guest: true },
    },
    {
      path: '/verify-otp',
      component: () => import('../views/auth/VerifyOTP.vue'),
      meta: { guest: true },
    },
    {
      path: '/dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) return '/login'
  if (to.meta.guest && auth.isLoggedIn) return '/dashboard'
})

export default router
