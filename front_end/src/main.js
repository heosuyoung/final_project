import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import SignupForm from './components/SignupForm.vue'
import LoginForm from './components/LoginForm.vue'
import ProfilePage from './components/ProfilePage.vue'

const routes = [
  { path: '/', name: 'home', component: { template: '<div></div>' } }, // 빈 컴포넌트로 홈 경로 처리
  { path: '/signup', component: SignupForm },
  { path: '/login', component: LoginForm },
  { path: '/profile', component: ProfilePage, meta: { requiresAuth: true } },
  // 필요시 다른 라우트도 추가
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 인증 상태 확인 함수 임포트
import { isAuthenticated } from './services/auth.js'

// 인증이 필요한 라우트 보호
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    // 인증 상태 확인
    if (!isAuthenticated()) {
      // 로그인되지 않은 경우 로그인 페이지로 리다이렉트
      next({ 
        path: '/login',
        query: { redirect: to.fullPath } // 로그인 후 원래 가려던 페이지로 이동하기 위한 정보 저장
      })
    } else {
      // 로그인된 상태면 진행
      next()
    }
  } else {
    // 인증이 필요없는 페이지는 그대로 진행
    next()
  }
})

createApp(App).use(router).mount('#app')
