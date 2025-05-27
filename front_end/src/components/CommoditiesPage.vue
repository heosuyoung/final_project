<template>
  <div class="commodities-container">
    <div class="sidebar">
      <h2>현물가격 & 환율 정보</h2>
      
      <div class="category">
        <h3>환율</h3>
        <select v-model="selectedCurrency" @change="updateCurrencyData" class="currency-select">
          <option value="USD">미국 달러 (USD)</option>
          <option value="EUR">유로 (EUR)</option>
          <option value="JPY">일본 엔 (JPY)</option>
          <option value="CNY">중국 위안 (CNY)</option>
          <option value="GBP">영국 파운드 (GBP)</option>
          <option value="AUD">호주 달러 (AUD)</option>
          <option value="CAD">캐나다 달러 (CAD)</option>
          <option value="HKD">홍콩 달러 (HKD)</option>
          <option value="SGD">싱가포르 달러 (SGD)</option>
        </select>
        
        <div class="data-item">
          <p>{{ selectedCurrency }} / KRW: {{ currencyData[selectedCurrency].rate }}</p>
          <p>변동: <span :class="currencyData[selectedCurrency].change >= 0 ? 'positive' : 'negative'">
            {{ currencyData[selectedCurrency].change >= 0 ? '+' : '' }}{{ currencyData[selectedCurrency].change }}%
          </span></p>
        </div>
      </div>
        <div class="category">
        <h3>귀금속</h3>
        <select v-model="selectedCommodity" @change="updateCommodityData" class="currency-select">
          <option value="Gold">금 (Gold)</option>
          <option value="Silver">은 (Silver)</option>
          <option value="Copper">구리 (Copper)</option>
          <option value="Crude Oil">원유 (Crude Oil)</option>
          <option value="Natural Gas">천연가스 (Natural Gas)</option>
        </select>
        
        <div class="data-item">
          <p>{{ commodityLabels[selectedCommodity] }}: {{ commoditiesData[selectedCommodity].price }} USD</p>
          <p>변동: <span :class="commoditiesData[selectedCommodity].change >= 0 ? 'positive' : 'negative'">
            {{ commoditiesData[selectedCommodity].change >= 0 ? '+' : '' }}{{ commoditiesData[selectedCommodity].change }}%
          </span></p>
        </div>
      </div>
        <div class="category">
        <h3>지수</h3>
        <select v-model="selectedIndex" @change="updateIndexData" class="currency-select">
          <option value="KOSPI">코스피 (KOSPI)</option>
          <option value="KOSDAQ">코스닥 (KOSDAQ)</option>
        </select>
        
        <div class="data-item">
          <p>{{ indexLabels[selectedIndex] }}: {{ indexData[selectedIndex].value }}</p>
          <p>변동: <span :class="indexData[selectedIndex].change >= 0 ? 'positive' : 'negative'">
            {{ indexData[selectedIndex].change >= 0 ? '+' : '' }}{{ indexData[selectedIndex].change }}%
          </span></p>
        </div>
      </div>
    </div>
      <div class="main-content">
      <h1>현물가격 및 환율 정보</h1>
      <p>좌측 사이드바에서 각국의 환율, 귀금속 가격, 주식 지수 정보를 확인하실 수 있습니다.</p>
      
      <div class="charts-section">
        <div class="chart-wrapper">
          <h2>{{ selectedCurrency }}/KRW 환율 추이</h2>
          <CommodityLineChart :chartData="currencyChartData" :chartOptions="currencyChartOptions" />
        </div>
          <div class="chart-wrapper">
          <h2>{{ commodityLabels[selectedCommodity] }} 가격 추이</h2>
          <CommodityLineChart :chartData="commoditiesChartData" :chartOptions="commoditiesChartOptions" />
        </div>
        
        <div class="chart-wrapper">
          <h2>{{ indexLabels[selectedIndex] }} 추이</h2>
          <CommodityLineChart :chartData="indexChartData" :chartOptions="indexChartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CommodityLineChart from './CommodityLineChart.vue';
import axios from 'axios';

