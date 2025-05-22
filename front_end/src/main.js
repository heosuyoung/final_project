import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import SignupForm from './components/SignupForm.vue'
import LoginForm from './components/LoginForm.vue'
import ProfilePage from './components/ProfilePage.vue'
import MapPage from './components/MapPage.vue' // ✅ 추가된 라인

const routes = [
  { path: '/', name: 'home', component: { template: '<div></div>' } },
  { path: '/signup', component: SignupForm },
  { path: '/login', component: LoginForm },
  { path: '/profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/map', component: MapPage }, // ✅ 딱 이 한 줄 추가
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

import { isAuthenticated } from './services/auth.js'

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      next({ 
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

createApp(App).use(router).mount('#app')
