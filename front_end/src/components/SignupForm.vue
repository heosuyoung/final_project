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
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup } from '../services/auth.js'

const router = useRouter()
const isLoading = ref(false)
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

const onSubmit = async () => {
  // 유효성 검사
  if (form.username.length < 4) {
    alert('아이디는 최소 4자 이상이어야 합니다.')
    return
  }
  
  if (form.password.length < 6) {
    alert('비밀번호는 최소 6자 이상이어야 합니다.')
    return
  }
  
  if (form.birth.length !== 8 || isNaN(form.birth)) {
    alert('생년월일은 8자리 숫자(YYYYMMDD)로 입력해주세요.')
    return
  }
  
  isLoading.value = true
  
  try {
    // auth 서비스를 통한 회원가입 API 호출
    await signup(form)
    
    alert('회원가입 완료! 로그인 페이지로 이동합니다.')
    router.push('/login')
  } catch (error) {
    console.error('회원가입 처리 중 오류 발생:', error)
    alert(error.message || '회원가입 처리 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
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
  max-width: 600px; /* 최대 너비 제한 */
  margin: 0 auto;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 8px 40px #007bff11, 0 2px 16px #0002;
  padding: 3rem 4rem; /* 패딩 축소 */
  box-sizing: border-box;
}

.signup-logo {
  font-size: 2.2rem;
  font-weight: 900;
  color: #007bff;
  letter-spacing: 2px;
  margin-bottom: 2rem;
  text-align: center;
}

.signup-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  align-items: stretch; /* 핵심: 내부 요소 가득 차게 */
}

.signup-form input,
.signup-form select,
.signup-btn {
  width: 100%;
  max-width: 100%;
  min-width: 100%;
  font-size: 1rem;
  padding: 0.9rem 1.2rem;
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
  gap: 2rem;
  justify-content: center;
  margin: 0.5rem 0 0.2rem 0;
}

.nationality-group label {
  font-size: 0.95rem;
  color: #333;
}

.terms-group {
  margin: 0.5rem 0 0.2rem 0;
  font-size: 0.95rem;
  color: #007bff;
  display: flex;
  align-items: center;
}

.signup-btn {
  background: linear-gradient(90deg, #7ecbff 0%, #007bff 100%);
  color: #fff;
  font-size: 1.1rem;
  font-weight: 700;
  border: none;
  border-radius: 10px;
  padding: 1rem 0;
  margin-top: 0.8rem;
  cursor: pointer;
  box-shadow: 0 4px 18px #007bff22;
  transition: background 0.2s;
}

.signup-btn:hover {
  background: linear-gradient(90deg, #4fa3e3 0%, #0056b3 100%);
}

@media (max-width: 1000px) {
  .signup-container {
    max-width: 90vw;
    padding: 1.5rem 1rem;
    border-radius: 16px;
  }

  .signup-logo {
    font-size: 1.8rem;
    margin-bottom: 1rem;
  }

  .signup-form input,
  .signup-form select {
    font-size: 0.9rem;
    padding: 0.7rem 0.6rem;
    border-radius: 6px;
  }

  .signup-btn {
    font-size: 1rem;
    padding: 0.8rem 0;
    border-radius: 6px;
  }
}

</style>

:global(body), :global(html) {
  background: #fff !important;
}