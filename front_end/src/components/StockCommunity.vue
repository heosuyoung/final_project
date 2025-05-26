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
      </div>      <!-- 분석 탭 -->
      <div v-if="activeTab === 'analysis'" class="tab-content analysis-tab">
        <div class="analysis-container">          <!-- 주가 차트 영역 -->
          <div class="chart-section">
            <div class="chart-header">
              <h3 class="section-title">📈 주가 차트</h3>
              <div class="chart-period-buttons">
                <button 
                  class="period-btn"
                  :class="{ 'active': chartPeriod === '1d' }"
                  @click="changeChartPeriod('1d')">
                  일봉
                </button>
                <button 
                  class="period-btn"
                  :class="{ 'active': chartPeriod === '1wk' }"
                  @click="changeChartPeriod('1wk')">
                  주봉
                </button>
                <button 
                  class="period-btn"
                  :class="{ 'active': chartPeriod === '1mo' }"
                  @click="changeChartPeriod('1mo')">
                  월봉
                </button>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="stockChart" width="800" height="400"></canvas>
            </div>
          </div>          <!-- 재무정보 영역 -->
          <div class="financial-info-section">
            <h3 class="section-title">💰 재무정보</h3>
            <div class="financial-cards">
              <!-- PER 카드 (데이터가 있을 때만 표시) -->
              <div class="financial-card" v-if="financialData.per !== undefined">
                <div class="financial-label">PER (Price Earning Ratio)</div>
                <div class="financial-value">{{ financialData.per }}</div>
                <div class="financial-desc">주가수익비율</div>
              </div>
              
              <!-- PBR 카드 (데이터가 있을 때만 표시) -->
              <div class="financial-card" v-if="financialData.pbr !== undefined">
                <div class="financial-label">PBR (Price Book-value Ratio)</div>
                <div class="financial-value">{{ financialData.pbr }}</div>
                <div class="financial-desc">주가순자산비율</div>
              </div>
              
              <!-- ROE 카드 (데이터가 있을 때만 표시) -->
              <div class="financial-card" v-if="financialData.roe !== undefined">
                <div class="financial-label">ROE (Return on Equity)</div>
                <div class="financial-value">{{ financialData.roe }}%</div>
                <div class="financial-desc">자기자본이익률</div>
              </div>
              
              <!-- 부채비율 카드 (데이터가 있을 때만 표시) -->
              <div class="financial-card" v-if="financialData.debtRatio !== undefined">
                <div class="financial-label">부채비율</div>
                <div class="financial-value">{{ financialData.debtRatio }}%</div>
                <div class="financial-desc">총부채/총자본</div>
              </div>
              
              <!-- 영업이익률 카드 (데이터가 있을 때만 표시) -->
              <div class="financial-card" v-if="financialData.operatingMargin !== undefined">
                <div class="financial-label">영업이익률</div>
                <div class="financial-value">{{ financialData.operatingMargin }}%</div>
                <div class="financial-desc">영업이익/매출액</div>
              </div>
              
              <!-- 배당수익률 카드 (데이터가 있을 때만 표시) -->
              <div class="financial-card" v-if="financialData.dividendYield !== undefined">
                <div class="financial-label">배당수익률</div>
                <div class="financial-value">{{ financialData.dividendYield }}%</div>
                <div class="financial-desc">연간배당금/주가</div>
              </div>
              
              <!-- 시가총액 카드 (항상 표시) -->
              <div class="financial-card" v-if="financialData.marketCap !== 'N/A'">
                <div class="financial-label">시가총액</div>
                <div class="financial-value">{{ formatMarketCap(financialData.marketCap) }}</div>
                <div class="financial-desc">발행주식수 × 주가</div>
              </div>
            </div>
          </div>

          <!-- 기술적 분석 영역 -->
          <div class="technical-analysis-section">
            <h3 class="section-title">📊 기술적 분석</h3>
            <div class="technical-indicators">
              <div class="indicator-item">
                <span class="indicator-label">RSI (14일)</span>
                <span class="indicator-value" :class="getRsiClass(technicalData.rsi)">{{ technicalData.rsi }}</span>
                <span class="indicator-status">{{ getRsiStatus(technicalData.rsi) }}</span>
              </div>
              
              <div class="indicator-item">
                <span class="indicator-label">이동평균선 (20일)</span>
                <span class="indicator-value">{{ technicalData.ma20 }}원</span>
                <span class="indicator-status" :class="getMaClass(stockPrice?.price, technicalData.ma20)">
                  {{ getMaStatus(stockPrice?.price, technicalData.ma20) }}
                </span>
              </div>
              
              <div class="indicator-item">
                <span class="indicator-label">이동평균선 (60일)</span>
                <span class="indicator-value">{{ technicalData.ma60 }}원</span>
                <span class="indicator-status" :class="getMaClass(stockPrice?.price, technicalData.ma60)">
                  {{ getMaStatus(stockPrice?.price, technicalData.ma60) }}
                </span>
              </div>
              
              <div class="indicator-item">
                <span class="indicator-label">볼린저 밴드</span>
                <span class="indicator-value">{{ technicalData.bollingerStatus }}</span>
                <span class="indicator-desc">상단: {{ technicalData.bollingerUpper }}원, 하단: {{ technicalData.bollingerLower }}원</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { isAuthenticated } from '../services/auth'
