<template>
  <section class="auto-invest-section">
    <div class="overlay-pattern"></div>
    <div class="content-container">
      <div class="section-header">
        <div class="header-badge">자동화</div>
        <h2 class="section-title">소액으로 시작하는 저금통 자동투자</h2>
        <p class="section-desc">티끌 모아 태산! 매일 조금씩 모으는 습관으로 당신의 자산을 키워보세요.</p>
      </div>
      
      <div class="investment-layout">
        <div class="investment-visual">
          <!-- 투자 설정 탭 추가 -->
          <div class="settings-tabs">
            <button 
              :class="['tab-btn', activeTab === 'savings' ? 'active' : '']" 
              @click="activeTab = 'savings'">
              저금 설정
            </button>
            <button 
              :class="['tab-btn', activeTab === 'stocks' ? 'active' : '']" 
              @click="activeTab = 'stocks'">
              관심종목 매수
            </button>
            <button 
              :class="['tab-btn', activeTab === 'status' ? 'active' : '']" 
              @click="activeTab = 'status'">
              투자 현황
            </button>
          </div>
          
          <!-- 저금 설정 탭 내용 -->
          <div v-if="activeTab === 'savings'" class="tab-content">
            <div class="savings-simulator">
              <div class="simulator-header">일일 자동저축 시뮬레이션</div>
              <div class="simulator-content">
                <div class="simulator-input">
                  <span class="input-label">일일 저축액</span>
                  <div class="input-group">
                    <input type="number" v-model="dailySavings" min="1000" step="1000" /> 원
                  </div>
                </div>
                
                <div class="payment-ratio-setting">
                  <div class="setting-label">결제금액 저금 비율</div>
                  <div class="ratio-slider">
                    <input 
                      type="range" 
                      v-model="paymentRatio" 
                      min="1" 
                      max="20" 
                      step="1" 
                      class="slider" 
                    />
                    <div class="ratio-value">{{ paymentRatio }}%</div>
                  </div>
                  <div class="ratio-info">
                    매달 평균 결제금액 <span class="highlight-text">{{ formatCurrency(monthlyPayment) }}</span>의 
                    {{ paymentRatio }}% ({{ formatCurrency(monthlyPayment * paymentRatio / 100) }})가 저금됩니다.
                  </div>
                </div>
                
                <div class="simulator-result">
                  <div class="result-item">
                    <div class="result-label">1년 후</div>
                    <div class="result-value">{{ formatCurrency(calculateSavings(1)) }}</div>
                  </div>
                  <div class="result-item highlight">
                    <div class="result-label">3년 후</div>
                    <div class="result-value">{{ formatCurrency(calculateSavings(3)) }}</div>
                  </div>
                  <div class="result-item">
                    <div class="result-label">5년 후</div>
                    <div class="result-value">{{ formatCurrency(calculateSavings(5)) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 관심종목 매수 설정 탭 내용 -->
          <div v-if="activeTab === 'stocks'" class="tab-content">
            <div class="stocks-setup">
              <div class="setup-header">관심종목 자동 매수 설정</div>
              <div class="setup-content">
                <div class="favorite-stocks">
                  <h4>관심종목 선택 <span class="selection-count">({{ selectedStocks.length }}/{{ favoriteStocks.length }})</span></h4>
                  <div v-if="favoriteStocks.length === 0" class="empty-state">
                    관심종목이 없습니다. 주식 페이지에서 관심종목을 추가해주세요.
                  </div>
                  <div v-else class="stocks-list">
                    <div 
                      v-for="stock in favoriteStocks" 
                      :key="stock.code" 
                      class="stock-item"
                      :class="{ 'selected': selectedStocks.includes(stock.code) }"
                      @click="toggleStockSelection(stock.code)"
                    >
                      <div class="stock-info">
                        <div class="stock-name">{{ stock.name }}</div>
                        <div class="stock-code">{{ stock.code }}</div>
                      </div>
                      <div class="stock-price">{{ stock.price }}원</div>
                      <div class="selection-indicator">
                        <div class="check-mark" v-if="selectedStocks.includes(stock.code)">✓</div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="favoriteStocks.length > 0" class="stock-selection-buttons">
                    <button @click="selectAllStocks" class="selection-btn">전체 선택</button>
                    <button @click="clearStockSelection" class="selection-btn">선택 취소</button>
                    <button @click="equalizeWeights" class="selection-btn" :disabled="selectedStocks.length === 0">
                      비중 균등 분배
                    </button>
                  </div>
                  
                  <!-- 선택된 종목 비중 설정 -->
                  <div v-if="selectedStocks.length > 0" class="weight-configuration">
                    <h4>투자 비중 설정</h4>
                    <p class="weight-desc">각 종목별 투자 비중을 설정해주세요. (총합 100%)</p>
                    
                    <div class="weight-list">
                      <div v-for="code in selectedStocks" :key="code" class="weight-item">
                        <div class="weight-stock">
                          <div class="weight-stock-name">
                            {{ favoriteStocks.find(s => s.code === code)?.name }}
                          </div>
                          <div class="weight-stock-code">{{ code }}</div>
                        </div>
                        <div class="weight-control">
                          <button 
                            class="weight-btn" 
                            @click="adjustWeight(code, -5)" 
                            :disabled="getStockWeight(code) <= 5"
                          >-</button>
                          <div class="weight-display">
                            <input 
                              type="number" 
                              v-model="stockWeights[code]" 
                              @change="validateWeight(code)"
                              min="5" 
                              max="100"
                              step="5"
                            />
                            <span class="weight-percent">%</span>
                          </div>
                          <button 
                            class="weight-btn" 
                            @click="adjustWeight(code, 5)"
                            :disabled="getStockWeight(code) >= 100 || getTotalWeight() >= 100"
                          >+</button>
                        </div>
                      </div>
                    </div>
                    
                    <div class="weight-summary">
                      <div class="weight-total">
                        총 비중: <span :class="{ 'weight-warning': getTotalWeight() !== 100 }">{{ getTotalWeight() }}%</span>
                      </div>
                      <div v-if="getTotalWeight() !== 100" class="weight-error">
                        * 총 비중이 100%가 되도록 설정해주세요
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="purchase-settings">
                  <div class="setting-group">
                    <label class="setting-label">매수 주기</label>
                    <div class="select-wrapper">
                      <select v-model="purchaseInterval">
                        <option value="daily">매일</option>
                        <option value="weekly">매주</option>
                        <option value="monthly">매월</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-group">
                    <label class="setting-label">매수 금액</label>
                    <div class="input-group">
                      <input type="number" v-model="purchaseAmount" min="10000" step="10000" /> 원
                    </div>
                  </div>

                  <div class="setting-group">
                    <label class="setting-label">시작일</label>
                    <div class="input-group">
                      <input type="date" v-model="purchaseStartDate" />
                    </div>
                  </div>
                </div>
                
                <div class="setting-summary">
                  <div class="summary-title">자동 매수 요약</div>
                  <div class="summary-content">
                    <p>
                      <b>시작일</b>: {{ formatDate(purchaseStartDate) }} 부터
                    </p>
                    <p>
                      선택된 <span class="highlight-text">{{ selectedStocks.length }}개 종목</span>에 
                      <span class="highlight-text">{{ purchaseIntervalLabel }}</span> 
                      <span class="highlight-text">{{ formatCurrency(purchaseAmount) }}원</span>씩
                      {{ selectedStocks.length > 0 ? '설정된 비중에 따라 투자됩니다.' : '투자할 예정입니다.' }}
                    </p>
                    
                    <div v-if="selectedStocks.length > 0" class="weight-distribution">
                      <div class="distribution-title">종목별 투자 비중:</div>
                      <div class="distribution-bars">
                        <div 
                          v-for="code in selectedStocks" 
                          :key="code" 
                          class="distribution-bar" 
                          :style="{
                            width: `${stockWeights[code] || 0}%`, 
                            backgroundColor: getDistributionColor(selectedStocks.indexOf(code))
                          }"
                          :title="`${favoriteStocks.find(s => s.code === code)?.name}: ${stockWeights[code] || 0}%`"
                        >
                          <span v-if="(stockWeights[code] || 0) >= 10">
                            {{ stockWeights[code] || 0 }}%
                          </span>
                        </div>
                      </div>
                      <div class="distribution-labels">
                        <div 
                          v-for="code in selectedStocks" 
                          :key="`label-${code}`" 
                          class="distribution-label"
                        >
                          <div 
                            class="label-color" 
                            :style="{ backgroundColor: getDistributionColor(selectedStocks.indexOf(code)) }"
                          ></div>
                          <div class="label-stock-name">
                            {{ favoriteStocks.find(s => s.code === code)?.name }}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <p>
                      <b>연간 총 투자금액</b>: {{ formatCurrency(calculateAnnualInvestment()) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 투자 현황 탭 내용 -->
          <div v-if="activeTab === 'status'" class="tab-content">
            <div class="investment-status">
              <div class="status-header">투자 현황</div>
              <div class="status-content">
                <div class="status-summary">
                  <div class="status-item">
                    <div class="status-label">총 저축액</div>
                    <div class="status-value">{{ formatCurrency(totalSavings) }}</div>
                    <div class="status-percent">{{ calculateAssetPercent(totalSavings) }}%</div>
                  </div>
                  <div class="status-item">
                    <div class="status-label">총 주식 투자액</div>
                    <div class="status-value">{{ formatCurrency(totalStockInvestment) }}</div>
                    <div class="status-percent">{{ calculateAssetPercent(totalStockInvestment) }}%</div>
                  </div>
                  <div class="status-item highlight">
                    <div class="status-label">총 자산</div>
                    <div class="status-value">{{ formatCurrency(totalAssets) }}</div>
                    <div class="status-progress">
                      <div class="progress-bar">
                        <div class="progress-fill savings" :style="`width: ${calculateAssetPercent(totalSavings)}%`"></div>
                        <div class="progress-fill stocks" :style="`width: ${calculateAssetPercent(totalStockInvestment)}%`"></div>
                      </div>
                      <div class="progress-legend">
                        <div class="legend-item">
                          <div class="legend-color savings-color"></div>
                          <span>저축</span>
                        </div>
                        <div class="legend-item">
                          <div class="legend-color stocks-color"></div>
                          <span>주식</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="investment-analytics">
                  <div class="analytics-item">
                    <h4>월간 자동저축 현황</h4>
                    <div class="analytics-value">{{ formatCurrency(monthlyAutoSavings) }}</div>
                    <div class="analytics-detail">
                      <div>일일저축: {{ formatCurrency(dailySavings * 30) }}</div>
                      <div>결제저금: {{ formatCurrency(monthlyPayment * paymentRatio / 100) }}</div>
                    </div>
                  </div>
                  
                  <div class="analytics-item">
                    <h4>월간 주식매수 현황</h4>
                    <div class="analytics-value">{{ formatCurrency(monthlyStockPurchase) }}</div>
                    <div class="analytics-detail">
                      <div>종목수: {{ selectedStocks.length }}개</div>
                      <div>{{ purchaseIntervalLabel }}: {{ formatCurrency(purchaseAmount) }}</div>
                    </div>
                  </div>
                </div>
                
                <div class="stocks-portfolio">
                  <h4>주식 포트폴리오 <span class="portfolio-count">({{ portfolioStocks.length }} 종목)</span></h4>
                  <div v-if="portfolioStocks.length === 0" class="empty-state">
                    아직 자동 매수한 주식이 없습니다.
                  </div>
                  <div v-else>
                    <div class="portfolio-chart">
                      <div class="pie-chart" :style="{ background: createPieChartGradient }">
                      </div>
                      <div class="chart-labels">
                        <div v-for="segment in getPieChartSegments()" :key="segment.code" class="chart-label-item">
                          <div class="label-color" :style="`background-color: ${segment.color}`"></div>
                          <div class="label-name">{{ segment.name }}</div>
                          <div class="label-value">{{ segment.percent }}%</div>
                        </div>
                      </div>
                    </div>                      <div class="portfolio-list">
                      <div v-for="stock in portfolioStocks" :key="stock.code" class="portfolio-item">
                        <div class="portfolio-stock-info">
                          <div class="stock-name">{{ stock.name }}</div>
                          <div class="stock-code">{{ stock.code }}</div>
                          <div class="stock-weight">투자 비중: <span class="highlight-weight">{{ stock.weight || 0 }}%</span></div>
                        </div>
                        <div class="portfolio-details">
                          <div class="purchase-info">
                            <div>보유수량: <span class="highlight-text">{{ stock.quantity }}주</span></div>
                            <div>평균단가: {{ stock.avgPrice }}원</div>
                            <div>매수금액: {{ formatCurrency(parseInt(stock.avgPrice.replace(/,/g, '')) * stock.quantity) }}</div>
                          </div>
                          <div class="current-info">
                            <div>현재가: {{ stock.currentPrice }}원</div>
                            <div>평가금액: {{ formatCurrency(parseInt(stock.currentPrice.replace(/,/g, '')) * stock.quantity) }}</div>
                            <div>수익률: <span :class="stock.profitRate >= 0 ? 'profit-up' : 'profit-down'">
                              {{ stock.profitRate >= 0 ? '+' : '' }}{{ stock.profitRate }}%
                            </span></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 투자 차트 (저금 탭일 때만 표시) -->
          <div v-if="activeTab === 'savings'" class="investment-chart">
            <div class="chart-container">
              <div class="chart-bar chart-bar-1"></div>
              <div class="chart-bar chart-bar-2"></div>
              <div class="chart-bar chart-bar-3"></div>
              <div class="chart-bar chart-bar-4"></div>
              <div class="chart-bar chart-bar-5"></div>
              <div class="chart-line"></div>
            </div>
            <div class="chart-legend">
              <div class="legend-item">
                <div class="legend-color start-color"></div>
                <span>시작</span>
              </div>
              <div class="legend-item">
                <div class="legend-color end-color"></div>
                <span>1년 후</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="investment-features">
          <div class="feature-item">
            <div class="feature-icon">
              <img src="/piggy-bank.png" alt="저금통 아이콘" />
            </div>
            <div class="feature-content">
              <h3>결제 금액 자동 저금</h3>
              <p>결제할 때마다 일정 비율을 자동으로 저금해 소비하면서도 저축하는 습관을 만들어보세요.</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">
              <img src="/investment-graph.png" alt="투자 그래프 아이콘" />
            </div>
            <div class="feature-content">
              <h3>관심종목 자동 매수</h3>
              <p>설정한 주기와 금액에 따라 관심종목을 자동으로 매수하여 장기투자 전략을 실천하세요.</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">
              <img src="/easy-setup.png" alt="간편 설정 아이콘" />
            </div>
            <div class="feature-content">
              <h3>한눈에 보는 투자현황</h3>
              <p>총 자산 및 포트폴리오 수익률을 한눈에 확인하고 더 나은 투자 결정을 내리세요.</p>
            </div>
          </div>
          
          <button class="cta-button" @click="startAutoInvestment">자동투자 시작하기</button>
        </div>
      </div>
    </div>
    
    <!-- 자동투자 설정 완료 모달 -->
    <div v-if="showSuccessModal" class="modal-overlay">
      <div class="success-modal">
        <div class="modal-icon">✓</div>
        <h3>자동투자 설정 완료!</h3>
        <p>설정하신 내용대로 자동투자가 시작되었습니다.</p>
        <button @click="showSuccessModal = false" class="close-modal-btn">확인</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

// 현재 활성화된 탭
const activeTab = ref('savings');

// 자동저축 관련 상태
const dailySavings = ref(5000);
const paymentRatio = ref(5);
const monthlyPayment = ref(500000); // 월 평균 결제금액

// 관심종목 관련 상태
const favoriteStocks = ref([]);
const selectedStocks = ref([]);
const stockWeights = ref({}); // 각 종목별 투자 비중 (%)
const purchaseInterval = ref('monthly');
const purchaseAmount = ref(50000);
const purchaseStartDate = ref(new Date().toISOString().split('T')[0]); // 오늘 날짜를 기본값으로 설정

// 자동투자 현황 관련 상태
const portfolioStocks = ref([]);
const monthlyAutoSavings = ref(0);
const monthlyStockPurchase = ref(0);
const showSuccessModal = ref(false);
const investmentStartDate = ref(new Date().setMonth(new Date().getMonth() - 6)); // 6개월 전 시작 가정

// 총 저축액 계산 (computed로 변경)
const totalSavings = computed(() => {
  // 매월 저축금액 * 투자 개월 수
  const months = Math.max(1, Math.floor((new Date() - new Date(investmentStartDate.value)) / (30 * 24 * 60 * 60 * 1000)));
  return monthlyAutoSavings.value * months;
});

// 총 주식 투자액 계산 (computed로 변경)
const totalStockInvestment = computed(() => {
  // 매월 주식매수금액 * 투자 개월 수
  const months = Math.max(1, Math.floor((new Date() - new Date(investmentStartDate.value)) / (30 * 24 * 60 * 60 * 1000)));
  return monthlyStockPurchase.value * months;
});

// 구매 주기 표시 텍스트
const purchaseIntervalLabel = computed(() => {
  switch (purchaseInterval.value) {
    case 'daily': return '매일';
    case 'weekly': return '매주';
    case 'monthly': return '매월';
    default: return '';
  }
});

// 총 자산 계산
const totalAssets = computed(() => {
  return totalSavings.value + totalStockInvestment.value;
});

// 저축액 계산 함수
const calculateSavings = (years) => {
  // 일일 저축액 * 365일 * 연도 + 평균 결제액 * 결제 비율 * 12개월 * 연도
  const baseAmount = dailySavings.value * 365 * years;
  const paymentAmount = monthlyPayment.value * (paymentRatio.value / 100) * 12 * years;
  return baseAmount + paymentAmount;
};

// 금액 포맷 함수
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ko-KR', { 
    style: 'currency', 
    currency: 'KRW',
    maximumFractionDigits: 0
  }).format(amount);
};

