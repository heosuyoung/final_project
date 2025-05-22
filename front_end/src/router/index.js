import { createRouter, createWebHistory } from 'vue-router'
import MapPage from '@/components/MapPage.vue'
import App from '@/App.vue' // 이건 진짜 있는 파일임

const routes = [
  { path: '/', component: App },       // 홈 → App.vue로 보여줌
  { path: '/map', component: MapPage } // /map → 카카오 지도 페이지
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