import YouTubeSection from '@/components/YouTubeSection.vue'
import { Chart, registerables } from 'chart.js'

// Chart.js 등록
Chart.register(...registerables)

const route = useRoute()
const router = useRouter()
const stockCode = route.params.code
const stockName = ref('')
const activeTab = ref('discussion')
const sortOption = ref('latest')
const isFavorite = ref(false)
const stockPrice = ref(null)

// 차트와 분석을 위한 새로운 ref들
const stockChart = ref(null)
const financialData = ref({})
const technicalData = ref({})
const chartInstance = ref(null)
const chartPeriod = ref('1d') // 기본값: 일봉
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
    dummyPosts.value = [...newPosts, ...dummyPosts.value]  }
}

// 재무정보 생성 함수
const generateFinancialData = async () => {
  try {
    // 실제 API에서 재무정보 가져오기
    const response = await axios.get(`http://localhost:5000/stock-analysis/${stockCode}`);
    
    if (response.data.success) {
      const apiFinancialData = response.data.data.financial_data;
      financialData.value = {
        per: apiFinancialData.per,
        pbr: apiFinancialData.pbr,
        roe: apiFinancialData.roe,
        debtRatio: apiFinancialData.debtRatio,
        operatingMargin: apiFinancialData.operatingMargin,
        dividendYield: apiFinancialData.dividendYield
      };
    } else {
      throw new Error('API 응답 실패');
    }
  } catch (error) {
    console.warn('실제 재무정보 가져오기 실패, 가상 데이터 사용:', error);
    
    // API 실패 시 기존 가상 데이터 사용
    const codeSum = [...stockCode].reduce((sum, char) => sum + (parseInt(char) || 0), 0);
    
    const per = (8 + (codeSum % 20)).toFixed(1);
    const pbr = (0.5 + (codeSum % 30) / 10).toFixed(1);
    const roe = (5 + (codeSum % 25)).toFixed(1);
    const debtRatio = (20 + (codeSum % 80)).toFixed(1);
    const operatingMargin = (3 + (codeSum % 15)).toFixed(1);
    const dividendYield = (1 + (codeSum % 5)).toFixed(1);
    
    financialData.value = {
      per,
      pbr,
      roe,
      debtRatio,
      operatingMargin,
      dividendYield
    };
  }
};

