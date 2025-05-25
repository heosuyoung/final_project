<template>
  <section class="favorites-section">
    <h2 class="section-title">즐겨찾기 종목</h2>
    <div class="slider-wrapper">
      <button @click="prev" class="nav-btn prev-btn" :disabled="currentIndex <= 0">
        <span class="nav-icon">&#10094;</span>
      </button>
      
      <div class="slider-container">
        <transition-group 
          name="slide" 
          tag="div" 
          class="slider"
          :style="`transform: translateX(-${currentIndex * (cardWidth + 16)}px)`">
          <div
            v-for="stock in allFavorites"
            :key="stock.code"
            class="card"
          >
            <div class="card-header">
              <span class="stock-name">{{ stock.name }}</span>
              <span class="stock-code">{{ stock.code }}</span>
            </div>
            <div class="card-body">
              <div class="price-info">
                <p class="price">{{ stock.price }}원</p>
                <p class="change-rate" :class="getChangeRateClass(stock.changeRate)">
                  {{ stock.changeRate }}
                </p>
              </div>
              <div class="chart-placeholder">
                <!-- 여기에 미니 차트를 추가할 수 있음 -->
              </div>
              <router-link :to="`/community/${stock.code}`" class="card-link">
                자세히 보기
              </router-link>
            </div>
          </div>
        </transition-group>
      </div>
      
      <button @click="next" class="nav-btn next-btn" :disabled="currentIndex + visibleCardCount >= allFavorites.length">
        <span class="nav-icon">&#10095;</span>
      </button>
    </div>
    
    <div class="pagination">
      <span 
        v-for="(_, index) in Math.ceil(allFavorites.length / visibleCardCount)" 
        :key="index"
        class="pagination-dot"
        :class="{ active: Math.floor(currentIndex / visibleCardCount) === index }"
        @click="goToPage(index)">
      </span>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const allFavorites = ref([
  // 예시 데이터로 시작 (데이터가 없을 때를 대비)
  { 
    code: 'SAMPLE1', 
    name: '삼성전자', 
    price: '72,000', 
    changeRate: '+2.3%', 
    trend: 'up' 
  },
  { 
    code: 'SAMPLE2', 
    name: 'SK하이닉스', 
    price: '115,000', 
    changeRate: '-0.5%', 
    trend: 'down' 
  },
  { 
    code: 'SAMPLE3', 
    name: '카카오', 
    price: '47,500', 
    changeRate: '+1.2%', 
    trend: 'up' 
  },
  { 
    code: 'SAMPLE4', 
    name: '네이버', 
    price: '345,000', 
    changeRate: '+0.8%', 
    trend: 'up' 
  },
  { 
    code: 'SAMPLE5', 
    name: '현대차', 
    price: '182,500', 
    changeRate: '-1.3%', 
    trend: 'down' 
  },
])
const currentIndex = ref(0)
const cardWidth = ref(280) // 카드 너비 + 간격
const visibleCardCount = ref(3) // 한 번에 보이는 카드 수
let autoSlideInterval = null

// 저장된 데이터 불러오기
onMounted(() => {
  try {
    const stored = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')
    if (stored.length > 0) {
      // 각 항목이 필수 필드를 가지고 있는지 확인하고 정리
      allFavorites.value = stored.map(stock => {
        // 기본값으로 디폴트 값 설정
        const formattedStock = {
          code: stock.code || 'UNKNOWN',
          name: stock.name || '알 수 없음',
          price: stock.price || '0',
          changeRate: stock.changeRate || '0.00%',
          isUp: stock.isUp !== undefined ? stock.isUp : false
        }
        
        // changeRate가 문자열이 아니면 포맷팅
        if (typeof formattedStock.changeRate !== 'string') {
          formattedStock.changeRate = formattedStock.isUp ? '+0.00%' : '-0.00%'
        }
        
        // +/- 기호가 없는 경우 추가
        if (!formattedStock.changeRate.includes('+') && !formattedStock.changeRate.includes('-')) {
          formattedStock.changeRate = formattedStock.isUp ? `+${formattedStock.changeRate}` : `-${formattedStock.changeRate}`
        }
        
        // % 기호가 없는 경우 추가
        if (!formattedStock.changeRate.includes('%')) {
          formattedStock.changeRate = `${formattedStock.changeRate}%`
        }
        
        return formattedStock
      })
    }
  } catch (error) {
    console.error('즐겨찾기 주식 데이터 로드 실패:', error)
    // 에러 발생 시 예시 데이터 유지
  }
  
  // 화면 크기에 따라 visible 카드 수 조절
  updateVisibleCardCount()
  window.addEventListener('resize', updateVisibleCardCount)
  
  // 자동 슬라이드 시작
  startAutoSlide()
})

