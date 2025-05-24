<template>
  <div class="post-detail" v-if="post">
    <h2>{{ stockName }} - 글 상세</h2>
    <h3>{{ post.title }}</h3>
    <p><strong>작성자:</strong> {{ post.author }}</p>
    <p><strong>날짜:</strong> {{ post.date }}</p>
    <p class="content">{{ post.content }}</p>

    <div v-if="isLoggedIn" class="delete-box">
      <button @click="deletePost" class="delete-btn">🗑 삭제</button>
    </div>

    <div class="comments">
      <h4>💬 댓글</h4>

      <template v-if="comments.length > 0">
        <ul>
          <li v-for="(c, i) in comments" :key="i" class="comment-item">
            <div class="comment-content">
              • <router-link :to="`/user/${c.author}`" class="comment-author">
                <strong>{{ c.author }}</strong>
              </router-link> ({{ c.date }}): {{ c.content }}
            </div>
            <div class="comment-actions">
              <button @click="toggleLike(i)">👍 {{ c.likedBy.length }}</button>
              <button @click="toggleDislike(i)">👎 {{ c.dislikedBy.length }}</button>
              <button v-if="isLoggedIn" @click="deleteComment(i)" class="comment-delete">🗑</button>
            </div>
          </li>
        </ul>
      </template>
      <template v-else>
        <p>아직 댓글이 없습니다.</p>
      </template>

      <div v-if="isLoggedIn">
        <input v-model="newComment" placeholder="댓글 입력..." />
        <button @click="addComment">작성</button>
      </div>
      <p v-else>댓글 작성을 하려면 로그인하세요.</p>
    </div>
  </div>

  <div v-else>
    <p>글을 찾을 수 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { isAuthenticated } from '../services/auth'

const route = useRoute()
const router = useRouter()
const stockCode = route.params.code
const postId = route.params.postId
const commentKey = `comments_${stockCode}_${postId}`

const isLoggedIn = computed(() => isAuthenticated())
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
const post = ref(null)
const comments = ref([])
const newComment = ref('')

onMounted(() => {
  const stored = localStorage.getItem(`post_${stockCode}_${postId}`)
  if (stored) {
    post.value = JSON.parse(stored)
  }
  const storedComments = localStorage.getItem(commentKey)
  if (storedComments) {
    const parsed = JSON.parse(storedComments)
    comments.value = parsed.filter(c => typeof c === 'object' && c.author && c.content)
  }
})

const addComment = () => {
  const username = localStorage.getItem('username')
  if (!username) return alert('로그인이 필요합니다.')
  if (newComment.value.trim()) {
    const date = new Date().toLocaleString('ko-KR', {
      year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'
    })
    comments.value.push({
      content: newComment.value,
      author: username,
      date,
      likedBy: [],
      dislikedBy: []
    })
    newComment.value = ''
    localStorage.setItem(commentKey, JSON.stringify(comments.value))
  }
}

const toggleLike = (index) => {
  const username = localStorage.getItem('username')
  const c = comments.value[index]
  if (!username || !c) return

  const liked = c.likedBy.includes(username)
  if (liked) {
    c.likedBy = c.likedBy.filter(u => u !== username)
  } else {
    c.likedBy.push(username)
    c.dislikedBy = c.dislikedBy.filter(u => u !== username)
  }
  localStorage.setItem(commentKey, JSON.stringify(comments.value))
}

const toggleDislike = (index) => {
  const username = localStorage.getItem('username')
  const c = comments.value[index]
  if (!username || !c) return

  const disliked = c.dislikedBy.includes(username)
  if (disliked) {
    c.dislikedBy = c.dislikedBy.filter(u => u !== username)
  } else {
    c.dislikedBy.push(username)
    c.likedBy = c.likedBy.filter(u => u !== username)
  }
  localStorage.setItem(commentKey, JSON.stringify(comments.value))
}

const deleteComment = (index) => {
  comments.value.splice(index, 1)
  localStorage.setItem(commentKey, JSON.stringify(comments.value))
}

const deletePost = () => {
  const confirmDelete = confirm('정말로 이 게시글을 삭제하시겠습니까?')
  if (!confirmDelete) return
  localStorage.removeItem(`post_${stockCode}_${postId}`)
  localStorage.removeItem(commentKey)
  alert('게시글이 삭제되었습니다.')
  router.push(`/community/${stockCode}`)
}
</script>

<style scoped>
.post-detail {
  padding: 20px 40px;
  max-width: 700px;
  margin: 60px auto 0 auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  text-align: left;
}
.comment-author {
  color: #0073e9;
  text-decoration: none;
  font-weight: bold;
}
.comment-author:hover {
  text-decoration: underline;
}
h2 {
  font-size: 20px;
  font-weight: bold;
  color: #222;
  margin-bottom: 10px;
}
h3 {
  font-size: 18px;
  color: #444;
  margin-top: 20px;
  margin-bottom: 5px;
}
.content {
  font-size: 16px;
  line-height: 1.6;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}
.comments h4 {
  margin-top: 30px;
  font-size: 17px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}
.comment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 6px;
}
.comment-content {
  flex-grow: 1;
}
.comment-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}
.comment-actions button {
  font-size: 14px;
  background: none;
  border: none;
  cursor: pointer;
}
.comments input {
  margin-top: 10px;
  padding: 6px;
  width: 80%;
  font-size: 15px;
}
.comments button {
  margin-left: 10px;
  padding: 6px 10px;
}
.delete-box {
  margin: 20px 0;
}
.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
.comment-delete {
  color: #f44336;
}
</style>
