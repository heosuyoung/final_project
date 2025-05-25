<template>
  <div class="stocks-page">
    <!-- 페이지 헤더 섹션 -->
    <div class="stocks-header">
      <div class="header-content">
        <h1 class="page-title">주식 정보</h1>
        <p class="page-subtitle">국내 시가총액 상위 30 종목의 실시간 정보를 확인하세요</p>
      </div>
    </div>
    
    <!-- 필터 및 검색 섹션 -->
    <div class="filter-section">
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="종목명 검색..." 
          @input="filterStocks"
        >
        <span class="search-icon">🔍</span>
      </div>
      
      <div class="filter-options">
        <span class="filter-label">정렬:</span>
        <button 
          class="filter-btn" 
          :class="{ active: sortBy === 'marketCap' }" 
          @click="sortStocks('marketCap')"
        >
          시가총액
        </button>
        <button 
          class="filter-btn" 
          :class="{ active: sortBy === 'changeRate' }" 
          @click="sortStocks('changeRate')"
        >
          등락률
        </button>
        <button 
          class="filter-btn" 
          :class="{ active: sortBy === 'volume' }" 
          @click="sortStocks('volume')"
        >
          거래량
        </button>
        <button 
          class="filter-btn" 
          :class="{ active: filterFavorites }" 
          @click="toggleFavoritesOnly"
        >
          즐겨찾기만 보기
        </button>
      </div>
    </div>
    
    <!-- 마켓 인사이트 섹션 -->
    <div class="market-insight">
      <div class="insight-card">
        <div class="insight-icon up">📈</div>
        <div class="insight-content">
          <h3>상승률 1위</h3>
          <p v-if="topGainer">{{ topGainer.name }} ({{ topGainer.changeRate }})</p>
          <p v-else>로딩 중...</p>
        </div>
      </div>
      
      <div class="insight-card">
        <div class="insight-icon down">📉</div>
        <div class="insight-content">
          <h3>하락률 1위</h3>
          <p v-if="topLoser">{{ topLoser.name }} ({{ topLoser.changeRate }})</p>
          <p v-else>로딩 중...</p>
        </div>
      </div>
      
      <div class="insight-card">
        <div class="insight-icon">📊</div>
        <div class="insight-content">
          <h3>거래량 1위</h3>
          <p v-if="topVolume">{{ topVolume.name }} ({{ topVolume.volume }})</p>
          <p v-else>로딩 중...</p>
        </div>
      </div>
      
      <div class="insight-card">
        <div class="insight-icon">⭐</div>
        <div class="insight-content">
          <h3>즐겨찾기 수</h3>
          <p>{{ favoriteCount }} 종목</p>
        </div>
      </div>
    </div>
    
    <!-- 주식 테이블 섹션 -->
    <div class="stock-table-container">
      <h2 class="section-title">
        <span v-if="filterFavorites">즐겨찾기 종목</span>
        <span v-else>시가총액 상위 종목</span>
        <span class="stock-count">{{ filteredStocks.length }}종목</span>
      </h2>
      
      <div class="table-responsive">
        <table class="stock-table">
          <thead>
            <tr>
              <th>종목명</th>
              <th>현재가</th>
              <th>등락률</th>
              <th>시가총액</th>
              <th>거래량</th>
              <th>즐겨찾기</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stock in filteredStocks" :key="stock.code" class="stock-row">
              <td>
                <router-link :to="`/community/${stock.code}`" class="stock-link">
                  {{ stock.name }}
                </router-link>
              </td>
              <td class="price">{{ formatPrice(stock.price) }}</td>
              <td :class="{ 'up-value': stock.changeRate.includes('+'), 'down-value': stock.changeRate.includes('-') }">
                {{ stock.changeRate }}
              </td>
              <td>{{ stock.marketCap }}</td>
              <td>{{ stock.volume }}</td>
              <td @click="toggleFavorite(stock)" class="star-cell">
                <div class="star" :class="{ 'is-favorite': stock.isFavorite }">
                  {{ stock.isFavorite ? '★' : '☆' }}
                </div>
              </td>
            </tr>
            <tr v-if="filteredStocks.length === 0">
              <td colspan="6" class="no-data">
                <p>검색 결과가 없습니다</p>
                <button class="reset-btn" @click="resetFilters">필터 초기화</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 커뮤니티 섹션 -->
    <div class="community-section">
      <h2 class="section-title">종목 커뮤니티</h2>
      <p class="section-desc">관심 종목의 커뮤니티에 참여하여 다양한 투자 정보를 얻고 의견을 나눠보세요.</p>
      <div class="community-cards">
        <div 
          v-for="stock in favoriteStocks.slice(0, 3)" 
          :key="stock.code" 
          class="community-card"
          @click="navigateToCommunity(stock.code)"
        >
          <h3>{{ stock.name }} 커뮤니티</h3>
          <p>실시간 정보 공유 및 토론</p>
          <div class="card-price" :class="{ 'up-value': stock.changeRate.includes('+'), 'down-value': stock.changeRate.includes('-') }">
            {{ formatPrice(stock.price) }} ({{ stock.changeRate }})
          </div>
          <button class="join-btn">참여하기</button>
        </div>
        <div v-if="favoriteStocks.length === 0" class="community-card empty">
          <h3>즐겨찾기 추가</h3>
          <p>종목을 즐겨찾기에 추가하면 이곳에서 바로 커뮤니티에 참여할 수 있습니다.</p>
          <div class="empty-star">★</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const stocks = ref([])