// 관심종목 선택 토글
const toggleStockSelection = (code) => {
  const index = selectedStocks.value.indexOf(code);
  if (index === -1) {
    selectedStocks.value.push(code);
    // 기본 비중 설정
    stockWeights.value[code] = calculateDefaultWeight();
  } else {
    selectedStocks.value.splice(index, 1);
    // 비중 제거 및 재분배
    delete stockWeights.value[code];
    if (selectedStocks.value.length > 0) {
      equalizeWeights();
    }
  }
};

// 기본 비중 계산 (균등 분배)
const calculateDefaultWeight = () => {
  const count = selectedStocks.value.length;
  if (count === 0) return 0;
  return Math.floor(100 / count);
};

// 주식 비중 조회
const getStockWeight = (code) => {
  return stockWeights.value[code] || 0;
};

// 총 비중 계산
const getTotalWeight = () => {
  return Object.values(stockWeights.value).reduce((sum, weight) => sum + Number(weight), 0);
};

// 비중 조정
const adjustWeight = (code, amount) => {
  if (!stockWeights.value[code]) {
    stockWeights.value[code] = 0;
  }
  
  const newWeight = Number(stockWeights.value[code]) + amount;
  if (newWeight >= 5 && newWeight <= 100) {
    stockWeights.value[code] = newWeight;
  }
};

