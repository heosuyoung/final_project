<template>
  <section class="content-section alt-bg">
    <div class="content-container">
      <h2>저금통 자동투자</h2>
      <p>티끌 모아 태산! 소액으로 시작하는 자동투자 습관을 만들어보세요.</p>
      <div class="feature-grid">
        <div class="feature-item">
          <div class="feature-icon">
            <img src="/piggy-bank.png" alt="저금통 아이콘" />
          </div>
          <h3>매일 자동투자</h3>
          <p>커피 한 잔 값으로 매일 꾸준히 투자하여 목돈을 만들어보세요.</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">
            <img src="/investment-graph.png" alt="투자 그래프 아이콘" />
          </div>
          <h3>AI 포트폴리오</h3>
          <p>나에게 맞는 투자 성향을 분석하여 AI가 최적의 포트폴리오를 추천합니다.</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">
            <img src="/easy-setup.png" alt="간편 설정 아이콘" />
          </div>
          <h3>간편한 설정</h3>
          <p>복잡한 절차 없이 몇 번의 클릭만으로 자동투자를 시작할 수 있습니다.</p>
        </div>
      </div>
      <button class="cta-button">자동투자 시작하기</button>
    </div>
  </section>
</template>

<script>
export default {
  name: 'AutoInvestmentSection',
};
</script>

<style scoped>
.content-section {
  padding: 5rem 0;
  text-align: center;
  width: 100vw; /* 브라우저 너비 전체를 사용 */
  margin-left: calc(-50vw + 50%); /* 왼쪽 여백을 없애고 전체 너비로 확장 */
  position: relative; /* 위치 기준점 */
  margin-top: 3rem; /* 위쪽 추가 여백 */
  margin-bottom: 3rem; /* 아래쪽 추가 여백 */
}

.alt-bg {
  background-color: #fff; /* 흰색 배경 */
}

.content-container {
  max-width: 1500px;
  margin: 0 auto;
  padding: 0 2rem;
}

h2 {
  font-size: 2.3rem;
  color: #333;
  margin-bottom: 1.2rem;
}

p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
  margin-left: auto;
  margin-right: auto;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 8rem;
  margin: 0 auto 3rem auto;
}

.feature-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2.5rem 2rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.07);
}

.feature-icon {
  margin-bottom: 1rem;
}

.feature-icon img {
  width: 60px;
  height: 60px;
}

.feature-item h3 {
  font-size: 1.2rem;
  color: #007bff;
  margin-bottom: 1rem;
}

.feature-item p {
  font-size: 1.05rem;
  color: #555;
  line-height: 1.7;
  margin-bottom: 0;
}

.cta-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  font-weight: 500;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.cta-button:hover {
  background-color: #218838;
}
</style> 