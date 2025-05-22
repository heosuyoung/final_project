<template>
  <section class="content-section">
    <div class="content-container">
      <h2>주식비교</h2>
      <p>관심 있는 종목들을 한눈에 비교하고 투자 기회를 찾아보세요.</p>
      <div class="card-grid">
        <div class="card">
          <div class="card-header">삼성전자</div>
          <div class="card-body">
            <p>현재가: 75,000원</p>
            <p>전일대비: +1,200원 (+1.63%)</p>
            <a href="#" class="card-link">자세히 보기</a>
          </div>
        </div>
        <div class="card">
          <div class="card-header">카카오</div>
          <div class="card-body">
            <p>현재가: 55,000원</p>
            <p>전일대비: -500원 (-0.90%)</p>
            <a href="#" class="card-link">자세히 보기</a>
          </div>
        </div>
        <div class="card">
          <div class="card-header">현대차</div>
          <div class="card-body">
            <p>현재가: 280,000원</p>
            <p>전일대비: +3,000원 (+1.08%)</p>
            <a href="#" class="card-link">자세히 보기</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'StockComparisonSection',
};
</script>

<style scoped>
.content-section {
  padding: 5rem 0;
  background-color: #f8f9fa;
  text-align: center;
  width: 100vw; /* 브라우저 너비 전체를 사용 */
  margin-left: calc(-50vw + 50%); /* 왼쪽 여백을 없애고 전체 너비로 확장 */
  position: relative; /* 위치 기준점 */
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

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 15rem;
  margin: 0 auto;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10);
  text-align: left;
  overflow: hidden;
  padding: 2.5rem 2rem;
}

.card-header {
  background-color: #007bff;
  color: white;
  padding: 1.3rem 1.5rem;
  font-size: 1.3rem;
  font-weight: 700;
}

.card-body {
  padding: 1.5rem 0 0 0;
  font-size: 1.1rem;
  color: #444;
}

.card-body p {
  margin-bottom: 0.6rem;
  font-size: 0.95rem;
  color: #555;
}

.card-link {
  display: inline-block;
  margin-top: 0.8rem;
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.card-link:hover {
  text-decoration: underline;
}
</style> 