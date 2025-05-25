<template>
  <div class="community">
    <h2>{{ stockName }} 종목 토론방</h2>

    <div v-if="isLoggedIn">
      <router-link :to="`/community/${stockCode}/write`">
        <button class="write-btn">✍ 글쓰기</button>
      </router-link>
    </div>
    <p v-else>로그인 후 글쓰기가 가능합니다.</p>

    <ul class="post-list">
      <li v-for="post in dummyPosts" :key="post.id" class="post-item">
        <router-link :to="`/community/${stockCode}/${post.id}`" class="post-title">
          {{ post.title }}
        </router-link>
        <div class="post-meta">{{ post.author }} · {{ post.date }}</div>
      </li>
    </ul>

    <div class="youtube-box">
      <h3>📺 {{ stockName }} 관련 유튜브 영상</h3>
      <YouTubeSection :stock-name="stockName" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { isAuthenticated } from '../services/auth'
import YouTubeSection from '@/components/YouTubeSection.vue'

const route = useRoute()
const stockCode = route.params.code
const stockName = ref('')
const showForm = ref(false)

const dummyPosts = ref([
  { id: 1, title: '요즘 분위기 어떤가요?', author: 'user1', date: '2024-05-01' },
  { id: 2, title: '2분기 실적 예상', author: 'user2', date: '2024-05-15' },
])

const isLoggedIn = computed(() => isAuthenticated())

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:5000/stocks')
    const stockList = res.data
    const match = stockList.find(item => item.code === stockCode)
    stockName.value = match?.name || stockCode
  } catch (error) {
    console.error('종목명 불러오기 실패', error)
    stockName.value = stockCode
  }

  const allKeys = Object.keys(localStorage)
  const postKeys = allKeys.filter(k => k.startsWith(`post_${stockCode}_`))
  const loadedPosts = postKeys.map(k => {
    const raw = localStorage.getItem(k)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed.id) {
      const extractedId = k.split(`post_${stockCode}_`)[1]
      if (extractedId) parsed.id = extractedId
    }
    return parsed
  }).filter(p => p !== null && p.id)
  loadedPosts.sort((a, b) => Number(b.id) - Number(a.id))
  dummyPosts.value = [...loadedPosts, ...dummyPosts.value]
})
</script>

<style scoped>
.community {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Noto Sans KR', sans-serif;
}

.write-btn {
  margin: 16px 0;
  padding: 8px 14px;
  background-color: #0073e9;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* ✅ 글 목록 박스 UI */
.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
  padding: 0;
  list-style: none;
}

.post-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s ease;
}

.post-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.post-title {
  font-size: 18px;
  font-weight: bold;
  color: #0073e9;
  text-decoration: none;
}

.post-title:hover {
  text-decoration: underline;
}

.post-meta {
  font-size: 14px;
  color: #888;
  margin-top: 6px;
}

.youtube-box {
  margin-top: 50px;
  border-top: 1px solid #ddd;
  padding-top: 30px;
}
</style>
