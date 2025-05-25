<template>
  <div class="about-page">
    <div class="about-header">
      <div class="header-content">
        <h1 class="title">EA$E 소개</h1>
        <p class="subtitle">금융의 복잡함을 해결하는 맞춤형 금융 서비스</p>
      </div>
    </div>
    
    <div class="about-container">
      <section class="mission-section">
        <h2>우리의 미션</h2>
        <div class="mission-content">
          <div class="mission-text">
            <p class="highlight-text">EA$E는 누구나 쉽고 편리하게 금융 서비스를 이용할 수 있도록 만들기 위해 태어났습니다.</p>
            <p>복잡한 금융 지식 없이도 효율적인 자산 관리와 성장을 도와주는 플랫폼을 통해 모든 사용자가 경제적 자유를 향해 한 걸음 더 나아갈 수 있도록 돕습니다.</p>
          </div>
          <div class="mission-image">
            <img src="/lucky-bag.png" alt="EA$E 미션" class="floating-slow" />
          </div>
        </div>
      </section>

      <section class="services-section">
        <h2>EA$E 주요 서비스</h2>
        
        <div class="service-card">
          <div class="service-icon">📈</div>
          <div class="service-content">
            <h3>실시간 주식 정보</h3>
            <p>국내외 주요 주식 시장 정보를 실시간으로 제공하며, 관심 종목을 쉽게 관리할 수 있습니다.</p>
            <button class="service-btn" @click="navigateTo('/stocks')">주식 정보 보기</button>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon">🤖</div>
          <div class="service-content">
            <h3>AI 금융 상담</h3>
            <p>인공지능 기반 금융 상담사가 당신의 재무 상황에 맞는 맞춤형 조언을 제공합니다.</p>
            <button class="service-btn" @click="navigateTo('/')">AI 상담 시작하기</button>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon">🏦</div>
          <div class="service-content">
            <h3>금융기관 찾기</h3>
            <p>내 주변 은행, ATM 등 금융 시설을 지도에서 쉽게 찾고 정보를 확인할 수 있습니다.</p>
            <button class="service-btn" @click="navigateTo('/map')">주변 금융기관 찾기</button>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon">💰</div>
          <div class="service-content">
            <h3>맞춤형 저축 추천</h3>
            <p>개인의 재정 목표와 상황에 맞는 최적의 저축 방법을 추천해드립니다.</p>
            <button class="service-btn" @click="navigateTo('/savings')">저축 상품 추천받기</button>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon">🌎</div>
          <div class="service-content">
            <h3>국제 원자재 시세</h3>
            <p>금, 은, 석유 등 주요 원자재의 국제 시세를 차트와 함께 제공합니다.</p>
            <button class="service-btn" @click="navigateTo('/commodities')">원자재 시세 보기</button>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon">👥</div>
          <div class="service-content">
            <h3>투자 커뮤니티</h3>
            <p>다른 투자자들과 정보를 공유하고 소통할 수 있는 커뮤니티 공간을 제공합니다.</p>
            <button class="service-btn" @click="navigateTo('/stocks')">커뮤니티 참여하기</button>
          </div>
        </div>
      </section>

      <section class="values-section">
        <h2>EA$E의 핵심 가치</h2>
        <div class="values-grid">
          <div class="value-item">
            <h3>접근성</h3>
            <p>금융 서비스를 누구나 쉽게 이용할 수 있도록 합니다.</p>
          </div>
          <div class="value-item">
            <h3>투명성</h3>
            <p>모든 정보와 서비스는 투명하게 제공됩니다.</p>
          </div>
          <div class="value-item">
            <h3>개인화</h3>
            <p>각 사용자의 상황과 목표에 맞는 맞춤형 서비스를 제공합니다.</p>
          </div>
          <div class="value-item">
            <h3>신뢰성</h3>
            <p>정확하고 신뢰할 수 있는 정보와 서비스를 약속합니다.</p>
          </div>
        </div>
      </section>

      <section class="start-section">
        <h2>지금 바로 시작하세요</h2>
        <p>금융의 복잡함을 EA$E와 함께 쉽게 해결하세요.</p>
        <div class="start-buttons">
          <button class="primary-action" @click="navigateTo('/stocks')">서비스 시작하기</button>
          <button class="secondary-action" @click="navigateTo('/login')">로그인하기</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

// 라우터 설정
const router = useRouter();

// 페이지 이동 함수
const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.about-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f8f9ff;
}

.about-header {
  background: linear-gradient(135deg, #007bff 0%, #00bcd4 100%);
  color: white;
  padding: 5rem 0 3rem;
  text-align: center;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.3rem;
  font-weight: 400;
  opacity: 0.9;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

section {
  margin-bottom: 4rem;
  padding: 2rem 0;
}

h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
  position: relative;
}

h2::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #007bff, #00bcd4);
}

/* 미션 섹션 */
.mission-section {
  background-color: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-top: -4rem;
  position: relative;
}

.mission-content {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.mission-text {
  flex: 2;
}

.mission-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mission-image img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
}

.highlight-text {
  font-size: 1.3rem;
  color: #007bff;
  font-weight: 600;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.mission-text p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #555;
}

.floating-slow {
  animation: floatSlow 8s ease-in-out infinite;
}

/* 서비스 섹션 */
.services-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.service-card {
  display: flex;
  background-color: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.service-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  font-size: 2.5rem;
  background: linear-gradient(135deg, rgba(0,123,255,0.1) 0%, rgba(0,188,212,0.1) 100%);
  border-right: 1px solid #f0f0f0;
}

.service-content {
  flex: 1;
  padding: 1.5rem 2rem;
}

.service-content h3 {
  font-size: 1.4rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.8rem;
}

.service-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.service-btn {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.service-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 123, 255, 0.2);
}

/* 가치 섹션 */
.values-section {
  padding: 3rem;
  background-color: #f0f4ff;
  border-radius: 20px;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.value-item {
  background-color: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s ease;
}

.value-item:hover {
  transform: translateY(-5px);
}

.value-item h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #007bff;
  margin-bottom: 1rem;
}

.value-item p {
  color: #666;
  line-height: 1.5;
}

/* 시작 섹션 */
.start-section {
  text-align: center;
  padding: 3rem;
  background: linear-gradient(135deg, rgba(0,123,255,0.05) 0%, rgba(0,188,212,0.05) 100%);
  border-radius: 20px;
}

.start-section p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.start-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.primary-action {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 30px;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
  transition: all 0.3s ease;
}

.secondary-action {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-action:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);
}

.secondary-action:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

@keyframes floatSlow {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
  100% {
    transform: translateY(0px);
  }
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .mission-content {
    flex-direction: column-reverse;
    gap: 2rem;
  }
  
  .mission-image {
    max-width: 300px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .highlight-text {
    font-size: 1.2rem;
  }
  
  .mission-text p {
    font-size: 1rem;
  }
  
  .service-card {
    flex-direction: column;
  }
  
  .service-icon {
    width: 100%;
    height: 80px;
    border-right: none;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .start-buttons {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