// 비중 유효성 검사
const validateWeight = (code) => {
  let value = Number(stockWeights.value[code]);
  if (isNaN(value) || value < 5) {
    value = 5;
  } else if (value > 100) {
    value = 100;
  }
  stockWeights.value[code] = value;
};

// 균등 비중 설정
const equalizeWeights = () => {
  const count = selectedStocks.value.length;
  if (count === 0) return;
  
  const equalWeight = Math.floor(100 / count);
  const remainder = 100 - (equalWeight * count);
  
  selectedStocks.value.forEach((code, index) => {
    stockWeights.value[code] = equalWeight + (index < remainder ? 1 : 0);
  });
};

// 차트 스타일 생성
const getPieChartSegments = () => {
  if (portfolioStocks.value.length === 0) return [];

  // 색상 배열 (더 다양하고 구분되는 색상으로 확장)
  const colors = [
    '#4CAF50', '#2196F3', '#FFC107', '#E91E63', '#9C27B0', '#FF5722', 
    '#009688', '#3F51B5', '#CDDC39', '#795548', '#607D8B', '#00BCD4'
  ];
  
  // 각 종목의 가치 계산 (currentPrice가 없으면 '0' 사용)
  const stockValues = portfolioStocks.value.map(stock => {
    const price = parseInt((stock.currentPrice || '0').toString().replace(/,/g, ''));
    return {
      code: stock.code,
      name: stock.name,
      value: price * (stock.quantity || 0)
    };
  });
  
  // 총 포트폴리오 가치 계산
  const totalValue = stockValues.reduce((sum, stock) => sum + stock.value, 0);
  
  // 각 종목의 비율과 각도 계산 후 결과 배열 생성
  let cumulativePercent = 0;
  const segments = stockValues.map((stock, index) => {
    // 사용자 설정 비중 또는 계산된 비율 사용
    // 포트폴리오 화면에서는 실제 보유 종목 가치 기반, 설정 화면에서는 사용자 지정 비중 사용
    const stockInPortfolio = portfolioStocks.value.find(s => s.code === stock.code);
    const percent = stockInPortfolio?.weight || (totalValue > 0 ? (stock.value / totalValue * 100) : 0);
    
    // 시작 및 종료 각도 계산
    const startPercent = cumulativePercent;
    cumulativePercent += percent;
    
    return {
      code: stock.code,
      name: stock.name,
      color: colors[index % colors.length],
      percent: Math.round(percent)
    };
  });

  return segments;
};

