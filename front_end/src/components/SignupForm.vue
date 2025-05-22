<template>
  <div class="signup-bg">
    <div class="signup-container">
      <div class="signup-logo">EA$E</div>
      <form class="signup-form" @submit.prevent="onSubmit">
        <input v-model="form.username" type="text" placeholder="아이디" required />
        <input v-model="form.password" type="password" placeholder="비밀번호" required />
        <input v-model="form.email" type="email" placeholder="이메일 (선택)" />
        <input v-model="form.name" type="text" placeholder="이름" required />
        <input v-model="form.birth" type="text" maxlength="8" placeholder="생년월일 8자리" required />
        <select v-model="form.gender" required>
          <option value="">성별 선택</option>
          <option value="male">남자</option>
          <option value="female">여자</option>
        </select>
        <div class="nationality-group">
          <label>
            <input type="radio" value="domestic" v-model="form.nationality" required /> 내국인
          </label>
          <label>
            <input type="radio" value="foreigner" v-model="form.nationality" required /> 외국인
          </label>
        </div>
        <div class="terms-group">
          <label>
            <input type="checkbox" v-model="form.terms" required />
            <span>EA$E 이용약관 전체동의</span>
          </label>
        </div>
        <button class="signup-btn" type="submit">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  username: '',
  password: '',
  email: '',
  name: '',
  birth: '',
  gender: '',
  nationality: '',
  terms: false,
})

const onSubmit = () => {
  // TODO: 실제 회원가입 API 연동
  alert('회원가입 완료!')
}
</script>

<style scoped>
.signup-bg {
  min-height: 100vh;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.signup-container {
  width: 100%;
  max-width: none; /* ← 제한 없앰 */
  margin: 0 auto;
  background: #fff;
  border-radius: 32px;
  box-shadow: 0 8px 40px #007bff11, 0 2px 16px #0002;
  padding: 5rem 8rem; /* ← 좌우 여유 줌 */
  box-sizing: border-box;
}

.signup-logo {
  font-size: 2.7rem;
  font-weight: 900;
  color: #007bff;
  letter-spacing: 2.5px;
  margin-bottom: 2.5rem;
  text-align: center;
}

.signup-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.7rem;
  align-items: stretch; /* 핵심: 내부 요소 가득 차게 */
}

.signup-form input,
.signup-form select,
.signup-btn {
  width: 100%;
  max-width: 100%;
  min-width: 100%;
  font-size: 1.25rem;
  padding: 1.3rem 1.7rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: #fafbfc;
  outline: none;
  transition: border 0.2s;
  box-sizing: border-box;
}

.signup-form input:focus,
.signup-form select:focus {
  border: 1.5px solid #007bff;
  background: #fff;
}

.nationality-group {
  display: flex;
  gap: 3.5rem;
  justify-content: center;
  margin: 0.7rem 0 0.3rem 0;
}

.nationality-group label {
  font-size: 1.15rem;
  color: #333;
}

.terms-group {
  margin: 0.7rem 0 0.3rem 0;
  font-size: 1.1rem;
  color: #007bff;
  display: flex;
  align-items: center;
}

.signup-btn {
  background: linear-gradient(90deg, #7ecbff 0%, #007bff 100%);
  color: #fff;
  font-size: 1.35rem;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  padding: 1.3rem 0;
  margin-top: 1.1rem;
  cursor: pointer;
  box-shadow: 0 4px 18px #007bff22;
  transition: background 0.2s;
}

.signup-btn:hover {
  background: linear-gradient(90deg, #4fa3e3 0%, #0056b3 100%);
}

@media (max-width: 1000px) {
  .signup-container {
    max-width: 98vw;
    padding: 2rem 0.5rem;
    border-radius: 16px;
  }

  .signup-logo {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .signup-form input,
  .signup-form select {
    font-size: 1rem;
    padding: 0.8rem 0.7rem;
    border-radius: 7px;
  }

  .signup-btn {
    font-size: 1.1rem;
    padding: 0.9rem 0;
    border-radius: 7px;
  }
}

</style>

:global(body), :global(html) {
  background: #fff !important;
} 