<template>
  <div class="financial-data-form">
    <h3>재무 상황 입력</h3>
    <p>더 정확한 금융 상담을 위해 귀하의 재무 상황을 알려주세요.</p>
    
    <form @submit.prevent="submitForm">
      <div class="form-section">
        <h4>기본 정보</h4>
        <div class="form-group">
          <label for="age">연령대</label>
          <select id="age" v-model="formData.ageGroup" required>
            <option value="">선택해주세요</option>
            <option value="20대">20대</option>
            <option value="30대">30대</option>
            <option value="40대">40대</option>
            <option value="50대">50대</option>
            <option value="60대 이상">60대 이상</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="income">월평균 소득</label>
          <div class="input-with-unit">
            <input type="number" id="income" v-model.number="formData.monthlyIncome" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="expense">월평균 지출</label>
          <div class="input-with-unit">
            <input type="number" id="expense" v-model.number="formData.monthlyExpense" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
      </div>
      
      <div class="form-section">
        <h4>자산 현황</h4>
        <div class="form-group">
          <label for="savings">예금/적금</label>
          <div class="input-with-unit">
            <input type="number" id="savings" v-model.number="formData.savings" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="stocks">주식/펀드</label>
          <div class="input-with-unit">
            <input type="number" id="stocks" v-model.number="formData.stocks" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="realestate">부동산</label>
          <div class="input-with-unit">
            <input type="number" id="realestate" v-model.number="formData.realestate" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
      </div>
      
      <div class="form-section">
        <h4>부채 현황</h4>
        <div class="form-group">
          <label for="loan">대출 잔액</label>
          <div class="input-with-unit">
            <input type="number" id="loan" v-model.number="formData.loans" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="credit">신용카드 부채</label>
          <div class="input-with-unit">
            <input type="number" id="credit" v-model.number="formData.creditCardDebt" min="0" required>
            <span class="unit">만원</span>
          </div>
        </div>
      </div>
      
      <div class="form-section">
        <h4>금융 목표</h4>
        <div class="form-group">
          <label for="goal">주요 금융 목표</label>
          <select id="goal" v-model="formData.financialGoal" required>
            <option value="">선택해주세요</option>
            <option value="단기 저축">단기 저축 (6개월 ~ 1년)</option>
            <option value="주택 구입">주택 구입</option>
            <option value="자녀 교육">자녀 교육 자금</option>
            <option value="은퇴 준비">은퇴 준비</option>
            <option value="부채 상환">부채 상환</option>
            <option value="투자 수익률 향상">투자 수익률 향상</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="risk">투자 성향</label>
          <select id="risk" v-model="formData.riskTolerance" required>
            <option value="">선택해주세요</option>
            <option value="안정형">안정형 (원금 보존 우선)</option>
            <option value="중립형">중립형 (안정성과 수익성 균형)</option>
            <option value="수익형">수익형 (높은 수익 추구)</option>
            <option value="공격형">공격형 (최대 수익 추구, 위험 감수)</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="timeframe">투자 기간</label>
          <select id="timeframe" v-model="formData.investmentTimeframe" required>
            <option value="">선택해주세요</option>
            <option value="단기 (1년 미만)">단기 (1년 미만)</option>
            <option value="중기 (1~5년)">중기 (1~5년)</option>
            <option value="장기 (5~10년)">장기 (5~10년)</option>
            <option value="초장기 (10년 이상)">초장기 (10년 이상)</option>
          </select>
        </div>
      </div>
      
      <div class="form-section">
        <h4>추가 정보</h4>
        <div class="form-group">
          <label for="additional">추가 질문 또는 고려사항</label>
          <textarea id="additional" v-model="formData.additionalInfo" rows="3" placeholder="금융 상담에 도움이 될 추가 정보를 입력해주세요."></textarea>
        </div>
      </div>
      
      <div class="form-actions">
        <button type="button" class="cancel-button" @click="cancelForm">취소</button>
        <button type="submit" class="submit-button">분석 시작하기</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({
  ageGroup: '',
  monthlyIncome: null,
  monthlyExpense: null,
  savings: null,
  stocks: null,
  realestate: null,
  loans: null,
  creditCardDebt: null,
  financialGoal: '',
  riskTolerance: '',
  investmentTimeframe: '',
  additionalInfo: ''
});

const submitForm = () => {
  // 폼 데이터를 부모 컴포넌트로 전달
  emit('submit', { ...formData.value });
};

const cancelForm = () => {
  // 취소 이벤트 발생
  emit('cancel');
};
</script>

<style scoped>
.financial-data-form {
  background-color: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

p {
  color: #666;
  margin-bottom: 1.5rem;
}

.form-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.form-section:last-child {
  border-bottom: none;
}

h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #007bff;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #444;
}

input, select, textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus, select:focus, textarea:focus {
  border-color: #007bff;
  outline: none;
}

.input-with-unit {
  position: relative;
}

.input-with-unit input {
  padding-right: 3.5rem;
}

.unit {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.submit-button, .cancel-button {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.submit-button {
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  flex-grow: 1;
  margin-left: 0.5rem;
}

.cancel-button {
  background: #f5f5f5;
  color: #555;
  border: 1px solid #ddd;
}

.submit-button:hover {
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
}

.cancel-button:hover {
  background: #eee;
}

@media (max-width: 576px) {
  .financial-data-form {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .submit-button, .cancel-button {
    width: 100%;
    margin: 0;
  }
}
</style>