// 전체 파이 차트를 하나의 conic gradient로 생성
const createPieChartGradient = computed(() => {
  if (portfolioStocks.value.length === 0) return 'conic-gradient(#f0f0f0 0%, #f0f0f0 100%)';
  
  // 색상 배열
  const colors = [
    '#4CAF50', '#2196F3', '#FFC107', '#E91E63', '#9C27B0', '#FF5722', 
    '#009688', '#3F51B5', '#CDDC39', '#795548', '#607D8B', '#00BCD4'
  ];
  
  // 각 종목의 가치 계산 (price가 없으면 '0' 사용)
  const stockValues = portfolioStocks.value.map(stock => {
    const price = parseInt((stock.price || '0').toString().replace(/,/g, ''));
    return price * (stock.quantity || 0);
  });
  
  // 총 포트폴리오 가치 계산
  const totalValue = stockValues.reduce((sum, value) => sum + value, 0);
  
  // 각 종목의 비율과 각도 계산 후 conic-gradient 속성 값 생성
  let cumulativePercent = 0;
  let gradientString = 'conic-gradient(';
  
  portfolioStocks.value.forEach((stock, index) => {
    const value = stockValues[index];
    // 사용자가 설정한 비중 우선 사용 (없으면 실제 가치 기반 계산)
    const percent = stock.weight || (totalValue > 0 ? (value / totalValue * 100) : 0);
    const color = colors[index % colors.length];
    
    // 시작 위치
    gradientString += `${color} ${cumulativePercent}%, `;
    
    // 종료 위치 (다음 세그먼트의 시작)
    cumulativePercent += percent;
    gradientString += `${color} ${cumulativePercent}%, `;
  });
  
  // 마지막 콤마와 공백 제거 후 닫기
  gradientString = gradientString.slice(0, -2);
  gradientString += ')';
  
  return gradientString;
});

