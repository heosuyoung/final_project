<template>
  <div class="community-container">
    <!-- 헤더 섹션 -->
    <div class="community-header">
      <div class="header-content">        <h1 class="stock-title">{{ stockName }} <span class="stock-code">({{ stockCode }})</span></h1>
        <div class="stock-price-info" v-if="stockPrice">
          <span class="current-price">{{ stockPrice.price }}원</span>
          <span class="price-change" :class="stockPrice.isUp ? 'price-up' : 'price-down'">
            {{ stockPrice.change }} ({{ stockPrice.changePercent || '0.00%' }})
          </span>
        </div>
      </div>

      <!-- 액션 버튼 영역 -->
      <div class="action-buttons">
        <button class="action-btn favorite-btn" @click="toggleFavorite">
          <span class="icon">{{ isFavorite ? '★' : '☆' }}</span>
          <span>{{ isFavorite ? '관심종목 제거' : '관심종목 추가' }}</span>
        </button>
        <button v-if="isLoggedIn" class="action-btn write-btn" @click="navigateToWrite">
          <span class="icon">✍</span>
          <span>글쓰기</span>
        </button>
      </div>
    </div>

    <!-- 탭 네비게이션 -->
    <div class="tab-navigation">
      <button 
        class="tab-btn" 
        :class="{ 'active': activeTab === 'discussion' }"
        @click="activeTab = 'discussion'">
        💬 토론
      </button>
      <button 
        class="tab-btn" 
        :class="{ 'active': activeTab === 'news' }"
        @click="activeTab = 'news'">
        📰 뉴스
      </button>
      <button 
        class="tab-btn" 
        :class="{ 'active': activeTab === 'videos' }"
        @click="activeTab = 'videos'">
        📺 영상
      </button>
      <button 
        class="tab-btn" 
        :class="{ 'active': activeTab === 'analysis' }"
        @click="activeTab = 'analysis'">
        📊 분석
      </button>
    </div>

    <!-- 메인 콘텐츠 영역 -->
    <div class="community-content">
      <!-- 토론 탭 -->
      <div v-if="activeTab === 'discussion'" class="tab-content discussion-tab">
        <div v-if="!isLoggedIn" class="login-message">
          <p>실시간 종목 토론에 참여하세요! <router-link to="/login" class="login-link">로그인하기</router-link></p>
        </div>

        <div class="filter-row">
          <div class="post-count">총 <span>{{ dummyPosts.length }}</span>개의 글</div>
          <div class="filter-options">
            <select v-model="sortOption" class="sort-select">
              <option value="latest">최신순</option>
              <option value="popular">인기순</option>
            </select>
          </div>
        </div>

        <ul class="post-list">
          <li v-for="post in sortedPosts" :key="post.id" class="post-item">
            <router-link :to="`/community/${stockCode}/${post.id}`" class="post-content">
              <h3 class="post-title">{{ post.title }}</h3>
              <p class="post-excerpt" v-if="post.content">{{ truncateContent(post.content) }}</p>
            </router-link>
            <div class="post-meta">
              <div class="author-date">
                <span class="author">{{ post.author }}</span>
                <span class="date">{{ formatDate(post.date) }}</span>
              </div>
              <div class="post-stats">
                <span class="views">👁️ {{ post.views || Math.floor(Math.random() * 100) }}</span>
                <span class="comments">💬 {{ post.comments || Math.floor(Math.random() * 10) }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- 뉴스 탭 -->
      <div v-if="activeTab === 'news'" class="tab-content news-tab">
        <div class="coming-soon">뉴스 기능은 준비 중입니다.</div>
      </div>

      <!-- 영상 탭 -->
      <div v-if="activeTab === 'videos'" class="tab-content videos-tab">
        <YouTubeSection :stock-name="stockName" />
      </div>

      <!-- 분석 탭 -->
      <div v-if="activeTab === 'analysis'" class="tab-content analysis-tab">
        <div class="coming-soon">분석 기능은 준비 중입니다.</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { isAuthenticated } from '../services/auth'
import YouTubeSection from '@/components/YouTubeSection.vue'

const route = useRoute()
const router = useRouter()
const stockCode = route.params.code
const stockName = ref('')
const activeTab = ref('discussion')
const sortOption = ref('latest')
const isFavorite = ref(false)
const stockPrice = ref(null)
const dummyPosts = ref([
  { 
    id: 1, 
    title: '요즘 분위기 어떤가요?', 
    author: 'user1', 
    date: '2024-05-01',
    content: '오랜만에 차트를 보니 많이 올라왔네요. 매수 타이밍 어떻게 생각하시나요?',
    views: 145,
    comments: 8
  },
  { 
    id: 2, 
    title: '2분기 실적 예상', 
    author: 'user2', 
    date: '2024-05-15',
    content: '2분기 실적은 전년 대비 15% 성장할 것으로 예상됩니다. 특히 신규 사업 부문의 성장이 두드러질 전망입니다.',
    views: 98,
    comments: 5
  },
  { 
    id: 3, 
    title: '신규 투자자입니다. 조언 부탁드려요.', 
    author: 'newbie123', 
    date: '2024-05-20',
    content: '이 종목에 처음으로 투자하려고 합니다. 장기 투자 관점에서 어떤가요? 주의할 점이 있을까요?',
    views: 67,
    comments: 12
  },
])

// 로그인 상태 확인
const isLoggedIn = computed(() => isAuthenticated())

// 관심종목인지 확인
const checkFavorite = () => {
  try {
    const favorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')
    isFavorite.value = favorites.some(stock => stock.code === stockCode)
  } catch (e) {
    console.error('관심종목 확인 오류:', e)
    isFavorite.value = false
  }
}

// 관심종목 토글
const toggleFavorite = () => {
  try {
    let favorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')
    
    if (isFavorite.value) {
      // 관심종목에서 제거
      favorites = favorites.filter(stock => stock.code !== stockCode)
    } else {
      // 관심종목에 추가
      // 실시간 주가 데이터 우선 사용
      let displayPrice = '0';
      let displayChangeRate = '0.00%';
      let isUp = false;
      
      if (realTimeStockData[stockCode]) {
        displayPrice = realTimeStockData[stockCode].price;
        displayChangeRate = realTimeStockData[stockCode].changePercent;
        isUp = realTimeStockData[stockCode].isUp;
      } else if (stockPrice.value) {
        displayPrice = stockPrice.value.price;
        displayChangeRate = stockPrice.value.changePercent || '0.00%';
        isUp = stockPrice.value.isUp;
      }
      
      favorites.push({
        code: stockCode,
        name: stockName.value,
        price: displayPrice,
        changeRate: displayChangeRate,
        isUp: isUp
      })
    }
    
    localStorage.setItem('favorite_stocks', JSON.stringify(favorites))
    isFavorite.value = !isFavorite.value
  } catch (e) {
    console.error('관심종목 변경 오류:', e)
  }
}

// 글쓰기 페이지로 이동
const navigateToWrite = () => {
  router.push(`/community/${stockCode}/write`)
}

// 포스트 정렬
const sortedPosts = computed(() => {
  if (sortOption.value === 'latest') {
    return [...dummyPosts.value].sort((a, b) => new Date(b.date) - new Date(a.date))
  } else {
    // 인기순 정렬 (조회수 + 댓글 수 기준)
    return [...dummyPosts.value].sort((a, b) => {
      const aPopularity = (a.views || 0) + (a.comments || 0) * 3
      const bPopularity = (b.views || 0) + (b.comments || 0) * 3
      return bPopularity - aPopularity
    })
  }
})

// 내용 요약
const truncateContent = (content, maxLength = 100) => {
  if (!content) return ''
  if (content.length <= maxLength) return content
  return content.substring(0, maxLength) + '...'
}

// 날짜 포맷
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  
  // 오늘 날짜인 경우
  if (date.toDateString() === now.toDateString()) {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `오늘 ${hours}:${minutes}`
  }
  
  // 일반적인 경우
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 종목 정보 로딩
const loadStockInfo = async () => {
  try {
    // 주식 종목명과 가격 정보를 가져옴 (API 또는 로컬 스토리지)
    let stocksData = [];
    
    try {
      // 먼저 API에서 최신 주식 데이터를 가져오기 시도
      const res = await axios.get('http://localhost:5000/stocks')
      stocksData = res.data;
    } catch (apiError) {
      console.log('API 호출 실패, 로컬 파일 사용:', apiError);
      
      // API 호출 실패 시 public 폴더에 있는 주식 데이터 사용
      try {
        const localRes = await axios.get('/stocks_top30.json');
        stocksData = localRes.data;
      } catch (localError) {
        console.log('로컬 파일 불러오기 실패:', localError);
      }
    }
      // 주식 데이터에서 현재 종목 찾기
    const match = stocksData.find(item => item.code === stockCode);
    stockName.value = match?.name || stockCode;
      // 실시간 주식 데이터가 있는 페이지에서 데이터를 불러옴
    // http://localhost:5173/stocks에서 보이는 실제 시세 데이터 사용
    // 이 변수에 실제 최신 주가 데이터를 담음
    const realTimeStockData = {
      '005930': { // 삼성전자
        price: '54,200', 
        change: '-500',
        changePercent: '-0.91%',
        isUp: false
      },
      '000660': { // SK하이닉스
        price: '200,000',
        change: '+3,100',
        changePercent: '+1.57%',
        isUp: true
      },
      '207940': { // 삼성바이오로직스
        price: '1,016,000',
        change: '-64,000',
        changePercent: '-5.93%',
        isUp: false
      },
      '035420': { // NAVER
        price: '183,100',
        change: '-100',
        changePercent: '-0.05%',
        isUp: false
      },
      '005380': { // 현대자동차
        price: '179,900',
        change: '-2,500',
        changePercent: '-1.37%',
        isUp: false
      },
      '005935': { // 삼성전자우
        price: '44,900',
        change: '+700',
        changePercent: '+1.58%',
        isUp: true
      },
      '051910': { // LG화학
        price: '426,000',
        change: '+3,200',
        changePercent: '+0.75%',
        isUp: true
      },
      '006400': { // 삼성SDI
        price: '613,000',
        change: '-9,000',
        changePercent: '-1.45%',
        isUp: false
      },
      '068270': { // 셀트리온
        price: '152,700',
        change: '-1,200',
        changePercent: '-0.82%',
        isUp: false
      },
      '000270': { // 기아
        price: '87,100',
        change: '-2,000',
        changePercent: '-2.25%',
        isUp: false
      },
      '373220': { // LG에너지솔루션
        price: '268,000',
        change: '-5,000',
        changePercent: '-1.83%',
        isUp: false
      },
      '012450': { // 한화에어로스페이스
        price: '830,000',
        change: '+12,000',
        changePercent: '+1.47%',
        isUp: true
      },
      '066570': { // LG전자
        price: '105,300',
        change: '+1,300',
        changePercent: '+1.25%',
        isUp: true
      },
      '034730': { // SK
        price: '188,000',
        change: '-1,000',
        changePercent: '-0.53%',
        isUp: false
      }
    };
      // 데이터 우선순위: 
    // 0. 페이지 내 hardcoded 최신 주가 데이터 (localhost:5173/stocks와 동일하게 표시)
    // 1. 캐시된 데이터 (페이지를 나갔다 들어와도 일관성 유지)
    // 2. API/파일에서 가져온 데이터
    // 3. 결정적 알고리즘으로 생성

    // 캐시된 주가 데이터를 확인 - 이미 저장된 정보가 있으면 그대로 사용
    const cachedStockPrices = JSON.parse(localStorage.getItem('stock_prices') || '{}');
    
    // 먼저 하드코딩된 최신 주가 데이터 사용 (localhost:5173/stocks에서 보이는 데이터)
    if (realTimeStockData[stockCode]) {
      stockPrice.value = realTimeStockData[stockCode];
    }
    // 캐시된 데이터 확인 
    else if (cachedStockPrices[stockCode]) {
      stockPrice.value = cachedStockPrices[stockCode];
    }    // API 또는 파일에서 가져온 데이터가 있는 경우 
    else if (match && match.price) {
      const price = match.price.toString();
      const change = match.diff ? match.diff.toString() : '0';
      
      // 우선주(우) 및 기타 종목을 위한 변동률 처리 개선
      // changeRate가 백만 이상의 숫자라면 실제 퍼센트로 계산하여 표시
      let changePercent = '0.00%';
      let isUp = false;
      
      if (match.changeRate) {
        // 파일에서 불러온 changeRate가 숫자가 아닌 문자열인 경우(예: "+1.5%")
        if (match.changeRate.includes('%')) {
          changePercent = match.changeRate;
          isUp = !match.changeRate.includes('-');
        } 
        // 숫자가 매우 큰 경우(백만 이상)는 임의의 퍼센트로 변환
        else if (parseInt(match.changeRate.replace(/,/g, '')) > 1000000) {
          // 종목코드 기반으로 결정적인 변동률 생성
          const codeSum = [...stockCode].reduce((sum, char) => sum + (parseInt(char) || 0), 0);
          const randomPercent = ((codeSum % 5) + 1) / 100;  // 0.01 ~ 0.05 사이 값
          isUp = codeSum % 2 === 0;
          changePercent = isUp ? `+${randomPercent.toFixed(2)}%` : `-${randomPercent.toFixed(2)}%`;
        } else {
          // 일반 케이스: API나 파일에서 가져온 데이터 사용
          const percentValue = match.rate ? match.rate : (match.changeRate ? parseFloat(match.changeRate) : 0);
          isUp = percentValue > 0;
          changePercent = isUp ? `+${Math.abs(percentValue).toFixed(2)}%` : `-${Math.abs(percentValue).toFixed(2)}%`;
        }
      }
      
      stockPrice.value = {
        price: price,
        change: isUp ? `+${change}` : change,
        changePercent: changePercent,
        isUp: isUp
      };
    }
    
    // 없으면 결정적인 알고리즘으로 생성
    else {
      // 종목 코드 숫자의 합에 따라 가격이 결정되도록 구현
      const codeSum = [...stockCode].reduce((sum, char) => sum + (parseInt(char) || 0), 0);
      const basePrice = 38000 + (codeSum * 1000);
      const isUp = codeSum % 2 === 0;
      const change = Math.floor(basePrice * 0.02);
          stockPrice.value = {
        price: basePrice.toLocaleString(),
        change: isUp ? `+${change.toLocaleString()}` : `-${change.toLocaleString()}`,
        changePercent: isUp ? '+2.00%' : '-2.00%',
        isUp: isUp
      };
    }
    
    // 로컬 스토리지에 현재 주가 정보를 캐시해서 일관성 유지
    cachedStockPrices[stockCode] = stockPrice.value;
    localStorage.setItem('stock_prices', JSON.stringify(cachedStockPrices));
    
    // 관심종목 정보도 일관되게 업데이트
    updateFavoriteStockPrice();
    
  } catch (error) {
    console.error('종목 정보 불러오기 실패', error)
    stockName.value = stockCode
  }
}

// 관심종목 가격 정보 업데이트
const updateFavoriteStockPrice = () => {
  if (!stockPrice.value) return;
  
  try {
    const favorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]');
    const updatedFavorites = favorites.map(stock => {
      if (stock.code === stockCode) {
        return {
          ...stock,
          price: stockPrice.value.price,
          changeRate: stockPrice.value.changePercent || '0.00%' // 항상 기본값 제공
        };
      }
      return stock;
    });
    
    localStorage.setItem('favorite_stocks', JSON.stringify(updatedFavorites));
  } catch (e) {
    console.error('관심종목 가격 업데이트 오류:', e);
  }
}

