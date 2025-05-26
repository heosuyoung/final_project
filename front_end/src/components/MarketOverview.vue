<template>
  <section class="market-overview">
    <div class="content-container">
      <h2 class="section-title">주요 시장 동향</h2>
      <p class="section-desc">국내외 주요 지수 및 환율, 상품 가격을 확인하세요.</p>
      
      <div class="market-data-container">
        <!-- 주요 지수 -->
        <div class="market-card">
          <h3 class="market-card-title">주요 지수</h3>
          <div class="data-list">
            <div class="data-item" v-for="(index, i) in marketIndices" :key="i">
              <div class="data-name">{{ index.name }}</div>
              <div class="data-value">{{ index.value }}</div>
              <div :class="['data-change', index.isUp ? 'positive' : 'negative']">
                {{ index.isUp ? '+' : '' }}{{ index.change }} ({{ index.changePercent }})
              </div>
            </div>
          </div>
        </div>
        
        <!-- 환율 -->
        <div class="market-card">
          <h3 class="market-card-title">주요 환율</h3>
          <div class="data-list">
            <div class="data-item" v-for="(currency, i) in currencies" :key="i">
              <div class="data-name">{{ currency.name }}</div>
              <div class="data-value">{{ currency.value }}</div>
              <div :class="['data-change', currency.isUp ? 'positive' : 'negative']">
                {{ currency.isUp ? '+' : '' }}{{ currency.change }} ({{ currency.changePercent }})
              </div>
            </div>
          </div>
        </div>
        
        <!-- 상품 가격 -->
        <div class="market-card">
          <h3 class="market-card-title">상품 가격</h3>
          <div class="data-list">
            <div class="data-item" v-for="(commodity, i) in commodities" :key="i">
              <div class="data-name">{{ commodity.name }}</div>
              <div class="data-value">{{ commodity.value }}</div>
              <div :class="['data-change', commodity.isUp ? 'positive' : 'negative']">
                {{ commodity.isUp ? '+' : '' }}{{ commodity.change }} ({{ commodity.changePercent }})
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="view-more-container">
        <button class="view-more-btn" @click="navigateTo('/commodities')">시장 동향 더보기</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

// 주요 지수 데이터
const marketIndices = ref([
  {
    name: '코스피',
    value: '2,674.25',
    change: '12.87',
    changePercent: '0.48%',
    isUp: true
  },
  {
    name: '코스닥',
    value: '842.18',
    change: '-5.47',
    changePercent: '-0.65%',
    isUp: false
  },
  {
    name: '다우 존스',
    value: '38,676.21',
    change: '35.82',
    changePercent: '0.09%',
    isUp: true
  },
  {
    name: '나스닥',
    value: '16,735.02',
    change: '-124.21',
    changePercent: '-0.74%',
    isUp: false
  }
]);

// 환율 데이터 (실시간으로 업데이트됨)
const currencies = ref([
  {
    name: 'USD/KRW',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: true
  },
  {
    name: 'EUR/KRW',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: false
  },
  {
    name: 'JPY/KRW',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: true
  },
  {
    name: 'CNY/KRW',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: false
  }
]);

// 상품 가격 데이터 (실시간으로 업데이트됨)
const commodities = ref([
  {
    name: '금(USD/oz)',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: true
  },
  {
    name: '은(USD/oz)',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: false
  },
  {
    name: 'WTI(USD/배럴)',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: true
  },
  {
    name: '천연가스(USD/MMBtu)',
    value: '0.00',
    change: '0.00',
    changePercent: '0.00%',
    isUp: false
  }
]);

// 실시간 환율 데이터 가져오기
const fetchExchangeRates = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/exchange-rates');
    if (response.data.success) {
      const data = response.data.data;
      
      // 환율 데이터 업데이트
      currencies.value = [
        {
          name: 'USD/KRW',
          value: parseFloat(data.USD.rate).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.USD.change_amount,
          changePercent: `${data.USD.change >= 0 ? '+' : ''}${data.USD.change.toFixed(2)}%`,
          isUp: data.USD.change >= 0
        },
        {
          name: 'EUR/KRW',
          value: parseFloat(data.EUR.rate).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.EUR.change_amount,
          changePercent: `${data.EUR.change >= 0 ? '+' : ''}${data.EUR.change.toFixed(2)}%`,
          isUp: data.EUR.change >= 0
        },
        {
          name: 'JPY/KRW',
          value: parseFloat(data.JPY.rate).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.JPY.change_amount,
          changePercent: `${data.JPY.change >= 0 ? '+' : ''}${data.JPY.change.toFixed(2)}%`,
          isUp: data.JPY.change >= 0
        },
        {
          name: 'CNY/KRW',
          value: parseFloat(data.CNY.rate).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.CNY.change_amount,
          changePercent: `${data.CNY.change >= 0 ? '+' : ''}${data.CNY.change.toFixed(2)}%`,
          isUp: data.CNY.change >= 0
        }
      ];
      
      console.log('MarketOverview - 실시간 환율 데이터 업데이트 완료:', data);
    }
  } catch (error) {
    console.error('MarketOverview - 환율 데이터 가져오기 실패:', error);
    // 기본값으로 복원
    currencies.value = [
      {
        name: 'USD/KRW',
        value: '1,338.50',
        change: '3.30',
        changePercent: '0.25%',
        isUp: true
      },
      {
        name: 'EUR/KRW',
        value: '1,456.20',
        change: '-2.10',
        changePercent: '-0.15%',
        isUp: false
      },
      {
        name: 'JPY/KRW',
        value: '8.75',
        change: '0.09',
        changePercent: '1.04%',
        isUp: true
      },
      {
        name: 'CNY/KRW',
        value: '184.60',
        change: '-0.55',
        changePercent: '-0.30%',
        isUp: false
      }
    ];
  }
};