// 투자 분포 색상 얻기
const getDistributionColor = (index) => {
  const colors = [
    '#4CAF50', '#2196F3', '#FFC107', '#E91E63', '#9C27B0', '#FF5722', 
    '#009688', '#3F51B5', '#CDDC39', '#795548', '#607D8B', '#00BCD4'
  ];
  return colors[index % colors.length];
};

// 포트폴리오 업데이트
const updatePortfolio = () => {
  if (selectedStocks.value.length === 0) {
    // 선택된 종목이 없으면 포트폴리오를 비움
    portfolioStocks.value = [];
    return;
  }
  
  // 선택된 종목만 필터링하여 포트폴리오에 추가
  const selectedFavorites = favoriteStocks.value.filter(stock => 
    selectedStocks.value.includes(stock.code)
  );
  
  // 비중이 설정되지 않은 종목이 있으면 균등 분배
  if (selectedStocks.value.some(code => !stockWeights.value[code])) {
    equalizeWeights();
  }
  
  // 새로운 포트폴리오 데이터 생성
  portfolioStocks.value = selectedFavorites.map(stock => {
    // 기존 데이터가 있으면 유지, 없으면 새로 생성
    const existingStock = portfolioStocks.value.find(s => s.code === stock.code);
    const weight = stockWeights.value[stock.code] || calculateDefaultWeight();
    
    if (existingStock) {
      // 기존 데이터를 유지하지만 비중 업데이트
      return {
        ...existingStock,
        weight: weight
      };
    } else {
      // 새 종목 추가 시 랜덤 데이터 생성 (실제로는 API나 DB에서)
      const price = parseInt(stock.price.replace(/,/g, ''));
      // 투자 비중에 따른 매수 금액 계산
      const investmentAmount = purchaseAmount.value * (weight / 100);
      // 매수 가능한 주식 수량 계산
      const quantity = Math.floor(investmentAmount / price);
      
      const avgPrice = price;
      const currentPrice = avgPrice * (1 + (Math.random() * 0.2 - 0.1));
      const profitRate = parseFloat(((currentPrice / avgPrice - 1) * 100).toFixed(2));
      
      return {
        code: stock.code,
        name: stock.name,
        quantity: quantity,
        avgPrice: avgPrice.toLocaleString(),
        currentPrice: Math.round(currentPrice).toLocaleString(),
        profitRate: profitRate,
        weight: weight
      };
    }
  });
  
  // 포트폴리오 정보 저장
  localStorage.setItem('portfolioStocks', JSON.stringify(portfolioStocks.value));
};

// 전체 관심종목 선택
const selectAllStocks = () => {
  selectedStocks.value = favoriteStocks.value.map(stock => stock.code);
  // 모든 종목 선택 시 비중 균등 분배
  equalizeWeights();
};

// 선택된 관심종목 취소
const clearStockSelection = () => {
  selectedStocks.value = [];
  stockWeights.value = {};
};

// 자동투자 시작
const startAutoInvestment = () => {
  // 투자 비중 유효성 검증
  if (selectedStocks.value.length > 0 && getTotalWeight() !== 100) {
    alert('투자 비중의 총합이 100%가 되어야 합니다.');
    return;
  }

  // 설정 데이터 저장
  localStorage.setItem('autoInvestSettings', JSON.stringify({
    dailySavings: dailySavings.value,
    paymentRatio: paymentRatio.value,
    selectedStocks: selectedStocks.value,
    stockWeights: stockWeights.value,
    purchaseInterval: purchaseInterval.value,
    purchaseAmount: purchaseAmount.value,
    purchaseStartDate: purchaseStartDate.value
  }));
  
  // 월간 저축액 및 주식매수액 업데이트
  monthlyAutoSavings.value = dailySavings.value * 30 + (monthlyPayment.value * paymentRatio.value / 100);
  
  // 매수 주기에 따른 월간 주식매수액 계산
  switch (purchaseInterval.value) {
    case 'daily':
      monthlyStockPurchase.value = purchaseAmount.value * 30;
      break;
    case 'weekly':
      monthlyStockPurchase.value = purchaseAmount.value * 4;
      break;
    case 'monthly':
      monthlyStockPurchase.value = purchaseAmount.value;
      break;
  }
  
  // 포트폴리오 업데이트 (선택된 종목만 포트폴리오에 추가)
  updatePortfolio();
  
  // 투자 시작일 저장 (처음 설정하는 경우)
  if (!localStorage.getItem('investmentStartDate')) {
    investmentStartDate.value = new Date().getTime();
    localStorage.setItem('investmentStartDate', investmentStartDate.value.toString());
  }
  
  // 성공 모달 표시
  showSuccessModal.value = true;
};

