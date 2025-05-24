<template>
  <div class="stocks-page">
    <h2>시가총액 상위 20 종목</h2>
    <table class="stock-table">
      <thead>
        <tr>
          <th>종목명</th>
          <th>현재가</th>
          <th>등락률</th>
          <th>시가총액</th>
          <th>거래량</th>
          <th>★</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in stocks" :key="stock.code">
          <td>
            <router-link :to="`/community/${stock.code}`" class="stock-link">
              {{ stock.name }}
            </router-link>
          </td>
          <td>{{ stock.price }}</td>
          <td :class="{ up: stock.changeRate.includes('+'), down: stock.changeRate.includes('-') }">
            {{ stock.changeRate }}
          </td>
          <td>{{ stock.marketCap }}</td>
          <td>{{ stock.volume }}</td>
          <td @click="toggleFavorite(stock)" class="star">
            {{ stock.isFavorite ? '⭐' : '☆' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import stocksData from '../assets/stocks_top50.json'

const stocks = ref([])

onMounted(() => {
  stocks.value = stocksData
})

const toggleFavorite = (stock) => {
  stock.isFavorite = !stock.isFavorite
}
</script>

<style scoped>
.stocks-page {
  padding: 20px;
   margin-top: 60px; /* ✅ 이거 추가! */
  font-family: 'Noto Sans KR', sans-serif;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.stock-table th {
  background-color: #f0f0f0;
  padding: 10px;
  font-weight: 600;
}

.stock-table td {
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.stock-link {
  color: #0073e9;
  text-decoration: none;
  font-weight: bold;
}

.up {
  color: red;
}

.down {
  color: blue;
}

.star {
  cursor: pointer;
  font-size: 20px;
}
</style>
