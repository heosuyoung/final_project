<template>
  <div class="charts-container">
    <div v-if="financialData">
      <h3>재무 데이터 분석</h3>
      <div class="charts-grid">
        <div class="chart-box">
          <h4>자산 구성</h4>
          <div class="chart-wrapper">
            <canvas ref="assetsChart"></canvas>
          </div>
        </div>
        
        <div class="chart-box">
          <h4>소득 대비 지출</h4>
          <div class="chart-wrapper">
            <canvas ref="incomeExpenseChart"></canvas>
          </div>
        </div>
        
        <div class="chart-box">
          <h4>순자산 분석</h4>
          <div class="chart-wrapper">
            <canvas ref="netWorthChart"></canvas>
          </div>
        </div>
        
        <div class="chart-box">
          <h4>목표 달성 예상</h4>
          <div class="chart-wrapper">
            <canvas ref="goalProjectionChart"></canvas>
          </div>
        </div>
      </div>
      
      <div class="summary-stats">
        <div class="stat-card">
          <div class="stat-title">순자산</div>
          <div class="stat-value">{{ formatCurrency(calculateNetWorth()) }}</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-title">월 저축 가능액</div>
          <div class="stat-value">{{ formatCurrency(calculateMonthlySavings()) }}</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-title">부채 비율</div>
          <div class="stat-value">{{ calculateDebtRatio() }}%</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-title">투자 비중</div>
          <div class="stat-value">{{ calculateInvestmentRatio() }}%</div>
        </div>
      </div>
      
      <div class="recommendations">
        <h4>재무 분석 결과</h4>
        <div class="recommendation-list">
          <div class="recommendation-item" v-for="(item, index) in generateRecommendations()" :key="index">
            <div class="recommendation-icon">{{ item.icon }}</div>
            <div class="recommendation-content">
              <h5>{{ item.title }}</h5>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="no-data">
      <div class="no-data-message">
        <div class="no-data-icon">📊</div>
        <h4>재무 데이터가 필요합니다</h4>
        <p>재무 정보를 입력하시면 상세한 분석과 시각화를 제공해드립니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  financialData: {
    type: Object,
    default: null
  }
});

// 차트 참조
const assetsChart = ref(null);
const incomeExpenseChart = ref(null);
const netWorthChart = ref(null);
const goalProjectionChart = ref(null);

// 차트 인스턴스 저장용
let assetsChartInstance = null;
let incomeExpenseChartInstance = null;
let netWorthChartInstance = null;
let goalProjectionChartInstance = null;

// 금액 포맷팅 함수
const formatCurrency = (value) => {
  return value ? `${value.toLocaleString()}만원` : '0만원';
};

// 순자산 계산
const calculateNetWorth = () => {
  if (!props.financialData) return 0;
  
  const assets = (props.financialData.savings || 0) + 
                 (props.financialData.stocks || 0) + 
                 (props.financialData.realestate || 0);
  
  const debts = (props.financialData.loans || 0) + 
                (props.financialData.creditCardDebt || 0);
  
  return assets - debts;
};

// 월 저축 가능액 계산
const calculateMonthlySavings = () => {
  if (!props.financialData) return 0;
  
  const income = props.financialData.monthlyIncome || 0;
  const expense = props.financialData.monthlyExpense || 0;
  
  return Math.max(0, income - expense);
};

// 부채 비율 계산
const calculateDebtRatio = () => {
  if (!props.financialData) return 0;
  
  const assets = (props.financialData.savings || 0) + 
                 (props.financialData.stocks || 0) + 
                 (props.financialData.realestate || 0);
  
  const debts = (props.financialData.loans || 0) + 
                (props.financialData.creditCardDebt || 0);
  
  if (assets === 0) return 0;
  
  return Math.round((debts / assets) * 100);
};

// 투자 비중 계산
const calculateInvestmentRatio = () => {
  if (!props.financialData) return 0;
  
  const assets = (props.financialData.savings || 0) + 
                 (props.financialData.stocks || 0) + 
                 (props.financialData.realestate || 0);
  
  const investments = (props.financialData.stocks || 0);
  
  if (assets === 0) return 0;
  
  return Math.round((investments / assets) * 100);
};

