<template>
  <section class="ai-advisor-section">
    <div class="content-container">
      <h2 class="section-title">AI 금융 상담</h2>
      <p class="section-desc">당신의 재무 상황에 맞는 1:1 맞춤형 금융 상담을 AI가 도와드립니다.</p>
      
      <div class="view-toggle">
        <button 
          :class="['toggle-btn', activeView === 'info' ? 'active' : '']" 
          @click="setActiveView('info')">
          서비스 안내
        </button>
        <button 
          :class="['toggle-btn', activeView === 'chat' ? 'active' : '']" 
          @click="setActiveView('chat')">
          상담 시작하기
        </button>
      </div>
      
      <!-- 서비스 소개 뷰 -->
      <div v-if="activeView === 'info'" class="advisor-content">
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
          
          <button class="cta-button" @click="setActiveView('chat')">무료 상담 시작하기</button>
        </div>
        
        <div class="advisor-image">
          <div class="chat-ui demo-chat">
            <div class="chat-header">
              <div class="chat-avatar">🤖</div>
              <div class="chat-title">EA$E AI 어드바이저</div>
            </div>
            <div class="chat-body">
              <div class="message ai-message">
                <span>안녕하세요! EA$E AI 금융 어드바이저입니다. 어떤 금융 목표를 달성하고 싶으신가요?</span>
              </div>
              <div class="message user-message">
                <span>주택 구매를 위해 돈을 모으고 있어요. 어떻게 해야 할까요?</span>
              </div>
              <div class="message ai-message">
                <span>주택 구매를 위한 저축은 목표 금액, 시간, 현재 자산 상태에 따라 전략이 달라집니다. 재무 정보를 입력하시면 맞춤형 전략을 제안해드릴게요.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 상담 시작 뷰 -->
      <div v-else-if="activeView === 'chat'" class="chat-view">
        <div v-if="showFinancialForm" class="form-container">
          <FinancialDataForm 
            @submit="handleFormSubmit" 
            @cancel="showFinancialForm = false" 
          />
        </div>
        
        <div v-else class="chat-container">
          <div class="chat-options">
            <button class="option-btn" @click="showFinancialForm = true">
              <span class="option-icon">📋</span>
              재무 정보 입력
            </button>
            <button class="option-btn" v-if="financialData" @click="showFinancialSummary = !showFinancialSummary">
              <span class="option-icon">📊</span>
              재무 정보 보기
            </button>
            <button class="option-btn" @click="showMarketData = !showMarketData">
              <span class="option-icon">📈</span>
              시장 데이터
            </button>
          </div>
          
          <MarketDataWidget v-if="showMarketData" class="market-data-section" />
          
          <div v-if="showFinancialSummary && financialData" class="financial-summary">
            <h4>재무 정보 요약</h4>
            <div class="summary-content">
              <div class="summary-text">
                <ul>
                  <li><strong>연령대:</strong> {{ financialData.ageGroup }}</li>
                  <li><strong>월 소득:</strong> {{ financialData.monthlyIncome }}만원</li>
                  <li><strong>자산 총액:</strong> {{ getTotalAssets() }}만원</li>
                  <li><strong>부채 총액:</strong> {{ getTotalDebt() }}만원</li>
                  <li><strong>금융 목표:</strong> {{ financialData.financialGoal }}</li>
                  <li><strong>투자 성향:</strong> {{ financialData.riskTolerance }}</li>
                </ul>
              </div>
              
              <div class="charts-toggle">
                <button class="show-charts-btn" @click="showCharts = !showCharts">
                  {{ showCharts ? '차트 숨기기' : '차트 보기' }}
                </button>
              </div>
            </div>
            
            <div v-if="showCharts" class="charts-container">
              <FinancialCharts :financialData="financialData" />
            </div>
            
            <button class="close-summary-btn" @click="showFinancialSummary = false">닫기</button>
          </div>
          
          <div class="chat-ui">
            <div class="chat-header">
              <div class="chat-avatar">🤖</div>
              <div class="chat-title">EA$E AI 어드바이저</div>
              <button class="data-btn" @click="showFinancialForm = true" title="재무 정보 입력">
                <span class="data-icon">📋</span>
              </button>
            </div>
            <div class="chat-body" ref="chatBody">
              <div v-for="(message, index) in messages" :key="index" 
                   :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']">
                <span>{{ message.content }}</span>
              </div>
              <div v-if="isLoading" class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div class="chat-input">
              <input type="text" 
                     v-model="userMessage" 
                     placeholder="메시지를 입력하세요..." 
                     @keyup.enter="sendMessage" />
              <button class="send-button" 
                      :disabled="!userMessage.trim() || isLoading" 
                      @click="sendMessage">▶</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, computed } from 'vue';