// 실시간 상품 가격 데이터 가져오기
const fetchCommoditiesData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/commodities');
    if (response.data.success) {
      const data = response.data.data;
      
      // 상품 가격 데이터 업데이트
      commodities.value = [
        {
          name: '금(USD/oz)',
          value: parseFloat(data.gold.price).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.gold.change_amount,
          changePercent: `${data.gold.change >= 0 ? '+' : ''}${data.gold.change.toFixed(2)}%`,
          isUp: data.gold.change >= 0
        },
        {
          name: '은(USD/oz)',
          value: parseFloat(data.silver.price).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.silver.change_amount,
          changePercent: `${data.silver.change >= 0 ? '+' : ''}${data.silver.change.toFixed(2)}%`,
          isUp: data.silver.change >= 0
        },
        {
          name: 'WTI(USD/배럴)',
          value: parseFloat(data.crude_oil.price).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.crude_oil.change_amount,
          changePercent: `${data.crude_oil.change >= 0 ? '+' : ''}${data.crude_oil.change.toFixed(2)}%`,
          isUp: data.crude_oil.change >= 0
        },
        {
          name: '천연가스(USD/MMBtu)',
          value: parseFloat(data.natural_gas.price).toLocaleString('ko-KR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }),
          change: data.natural_gas.change_amount,
          changePercent: `${data.natural_gas.change >= 0 ? '+' : ''}${data.natural_gas.change.toFixed(2)}%`,
          isUp: data.natural_gas.change >= 0
        }
      ];
      
      console.log('MarketOverview - 실시간 상품 가격 데이터 업데이트 완료:', data);
    }
  } catch (error) {
    console.error('MarketOverview - 상품 가격 데이터 가져오기 실패:', error);
    // 기본값으로 복원
    commodities.value = [
      {
        name: '금(USD/oz)',
        value: '2,345.60',
        change: '17.50',
        changePercent: '0.75%',
        isUp: true
      },
      {
        name: '은(USD/oz)',
        value: '28.40',
        change: '-0.09',
        changePercent: '-0.32%',
        isUp: false
      },
      {
        name: 'WTI(USD/배럴)',
        value: '76.82',
        change: '1.25',
        changePercent: '1.65%',
        isUp: true
      },
      {
        name: '천연가스(USD/MMBtu)',
        value: '2.48',
        change: '-0.05',
        changePercent: '-1.98%',
        isUp: false
      }
    ];
  }
};

// 컴포넌트 마운트 시 실시간 데이터 가져오기 및 자동 갱신 설정
onMounted(async () => {
  // 초기 데이터 로드
  await fetchExchangeRates();
  await fetchCommoditiesData();
  
  // 30초마다 데이터 업데이트
  setInterval(async () => {
    await fetchExchangeRates();
    await fetchCommoditiesData();
  }, 30000);
});

// 페이지 이동 함수
const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.market-overview {
  padding: 5rem 0;
  background-color: #ffffff;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 1rem;
  position: relative;
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

.section-desc {
  font-size: 1.1rem;
  color: #666;
  text-align: center;
  margin-bottom: 3rem;
}

.market-data-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.market-card {
  background: #f9fafd;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.market-card-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
  position: relative;
}

.market-card-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 50px;
  height: 2px;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  border-radius: 2px;
}

.data-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.data-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  align-items: center;
  padding: 0.8rem 0;
  border-bottom: 1px solid #eee;
}

.data-item:last-child {
  border-bottom: none;
}

.data-name {
  font-weight: 500;
  color: #555;
}

.data-value {
  font-weight: 700;
  color: #333;
  text-align: center;
}

.data-change {
  font-weight: 600;
  text-align: right;
}

.positive {
  color: #FF5252;
}

.negative {
  color: #4CAF50;
}

.view-more-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.view-more-btn {
  padding: 0.8rem 2.5rem;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
}

/* 반응형 스타일 */
@media (max-width: 992px) {
  .market-data-container {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .market-data-container {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .section-desc {
    font-size: 1rem;
  }
  
  .market-card {
    padding: 1.2rem;
  }
}
</style>