// 기술적 분석 데이터 생성 함수
const generateTechnicalData = async () => {
  try {
    // 실제 API에서 기술적 분석 데이터 가져오기
    const response = await axios.get(`http://localhost:5000/stock-analysis/${stockCode}`);
    
    if (response.data.success) {
      const apiTechnicalData = response.data.data.technical_data;
      if (Object.keys(apiTechnicalData).length > 0) {
        technicalData.value = {
          rsi: apiTechnicalData.rsi,
          ma20: apiTechnicalData.ma20?.toLocaleString() || '0',
          ma60: apiTechnicalData.ma60?.toLocaleString() || '0',
          bollingerUpper: apiTechnicalData.bollingerUpper?.toLocaleString() || '0',
          bollingerLower: apiTechnicalData.bollingerLower?.toLocaleString() || '0',
          bollingerStatus: apiTechnicalData.bollingerStatus || '데이터 없음'
        };
        return;
      }
    }
    throw new Error('API 데이터 없음');
  } catch (error) {
    console.warn('실제 기술적 분석 데이터 가져오기 실패, 가상 데이터 사용:', error);
    
    // API 실패 시 기존 가상 데이터 사용
    if (!stockPrice.value) return;
    
    const currentPrice = parseInt(stockPrice.value.price.replace(/,/g, ''));
    const codeSum = [...stockCode].reduce((sum, char) => sum + (parseInt(char) || 0), 0);
    
    const rsi = 30 + (codeSum % 40);
    const ma20 = Math.round(currentPrice * (0.95 + (codeSum % 10) / 100));
    const ma60 = Math.round(currentPrice * (0.90 + (codeSum % 15) / 100));
    const bollingerUpper = Math.round(currentPrice * 1.05);
    const bollingerLower = Math.round(currentPrice * 0.95);
    
    let bollingerStatus = '중간대';
    if (currentPrice >= bollingerUpper * 0.98) {
      bollingerStatus = '상단 근접';
    } else if (currentPrice <= bollingerLower * 1.02) {
      bollingerStatus = '하단 근접';
    }
    
    technicalData.value = {
      rsi,
      ma20: ma20.toLocaleString(),
      ma60: ma60.toLocaleString(),
      bollingerUpper: bollingerUpper.toLocaleString(),
      bollingerLower: bollingerLower.toLocaleString(),
      bollingerStatus
    };
  }
};

// RSI 상태 판단 함수들
const getRsiClass = (rsi) => {
  if (rsi >= 70) return 'rsi-overbought';
  if (rsi <= 30) return 'rsi-oversold';
  return 'rsi-neutral';
};

const getRsiStatus = (rsi) => {
  if (rsi >= 70) return '과매수';
  if (rsi <= 30) return '과매도';
  return '중립';
};

// 이동평균선 상태 판단 함수들
const getMaClass = (currentPrice, maPrice) => {
  if (!currentPrice || !maPrice) return '';
  const current = parseInt(currentPrice.replace(/,/g, ''));
  const ma = parseInt(maPrice.replace(/,/g, ''));
  return current > ma ? 'ma-above' : 'ma-below';
};

const getMaStatus = (currentPrice, maPrice) => {
  if (!currentPrice || !maPrice) return '';
  const current = parseInt(currentPrice.replace(/,/g, ''));
  const ma = parseInt(maPrice.replace(/,/g, ''));
  return current > ma ? '상향돌파' : '하향이탈';
};

// 차트 생성 함수
const createStockChart = async () => {
  if (!stockChart.value) return;
  
  await nextTick();
  
  try {
    // Chart.js 동적 import
    const { Chart, registerables } = await import('chart.js');
    Chart.register(...registerables);
    
    const ctx = stockChart.value.getContext('2d');
    
    // 기존 차트가 있으면 제거
    if (chartInstance.value) {
      chartInstance.value.destroy();
    }
    
    // 실제 API에서 차트 데이터 가져오기
    let chartData = [];
    let chartLabels = [];
      try {
      const response = await axios.get(`http://localhost:5000/stock-analysis/${stockCode}`, {
        params: { period: chartPeriod.value }
      });
      
      if (response.data.success && response.data.data.chart_data.length > 0) {
        const apiChartData = response.data.data.chart_data;
        chartLabels = apiChartData.map(item => {
          const date = new Date(item.date);
          if (chartPeriod.value === '1d') {
            return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
          } else if (chartPeriod.value === '1wk') {
            return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
          } else { // 1mo
            return date.toLocaleDateString('ko-KR', { year: '2-digit', month: 'short' });
          }
        });
        chartData = apiChartData.map(item => item.price);
      } else {
        throw new Error('API 차트 데이터 없음');
      }
    } catch (error) {
      console.warn('실제 차트 데이터 가져오기 실패, 가상 데이터 사용:', error);
      
      // API 실패 시 가상 데이터 생성
      if (!stockPrice.value) return;
      
      const currentPrice = parseInt(stockPrice.value.price.replace(/,/g, ''));
      let price = currentPrice * 0.9;
      
      for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        chartLabels.push(date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' }));
        
        if (i === 0) {
          price = currentPrice;
        } else {
          const variation = (Math.random() - 0.5) * 0.06;
          price = price * (1 + variation);
        }
        chartData.push(Math.round(price));
      }
    }
    
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartLabels,
        datasets: [{
          label: `${stockName.value} 주가`,
          data: chartData,
          borderColor: stockPrice.value?.isUp ? '#FF5252' : '#007bff',
          backgroundColor: stockPrice.value?.isUp ? 'rgba(255, 82, 82, 0.1)' : 'rgba(0, 123, 255, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: `${stockName.value} (${stockCode}) 주가 추이`,
            font: {
              size: 16,
              weight: 'bold'
            }
          },
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              callback: function(value) {
                return value.toLocaleString() + '원';
              }
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    });
  } catch (error) {
    console.error('차트 생성 실패:', error);
  }
};

