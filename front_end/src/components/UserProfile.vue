<template>
  <div class="user-profile">
    <h2>{{ username }}님의 프로필</h2>

    <button v-if="!isMe" @click="toggleFollow" class="follow-btn">
      {{ isFollowing ? '언팔로우' : '팔로우' }}
    </button>    <div class="info-box">
      <div class="follow-info clickable" @click="showFollowersList = !showFollowersList">
        <strong>팔로워:</strong> {{ followers.length }}명
      </div>
      <div v-if="showFollowersList" class="follow-list">
        <h4>팔로워 목록</h4>
        <ul>
          <li v-for="follower in followers" :key="follower">
            <router-link :to="`/user/${follower}`">{{ follower }}</router-link>
          </li>
          <li v-if="followers.length === 0">아직 팔로워가 없습니다.</li>
        </ul>
      </div>
      
      <div class="follow-info clickable" @click="showFollowingsList = !showFollowingsList">
        <strong>팔로잉:</strong> {{ theirFollowings.length }}명
      </div>
      <div v-if="showFollowingsList" class="follow-list">
        <h4>팔로잉 목록</h4>
        <ul>
          <li v-for="following in theirFollowings" :key="following">
            <router-link :to="`/user/${following}`">{{ following }}</router-link>
          </li>
          <li v-if="theirFollowings.length === 0">아직 팔로우한 사용자가 없습니다.</li>
        </ul>
      </div>
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
const showFollowersList = ref(false)
const showFollowingsList = ref(false)

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
.follow-info {
  margin: 8px 0;
  font-size: 15px;
  cursor: pointer;
  color: #007bff;
}
.follow-info:hover {
  text-decoration: underline;
}
.follow-list {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 10px 15px;
  margin: 8px 0 16px 0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.follow-list h4 {
  margin-top: 0;
  color: #343a40;
  font-size: 16px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.follow-list ul {
  padding-left: 20px;
  margin: 8px 0;
  list-style-type: none;
  padding: 0;
}
.follow-list li {
  margin-bottom: 6px;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}
.follow-list li:last-child {
  border-bottom: none;
}
.follow-list a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}
.follow-list a:hover {
  text-decoration: underline;
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