// 연간 총 투자금액 계산
const calculateAnnualInvestment = () => {
  switch (purchaseInterval.value) {
    case 'daily':
      return purchaseAmount.value * 365;
    case 'weekly':
      return purchaseAmount.value * 52;
    case 'monthly':
      return purchaseAmount.value * 12;
    default:
      return 0;
  }
};

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ko-KR', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }).format(date);
};

// 자산 비율 계산
const calculateAssetPercent = (value) => {
  if (totalAssets.value === 0) return 0;
  return Math.round((value / totalAssets.value) * 100);
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  // 저장된 설정 불러오기
  const savedSettings = JSON.parse(localStorage.getItem('autoInvestSettings') || 'null');
  if (savedSettings) {
    dailySavings.value = savedSettings.dailySavings || 5000;
    paymentRatio.value = savedSettings.paymentRatio || 5;
    selectedStocks.value = savedSettings.selectedStocks || [];
    stockWeights.value = savedSettings.stockWeights || {};
    purchaseInterval.value = savedSettings.purchaseInterval || 'monthly';
    purchaseAmount.value = savedSettings.purchaseAmount || 50000;
  }
  
  // 월간 자동저축 및 주식매수 현황 계산
  monthlyAutoSavings.value = dailySavings.value * 30 + (monthlyPayment.value * paymentRatio.value / 100);
  
  // 매수 주기에 따른 월간 주식매수액 계산
  switch (purchaseInterval.value) {
    case 'daily':
      monthlyStockPurchase.value = purchaseAmount.value * 30;
      break;
    case 'weekly':
      monthlyStockPurchase.value = purchaseAmount.value * 4;
      break;
    case 'monthly':
      monthlyStockPurchase.value = purchaseAmount.value;
      break;
  }
  
  // 관심종목 불러오기
  try {
    const storedFavorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]');
    favoriteStocks.value = storedFavorites;
    
    // 저장된 포트폴리오 정보 불러오기
    const savedPortfolio = JSON.parse(localStorage.getItem('portfolioStocks') || 'null');
    if (savedPortfolio) {
      portfolioStocks.value = savedPortfolio;
      selectedStocks.value = portfolioStocks.value.map(stock => stock.code);
    } else if (storedFavorites.length > 0) {
      // 저장된 포트폴리오가 없으면 관심종목에서 초기 포트폴리오 생성
      updatePortfolio();
    }
    
    // 저장된 투자 시작일 불러오기
    const savedStartDate = localStorage.getItem('investmentStartDate');
    if (savedStartDate) {
      investmentStartDate.value = parseInt(savedStartDate);
    }
  } catch (error) {
    console.error('관심종목 로드 오류:', error);
    favoriteStocks.value = [];
  }
  
  // 투자 시작일 불러오기
  const savedStartDate = localStorage.getItem('investmentStartDate');
  if (savedStartDate) {
    investmentStartDate.value = new Date(parseInt(savedStartDate)).getTime();
  }
});

// 관련 값 변경 시 월간 자동저축 및 주식매수 현황 업데이트
// 주요값 변경 시 자동저축 금액 업데이트
watch([dailySavings, paymentRatio], () => {
  monthlyAutoSavings.value = dailySavings.value * 30 + (monthlyPayment.value * paymentRatio.value / 100);
});

// 매수 주기나 금액 변경 시 주식매수액 업데이트
watch([purchaseInterval, purchaseAmount], () => {
  switch (purchaseInterval.value) {
    case 'daily':
      monthlyStockPurchase.value = purchaseAmount.value * 30;
      break;
    case 'weekly':
      monthlyStockPurchase.value = purchaseAmount.value * 4;
      break;
    case 'monthly':
      monthlyStockPurchase.value = purchaseAmount.value;
      break;
  }
});

// 선택된 종목 변경시 포트폴리오 업데이트
watch(selectedStocks, (newVal) => {
  if (activeTab.value === 'stocks') {
    if (newVal.length > 0) {
      // 이전에 없던 새 종목이 추가된 경우 비중 균등 분배
      const hasNewStock = newVal.some(code => !stockWeights.value[code]);
      if (hasNewStock) {
        equalizeWeights();
      }
      updatePortfolio();
    }
  }
}, { deep: true });

// 투자 비중 변경 시 총합 확인
watch(stockWeights, () => {
  // 비중 변경 시 포트폴리오 업데이트
  if (selectedStocks.value.length > 0 && activeTab.value === 'stocks') {
    updatePortfolio();
  }
}, { deep: true });

