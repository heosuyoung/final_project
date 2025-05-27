import { createRouter, createWebHistory } from 'vue-router'
import MapPage from '../components/MapPage.vue'
import LoginForm from '../components/LoginForm.vue'
import SignupForm from '../components/SignupForm.vue'
import ProfilePage from '../components/ProfilePage.vue'
import MainSection from '../components/MainSection.vue'
import CommoditiesPage from '../components/CommoditiesPage.vue'
import SavingsRecommendation from '../components/SavingsRecommendation.vue'
// 추가로 isAuthenticated 함수 import
import { isAuthenticated } from '../services/auth.js'
import StocksPage from '@/components/StocksPage.vue'
import StockCommunity from '@/components/StockCommunity.vue'
import WritePost from '@/components/WritePost.vue'
import PostDetail from '@/components/PostDetail.vue'
import UserProfile from '../components/UserProfile.vue'
import OAuthCallback from '../components/OAuthCallback.vue'
import AboutPage from '../components/AboutPage.vue'

const routes = [
  { path: '/', component: MainSection },
  { path: '/map', component: MapPage },
  { path: '/login', component: LoginForm },
  { path: '/signup', component: SignupForm },  { path: '/profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/commodities', component: CommoditiesPage },
  { path: '/savings', component: SavingsRecommendation },
  { path: '/stocks', component: StocksPage },  { path: '/community/:code', component: StockCommunity },
  { path: '/community/:code/write', component: WritePost },
  { path: '/community/:code/:postId', component: PostDetail },
  { path: '/user/:username', component: UserProfile },
  { path: '/oauth/callback', component: OAuthCallback },  // 소셜 로그인 콜백 경로 추가
  { path: '/about', component: AboutPage }  // EA$E 소개 페이지 추가
]


const router = createRouter({
  history: createWebHistory(),
  routes
})

// 라우트 가드: 인증이 필요한 페이지 접근 제어
router.beforeEach((to, from, next) => {
  // 직접 localStorage를 확인하는 대신 auth.js의 isAuthenticated 함수 사용
  if (to.meta.requiresAuth && !isAuthenticated()) {
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
