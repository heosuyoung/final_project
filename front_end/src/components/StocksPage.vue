<template>
  <div class="stocks-page">
    <h2>시가총액 상위 30 종목</h2>
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
import axios from 'axios'

const stocks = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('/api/stocks')  // 프록시 설정 기준
    const data = res.data

    if (!Array.isArray(data)) {
      console.error('응답 데이터가 배열이 아닙니다:', data)
      return
    }

    const savedFavorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')

    stocks.value = data.map(stock => ({
      ...stock,
      isFavorite: savedFavorites.some(f => f.code === stock.code)
    }))
  } catch (e) {
    console.error('주식 데이터 로드 실패:', e)
  }
})

const toggleFavorite = (stock) => {
  stock.isFavorite = !stock.isFavorite
  let favs = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')

  if (stock.isFavorite) {
    favs.push(stock)
  } else {
    favs = favs.filter(s => s.code !== stock.code)
  }

  localStorage.setItem('favorite_stocks', JSON.stringify(favs))
}
</script>


<style scoped>
.stocks-page {
  padding: 20px;
  margin-top: 60px;
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