// 컴포넌트가 제거될 때 이벤트 리스너와 interval 제거
onBeforeUnmount(() => {
  window.removeEventListener('resize', updateVisibleCardCount)
  stopAutoSlide()
})

// 화면 크기에 따라 보이는 카드 개수 조절
const updateVisibleCardCount = () => {
  const width = window.innerWidth
  if (width < 768) {
    visibleCardCount.value = 1
  } else if (width < 1200) {
    visibleCardCount.value = 2
  } else {
    visibleCardCount.value = 3
  }
}

// 자동 슬라이드 시작
const startAutoSlide = () => {
  stopAutoSlide()
  autoSlideInterval = setInterval(() => {
    if (currentIndex.value + visibleCardCount.value >= allFavorites.value.length) {
      currentIndex.value = 0 // 마지막에 도달하면 처음으로 돌아감
    } else {
      currentIndex.value++
    }
  }, 5000) // 5초마다 슬라이드
}

// 자동 슬라이드 중지
const stopAutoSlide = () => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
    autoSlideInterval = null
  }
}

// 다음 슬라이드로 이동
const next = () => {
  stopAutoSlide() // 수동 조작시 자동 슬라이드 중지
  if (currentIndex.value + visibleCardCount.value < allFavorites.value.length) {
    currentIndex.value++
  }
  startAutoSlide() // 다시 자동 슬라이드 시작
}

// 이전 슬라이드로 이동
const prev = () => {
  stopAutoSlide() // 수동 조작시 자동 슬라이드 중지
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
  startAutoSlide() // 다시 자동 슬라이드 시작
}

// 페이지 번호로 이동
const goToPage = (pageIndex) => {
  stopAutoSlide()
  currentIndex.value = pageIndex * visibleCardCount.value
  startAutoSlide()
}

// 등락률에 따른 클래스 반환
const getChangeRateClass = (changeRate) => {
  // 문자열이 있고, +/-로 시작하는 경우
  if (typeof changeRate === 'string') {
    if (changeRate.startsWith('+')) return 'positive'
    if (changeRate.startsWith('-')) return 'negative'
  }
  // 객체에 isUp 속성이 있는 경우
  if (typeof changeRate === 'object' && changeRate !== null) {
    if (changeRate.isUp) return 'positive'
    return 'negative'
  }
  // 0% 또는 알 수 없는 값인 경우
  return ''
}
</script>

<style scoped>
.favorites-section {
  padding: 3rem 0;
  background-color: transparent;
  text-align: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.section-title {
  margin-bottom: 2rem;
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  border-radius: 3px;
}

.slider-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  position: relative;
  margin-bottom: 1.5rem;
}

.slider-container {
  width: 100%;
  max-width: 880px;
  overflow: hidden;
  padding: 1rem 0;
}

.slider {
  display: flex;
  gap: 16px;
  transition: transform 0.5s ease;
}

.card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
  width: 280px;
  min-width: 280px;
  transform-origin: center center;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 123, 255, 0.1);
}

.card-header {
  padding: 1.2rem;
  background: linear-gradient(90deg, #ffffff, #f8f9fa);
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stock-name {
  font-weight: 700;
  color: #333;
  font-size: 1.1rem;
}

.stock-code {
  font-size: 0.8rem;
  color: #777;
  background-color: #f5f5f5;
  padding: 2px 8px;
  border-radius: 12px;
}

.card-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.price-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  color: #333;
}

.change-rate {
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 20px;
  margin: 0;
  min-width: 60px;
  text-align: right;
  display: inline-block;
}

.positive {
  color: #FF5252;
  background-color: rgba(255, 82, 82, 0.1);
}

.negative {
  color: #4CAF50;
  background-color: rgba(76, 175, 80, 0.1);
}

.chart-placeholder {
  height: 80px;
  background: linear-gradient(to right, #f8f9fa 0%, #e9ecef 50%, #f8f9fa 100%);
  border-radius: 8px;
  margin: 0.5rem 0;
}

.card-link {
  display: inline-block;
  padding: 8px 16px;
  color: white;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  text-decoration: none;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  align-self: center;
}

.card-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 123, 255, 0.2);
}

.nav-btn {
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  z-index: 2;
}

.nav-btn:hover {
  background-color: #f8f9fa;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-icon {
  font-size: 1.2rem;
  color: #007bff;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 1rem;
}

.pagination-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #ddd;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-dot.active {
  background-color: #007bff;
  transform: scale(1.2);
}

/* 슬라이드 애니메이션 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

/* 반응형 */
@media (max-width: 1200px) {
  .slider-container {
    max-width: 580px;
  }
}

@media (max-width: 768px) {
  .slider-container {
    max-width: 280px;
  }
  
  .card {
    width: 280px;
  }
}
</style>