const originalStocks = ref([])
const searchTerm = ref('')
const sortBy = ref('marketCap')
const filterFavorites = ref(false)
const sortDirection = ref('desc')
const loadingData = ref(true)

// 필터링 및 정렬된 주식 목록
const filteredStocks = computed(() => {
  let result = [...stocks.value]
  
  // 검색어 필터링
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(stock => 
      stock.name.toLowerCase().includes(term) || 
      stock.code.toLowerCase().includes(term)
    )
  }
  
  // 즐겨찾기 필터링
  if (filterFavorites.value) {
    result = result.filter(stock => stock.isFavorite)
  }
  
  // 정렬
  result.sort((a, b) => {
    if (sortBy.value === 'changeRate') {
      // 등락률 정렬 로직
      const aValue = parseFloat(a.changeRate.replace('%', '').replace('+', ''))
      const bValue = parseFloat(b.changeRate.replace('%', '').replace('+', ''))
      return sortDirection.value === 'desc' ? bValue - aValue : aValue - bValue
    } else if (sortBy.value === 'volume') {
      // 거래량 정렬 로직 (쉼표 제거하고 숫자로 변환)
      const aValue = parseInt(a.volume.replace(/,/g, ''))
      const bValue = parseInt(b.volume.replace(/,/g, ''))
      return sortDirection.value === 'desc' ? bValue - aValue : aValue - bValue
    } else {
      // 시가총액 정렬 로직 (기본값)
      const aValue = parseInt(a.marketCap.replace(/,/g, ''))
      const bValue = parseInt(b.marketCap.replace(/,/g, ''))
      return sortDirection.value === 'desc' ? bValue - aValue : aValue - bValue
    }
  })
  
  return result
})

// 인사이트 계산 - 상승률 1위
const topGainer = computed(() => {
  if (originalStocks.value.length === 0) return null
  return [...originalStocks.value].sort((a, b) => {
    const aValue = parseFloat(a.changeRate.replace('%', '').replace('+', ''))
    const bValue = parseFloat(b.changeRate.replace('%', '').replace('+', ''))
    return bValue - aValue
  })[0]
})

// 인사이트 계산 - 하락률 1위
const topLoser = computed(() => {
  if (originalStocks.value.length === 0) return null
  return [...originalStocks.value].sort((a, b) => {
    const aValue = parseFloat(a.changeRate.replace('%', '').replace('+', ''))
    const bValue = parseFloat(b.changeRate.replace('%', '').replace('+', ''))
    return aValue - bValue
  })[0]
})

// 인사이트 계산 - 거래량 1위
const topVolume = computed(() => {
  if (originalStocks.value.length === 0) return null
  return [...originalStocks.value].sort((a, b) => {
    const aValue = parseInt(a.volume.replace(/,/g, ''))
    const bValue = parseInt(b.volume.replace(/,/g, ''))
    return bValue - aValue
  })[0]
})

// 즐겨찾기 종목 수
const favoriteCount = computed(() => {
  return stocks.value.filter(stock => stock.isFavorite).length
})

// 즐겨찾기 종목 리스트
const favoriteStocks = computed(() => {
  return stocks.value.filter(stock => stock.isFavorite)
})

// 초기 데이터 로드
onMounted(async () => {
  loadingData.value = true
  try {
    // 모의 API 대신 임시로 JSON 파일에서 데이터 불러오기
    let res
    try {
      res = await axios.get('/api/stocks')
    } catch (e) {
      // API 요청 실패 시 정적 JSON 파일 사용
      res = await axios.get('/stocks_top30.json')
    }
    
    const data = res.data
    
    if (!Array.isArray(data)) {
      console.error('응답 데이터가 배열이 아닙니다:', data)
      return
    }
    
    const savedFavorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')
    
    // 데이터 변환 및 즐겨찾기 상태 적용
    const processedData = data.map(stock => ({
      ...stock,
      isFavorite: savedFavorites.some(f => f.code === stock.code)
    }))
    
    originalStocks.value = [...processedData]
    stocks.value = processedData
  } catch (e) {
    console.error('주식 데이터 로드 실패:', e)
  } finally {
    loadingData.value = false
  }
})

// 즐겨찾기 토글
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

// 정렬 방식 변경
const sortStocks = (field) => {
  if (sortBy.value === field) {
    // 같은 필드로 정렬 시 방향 전환
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    // 다른 필드로 정렬 시 내림차순 기본값
    sortBy.value = field
    sortDirection.value = 'desc'
  }
}

// 즐겨찾기만 보기 토글
const toggleFavoritesOnly = () => {
  filterFavorites.value = !filterFavorites.value
}