// 시가총액 포맷 함수
const formatMarketCap = (marketCap) => {
  if (!marketCap || marketCap === 'N/A') return 'N/A';
  
  const num = typeof marketCap === 'string' ? parseFloat(marketCap) : marketCap;
  if (isNaN(num)) return 'N/A';
  
  if (num >= 1000000000000) {
    return `${(num / 1000000000000).toFixed(1)}조원`;
  } else if (num >= 100000000) {
    return `${(num / 100000000).toFixed(0)}억원`;
  } else {
    return `${num.toLocaleString()}원`;
  }
};

// 차트 기간 변경 함수
const changeChartPeriod = async (period) => {
  chartPeriod.value = period;
  if (activeTab.value === 'analysis') {
    await nextTick();
    createStockChart();
  }
};

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  loadStockInfo()
  loadPosts()
  checkFavorite()
})

// 탭 변경 감지 및 분석 탭일 때 차트 생성
watch(activeTab, async (newTab) => {
  if (newTab === 'analysis') {
    generateFinancialData();
    generateTechnicalData();
    await nextTick();
    createStockChart();
  }
  // URL에 탭 정보를 쿼리 파라미터로 추가 (필요시)
  // router.replace({ query: { ...route.query, tab: newTab } })
})

// 주가 정보가 로드된 후 분석 데이터 생성
watch(stockPrice, () => {
  if (stockPrice.value && activeTab.value === 'analysis') {
    generateFinancialData();
    generateTechnicalData();
    createStockChart();
  }
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

/* 분석 탭 스타일 */
.analysis-tab {
  margin-top: 1.5rem;
}

.analysis-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* 차트 섹션 */
.chart-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 차트 헤더 */
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* 차트 기간 선택 버튼 */
.chart-period-buttons {
  display: flex;
  gap: 0.5rem;
}

.period-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  color: #666;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
}

.period-btn:hover {
  border-color: #007bff;
  color: #007bff;
  background: #f8f9ff;
}

.period-btn.active {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border-color: #007bff;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.2);
}

.chart-container {
  position: relative;
  height: 400px;
  margin-top: 1rem;
}

.chart-container canvas {
  max-width: 100%;
  height: 100% !important;
}

/* 재무정보 섹션 */
.financial-info-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.financial-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.financial-card {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border: 1px solid #e3e8ff;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  transition: transform 0.2s ease;
}

.financial-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
}

.financial-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.financial-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #007bff;
  margin-bottom: 0.3rem;
}

.financial-desc {
  font-size: 0.8rem;
  color: #888;
}

/* 기술적 분석 섹션 */
.technical-analysis-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.technical-indicators {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.indicator-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.indicator-label {
  font-weight: 600;
  color: #333;
  flex: 1;
}

.indicator-value {
  font-weight: 700;
  font-size: 1.1rem;
  margin: 0 1rem;
}

.indicator-status {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.indicator-desc {
  font-size: 0.85rem;
  color: #666;
  margin-left: 1rem;
}

/* RSI 상태별 색상 */
.rsi-overbought {
  color: #dc3545;
  background-color: #ffeef0;
}

.rsi-oversold {
  color: #28a745;
  background-color: #eef8f0;
}

.rsi-neutral {
  color: #6c757d;
  background-color: #f8f9fa;
}

/* 이동평균선 상태별 색상 */
.ma-above {
  color: #28a745;
  background-color: #eef8f0;
}

.ma-below {
  color: #dc3545;
  background-color: #ffeef0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .financial-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .indicator-item {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .indicator-label,
  .indicator-value,
  .indicator-status {
    margin: 0;
  }
  
  .chart-container {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .financial-cards {
    grid-template-columns: 1fr;
  }
  
  .analysis-container {
    gap: 1.5rem;
  }
  
  .chart-section,
  .financial-info-section,
  .technical-analysis-section {
    padding: 1rem;
  }
}
</style>
