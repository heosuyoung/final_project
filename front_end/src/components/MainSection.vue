<template>
  <section class="main-section">
    <!-- 그라데이션 배경 효과 추가 -->
    <div class="gradient-background"></div>
    
    <div class="main-row">
      <div class="main-left">
        <div class="main-text-group">
          <div class="animated-text">
            <div class="main-line1">금융이 쉬워지는</div>
            <div class="main-ease">EA$E</div>
            <div class="main-line2">맞춤형 서비스</div>
          </div>          <div class="cta-buttons">
            <button class="primary-btn" @click="navigateTo('/stocks')">시작하기</button>
            <button class="secondary-btn" @click="navigateTo('/about')">더 알아보기</button>
          </div>
        </div>
      </div>
      <div class="main-right">
        <div class="main-img-bg">
          <img src="/lucky-bag.png" alt="복주머니 이모티콘" class="floating" />
        </div>
      </div>
    </div>
    
    <!-- 관심 종목 슬라이드 추가 -->
    <div class="section-divider">
      <div class="divider-line"></div>
      <div class="divider-line"></div>
    </div>
    
    <FavoriteSlide />    <!-- 시장 개요 섹션 추가 -->
    <MarketOverview />
      <!-- AI 상담 섹션 추가 -->
    <AIAdvisorSection />
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
import FavoriteSlide from './FavoriteSlide.vue';
import MarketOverview from './MarketOverview.vue';
import AIAdvisorSection from './AIAdvisorSection.vue';

// 라우터 설정
const router = useRouter();

// 페이지 이동 함수
const navigateTo = (path) => {
  router.push(path);
};
</script>

<style scoped>
.main-section {
  min-height: 80vh;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0 2rem 0;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
  overflow: hidden;
}

.gradient-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 10% 20%, rgba(216, 241, 230, 0.3) 0%, transparent 60%),
              radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.2) 0%, transparent 60%);
  z-index: 0;
}

.main-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  gap: 4rem;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.main-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  height: 100%;
  padding-right: 2rem;
}

.main-text-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  gap: 0.2em;
}

.main-line1,
.main-line2 {
  font-size: 3.5rem;
  font-weight: 700;
  color: #222;
  letter-spacing: -1px;
  line-height: 1.2;
  text-align: right;
}

.main-ease {
  color: #007bff;
  font-size: 4rem;
  font-weight: 900;
  letter-spacing: 0.1em;
  margin: 0.1em 0 0.1em 0;
  line-height: 1.1;
  text-align: right;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
}

.animated-text {
  animation: fadeIn 1s ease-out;
}

.cta-buttons {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
}

.primary-btn, .secondary-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.primary-btn {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid #007bff;
  color: #007bff;
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.floating {
  animation: float 6s ease-in-out infinite;
}

.section-divider {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 3rem auto 1rem;
  z-index: 1;
}

.divider-line {
  flex-grow: 1;
  height: 1px;
  background-color: #ddd;
}

.divider-text {
  padding: 0 1rem;
  font-weight: 700;
  font-size: 1.2rem;
  color: #555;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

@keyframes fadeIn {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1400px) {
  .main-row {
    gap: 2rem;
  }
  .main-img-bg {
    width: 400px;
    height: 400px;
  }
  .main-line1,
  .main-line2 {
    font-size: 3rem;
  }
  .main-ease {
    font-size: 3.5rem;
  }
}

@media (max-width: 1200px) {
  .main-row {
    gap: 1.5rem;
  }
  .main-img-bg {
    width: 300px;
    height: 300px;
  }
  .main-line1,
  .main-line2 {
    font-size: 2.5rem;
  }
  .main-ease {
    font-size: 3rem;
  }
}

@media (max-width: 900px) {
  .main-row {
    flex-direction: column;
    gap: 2rem;
  }
  .main-left,
  .main-right {
    width: 100%;
    justify-content: center;
    align-items: center;
    padding-left: 0;
    padding-right: 0;
  }
  .main-text-group {
    align-items: center;
  }
  .main-line1,
  .main-line2 {
    font-size: 2rem;
    text-align: center;
  }
  .main-ease {
    font-size: 2.5rem;
    text-align: center;
  }
  .main-img-bg {
    width: 200px;
    height: 200px;
  }
}

@media (max-width: 600px) {
  .main-line1,
  .main-line2 {
    font-size: 1.5rem;
  }
  .main-ease {
    font-size: 2rem;
  }
  .main-img-bg {
    width: 150px;
    height: 150px;
  }
}
</style>
