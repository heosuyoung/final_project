<template>
  <div class="user-profile">
    <h2>{{ username }}님의 프로필</h2>

    <button v-if="!isMe" @click="toggleFollow" class="follow-btn">
      {{ isFollowing ? '언팔로우' : '팔로우' }}
    </button>

    <div class="info-box">
      <p><strong>팔로워:</strong> {{ followers.length }}명</p>
      <p><strong>팔로잉:</strong> {{ theirFollowings.length }}명</p>
    </div>

    <div class="posts">
      <h3>작성한 글</h3>
      <ul>
        <li v-for="post in userPosts" :key="post.id">
          <router-link :to="`/community/${post.stockCode}/${post.id}`">
            {{ post.title }} ({{ post.date }})
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const username = route.params.username
const currentUser = localStorage.getItem('username')
const isMe = computed(() => username === currentUser)

const followers = ref([]) // 보고 있는 유저의 팔로워
const theirFollowings = ref([]) // 보고 있는 유저가 팔로우한 사람들
const isFollowing = ref(false)
const userPosts = ref([])

const followKey = `follow_${username}` // username의 팔로워 리스트
const myFollowKey = `followings_${currentUser}` // 현재 로그인 유저가 팔로우한 리스트
const theirFollowKey = `followings_${username}` // username이 팔로우한 사람들

onMounted(() => {
  // 팔로워 목록
  const storedFollowers = JSON.parse(localStorage.getItem(followKey) || '[]')
  followers.value = storedFollowers
  isFollowing.value = storedFollowers.includes(currentUser)

  // username 사용자가 팔로우한 사람들
  const storedTheirFollowings = JSON.parse(localStorage.getItem(theirFollowKey) || '[]')
  theirFollowings.value = storedTheirFollowings

  // 게시글 목록
  const allKeys = Object.keys(localStorage)
  const posts = allKeys
    .filter(k => k.startsWith('post_'))
    .map(k => JSON.parse(localStorage.getItem(k)))
    .filter(p => p && p.author === username)
  userPosts.value = posts
})

const toggleFollow = () => {
  if (!currentUser) {
    alert('로그인이 필요합니다.')
    return
  }

  let storedFollowers = JSON.parse(localStorage.getItem(followKey) || '[]')
  let storedMyFollowings = JSON.parse(localStorage.getItem(myFollowKey) || '[]')

  if (isFollowing.value) {
    // 언팔로우
    storedFollowers = storedFollowers.filter(u => u !== currentUser)
    storedMyFollowings = storedMyFollowings.filter(u => u !== username)
    isFollowing.value = false
  } else {
    // 팔로우
    storedFollowers.push(currentUser)
    storedMyFollowings.push(username)
    isFollowing.value = true
  }

  localStorage.setItem(followKey, JSON.stringify(storedFollowers))
  localStorage.setItem(myFollowKey, JSON.stringify(storedMyFollowings))

  followers.value = storedFollowers
}
</script>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  font-family: 'Noto Sans KR', sans-serif;
}
.follow-btn {
  background: #007bff;
  color: white;
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 16px;
}
.info-box p {
  margin: 4px 0;
  font-size: 15px;
}
.posts h3 {
  margin-top: 20px;
}
.posts ul {
  padding-left: 20px;
}
.posts li {
  margin-bottom: 6px;
}
</style>