import axios from 'axios';
import FinancialDataForm from './FinancialDataForm.vue';
import FinancialCharts from './FinancialCharts.vue';
import MarketDataWidget from './MarketDataWidget.vue';

// 뷰 관리 상태
const activeView = ref('info'); // 'info' 또는 'chat'
const showFinancialForm = ref(false);
const showFinancialSummary = ref(false);
const showCharts = ref(false);
const showMarketData = ref(false);
const financialData = ref(null);

// 채팅 관련 상태
const userMessage = ref('');
const messages = ref([
  { role: 'assistant', content: '안녕하세요! EA$E AI 금융 어드바이저입니다. 어떤 금융 목표를 가지고 계신가요? 더 정확한 상담을 위해 상단의 재무 정보 입력 버튼을 클릭하여 정보를 입력해주세요.' }
]);
const isLoading = ref(false);
const chatBody = ref(null);

// 활성 뷰 설정
const setActiveView = (view) => {
  activeView.value = view;
  if (view === 'chat') {
    scrollToBottom();
  }
};

// 재무 정보 합계 계산
const getTotalAssets = () => {
  if (!financialData.value) return 0;
  return (
    (financialData.value.savings || 0) +
    (financialData.value.stocks || 0) +
    (financialData.value.realestate || 0)
  );
};

const getTotalDebt = () => {
  if (!financialData.value) return 0;
  return (
    (financialData.value.loans || 0) +
    (financialData.value.creditCardDebt || 0)
  );
};

// 폼 제출 처리
const handleFormSubmit = async (formData) => {
  // 재무 정보 저장
  financialData.value = formData;
  showFinancialForm.value = false;
  
  // 재무 정보 요약 메시지 추가
  const summaryMessage = `
    재무 정보를 분석했습니다:
    - 연령대: ${formData.ageGroup}
    - 소득: 월 ${formData.monthlyIncome}만원 (지출: ${formData.monthlyExpense}만원)
    - 자산: ${getTotalAssets()}만원 (예금: ${formData.savings}만원, 투자: ${formData.stocks}만원, 부동산: ${formData.realestate}만원)
    - 부채: ${getTotalDebt()}만원
    - 금융목표: ${formData.financialGoal} (${formData.investmentTimeframe} 기간)
    - 투자성향: ${formData.riskTolerance}
    
    이제 어떤 금융 조언이 필요하신가요?
  `;
  
  // 시스템이 재무 정보를 분석했다는 메시지 추가
  messages.value.push({ role: 'assistant', content: summaryMessage.trim() });
  
  // 스크롤 처리
  await scrollToBottom();
  
  // 재무 데이터를 기반으로 백엔드로 초기 금융 조언 요청
  if (financialData.value) {
    isLoading.value = true;
    
    try {
      // 대화 컨텍스트와 함께 재무 정보 전송
      const context = messages.value
        .slice(-10)
        .map(msg => ({
          role: msg.role === 'user' ? 'user' : 'assistant',
          content: msg.content
        }));
      
      const response = await axios.post('/advisor/chat/', {
        message: `사용자 재무 상태 분석: ${formData.financialGoal}을 목표로 하는 ${formData.ageGroup} 고객의 금융 상담`,
        context: context,
        financial_data: financialData.value
      });
      
      if (response.data.success) {
        // AI 응답 추가
        messages.value.push({ role: 'assistant', content: response.data.response });
      } else {
        // 오류 메시지 표시
        messages.value.push({ role: 'assistant', content: '죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.' });
      }
    } catch (error) {
      console.error('AI 어드바이저 통신 오류:', error);
      messages.value.push({ role: 'assistant', content: '죄송합니다. 서버와의 통신 중 오류가 발생했습니다.' });
    } finally {
      isLoading.value = false;
      await scrollToBottom();
    }
  }
};

