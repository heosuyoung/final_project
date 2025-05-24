<template>
  <div class="community">
    <h2>{{ stockName }} 종목 토론방</h2>

    <div v-if="isLoggedIn">
      <router-link :to="`/community/${stockCode}/write`">
        <button class="write-btn">✍ 글쓰기</button>
      </router-link>
    </div>
    <p v-else>로그인 후 글쓰기가 가능합니다.</p>


    <!-- 글쓰기 폼 -->
    <div v-if="showForm" class="form-box">
      <input v-model="newTitle" placeholder="제목을 입력하세요" />
      <textarea v-model="newContent" placeholder="내용을 입력하세요"></textarea>
      <button @click="submitPost">등록</button>
      <button @click="cancelPost">취소</button>
    </div>

    <ul class="post-list">
      <li v-for="post in dummyPosts" :key="post.id" class="post-item">
        <router-link :to="`/community/${stockCode}/${post.id}`" class="post-title">
          {{ post.title }}
        </router-link>
        <div class="post-meta">
          {{ post.author }} · {{ post.date }}
        </div>
      </li>
    </ul>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { isAuthenticated } from '../services/auth'

const route = useRoute()
const stockCode = route.params.code
const stockName = ref('')
const showForm = ref(false)
// ✅ 종목 코드 → 이름 매핑
const stockMap = {
  '005930': '삼성전자',
  '000660': 'SK하이닉스',
  '207940': '삼성바이오로직스',
  '373220': 'LG에너지솔루션',
  '035720': '카카오',
  '035420': 'NAVER',
  '005380': '현대차',
  '006400': '삼성SDI'
}

// ✅ 게시글 목록 (기본 dummy 2개)
const dummyPosts = ref([
  { id: 1, title: '요즘 분위기 어떤가요?', author: 'user1', date: '2024-05-01' },
  { id: 2, title: '2분기 실적 예상', author: 'user2', date: '2024-05-15' },
])

// ✅ 로그인 여부 확인
const isLoggedIn = computed(() => isAuthenticated())

// ✅ 페이지 진입 시 해당 종목 글들 로컬에서 불러오기
onMounted(() => {
  stockName.value = stockMap[stockCode] || '알 수 없는 종목'

  const allKeys = Object.keys(localStorage)
  const postKeys = allKeys.filter(k => k.startsWith(`post_${stockCode}_`))

  const loadedPosts = postKeys.map(k => {
    const raw = localStorage.getItem(k)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    // ✅ id 추가 (없을 경우 key에서 뽑아내기)
    if (!parsed.id) {
      const extractedId = k.split(`post_${stockCode}_`)[1]
      if (extractedId) parsed.id = extractedId
    }
    return parsed
  }).filter(p => p !== null && p.id)


  // 최신 글이 위로 오게 정렬
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

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
}

.post-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #fff;
  transition: box-shadow 0.2s ease;
}

.post-item:hover {
  box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.post-title {
  font-size: 18px;
  font-weight: bold;
  color: #222;
  text-decoration: none;
}

.post-meta {
  font-size: 14px;
  color: #888;
  margin-top: 8px;
}

</style>
