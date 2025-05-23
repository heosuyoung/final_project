import { createRouter, createWebHistory } from 'vue-router'
import MapPage from '@/components/MapPage.vue'
import LoginForm from '@/components/LoginForm.vue'
import SignupForm from '@/components/SignupForm.vue'
import ProfilePage from '@/components/ProfilePage.vue'
import MainSection from '@/components/MainSection.vue'

const routes = [
  { path: '/', component: MainSection },
  { path: '/map', component: MapPage },
  { path: '/login', component: LoginForm },
  { path: '/signup', component: SignupForm },
  { path: '/profile', component: ProfilePage, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 라우트 가드: 인증이 필요한 페이지 접근 제어
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  
  // 인증이 필요한 페이지에 접근하려고 할 때
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('인증이 필요한 페이지에 접근 시도:', to.path)
    // 로그인 페이지로 리다이렉션하고, 원래 가려던 페이지 정보 전달
    next({ 
      path: '/login', 
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
})

export default router