// 재무 추천 생성
const generateRecommendations = () => {
  if (!props.financialData) return [];
  
  const recommendations = [];
  const netWorth = calculateNetWorth();
  const debtRatio = calculateDebtRatio();
  const savings = calculateMonthlySavings();
  const income = props.financialData.monthlyIncome || 0;
  const financialGoal = props.financialData.financialGoal || '';
  
  // 저축 관련 추천
  if (savings < income * 0.2) {
    recommendations.push({
      icon: '💰',
      title: '저축률 증가 필요',
      description: `현재 저축 가능액(${formatCurrency(savings)})은 소득의 ${Math.round((savings/income)*100)}%입니다. 재정 건전성을 위해 최소 20% 이상을 목표로 하세요.`
    });
  } else {
    recommendations.push({
      icon: '✅',
      title: '훌륭한 저축률',
      description: `소득의 ${Math.round((savings/income)*100)}%를 저축하고 있어 안정적인 재무 상태입니다.`
    });
  }
  
  // 부채 관련 추천
  if (debtRatio > 40) {
    recommendations.push({
      icon: '⚠️',
      title: '부채 비율 관리 필요',
      description: `부채 비율이 ${debtRatio}%로 다소 높습니다. 고금리 부채부터 상환하는 전략을 고려해보세요.`
    });
  } else if (debtRatio > 0) {
    recommendations.push({
      icon: '📝',
      title: '건전한 부채 관리',
      description: `부채 비율이 ${debtRatio}%로 관리 가능한 수준입니다. 꾸준한 상환을 유지하세요.`
    });
  }
  
  // 자산 배분 추천
  const investmentRatio = calculateInvestmentRatio();
  if (financialGoal.includes('투자 수익률 향상')) {
    recommendations.push({
      icon: '📈',
      title: '포트폴리오 다변화',
      description: `현재 투자 비중이 ${investmentRatio}%입니다. 해외 지수 ETF, 채권, 리츠 등을 통해 분산투자를 고려해보세요.`
    });
  }
  
  // 금융 목표별 맞춤 추천
  if (financialGoal.includes('주택 구입')) {
    recommendations.push({
      icon: '🏠',
      title: '주택 구입 계획',
      description: '주택 구입을 위해 일반 저축보다는 주택청약종합저축이나 주택 관련 펀드를 활용해보세요.'
    });
  } else if (financialGoal.includes('은퇴 준비')) {
    recommendations.push({
      icon: '🌴',
      title: '은퇴 준비 전략',
      description: 'IRP, 연금저축펀드 등 세제혜택이 있는 은퇴 관련 상품에 투자하는 것이 효과적입니다.'
    });
  }
  
  return recommendations;
};

