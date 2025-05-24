<template>
  <div class="write-post">
    <h2>{{ stockName }} - 글 작성</h2>

    <div class="form-box">
      <input v-model="title" placeholder="제목을 입력하세요" />
      <textarea v-model="content" placeholder="내용을 입력하세요"></textarea>
      <button @click="submitPost">등록</button>
      <button @click="cancel">취소</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const stockCode = route.params.code

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
const stockName = ref(stockMap[stockCode] || '알 수 없는 종목')

// 글쓰기 상태
const title = ref('')
const content = ref('')

// 등록 버튼
const submitPost = () => {
  const username = localStorage.getItem('username')
  if (!username) {
    alert('로그인이 필요합니다.')
    return
  }

  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력하세요.')
    return
  }

  const postId = Date.now().toString()

  localStorage.setItem(`post_${stockCode}_${postId}`, JSON.stringify({
    id: postId,
    stockCode: stockCode,
    title: title.value,
    content: content.value,
    author: username,
    date: new Date().toISOString().split('T')[0]
  }))

  router.push(`/community/${stockCode}/${postId}`)
}

const cancel = () => {
  router.push(`/community/${stockCode}`)
}
</script>

<style scoped>
.write-post {
  padding: 20px;
  margin-top: 60px;
}

.form-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

input {
  padding: 10px;
  font-size: 16px;
  height: 45px;
}

textarea {
  padding: 12px;
  font-size: 15px;
  min-height: 200px;
  resize: vertical;
}

button {
  width: 100px;
  padding: 8px;
  font-size: 14px;
}
</style>
