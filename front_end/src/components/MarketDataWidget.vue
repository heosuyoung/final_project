<template>
  <div class="market-data">
    <h3>시장 데이터</h3>
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>시장 데이터를 불러오는 중입니다...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="fetchData" class="retry-button">다시 시도</button>
    </div>
    
    <div v-else class="data-container">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id" 
          :class="['tab-button', activeTab === tab.id ? 'active' : '']"
          @click="changeTab(tab.id)">
          {{ tab.name }}
        </button>
      </div>
      
      <div class="tab-content">
        <!-- 주식 시장 정보 -->
        <div v-if="activeTab === 'stocks'" class="stocks-data">
          <div class="market-summary">
            <div class="market-index">
              <h4>코스피</h4>
              <div class="index-value" :class="getValueClass(stockData.kospi.change)">
                {{ stockData.kospi.value }}
                <span class="change">{{ formatChange(stockData.kospi.change) }}</span>
              </div>
            </div>
            
            <div class="market-index">
              <h4>코스닥</h4>
              <div class="index-value" :class="getValueClass(stockData.kosdaq.change)">
                {{ stockData.kosdaq.value }}
                <span class="change">{{ formatChange(stockData.kosdaq.change) }}</span>
              </div>
            </div>
          </div>
          
          <h4>인기 종목</h4>
          <table class="stocks-table">
            <thead>
              <tr>
                <th>종목명</th>
                <th>현재가</th>
                <th>등락</th>
                <th>거래량</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(stock, index) in stockData.topStocks" :key="index">
                <td>{{ stock.name }}</td>
                <td>{{ stock.price }}원</td>
                <td :class="getValueClass(stock.change)">{{ formatChange(stock.change) }}</td>
                <td>{{ formatVolume(stock.volume) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 금융 상품 정보 -->
        <div v-else-if="activeTab === 'products'" class="products-data">
          <h4>추천 금융 상품</h4>
          <table class="products-table">
            <thead>
              <tr>
                <th>상품명</th>
                <th>금융사</th>
                <th>수익률</th>
                <th>특징</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in financialProducts" :key="index">
                <td>{{ product.name }}</td>
                <td>{{ product.company }}</td>
                <td>{{ product.rate }}</td>
                <td>{{ product.feature }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- 금리 정보 -->
        <div v-else-if="activeTab === 'rates'" class="rates-data">
          <div class="rates-container">
            <div class="rate-card">
              <h4>기준금리</h4>
              <div class="rate-value">{{ ratesData.base }}%</div>
            </div>
            
            <div class="rate-card">
              <h4>평균 예금금리</h4>
              <div class="rate-value">{{ ratesData.deposit }}%</div>
            </div>
            
            <div class="rate-card">
              <h4>평균 대출금리</h4>
              <div class="rate-value">{{ ratesData.loan }}%</div>
            </div>
            
            <div class="rate-card">
              <h4>주택담보대출금리</h4>
              <div class="rate-value">{{ ratesData.mortgage }}%</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="data-footer">
        <p class="update-time">마지막 업데이트: {{ lastUpdated }}</p>
        <button class="refresh-button" @click="fetchData">새로고침</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

export default {
  name: 'MarketDataWidget',
  setup() {
    const loading = ref(true);
    const error = ref(null);
    const activeTab = ref('stocks');
    const lastUpdated = ref('');
    
    // 탭 정의
    const tabs = [
      { id: 'stocks', name: '주식 시장' },
      { id: 'products', name: '금융 상품' },
      { id: 'rates', name: '금리 정보' }
    ];
    
    // 데이터 상태
    const stockData = ref({
      kospi: { value: 0, change: 0 },
      kosdaq: { value: 0, change: 0 },
      topStocks: []
    });
    
    const financialProducts = ref([
      { name: 'EA$E 적금', company: 'EA$E 은행', rate: '연 3.5%', feature: '1년 만기, 월 50만원 한도' },
      { name: '슈퍼 정기예금', company: '국민은행', rate: '연 3.2%', feature: '3년 만기, 최소 1천만원' },
      { name: '디지털 입출금통장', company: '신한은행', rate: '연 2.5%', feature: '수수료 면제, 모바일 전용' },
      { name: '청년 우대 적금', company: '하나은행', rate: '연 4.0%', feature: '3년 만기, 39세 이하 가입가능' },
      { name: '직장인 월급통장', company: '우리은행', rate: '연 2.8%', feature: '급여 이체 시 우대금리' }
    ]);
    
    const ratesData = ref({
      base: 2.5,
      deposit: 3.2,
      loan: 4.8,
      mortgage: 4.5
    });
      // 데이터 가져오기
    const fetchData = async () => {
      loading.value = true;
      error.value = null;
      try {
        // Flask API 서버에서 실시간으로 크롤링된 주식 데이터 가져오기
        const response = await axios.get('http://127.0.0.1:5000/stocks');
        
        // 코스피, 코스닥 인덱스 값 (샘플 데이터 - 나중에 API로 대체 가능)
        stockData.value.kospi = {
          value: 2548.22,
          change: 0.75
        };
        
        stockData.value.kosdaq = {
          value: 758.14,
          change: -0.42
        };
        
        // 상위 5개 종목만 가져오기
        stockData.value.topStocks = response.data.slice(0, 5).map(stock => {
          // 변동률 파싱 (예: "-1.20%" -> -1.20)
          const changeRateStr = stock.changeRate.replace('%', '').trim();
          const change = parseFloat(changeRateStr) || 0;
          
          // 거래량이 문자열인 경우 처리 (실제 API가 반환하는 형식에 맞게 파싱)
          let volume = 0;
          if (typeof stock.volume === 'string') {
            // 콤마와 소수점 처리
            volume = parseFloat(stock.volume.replace(/,/g, '')) || 0;
            // 음수 거래량은 절대값으로 처리
            volume = Math.abs(volume);
          } else {
            volume = Math.abs(stock.volume); // 거래량이 숫자일 경우 절대값으로 처리
          }
          
          return {
            name: stock.name,
            price: stock.price, // API에서 반환된 형식 그대로 사용
            change: change,
            volume: volume
          };
        });
        
        // 마지막 업데이트 시간
        lastUpdated.value = new Date().toLocaleString();
      } catch (err) {
        console.error('시장 데이터 로딩 오류:', err);
        error.value = '시장 데이터를 불러오는데 실패했습니다.';
      } finally {
        loading.value = false;
      }
    };
    
    // 변경률에 따른 CSS 클래스 결정 (상승: 빨강, 하락: 파랑)
    const getValueClass = (change) => {
      if (change > 0) return 'up';
      if (change < 0) return 'down';
      return '';
    };
    
    // 변경률 포맷팅
    const formatChange = (change) => {
      const prefix = change > 0 ? '+' : '';
      return `${prefix}${change.toFixed(2)}%`;
    };
    
    // 거래량 포맷팅
    const formatVolume = (volume) => {
      if (volume >= 1000000) {
        return `${(volume / 1000000).toFixed(1)}M`;
      } else if (volume >= 1000) {
        return `${(volume / 1000).toFixed(1)}K`;
      } else {
        return volume.toString();
      }
    };
    
    // 탭 변경 함수
    const changeTab = (tabId) => {
      activeTab.value = tabId;
    };
      // 주기적으로 데이터 갱신
    const startAutoRefresh = () => {
      // 1분마다 자동 갱신
      const autoRefreshInterval = setInterval(() => {
        fetchData();
      }, 60000); // 60초 = 1분
      
      return autoRefreshInterval;
    };
    
    // 컴포넌트 마운트 시 데이터 로드 및 자동 갱신 시작
    onMounted(() => {
      fetchData();
      const interval = startAutoRefresh();
      
      // 컴포넌트가 언마운트될 때 인터벌 정리
      onUnmounted(() => {
        clearInterval(interval);
      });
    });
    
    return {
      loading,
      error,
      stockData,
      financialProducts,
      ratesData,
      activeTab,
      tabs,
      lastUpdated,
      fetchData,
      getValueClass,
      formatChange,
      formatVolume,
      changeTab
    };
  }
};
</script>

<style scoped>
.market-data {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.market-data h3 {
  font-size: 1.3rem;
  margin-bottom: 1.2rem;
  color: #333;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 123, 255, 0.1);
  border-left-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  text-align: center;
  padding: 1.5rem;
  color: #dc3545;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 1rem;
}

.tab-button {
  padding: 0.7rem 1.2rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #495057;
  font-weight: 500;
  position: relative;
}

.tab-button.active {
  color: #007bff;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #007bff;
}

.tab-content {
  padding: 1rem 0;
}

.market-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1.5rem;
  text-align: center;
}

.market-index h4 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #555;
}

.index-value {
  font-size: 1.5rem;
  font-weight: 600;
}

.change {
  font-size: 1rem;
  margin-left: 0.5rem;
}

.up {
  color: #e53e3e;
}

.down {
  color: #3182ce;
}

.stocks-table, .products-table {
  width: 100%;
  border-collapse: collapse;
}

.stocks-table th, .products-table th {
  text-align: left;
  padding: 0.8rem 0.5rem;
  border-bottom: 1px solid #ddd;
  color: #555;
  font-weight: 500;
}

.stocks-table td, .products-table td {
  padding: 0.8rem 0.5rem;
  border-bottom: 1px solid #eee;
}

.rates-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.rate-card {
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  text-align: center;
}

.rate-card h4 {
  font-size: 1rem;
  color: #555;
  margin-bottom: 0.8rem;
}

.rate-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.data-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.update-time {
  color: #6c757d;
  font-size: 0.9rem;
}

.refresh-button {
  padding: 0.4rem 0.8rem;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.refresh-button:hover {
  background: #e9ecef;
}

@media (max-width: 768px) {
  .market-summary {
    flex-direction: column;
    gap: 1rem;
  }
  
  .rates-container {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 576px) {
  .tabs {
    flex-wrap: wrap;
  }
  
  .tab-button {
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .rates-container {
    grid-template-columns: 1fr;
  }
}
</style>