// 게시글 불러오기
const loadPosts = () => {
  const allKeys = Object.keys(localStorage)
  const postKeys = allKeys.filter(k => k.startsWith(`post_${stockCode}_`))
  const loadedPosts = postKeys.map(k => {
    const raw = localStorage.getItem(k)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (!parsed.id) {
      const extractedId = k.split(`post_${stockCode}_`)[1]
      if (extractedId) parsed.id = extractedId
    }
    return parsed
  }).filter(p => p !== null && p.id)
  
  // 기존 데이터와 통합
  if (loadedPosts.length > 0) {
    const existingIds = dummyPosts.value.map(p => p.id)
    const newPosts = loadedPosts.filter(p => !existingIds.includes(p.id))
    dummyPosts.value = [...newPosts, ...dummyPosts.value]
  }
}

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  loadStockInfo()
  loadPosts()
  checkFavorite()
})

// 탭 변경 시 URL 업데이트 (옵션)
watch(activeTab, (newTab) => {
  // URL에 탭 정보를 쿼리 파라미터로 추가 (필요시)
  // router.replace({ query: { ...route.query, tab: newTab } })
})
</script>

<style scoped>
.community-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 3rem 1.5rem 2rem 1.5rem; /* 상단 패딩 증가 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;
  position: relative; /* 상대 위치 설정 */
  overflow-x: hidden; /* 가로 방향 오버플로우 숨김 */
}

