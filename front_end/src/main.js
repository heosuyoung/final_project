import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // 라우터 import 방식 변경

createApp(App).use(router).mount('#app')
