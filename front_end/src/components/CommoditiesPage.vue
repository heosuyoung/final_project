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
          <option value="gold">금 (Gold)</option>
          <option value="silver">은 (Silver)</option>
          <option value="copper">구리 (Copper)</option>
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
          <option value="kospi">코스피 (KOSPI)</option>
          <option value="kosdaq">코스닥 (KOSDAQ)</option>
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

export default {
  name: 'CommoditiesPage',
  components: {
    CommodityLineChart
  },  data() {
    return {
      selectedCurrency: 'USD',
      selectedCommodity: 'gold',
      selectedIndex: 'kospi',
      commodityLabels: {
        gold: '금(Gold)',
        silver: '은(Silver)',
        copper: '구리(Copper)'
      },
      indexLabels: {
        kospi: '코스피(KOSPI)',
        kosdaq: '코스닥(KOSDAQ)'
      },
      currencyData: {
        USD: { rate: '1,338.50', change: 0.25 },
        EUR: { rate: '1,456.20', change: -0.15 },
        JPY: { rate: '8.75', change: 0.10 },
        CNY: { rate: '184.60', change: -0.30 },
        GBP: { rate: '1,715.40', change: 0.20 },
        AUD: { rate: '887.30', change: -0.12 },
        CAD: { rate: '985.45', change: 0.18 },
        HKD: { rate: '171.25', change: 0.05 },
        SGD: { rate: '995.80', change: -0.08 }
      },
      commoditiesData: {
        gold: { price: '2,345.60', change: 0.75 },
        silver: { price: '28.40', change: -0.32 },
        copper: { price: '4.12', change: 1.25 }
      },
      indexData: {
        kospi: { value: '2,674.25', change: 0.48 },
        kosdaq: { value: '842.18', change: -0.65 }
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
    updateCurrencyData() {
      // 실제 API 연동 시 여기서 선택된 통화에 대한 데이터를 가져오는 로직을 구현합니다.
      // 지금은 이미 모든 통화의 데이터가 로컬에 있으므로 별도의 작업이 필요하지 않습니다.
      console.log(`통화가 ${this.selectedCurrency}로 변경되었습니다.`);
      
      // 선택한 통화에 따라 차트 데이터 갱신 (예시 데이터)
      const currencyData = {
        'USD': [1320.5, 1328.7, 1332.4, 1341.2, 1338.5, 1335.9],
        'EUR': [1435.7, 1442.3, 1450.8, 1454.2, 1456.2, 1460.5],
        'JPY': [8.45, 8.52, 8.65, 8.72, 8.75, 8.80],
        'CNY': [182.3, 183.1, 183.8, 184.2, 184.6, 185.1],
        'GBP': [1690.2, 1698.5, 1705.7, 1710.3, 1715.4, 1720.2],
        'AUD': [880.4, 883.2, 885.6, 889.1, 887.3, 886.5],
        'CAD': [975.2, 978.6, 981.3, 983.7, 985.5, 987.2],
        'HKD': [170.1, 170.5, 170.8, 171.0, 171.3, 171.6],
        'SGD': [990.3, 992.5, 994.2, 995.4, 995.8, 996.5]
      };
      
      this.currencyChartData = {
        ...this.currencyChartData,
        datasets: [{
          ...this.currencyChartData.datasets[0],
          label: `${this.selectedCurrency}/KRW`,
          data: currencyData[this.selectedCurrency]
        }]
      };
    },
    
    updateCommodityData() {
      console.log(`귀금속이 ${this.selectedCommodity}로 변경되었습니다.`);
      
      // 선택한 귀금속에 따라 차트 데이터 갱신 (예시 데이터)
      const commodityData = {
        'gold': {
          label: '금(USD)',
          backgroundColor: 'rgba(255, 206, 86, 0.2)',
          borderColor: 'rgb(255, 206, 86)',
          data: [2235.4, 2267.8, 2310.5, 2325.3, 2345.6, 2355.8]
        },
        'silver': {
          label: '은(USD)',
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgb(153, 102, 255)',
          data: [27.1, 27.5, 28.2, 28.6, 28.4, 28.3]
        },
        'copper': {
          label: '구리(USD)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgb(255, 99, 132)',
          data: [3.85, 3.92, 4.05, 4.18, 4.12, 4.08]
        }
      };
      
      this.commoditiesChartData = {
        ...this.commoditiesChartData,
        datasets: [{
          ...commodityData[this.selectedCommodity]
        }]
      };
    },
    
    updateIndexData() {
      console.log(`지수가 ${this.selectedIndex}로 변경되었습니다.`);
      
      // 선택한 지수에 따라 차트 데이터 갱신 (예시 데이터)
      const indexData = {
        'kospi': {
          label: '코스피',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgb(75, 192, 192)',
          data: [2620.4, 2642.7, 2655.8, 2668.5, 2674.3, 2685.2]
        },
        'kosdaq': {
          label: '코스닥',
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgb(255, 159, 64)',
          data: [832.6, 835.4, 839.7, 845.2, 842.2, 847.8]
        }
      };
      
      this.indexChartData = {
        ...this.indexChartData,
        datasets: [{
          ...indexData[this.selectedIndex]
        }]
      };
    }
  },  mounted() {
    // 페이지 로드 시 선택된 항목에 따른 차트 데이터 설정
    this.updateCurrencyData();
    this.updateCommodityData();
    this.updateIndexData();
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