// 메시지 스크롤 처리
const scrollToBottom = async () => {
  await nextTick();
  if (chatBody.value) {
    chatBody.value.scrollTop = chatBody.value.scrollHeight;
  }
};

// 메시지 전송
const sendMessage = async () => {
  if (!userMessage.value.trim() || isLoading.value) return;
  
  // 사용자 메시지 추가
  const message = userMessage.value;
  messages.value.push({ role: 'user', content: message });
  userMessage.value = '';
  
  // 스크롤 애니메이션
  await scrollToBottom();
  
  // AI 응답 로딩 시작
  isLoading.value = true;
  
  try {
    // 대화 컨텍스트 구성 (최근 10개 메시지만 전송)
    const context = messages.value
      .slice(-10)
      .map(msg => ({
        role: msg.role === 'user' ? 'user' : 'assistant',
        content: msg.content
      }));
    
    // API 요청 데이터
    const requestData = {
      message: message,
      context: context
    };
    
    // 재무 정보가 있으면 추가
    if (financialData.value) {
      requestData.financial_data = financialData.value;
    }
    
    // API 요청
    const response = await axios.post('/advisor/chat/', requestData);
    
    if (response.data.success) {
      // AI 응답 추가
      messages.value.push({ role: 'assistant', content: response.data.response });
    } else {
      // 오류 메시지 표시
      messages.value.push({ role: 'assistant', content: '죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.' });
    }
  } catch (error) {
    console.error('AI 어드바이저 통신 오류:', error);
    messages.value.push({ role: 'assistant', content: '죄송합니다. 서버와의 통신 중 오류가 발생했습니다.' });
  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};

// 메시지가 추가될 때마다 스크롤 하단으로 이동
watch(messages, scrollToBottom, { deep: true });

// 컴포넌트 마운트시 초기화
onMounted(() => {
  scrollToBottom();
});
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

/* 뷰 전환 스타일 */
.view-toggle {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.toggle-btn {
  padding: 0.7rem 1.5rem;
  border: none;
  background: #f0f4ff;
  border-radius: 30px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e0e0ff;
}

.toggle-btn.active {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  box-shadow: 0 3px 10px rgba(0, 123, 255, 0.2);
}

/* 채팅 뷰 스타일 */
.chat-view {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.chat-container {
  display: flex;
  flex-direction: column;
}

.chat-options {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.option-btn {
  padding: 0.6rem 1rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
}

.option-btn:hover {
  background: #f8f8f8;
  border-color: #ccc;
}

.option-icon {
  font-size: 1.2rem;
}

.data-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  margin-left: auto;
  color: rgba(255, 255, 255, 0.8);
}

.data-icon {
  font-size: 1.2rem;
}

/* 재무 정보 요약 스타일 */
.financial-summary {
  background: white;
  border-radius: 10px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.financial-summary h4 {
  margin-bottom: 1rem;
  color: #007bff;
  font-weight: 600;
}

.summary-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.summary-text {
  flex-grow: 1;
}

.financial-summary ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
}

.financial-summary li {
  color: #444;
}

.charts-toggle {
  margin-left: 1rem;
}

.show-charts-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.show-charts-btn:hover {
  box-shadow: 0 3px 8px rgba(0, 123, 255, 0.3);
}

.charts-container {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.close-summary-btn {
  position: absolute;
  top: 0.8rem;
  right: 0.8rem;
  background: none;
  border: none;
  color: #888;
  font-size: 0.9rem;
  cursor: pointer;
}

.close-summary-btn:hover {
  color: #333;
}

.market-data-section {
  margin-bottom: 1.5rem;
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 데모 채팅 스타일 */
.demo-chat {
  pointer-events: none;
}

/* 미디어 쿼리 추가 */
@media (max-width: 768px) {
  .financial-summary ul {
    grid-template-columns: 1fr;
  }
}
</style>