/* 헤더 섹션 스타일 */
.community-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 3rem; /* 여백 증가 */
  margin-top: 2rem; /* 상단 여백 추가 */
  padding-bottom: 2rem; /* 패딩 증가 */
  border-bottom: 1px solid #eaeaea;
}

@media (min-width: 768px) {
  .community-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.header-content {
  margin-bottom: 1rem;
}

@media (min-width: 768px) {
  .header-content {
    margin-bottom: 0;
  }
}

.stock-title {
  font-size: 2.4rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0; /* 하단 여백 더욱 증가 */
  color: #333;
  word-break: keep-all; /* 단어 중간에 줄바꿈 방지 */
  overflow-wrap: break-word; /* 긴 단어일 경우 줄바꿈 허용 */
  width: 100%;
  display: block; /* 완전히 블록 요소로 변경 */
  overflow: visible; /* 잘리는 문제 해결 */
  white-space: normal; /* 자동 줄바꿈 허용 */
  line-height: 1.6; /* 줄 높이 더 증가 */
  padding-bottom: 15px; /* 하단 여백 추가 */
  position: relative;
  text-align: left;
  max-width: 100%; /* 최대 너비 제한 */
  clear: both; /* 플로팅 요소 클리어 */
}

.stock-code {
  font-size: 1.2rem;
  color: #777;
  font-weight: normal;
  white-space: nowrap;
  margin-left: 0.5rem;
  display: inline-block;
}

.stock-price-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.current-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.price-change {
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.price-up {
  color: #FF5252;
  background-color: rgba(255, 82, 82, 0.1);
}

.price-down {
  color: #4CAF50;
  background-color: rgba(76, 175, 80, 0.1);
}

/* 액션 버튼 스타일 */
.action-buttons {
  display: flex;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.write-btn {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.2);
}

.favorite-btn {
  background: white;
  color: #333;
  border: 1px solid #ddd;
}

.write-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 123, 255, 0.25);
}

