<template>
  <section class="ai-advisor-section">
    <div class="content-container">
      <h2 class="section-title">AI 금융 상담</h2>
      <p class="section-desc">당신의 재무 상황에 맞는 1:1 맞춤형 금융 상담을 AI가 도와드립니다.</p>
      
      <div class="advisor-content">
        <div class="advisor-text">
          <div class="advisor-features">
            <div class="feature">
              <div class="feature-icon">
                <i class="icon-analysis">📊</i>
              </div>
              <div class="feature-text">
                <h3>맞춤형 자산 분석</h3>
                <p>당신의 소득, 지출 패턴과 금융 목표를 분석하여 개인 맞춤형 조언을 제공합니다.</p>
              </div>
            </div>
            
            <div class="feature">
              <div class="feature-icon">
                <i class="icon-portfolio">💼</i>
              </div>
              <div class="feature-text">
                <h3>최적의 포트폴리오</h3>
                <p>투자 성향에 맞는 최적의 포트폴리오를 구성하고 정기적인 리밸런싱 전략을 제안합니다.</p>
              </div>
            </div>
            
            <div class="feature">
              <div class="feature-icon">
                <i class="icon-goal">🎯</i>
              </div>
              <div class="feature-text">
                <h3>목표 달성 로드맵</h3>
                <p>주택 구매, 은퇴 계획 등 장기 금융 목표 달성을 위한 구체적인 로드맵을 제시합니다.</p>
              </div>
            </div>
          </div>
          
          <button class="cta-button">무료 상담 시작하기</button>
        </div>
        
        <div class="advisor-image">
          <div class="chat-ui">
            <div class="chat-header">
              <div class="chat-avatar">🤖</div>
              <div class="chat-title">EA$E AI 어드바이저</div>
            </div>
            <div class="chat-body">
              <div class="message ai-message">
                <span>안녕하세요! 어떤 금융 목표를 가지고 계신가요?</span>
              </div>
              <div class="message user-message">
                <span>주택 구입을 위해 저축하고 있어요.</span>
              </div>
              <div class="message ai-message">
                <span>목표 금액과 기간이 어떻게 되시나요?</span>
              </div>
              <div class="message user-message">
                <span>5년 내에 5억원이 필요해요.</span>
              </div>
              <div class="message ai-message">
                <span>월 저축 가능액과 현재 보유 자산을 알려주시면 맞춤형 계획을 세워드릴게요.</span>
              </div>
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div class="chat-input">
              <input type="text" placeholder="메시지를 입력하세요..." disabled />
              <button class="send-button" disabled>▶</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// 컴포넌트 로직이 필요하면 여기에 추가
</script>

<style scoped>
.ai-advisor-section {
  padding: 5rem 0;
  background-color: #f0f4ff;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
  overflow: hidden;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 1rem;
}

.section-desc {
  font-size: 1.1rem;
  color: #666;
  text-align: center;
  margin-bottom: 3rem;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.advisor-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.advisor-features {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
  margin-bottom: 2.5rem;
}

.feature {
  display: flex;
  gap: 1.2rem;
  align-items: flex-start;
}

.feature-icon {
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.1);
  font-size: 1.5rem;
}

.feature-text h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.feature-text p {
  color: #555;
  line-height: 1.6;
}

.cta-button {
  padding: 0.9rem 2rem;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);
}

.advisor-image {
  position: relative;
}

.chat-ui {
  width: 100%;
  max-width: 400px;
  height: 500px;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}

.chat-header {
  padding: 1rem;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.chat-avatar {
  width: 35px;
  height: 35px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.chat-title {
  font-weight: 600;
  font-size: 1.1rem;
}

.chat-body {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  background-color: #f8faff;
}

.message {
  max-width: 80%;
  padding: 0.8rem 1rem;
  border-radius: 18px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  line-height: 1.5;
  font-size: 0.95rem;
  position: relative;
}

.ai-message {
  background: white;
  align-self: flex-start;
  border-bottom-left-radius: 5px;
}

.user-message {
  background: #007bff;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 5px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0.8rem 1rem;
  background: white;
  border-radius: 18px;
  width: fit-content;
  margin-top: 0.5rem;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #ccc;
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0% {
    transform: scale(0.7);
    opacity: 0.5;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(0.7);
    opacity: 0.5;
  }
}

.chat-input {
  padding: 1rem;
  display: flex;
  gap: 0.5rem;
  background: white;
  border-top: 1px solid #eee;
}

.chat-input input {
  flex: 1;
  padding: 0.7rem 1rem;
  border: 1px solid #ddd;
  border-radius: 25px;
  outline: none;
  font-size: 0.95rem;
}

.chat-input input:focus {
  border-color: #007bff;
}

.send-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .advisor-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .advisor-image {
    order: -1;
  }
  
  .chat-ui {
    height: 400px;
  }
}

@media (max-width: 576px) {
  .section-title {
    font-size: 1.8rem;
  }
  
  .section-desc {
    font-size: 1rem;
  }
  
  .feature {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .feature-text h3 {
    margin-top: 0.5rem;
  }
}
</style>