// activeTab이 'status'로 변경될 때마다 현황 데이터 갱신
watch(activeTab, (newTab) => {
  if (newTab === 'status') {
    // 자동투자 설정 불러오기
    const savedSettings = JSON.parse(localStorage.getItem('autoInvestSettings') || 'null');
    if (savedSettings) {
      dailySavings.value = savedSettings.dailySavings || 5000;
      paymentRatio.value = savedSettings.paymentRatio || 5;
      selectedStocks.value = savedSettings.selectedStocks || [];
      stockWeights.value = savedSettings.stockWeights || {};
      purchaseInterval.value = savedSettings.purchaseInterval || 'monthly';
      purchaseAmount.value = savedSettings.purchaseAmount || 50000;
    }
    // 포트폴리오 불러오기
    const savedPortfolio = JSON.parse(localStorage.getItem('portfolioStocks') || 'null');
    if (savedPortfolio) {
      portfolioStocks.value = savedPortfolio;
    }
    // 투자 시작일 불러오기
    const savedStartDate = localStorage.getItem('investmentStartDate');
    if (savedStartDate) {
      investmentStartDate.value = parseInt(savedStartDate);
    }
    // 월간 자동저축 및 주식매수 현황 재계산
    monthlyAutoSavings.value = dailySavings.value * 30 + (monthlyPayment.value * paymentRatio.value / 100);
    switch (purchaseInterval.value) {
      case 'daily':
        monthlyStockPurchase.value = purchaseAmount.value * 30;
        break;
      case 'weekly':
        monthlyStockPurchase.value = purchaseAmount.value * 4;
        break;
      case 'monthly':
        monthlyStockPurchase.value = purchaseAmount.value;
        break;
    }
  }
});
</script>

<style scoped>
.auto-invest-section {
  padding: 5rem 0;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
  background-color: #f9faf7;
  overflow: hidden;
}

