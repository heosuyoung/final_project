<template>
  <div class="financial-charts">
    <div v-if="!financialData" class="no-data">
      <p>재무 정보를 입력하시면 시각화된 분석 결과를 확인할 수 있습니다.</p>
    </div>
    <div v-else class="charts-container">
      <div class="chart-section">
        <h3>자산 분배</h3>
        <div class="chart-wrapper">
          <canvas ref="assetDistributionChart"></canvas>
        </div>
      </div>
      
      <div class="chart-section">
        <h3>소득 대비 지출</h3>
        <div class="chart-wrapper">
          <canvas ref="incomeExpenseChart"></canvas>
        </div>
      </div>
      
      <div class="chart-section">
        <h3>투자 포트폴리오 분석</h3>
        <div class="chart-wrapper">
          <canvas ref="portfolioChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

export default {
  name: 'FinancialCharts',
  props: {
    financialData: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    // 차트 참조
    const assetDistributionChart = ref(null);
    const incomeExpenseChart = ref(null);
    const portfolioChart = ref(null);
      // 차트 인스턴스
    let assetChart = null;
    let incomeChart = null;
    let portfolioChartInstance = null;
    
    // 차트 초기화 함수
    const initCharts = () => {
      if (!props.financialData) return;
      
      // 차트 데이터 준비
      const assetData = {
        labels: ['예금/적금', '주식/펀드', '부동산'],
        datasets: [{
          data: [
            props.financialData.savings || 0,
            props.financialData.stocks || 0,
            props.financialData.realestate || 0
          ],
          backgroundColor: [
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 99, 132, 0.7)',
            'rgba(75, 192, 192, 0.7)'
          ],
          borderColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1
        }]
      };
      
      const incomeExpenseData = {
        labels: ['소득', '지출', '저축'],
        datasets: [{
          label: '금액 (만원)',
          data: [
            props.financialData.monthlyIncome || 0,
            props.financialData.monthlyExpense || 0,
            props.financialData.monthlyIncome - props.financialData.monthlyExpense || 0
          ],
          backgroundColor: [
            'rgba(75, 192, 192, 0.7)',
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)'
          ],
          borderColor: [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)'
          ],
          borderWidth: 1
        }]
      };
      
      // 투자 성향에 따른 권장 포트폴리오 생성
      let stockPercentage = 0;
      let bondPercentage = 0;
      let cashPercentage = 0;
      
      switch(props.financialData.riskTolerance) {
        case '안정형':
          stockPercentage = 20;
          bondPercentage = 50;
          cashPercentage = 30;
          break;
        case '중립형':
          stockPercentage = 40;
          bondPercentage = 40;
          cashPercentage = 20;
          break;
        case '수익형':
          stockPercentage = 60;
          bondPercentage = 30;
          cashPercentage = 10;
          break;
        case '공격형':
          stockPercentage = 80;
          bondPercentage = 15;
          cashPercentage = 5;
          break;
        default:
          stockPercentage = 40;
          bondPercentage = 40;
          cashPercentage = 20;
      }
      
      const portfolioData = {
        labels: ['주식', '채권', '현금성 자산'],
        datasets: [{
          data: [stockPercentage, bondPercentage, cashPercentage],
          backgroundColor: [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(75, 192, 192, 0.7)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1
        }]
      };
      
      // 차트 생성
      if (assetDistributionChart.value) {
        if (assetChart) assetChart.destroy();
        assetChart = new Chart(assetDistributionChart.value, {
          type: 'pie',
          data: assetData,
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom'
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const label = context.label || '';
                    const value = context.raw || 0;
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((value / total) * 100).toFixed(1);
                    return `${label}: ${value}만원 (${percentage}%)`;
                  }
                }
              }
            }
          }
        });
      }
      
      if (incomeExpenseChart.value) {
        if (incomeChart) incomeChart.destroy();
        incomeChart = new Chart(incomeExpenseChart.value, {
          type: 'bar',
          data: incomeExpenseData,
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            },
            plugins: {
              legend: {
                display: false
              }
            }
          }
        });
      }
        if (portfolioChart.value) {
        if (portfolioChartInstance) portfolioChartInstance.destroy();
        portfolioChartInstance = new Chart(portfolioChart.value, {
          type: 'doughnut',
          data: portfolioData,
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom'
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const label = context.label || '';
                    const value = context.raw || 0;
                    return `${label}: ${value}%`;
                  }
                }
              }
            }
          }
        });
      }
    };
    
    // 차트 업데이트
    const updateCharts = () => {
      if (assetChart && props.financialData) {
        assetChart.data.datasets[0].data = [
          props.financialData.savings || 0,
          props.financialData.stocks || 0,
          props.financialData.realestate || 0
        ];
        assetChart.update();
      }
      
      if (incomeChart && props.financialData) {
        incomeChart.data.datasets[0].data = [
          props.financialData.monthlyIncome || 0,
          props.financialData.monthlyExpense || 0,
          props.financialData.monthlyIncome - props.financialData.monthlyExpense || 0
        ];
        incomeChart.update();
      }
    };
      // 재무 데이터 변경 감시
    watch(() => props.financialData, (newVal) => {
      if (newVal) {
        if (!assetChart || !incomeChart || !portfolioChartInstance) {
          initCharts();
        } else {
          updateCharts();
        }
      }
    }, { deep: true });
    
    // 컴포넌트 마운트 시 초기화
    onMounted(() => {
      if (props.financialData) {
        initCharts();
      }
    });
    
    return {
      assetDistributionChart,
      incomeExpenseChart,
      portfolioChart
    };
  }
};
</script>

<style scoped>
.financial-charts {
  width: 100%;
}

.no-data {
  text-align: center;
  padding: 3rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.chart-section {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.chart-section h3 {
  font-size: 1rem;
  text-align: center;
  margin-bottom: 1rem;
  color: #495057;
}

.chart-wrapper {
  height: 250px;
  position: relative;
}

@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>
