<template>
  <div class="post-detail" v-if="post && post.title">
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

      <div v-if="isLoggedIn" class="comment-input-container">
        <input v-model="newComment" placeholder="댓글 입력..." />
        <button @click="addComment" class="comment-submit-btn">작성</button>
      </div>
      <p v-else>댓글 작성을 하려면 로그인하세요.</p>
    </div>
  </div>

  <div v-else>
    <p>글을 찾을 수 없습니다. (2초 후 목록으로 이동합니다)</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { isAuthenticated } from '../services/auth'

const route = useRoute()
const router = useRouter()
const stockCode = computed(() => route.params.code)
const postId = computed(() => route.params.postId)
const commentKey = computed(() => `comments_${stockCode.value}_${postId.value}`)


const stockName = ref('') // ✅ 종목명 받아올 변수
const post = ref(null)
const comments = ref([])
const newComment = ref('')
const isLoggedIn = computed(() => isAuthenticated())

onMounted(async () => {
  // ✅ 종목명 자동으로 불러오기
  try {
    const res = await axios.get('http://localhost:5000/stocks')
    const match = res.data.find(item => item.code === stockCode)
    stockName.value = match?.name || stockCode
  } catch (err) {
    console.error('종목명 불러오기 실패', err)
    stockName.value = stockCode
  }

  // ✅ 게시글 데이터 로딩
  const stored = localStorage.getItem(`post_${stockCode.value}_${postId.value}`)
  console.log('[PostDetail] 상세 key:', `post_${stockCode.value}_${postId.value}`)
  console.log('[PostDetail] 상세 데이터:', stored)
  if (stored) {
    post.value = JSON.parse(stored)
  }
  const storedComments = localStorage.getItem(commentKey.value)
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
  localStorage.removeItem(`post_${stockCode}_${postId.value}`)
  localStorage.removeItem(commentKey.value)
  alert('게시글이 삭제되었습니다.')
  router.push(`/community/${stockCode}`)
}
import { watch } from 'vue'

// 종목명 + 게시글 데이터 다시 불러오는 함수 정의
const reloadPostData = async () => {
  try {
    const res = await axios.get('http://localhost:5000/stocks')
    const match = res.data.find(item => item.code === route.params.code)
    stockName.value = match?.name || route.params.code
  } catch (err) {
    console.error('종목명 다시 불러오기 실패', err)
    stockName.value = route.params.code
  }

  const stored = localStorage.getItem(`post_${route.params.code}_${route.params.postId}`)
  if (stored) {
    post.value = JSON.parse(stored)
  }
  const storedComments = localStorage.getItem(`comments_${route.params.code}_${route.params.postId}`)
  if (storedComments) {
    const parsed = JSON.parse(storedComments)
    comments.value = parsed.filter(c => typeof c === 'object' && c.author && c.content)
  }
}

// ✅ watch 추가 - 코드(postId)가 변경되면 reloadPostData 재호출
watch(() => [route.params.code, route.params.postId], reloadPostData)

// 게시글이 없으면 2초 후 자동으로 커뮤니티 목록으로 이동
watch(post, (val) => {
  if (val === null) {
    setTimeout(() => {
      router.push(`/community/${route.params.code}`)
    }, 2000)
  }
})
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
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}
.comment-actions button:hover {
  background-color: #f0f0f0;
}
.comment-input-container {
  display: flex;
  margin-top: 15px;
  gap: 10px;
  align-items: center;
}
.comments input {
  padding: 8px 10px;
  flex-grow: 1;
  font-size: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.comment-submit-btn {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  min-width: 80px;
}
.comment-submit-btn:hover {
  background-color: #0056b3;
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
