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
          <div class="investment-chart">
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
          
          <div class="savings-simulator">
            <div class="simulator-header">일일 자동저축 시뮬레이션</div>
            <div class="simulator-content">
              <div class="simulator-input">
                <span class="input-label">일일 저축액</span>
                <div class="input-group">
                  <input type="number" value="5000" disabled /> 원
                </div>
              </div>
              <div class="simulator-result">
                <div class="result-item">
                  <div class="result-label">1년 후</div>
                  <div class="result-value">1,825,000원</div>
                </div>
                <div class="result-item highlight">
                  <div class="result-label">3년 후</div>
                  <div class="result-value">5,475,000원</div>
                </div>
                <div class="result-item">
                  <div class="result-label">5년 후</div>
                  <div class="result-value">9,125,000원</div>
                </div>
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
              <h3>매일 자동투자</h3>
              <p>커피 한 잔 값으로 매일 꾸준히 투자하여 목돈을 만들어보세요.</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">
              <img src="/investment-graph.png" alt="투자 그래프 아이콘" />
            </div>
            <div class="feature-content">
              <h3>맞춤형 포트폴리오</h3>
              <p>투자 목표와 기간에 따라 최적의 포트폴리오를 구성해 드립니다.</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">
              <img src="/easy-setup.png" alt="간편 설정 아이콘" />
            </div>
            <div class="feature-content">
              <h3>간편한 설정</h3>
              <p>복잡한 절차 없이 몇 번의 클릭만으로 자동투자를 시작할 수 있습니다.</p>
            </div>
          </div>
          
          <button class="cta-button">자동투자 시작하기</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// 컴포넌트 로직이 필요하면 여기에 추가
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

/* 반응형 디자인 */
@media (max-width: 992px) {
  .investment-layout {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
  
  .investment-visual {
    order: 1;
  }
  
  .investment-features {
    order: 0;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.8rem;
  }
  
  .section-desc {
    font-size: 1rem;
  }
  
  .simulator-result {
    grid-template-columns: 1fr;
  }
  
  .feature-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .feature-content {
    text-align: center;
  }
}
</style>