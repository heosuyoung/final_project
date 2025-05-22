import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import SignupForm from './components/SignupForm.vue'
import LoginForm from './components/LoginForm.vue'

const routes = [
  { path: '/signup', component: SignupForm },
  { path: '/login', component: LoginForm },
  // 필요시 다른 라우트도 추가
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).mount('#app')
