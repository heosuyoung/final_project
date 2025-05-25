<template>
  <section class="favorite-section">
    <h2 class="section-title">관심종목</h2>
    <div class="slider-container">
      <button @click="prevSlide" class="slide-btn">&lt;</button>
      <div class="cards-wrapper">
        <div class="stock-card" v-for="(stock, index) in visibleStocks" :key="stock.code">
          <h3>{{ stock.name }}</h3>
          <p>현재가: {{ stock.price }}원</p>
          <p>전일대비: {{ stock.changeRate }}</p>
          <router-link :to="`/community/${stock.code}`">자세히 보기</router-link>
        </div>
      </div>
      <button @click="nextSlide" class="slide-btn">&gt;</button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const allStocks = ref(JSON.parse(localStorage.getItem('favoriteStocks') || '[]'))
const currentIndex = ref(0)

const visibleStocks = computed(() => {
  return allStocks.value.slice(currentIndex.value, currentIndex.value + 3)
})

const nextSlide = () => {
  if (currentIndex.value + 3 < allStocks.value.length) {
    currentIndex.value += 1
  }
}

const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1
  }
}
</script>

<style scoped>
.favorite-section {
  background: #f9f9f9;
  padding: 2rem;
  margin-top: 3rem;
  text-align: center;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.slider-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.cards-wrapper {
  display: flex;
  gap: 1rem;
  overflow: hidden;
}

.stock-card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  width: 200px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.slide-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
}
</style>