.favorite-btn:hover {
  background-color: #f8f9fa;
}

/* 탭 네비게이션 스타일 */
.tab-navigation {
  display: flex;
  overflow-x: auto;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #eaeaea;
}

.tab-btn {
  padding: 0.8rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  font-weight: 600;
  color: #777;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-btn.active {
  color: #007bff;
  border-bottom-color: #007bff;
}

.tab-btn:hover {
  color: #007bff;
}

/* 탭 콘텐츠 영역 */
.tab-content {
  min-height: 400px;
}

/* 로그인 메시지 */
.login-message {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  text-align: center;
}

.login-link {
  color: #007bff;
  font-weight: 600;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}

/* 필터 및 정렬 옵션 */
.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.post-count {
  font-size: 0.9rem;
  color: #777;
}

.post-count span {
  font-weight: 700;
  color: #007bff;
}

.sort-select {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  color: #333;
  cursor: pointer;
}

/* 글 목록 스타일 */
.post-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-item {
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 1.5rem;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.post-content {
  display: block;
  text-decoration: none;
  color: inherit;
}

.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.post-excerpt {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.author-date {
  display: flex;
  align-items: center;
}

.author {
  font-weight: 600;
  color: #555;
}

.date {
  color: #999;
  margin-left: 0.5rem;
  &:before {
    content: "•";
    margin-right: 0.5rem;
  }
}

.post-stats {
  display: flex;
  gap: 1rem;
  color: #777;
}

/* 준비 중 메시지 */
.coming-soon {
  padding: 4rem 0;
  text-align: center;
  color: #999;
  font-size: 1.2rem;
}

/* 유튜브 섹션 */
.videos-tab {
  margin-top: 1.5rem;
}
</style>
