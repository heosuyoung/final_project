<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  stockName: {
    type: String,
    required: true
  }
})

const videos = ref([])

const fetchVideos = async (name) => {
  if (!name || name.length < 2) return  // 길이 제한만 적용

  const query = `${name} 주식`
  const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY
  const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=video&maxResults=3&key=${apiKey}`

  try {
    const res = await axios.get(url)
    videos.value = res.data.items
  } catch (e) {
    console.error('유튜브 API 호출 오류', e)
  }
}

watch(() => props.stockName, (newName) => {
  fetchVideos(newName)
}, { immediate: true })
</script>

<template>
  <div>
    <div v-if="videos.length === 0">관련 영상 불러오는 중...</div>
    <div v-for="video in videos" :key="video.id.videoId" style="margin-bottom: 20px;">
      <iframe
        width="100%"
        height="200"
        :src="`https://www.youtube.com/embed/${video.id.videoId}`"
        frameborder="0"
        allowfullscreen
      ></iframe>
      <p>{{ video.snippet.title }}</p>
    </div>
  </div>
</template>