export default {
  name: 'CommoditiesPage',
  components: {
    CommodityLineChart
  },
  data() {
    return {
      selectedCurrency: 'USD',
      selectedCommodity: 'Gold',  // 대문자로 수정
      selectedIndex: 'KOSPI',     // 대문자로 수정
      loading: false,
      lastUpdated: null,
      commodityLabels: {
        Gold: '금(Gold)',
        Silver: '은(Silver)',
        Copper: '구리(Copper)',
        'Crude Oil': 'WTI 원유',
        'Natural Gas': '천연가스'
      },
      indexLabels: {
        KOSPI: '코스피(KOSPI)',
        KOSDAQ: '코스닥(KOSDAQ)'
      },
      // 실시간 데이터로 업데이트될 환율 정보
      currencyData: {
        USD: { rate: '0.00', change: 0 },
        EUR: { rate: '0.00', change: 0 },
        JPY: { rate: '0.00', change: 0 },
        CNY: { rate: '0.00', change: 0 },
        GBP: { rate: '0.00', change: 0 },
        AUD: { rate: '0.00', change: 0 },
        CAD: { rate: '0.00', change: 0 },
        HKD: { rate: '0.00', change: 0 },
        SGD: { rate: '0.00', change: 0 }
      },
      // 실시간 데이터로 업데이트될 상품 가격 정보
      commoditiesData: {
        Gold: { price: '0.00', change: 0 },
        Silver: { price: '0.00', change: 0 },
        Copper: { price: '0.00', change: 0 },
        'Crude Oil': { price: '0.00', change: 0 },
        'Natural Gas': { price: '0.00', change: 0 }
      },
      indexData: {
        KOSPI: { value: '0.00', change: 0 },
        KOSDAQ: { value: '0.00', change: 0 }
      },
      // 차트 데이터 및 옵션
      currencyChartData: {
        labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
        datasets: [
          {
            label: 'USD/KRW',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            data: [1320.5, 1328.7, 1332.4, 1341.2, 1338.5, 1335.9],
            tension: 0.4
          }
        ]
      },
      currencyChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
          }
        }
      },      commoditiesChartData: {
        labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
        datasets: [
          {
            label: '금(USD)',
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            borderColor: 'rgb(255, 206, 86)',
            data: [2235.4, 2267.8, 2310.5, 2325.3, 2345.6, 2355.8],
            tension: 0.4
          }
        ]
      },
      commoditiesChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
          }
        }
      },      indexChartData: {
        labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
        datasets: [
          {
            label: '코스피',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgb(75, 192, 192)',
            data: [2620.4, 2642.7, 2655.8, 2668.5, 2674.3, 2685.2],
            tension: 0.4
          }
        ]
      },
      indexChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
          }
        }
      }
    };
  },  methods: {
    // 실시간 환율 데이터 가져오기
    async fetchExchangeRates() {
      this.loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:5000/exchange-rates');
        if (response.data.success) {
          Object.keys(response.data.data).forEach(currency => {
            if (this.currencyData[currency]) {
              const data = response.data.data[currency];
              this.currencyData[currency] = {
                rate: parseFloat(data.rate).toLocaleString('ko-KR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
                }),
                change: data.change
              };
            }
          });
          this.lastUpdated = response.data.last_updated;
          console.log('실시간 환율 데이터 업데이트 완료:', response.data.data);
        }
      } catch (error) {
        console.error('환율 데이터 가져오기 실패:', error);
      } finally {
        this.loading = false;
      }
    },
    
    // 실시간 상품 가격 데이터 가져오기
    async fetchCommoditiesData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/commodities');
        if (response.data.success) {
          // 실시간 데이터로 상품 가격 정보와 지수 정보 업데이트
          Object.keys(response.data.data).forEach(item => {
            const data = response.data.data[item];
            
            // 지수 데이터 처리 (KOSPI, KOSDAQ)
            if (item === 'KOSPI' || item === 'KOSDAQ') {
              if (this.indexData[item]) {
                this.indexData[item] = {
                  value: parseFloat(data.price).toLocaleString('ko-KR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  }),
                  change: data.change
                };
              }
            } 
            // 상품 데이터 처리
            else if (this.commoditiesData[item]) {
              this.commoditiesData[item] = {
                price: parseFloat(data.price).toLocaleString('ko-KR', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
                }),
                change: data.change
              };
            }
          });
          console.log('실시간 데이터 업데이트 완료:', response.data.data);
        }
      } catch (error) {
        console.error('데이터 가져오기 실패:', error);
      }
    },    // 선택된 통화에 따른 차트 업데이트
    async updateCurrencyData() {
      this.fetchExchangeRates();
      await this.fetchCurrencyHistoryData();
    },
    
    // 선택된 상품에 따른 차트 업데이트
    async updateCommodityData() {
      this.fetchCommoditiesData();
      await this.fetchCommodityHistoryData();
    },
    
    // 선택된 지수에 따른 차트 업데이트
    async updateIndexData() {
      this.fetchCommoditiesData();
      await this.fetchIndexHistoryData();
    },
    
    // 환율 히스토리 데이터 가져오기
    async fetchCurrencyHistoryData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/currency-history');
        if (response.data.success) {
          const historyData = response.data.data[this.selectedCurrency];
          if (historyData && historyData.length > 0) {
            // 최근 30일 데이터이므로 가독성을 위해 7일 간격으로 표시
            const labels = [];
            const data = [];
            
            // 데이터가 시간순으로 정렬되어 있는지 확인하고 필요하면 정렬
            historyData.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            // 가장 최근 7일 데이터만 사용
            const recentData = historyData.slice(-7);
            
            recentData.forEach(item => {
              // 날짜를 더 간단한 형식으로 변환 (예: 05-21)
              const date = new Date(item.date);
              const formattedDate = `${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
              labels.push(formattedDate);
              data.push(item.price);
            });
            
            // 차트 데이터 업데이트
            this.currencyChartData = {
              labels: labels,
              datasets: [
                {
                  label: `${this.selectedCurrency}/KRW`,
                  backgroundColor: 'rgba(54, 162, 235, 0.2)',
                  borderColor: 'rgb(54, 162, 235)',
                  data: data,
                  tension: 0.4
                }
              ]
            };
          }
        }
      } catch (error) {
        console.error('환율 히스토리 데이터 가져오기 실패:', error);
      }
    },
    
    // 상품 히스토리 데이터 가져오기
    async fetchCommodityHistoryData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/commodity-history');
        if (response.data.success) {
          const historyData = response.data.data[this.selectedCommodity];
          if (historyData && historyData.length > 0) {
            const labels = [];
            const data = [];
            
            // 데이터가 시간순으로 정렬되어 있는지 확인하고 필요하면 정렬
            historyData.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            // 가장 최근 7일 데이터만 사용
            const recentData = historyData.slice(-7);
            
            recentData.forEach(item => {
              // 날짜를 더 간단한 형식으로 변환 (예: 05-21)
              const date = new Date(item.date);
              const formattedDate = `${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
              labels.push(formattedDate);
              data.push(item.price);
            });
            
            // 차트 데이터 업데이트
            this.commoditiesChartData = {
              labels: labels,
              datasets: [
                {
                  label: `${this.commodityLabels[this.selectedCommodity]}`,
                  backgroundColor: 'rgba(255, 206, 86, 0.2)',
                  borderColor: 'rgb(255, 206, 86)',
                  data: data,
                  tension: 0.4
                }
              ]
            };
          }
        }
      } catch (error) {
        console.error('상품 히스토리 데이터 가져오기 실패:', error);
      }
    },
    
    // 지수 히스토리 데이터 가져오기
    async fetchIndexHistoryData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/index-history');
        if (response.data.success) {
          const historyData = response.data.data[this.selectedIndex];
          if (historyData && historyData.length > 0) {
            const labels = [];
            const data = [];
            
            // 데이터가 시간순으로 정렬되어 있는지 확인하고 필요하면 정렬
            historyData.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            // 가장 최근 7일 데이터만 사용
            const recentData = historyData.slice(-7);
            
            recentData.forEach(item => {
              // 날짜를 더 간단한 형식으로 변환 (예: 05-21)
              const date = new Date(item.date);
              const formattedDate = `${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
              labels.push(formattedDate);
              data.push(item.price);
            });
            
            // 차트 데이터 업데이트
            this.indexChartData = {
              labels: labels,
              datasets: [
                {
                  label: `${this.indexLabels[this.selectedIndex]}`,
                  backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  borderColor: 'rgb(75, 192, 192)',
                  data: data,
                  tension: 0.4
                }
              ]
            };
          }
        }
      } catch (error) {
        console.error('지수 히스토리 데이터 가져오기 실패:', error);
      }
    }
  },  async mounted() {
    // 페이지 로드 시 실시간 데이터 가져오기
    await this.fetchExchangeRates();
    await this.fetchCommoditiesData();
    
    // 히스토리 데이터 가져오기
    await this.fetchCurrencyHistoryData();
    await this.fetchCommodityHistoryData();
    await this.fetchIndexHistoryData();
    
    // 30초마다 실시간 데이터 업데이트
    setInterval(async () => {
      await this.fetchExchangeRates();
      await this.fetchCommoditiesData();
    }, 30000);
    
    // 5분마다 히스토리 차트 데이터 업데이트
    setInterval(async () => {
      await this.fetchCurrencyHistoryData();
      await this.fetchCommodityHistoryData();
      await this.fetchIndexHistoryData();
    }, 300000); // 5분 = 300,000밀리초
  }
};
</script>

<style>
.commodities-container {
  display: flex;
  height: 100%;
  padding-top: 90px; /* 헤더 높이만큼 패딩 추가 */
}

.sidebar {
  width: 300px;
  background-color: #f5f5f5;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  height: calc(100vh - 90px); /* 헤더 높이를 제외한 높이 */
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.category {
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 15px;
}

.category h3 {
  margin-bottom: 10px;
  color: #333;
  font-weight: 600;
}

.data-item {
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.data-item p {
  margin: 5px 0;
  font-size: 14px;
}

.positive {
  color: #2e7d32;
  font-weight: bold;
}

.negative {
  color: #c62828;
  font-weight: bold;
}

.currency-select {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: white;
}

.sidebar h2 {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #ddd;
  font-size: 18px;
  color: #333;
}

.main-content h1 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.main-content p {
  color: #666;
  line-height: 1.6;
}

.charts-section {
  margin-top: 30px;
}

.chart-wrapper {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.chart-wrapper h2 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #333;
  font-weight: 600;
}
</style>