.overlay-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%2328a745' fill-opacity='0.04' fill-rule='evenodd'/%3E%3C/svg%3E");
  z-index: 0;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  position: relative;
  z-index: 1;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.header-badge {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.35rem 0.8rem;
  border-radius: 20px;
  margin-bottom: 1rem;
  display: inline-block;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.section-desc {
  font-size: 1.1rem;
  color: #666;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.investment-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3.5rem;
  align-items: center;
}

.investment-visual {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.investment-chart {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.chart-container {
  height: 200px;
  display: flex;
  align-items: flex-end;
  gap: 12px;
  margin-bottom: 1rem;
  position: relative;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #28a745, #a0e8bc);
  border-radius: 6px 6px 0 0;
  position: relative;
  transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.chart-bar-1 {
  height: 40%;
}

.chart-bar-2 {
  height: 60%;
}

.chart-bar-3 {
  height: 55%;
}

.chart-bar-4 {
  height: 75%;
}

.chart-bar-5 {
  height: 90%;
}

.chart-line {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: #f0f0f0;
  z-index: 0;
}

.chart-legend {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.start-color {
  background-color: #a0e8bc;
}

.end-color {
  background-color: #28a745;
}

.savings-simulator {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.simulator-header {
  background-color: #28a745;
  color: white;
  padding: 1rem;
  font-weight: 600;
  font-size: 1.1rem;
  text-align: center;
}

.simulator-content {
  padding: 1.5rem;
}

.simulator-input {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.input-label {
  font-weight: 500;
  color: #444;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.input-group input {
  width: 100px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: right;
  font-size: 1rem;
  color: #333;
}

.simulator-result {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.result-item {
  text-align: center;
  padding: 0.8rem;
  border-radius: 8px;
  background-color: #f9faf7;
}

.result-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.result-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

/* 포트폴리오 차트 스타일 */
.portfolio-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 1.5rem 0;
}

.pie-chart {
  position: relative;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  margin-bottom: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.pie-chart:hover {
  transform: scale(1.05);
}

.chart-labels {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.8rem;
  width: 100%;
  margin-top: 0.5rem;
}

.chart-label-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  background-color: #f8f8f8;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  transition: all 0.2s ease;
}

.chart-label-item:hover {
  background-color: #efefef;
  transform: translateY(-2px);
}

.label-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.label-name {
  font-weight: 500;
  color: #444;
}

.label-value {
  font-weight: 500;
}

/* 비중 설정 관련 스타일 */
.weight-configuration {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  border: 1px solid #eee;
}

.weight-configuration h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  color: #333;
}

.weight-desc {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
}

.weight-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.weight-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.weight-stock {
  display: flex;
  flex-direction: column;
}

.weight-stock-name {
  font-weight: 500;
  color: #333;
}

.weight-stock-code {
  font-size: 0.8rem;
  color: #888;
}

.weight-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.weight-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: none;
  background-color: #f0f0f0;
  color: #555;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}

.weight-btn:hover:not(:disabled) {
  background-color: #28a745;
  color: white;
}

.weight-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.weight-display {
  display: flex;
  align-items: center;
  min-width: 80px;
}

.weight-display input {
  width: 50px;
  padding: 0.4rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: right;
  font-size: 1rem;
  font-weight: 500;
}

.weight-percent {
  font-weight: 500;
  margin-left: 2px;
}

.weight-summary {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.weight-total {
  font-weight: 500;
  font-size: 1.1rem;
}

.weight-warning {
  color: #ff5722;
  font-weight: bold;
}

.weight-error {
  font-size: 0.85rem;
  color: #ff5722;
  margin-top: 0.3rem;
}

/* 투자 분포 관련 스타일 */
.weight-distribution {
  margin: 1rem 0;
}

.distribution-title {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #444;
}

.distribution-bars {
  height: 30px;
  width: 100%;
  display: flex;
  border-radius: 4px;
  overflow: hidden;
}

.distribution-bar {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.distribution-bar:hover {
  filter: brightness(1.1);
}

.distribution-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 0.5rem;
}

.distribution-label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.8rem;
  color: #666;
}

.label-color {
  width: 10px;
  height: 10px;
  border-radius: 2px;
}

.highlight-weight {
  color: #28a745;
  font-weight: 500;
}

.result-item.highlight {
  background-color: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.result-item.highlight .result-value {
  color: #28a745;
}

.investment-features {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.feature-item {
  display: flex;
  gap: 1.2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.feature-icon {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(40, 167, 69, 0.1);
  border-radius: 10px;
}

.feature-icon img {
  width: 30px;
  height: 30px;
}

.feature-content {
  text-align: left;
}

.feature-content h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.feature-content p {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.cta-button {
  margin-top: 1rem;
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.9rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(40, 167, 69, 0.2);
  width: 100%;
}

.cta-button:hover {
  background-color: #218838;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
}

/* 투자 현황 탭 스타일 추가 */
.investment-status {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.status-header {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.status-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.status-item {
  background-color: white;
  padding: 1.2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.status-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.status-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.status-percent {
  font-size: 0.9rem;
  color: #28a745;
  font-weight: 500;
}

.status-progress {
  margin-top: 1rem;
}

.progress-bar {
  height: 12px;
  background-color: #f5f5f5;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  transition: width 0.5s ease;
}

.progress-fill.savings {
  background-color: #28a745;
}

.progress-fill.stocks {
  background-color: #007bff;
  left: auto;
  right: 0;
}

.progress-legend {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.legend-color {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.savings-color {
  background-color: #28a745;
}

.stocks-color {
  background-color: #007bff;
}

.investment-analytics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.analytics-item {
  background-color: white;
  padding: 1.2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.analytics-item h4 {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.analytics-value {
  font-size: 1.3rem;
  font-weight: 600;
  color: #28a745;
  margin-bottom: 0.8rem;
}

.analytics-detail {
  font-size: 0.85rem;
  color: #666;
}

.pie-chart {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #f5f5f5;
  position: relative;
  overflow: hidden;
  margin: 0 auto;
}

.pie-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  transform: rotate(0deg);
}

.portfolio-chart {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-labels {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.chart-label-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.label-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.label-value {
  font-weight: 500;
}

/* 추가된 기능 스타일 */
.ratio-info {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.5rem;
  line-height: 1.4;
}

.highlight-text {
  font-weight: 600;
  color: #28a745;
}

.payment-ratio-setting {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.setting-label {
  font-size: 0.95rem;
  font-weight: 500;
  color: #444;
  margin-bottom: 0.5rem;
}

.ratio-slider {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.slider {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: #e9ecef;
  border-radius: 2px;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #28a745;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.slider::-webkit-slider-thumb:hover {
  background: #218838;
  transform: scale(1.1);
}

.stocks-setup {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.setup-header {
  background-color: #28a745;
  color: white;
  padding: 1rem;
  font-weight: 600;
  font-size: 1.1rem;
  text-align: center;
}

.setup-content {
  padding: 1.5rem;
}

.favorite-stocks {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 1.5rem;
}

.favorite-stocks h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.selection-count {
  font-size: 0.9rem;
  color: #666;
  font-weight: normal;
}

.empty-state {
  background-color: #f9faf7;
  padding: 1.5rem;
  text-align: center;
  color: #666;
  border-radius: 8px;
  font-size: 0.95rem;
}

.stocks-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
}

.stock-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.stock-item:last-child {
  border-bottom: none;
}

.stock-item:hover {
  background-color: #f8faff;
}

.stock-item.selected {
  background-color: rgba(40, 167, 69, 0.05);
}

.stock-info {
  flex: 1;
}

.stock-name {
  font-size: 0.95rem;
  font-weight: 500;
  color: #333;
}

.stock-code {
  font-size: 0.8rem;
  color: #888;
}

.stock-price {
  font-size: 0.9rem;
  color: #333;
  margin-right: 1rem;
}

.selection-indicator {
  width: 20px;
  height: 20px;
  border: 1px solid #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-mark {
  color: #28a745;
  font-size: 0.8rem;
}

.stock-selection-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.selection-btn {
  background: none;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.selection-btn:hover {
  background-color: #f5f5f5;
  border-color: #ccc;
}

.purchase-settings {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
  appearance: none;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%23888' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E") no-repeat;
  background-position: calc(100% - 10px) center;
  padding-right: 30px;
}

.setting-summary {
  background-color: #f9faf7;
  padding: 1.2rem;
  border-radius: 8px;
}

.summary-title {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.8rem;
}

.summary-content {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
}

.summary-content p {
  margin: 0.5rem 0;
}

.portfolio-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.portfolio-item {
  background-color: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1.2rem;
}

.portfolio-stock-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.portfolio-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.purchase-info, .current-info {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #666;
}

.profit-up {
  color: #d63031;
  font-weight: 500;
}

.profit-down {
  color: #0984e3;
  font-weight: 500;
}

.portfolio-count {
  font-size: 0.9rem;
  color: #666;
  font-weight: normal;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.success-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.modal-icon {
  background-color: #28a745;
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin: 0 auto 1.5rem;
}

.success-modal h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.success-modal p {
  color: #666;
  margin-bottom: 1.5rem;
}

.close-modal-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.close-modal-btn:hover {
  background-color: #218838;
}

/* 탭 스타일 */
.settings-tabs {
  display: flex;
  gap: 1px;
  margin-bottom: 1rem;
  background-color: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
}

.tab-btn {
  flex: 1;
  padding: 0.8rem 1rem;
  border: none;
  background-color: #f8f9fa;
  color: #555;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  font-size: 0.95rem;
}

.tab-btn.active {
  background-color: #007bff;
  color: white;
}

.tab-btn:hover:not(.active) {
  background-color: #e9ecef;
  color: #333;
}

.tab-content {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
</style>