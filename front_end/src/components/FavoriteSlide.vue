<template>
  <section class="favorites-section">
    <h2>즐겨찾기 종목</h2>
    <div class="slider-wrapper">
      <button @click="prev" class="nav-btn">‹</button>
      <div class="slider">
        <div
          v-for="(stock, index) in visibleStocks"
          :key="stock.code"
          class="card"
        >
          <div class="card-header">{{ stock.name }}</div>
          <div class="card-body">
            <p>현재가: {{ stock.price }}원</p>
            <p>등락률: {{ stock.changeRate }}</p>
            <router-link :to="`/community/${stock.code}`" class="card-link">
              자세히 보기
            </router-link>
          </div>
        </div>
      </div>
      <button @click="next" class="nav-btn">›</button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const allFavorites = ref([])
const currentIndex = ref(0)

onMounted(() => {
  const stored = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')
  allFavorites.value = stored
})

const visibleStocks = computed(() =>
  allFavorites.value.slice(currentIndex.value, currentIndex.value + 3)
)

const next = () => {
  if (currentIndex.value + 3 < allFavorites.value.length) {
    currentIndex.value++
  }
}

const prev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}
</script>

<style scoped>
.favorites-section {
  padding: 3rem 0;
  background-color: #f8f9fa;
  text-align: center;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
}

h2 {
  margin-bottom: 1rem;
}

.slider-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.slider {
  display: flex;
  gap: 1rem;
  overflow: hidden;
  max-width: 1000px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 250px;
}

.card-header {
  background-color: #007bff;
  color: white;
  padding: 0.8rem;
  font-weight: 700;
  font-size: 1.1rem;
}

.card-link {
  display: inline-block;
  margin-top: 0.5rem;
  color: #007bff;
  text-decoration: none;
}
.nav-btn {
  font-size: 2rem;
  background: none;
  border: none;
  cursor: pointer;
}
</style>