// 자산 구성 차트 생성
const createAssetsChart = () => {
  if (!props.financialData) return;
  
  const ctx = assetsChart.value.getContext('2d');
  
  // 차트 인스턴스가 이미 있으면 파괴
  if (assetsChartInstance) {
    assetsChartInstance.destroy();
  }
  
  const savings = props.financialData.savings || 0;
  const stocks = props.financialData.stocks || 0;
  const realestate = props.financialData.realestate || 0;
  
  assetsChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['예금/적금', '주식/펀드', '부동산'],
      datasets: [{
        data: [savings, stocks, realestate],
        backgroundColor: [
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 99, 132, 0.7)',
          'rgba(255, 206, 86, 0.7)'
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
};

// 소득 대비 지출 차트
const createIncomeExpenseChart = () => {
  if (!props.financialData) return;
  
  const ctx = incomeExpenseChart.value.getContext('2d');
  
  // 차트 인스턴스가 이미 있으면 파괴
  if (incomeExpenseChartInstance) {
    incomeExpenseChartInstance.destroy();
  }
  
  const income = props.financialData.monthlyIncome || 0;
  const expense = props.financialData.monthlyExpense || 0;
  const savings = Math.max(0, income - expense);
  
  incomeExpenseChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['월별 재정'],
      datasets: [
        {
          label: '수입',
          data: [income],
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: '지출',
          data: [expense],
          backgroundColor: 'rgba(255, 99, 132, 0.7)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        },
        {
          label: '저축',
          data: [savings],
          backgroundColor: 'rgba(54, 162, 235, 0.7)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '만원'
          }
        }
      },
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
};

// 순자산 차트
const createNetWorthChart = () => {
  if (!props.financialData) return;
  
  const ctx = netWorthChart.value.getContext('2d');
  
  // 차트 인스턴스가 이미 있으면 파괴
  if (netWorthChartInstance) {
    netWorthChartInstance.destroy();
  }
  
  const assets = (props.financialData.savings || 0) + 
                 (props.financialData.stocks || 0) + 
                 (props.financialData.realestate || 0);
  
  const debts = (props.financialData.loans || 0) + 
                (props.financialData.creditCardDebt || 0);
  
  const netWorth = assets - debts;
  
  netWorthChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['자산 분석'],
      datasets: [
        {
          label: '총 자산',
          data: [assets],
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: '총 부채',
          data: [debts],
          backgroundColor: 'rgba(255, 99, 132, 0.7)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        },
        {
          label: '순자산',
          data: [netWorth],
          backgroundColor: 'rgba(153, 102, 255, 0.7)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '만원'
          }
        }
      },
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
};

// 목표 달성 예상 차트
const createGoalProjectionChart = () => {
  if (!props.financialData) return;
  
  const ctx = goalProjectionChart.value.getContext('2d');
  
  // 차트 인스턴스가 이미 있으면 파괴
  if (goalProjectionChartInstance) {
    goalProjectionChartInstance.destroy();
  }
  
  // 월 저축액 계산
  const monthlySavings = calculateMonthlySavings();
  const initialAssets = (props.financialData.savings || 0) + (props.financialData.stocks || 0);
  
  // 목표에 따른 예상 수익률 설정
  let annualReturnRate = 0.03; // 기본 3%
  const riskTolerance = props.financialData.riskTolerance || '';
  
  if (riskTolerance.includes('수익형')) {
    annualReturnRate = 0.06;
  } else if (riskTolerance.includes('공격형')) {
    annualReturnRate = 0.08;
  } else if (riskTolerance.includes('중립형')) {
    annualReturnRate = 0.05;
  }
  
  // 투자 기간에 따른 차트 기간 설정
  const timeframe = props.financialData.investmentTimeframe || '';
  let years = 5;
  
  if (timeframe.includes('단기')) {
    years = 1;
  } else if (timeframe.includes('중기')) {
    years = 3;
  } else if (timeframe.includes('장기')) {
    years = 7;
  } else if (timeframe.includes('초장기')) {
    years = 15;
  }
  
  // 차트 데이터 생성
  const labels = Array.from({ length: years + 1 }, (_, i) => `${i}년`);
  const conservativeData = [];
  const moderateData = [];
  const aggressiveData = [];
  
  let conservativeAmount = initialAssets;
  let moderateAmount = initialAssets;
  let aggressiveAmount = initialAssets;
  
  conservativeData.push(conservativeAmount);
  moderateData.push(moderateAmount);
  aggressiveData.push(aggressiveAmount);
  
  for (let year = 1; year <= years; year++) {
    // 보수적 시나리오 (연 2%)
    conservativeAmount = conservativeAmount * 1.02 + monthlySavings * 12;
    conservativeData.push(Math.round(conservativeAmount));
    
    // 중간 시나리오 (설정된 수익률)
    moderateAmount = moderateAmount * (1 + annualReturnRate) + monthlySavings * 12;
    moderateData.push(Math.round(moderateAmount));
    
    // 낙관적 시나리오 (설정된 수익률 + 2%)
    aggressiveAmount = aggressiveAmount * (1 + annualReturnRate + 0.02) + monthlySavings * 12;
    aggressiveData.push(Math.round(aggressiveAmount));
  }
  
  goalProjectionChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: '보수적 예상',
          data: conservativeData,
          backgroundColor: 'rgba(54, 162, 235, 0.1)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2,
          fill: false,
          tension: 0.1
        },
        {
          label: '기본 예상',
          data: moderateData,
          backgroundColor: 'rgba(75, 192, 192, 0.1)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 2,
          fill: false,
          tension: 0.1
        },
        {
          label: '낙관적 예상',
          data: aggressiveData,
          backgroundColor: 'rgba(153, 102, 255, 0.1)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 2,
          fill: false,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '만원'
          }
        }
      },
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}만원`;
            }
          }
        }
      }
    }
  });
};

// 모든 차트 생성 함수
const createCharts = () => {
  createAssetsChart();
  createIncomeExpenseChart();
  createNetWorthChart();
  createGoalProjectionChart();
};

// 재무 데이터 변경 시 차트 업데이트
watch(() => props.financialData, (newVal) => {
  if (newVal) {
    createCharts();
  }
}, { deep: true });

// 컴포넌트가 마운트되면 차트 생성
onMounted(() => {
  if (props.financialData) {
    createCharts();
  }
});
</script>

<style scoped>
.charts-container {
  padding: 2rem 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
}

.chart-wrapper {
  height: 250px;
  position: relative;
}

.chart-box h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  text-align: center;
}

.stat-title {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.recommendations {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
}

.recommendations h4 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
}

.recommendation-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.recommendation-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.recommendation-icon {
  font-size: 2rem;
  line-height: 1;
}

.recommendation-content h5 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: #333;
}

.recommendation-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
}

.no-data-message {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-data-message h4 {
  margin: 0 0 0.5rem;
  color: #333;
}

.no-data-message p {
  margin: 0;
  color: #666;
}

@media (max-width: 992px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-stats {
    grid-template-columns: 1fr 1fr;
  }
  
  .recommendation-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style>