// 필터 초기화
const resetFilters = () => {
  searchTerm.value = ''
  filterFavorites.value = false
  sortBy.value = 'marketCap'
  sortDirection.value = 'desc'
}

// 종목 검색
const filterStocks = () => {
  // 실시간 검색 처리는 computed 속성에서 처리
}

// 가격 형식화
const formatPrice = (price) => {
  if (!price) return '0'
  
  // 쉼표가 있는 경우 제거 후 숫자로 변환
  const numPrice = typeof price === 'string' 
    ? parseFloat(price.replace(/,/g, '')) 
    : price
    
  // 숫자 형식화
  return numPrice.toLocaleString('ko-KR')
}

// 커뮤니티 페이지 이동
const navigateToCommunity = (code) => {
  router.push(`/community/${code}`)
}
</script>


<style scoped>
.stocks-page {
  padding-bottom: 4rem;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
  background-color: #f8f9ff;
}

/* 헤더 스타일 */
.stocks-header {
  background: linear-gradient(135deg, #007bff 0%, #00bcd4 100%);
  padding: 5rem 0 3rem;
  color: white;
  text-align: center;
  margin-bottom: 3rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-title {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

/* 필터 섹션 */
.filter-section {
  max-width: 1200px;
  margin: -2rem auto 2rem;
  padding: 1.5rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  z-index: 10;
  position: relative;
}

.search-bar {
  flex: 1;
  position: relative;
  max-width: 400px;
}

.search-bar input {
  padding: 0.8rem 1rem 0.8rem 2.8rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background-color: #f7f7f7;
  width: 100%;
  font-size: 1rem;
  transition: all 0.3s;
}

.search-bar input:focus {
  outline: none;
  border-color: #007bff;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.search-icon {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
  font-size: 1.2rem;
}

.filter-options {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.filter-label {
  color: #888;
  margin-right: 0.4rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
  background: transparent;
  color: #555;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #f0f0f0;
}

.filter-btn.active {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border-color: transparent;
}

/* 인사이트 섹션 */
.market-insight {
  max-width: 1200px;
  margin: 0 auto 3rem;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.insight-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.insight-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.insight-icon {
  width: 50px;
  height: 50px;
  background-color: #e8f4ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.insight-icon.up {
  background-color: #ebfff0;
  color: #28a745;
}

.insight-icon.down {
  background-color: #fff0f0;
  color: #dc3545;
}

.insight-content h3 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
  color: #333;
}

.insight-content p {
  font-size: 1.05rem;
  color: #555;
  font-weight: 600;
  margin: 0;
}

/* 테이블 섹션 */
.stock-table-container {
  max-width: 1200px;
  margin: 0 auto 3rem;
  padding: 0 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stock-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: #666;
  background: #f0f0f0;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
}

.table-responsive {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.stock-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  text-align: center;
}

.stock-table th {
  background-color: #f8f9ff;
  padding: 1.2rem 1rem;
  font-weight: 600;
  color: #444;
  border-bottom: 1px solid #e8e8e8;
  position: sticky;
  top: 0;
  z-index: 2;
}

.stock-table td {
  padding: 1.2rem 1rem;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
}

.stock-row {
  transition: background-color 0.2s;
}

.stock-row:hover {
  background-color: #f8faff;
}

.stock-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
  position: relative;
  display: inline-block;
  padding-bottom: 2px;
}

.stock-link:hover {
  color: #0056b3;
}

.stock-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #0056b3;
  transition: width 0.3s;
}

.stock-link:hover::after {
  width: 100%;
}

.price {
  font-weight: 600;
  font-family: 'Roboto', sans-serif;
}

.up-value {
  color: #d63031;
  font-weight: 600;
}

.down-value {
  color: #0984e3;
  font-weight: 600;
}

.star-cell {
  cursor: pointer;
  width: 60px;
}

.star {
  display: inline-block;
  font-size: 1.5rem;
  color: #ccc;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.star.is-favorite {
  color: #f1c40f;
  transform: scale(1.2);
}

.no-data {
  text-align: center;
  padding: 3rem 1rem !important;
  color: #888;
}

.reset-btn {
  background-color: #f0f0f0;
  color: #555;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.reset-btn:hover {
  background-color: #e0e0e0;
}

/* 커뮤니티 섹션 */
.community-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-desc {
  color: #666;
  margin-bottom: 2rem;
  text-align: center;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.community-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.community-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.community-card:hover {
  transform: translateY(-7px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.community-card h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #333;
}

.community-card p {
  color: #666;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.card-price {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.join-btn {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 25px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.join-btn:hover {
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
}

.community-card.empty {
  background: #f8f9ff;
  border: 2px dashed #ccc;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-star {
  font-size: 3rem;
  color: #ccc;
  margin-top: 1rem;
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-bar {
    max-width: 100%;
  }
  
  .filter-options {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2.2rem;
  }
  
  .stocks-header {
    padding: 4rem 0 2rem;
  }
  
  .market-insight {
    grid-template-columns: 1fr;
  }
  
  .insight-card {
    justify-content: center;
  }
  
  .section-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .stock-count {
    align-self: flex-start;
  }
}
</style>
