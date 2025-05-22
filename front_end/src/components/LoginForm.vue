<template>
  <div class="login-form">
    <h2>로그인</h2>
    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />
    <div class="btn-group">
      <button @click="handleLogin">로그인</button>
      <button @click="register">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../services/auth.js'

const username = ref('')
const password = ref('')
const router = useRouter()
const isLoading = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    alert('아이디와 비밀번호를 모두 입력해주세요.')
    return
  }

  isLoading.value = true
  try {
    // auth 서비스를 통한 로그인 처리
    const result = await login(username.value, password.value)
    console.log('로그인 성공 결과:', result)
    
    alert('로그인 성공!')
    
    // URL에서 redirect 쿼리 파라미터 확인
    const redirect = router.currentRoute.value.query.redirect
    console.log('리다이렉션 경로:', redirect || '홈페이지')
    
    // 로컬 스토리지 확인
    console.log('인증 토큰 존재:', !!localStorage.getItem('token'))
    console.log('사용자 데이터 존재:', !!localStorage.getItem('user'))
    
    // 프로필 페이지 이동 시 페이지 새로고침 처리
    if (redirect === '/profile') {
      window.location.href = redirect
    } else {
      // 리다이렉트 경로가 있으면 해당 경로로, 없으면 홈으로 이동
      router.push(redirect || '/')
    }
  } catch (e) {
    console.error('로그인 오류:', e)
    alert(e.message || '로그인 실패')
  } finally {
    isLoading.value = false
  }
}

const register = () => {
  router.push('/signup')
}
</script>

<style scoped>
.login-form {
  width: 100%;
  max-width: 500px;
  margin: 3rem auto;
  padding: 3rem 3rem;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 8px 40px #007bff11, 0 2px 16px #0002;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  box-sizing: border-box;
}

h2 {
  font-size: 1.7rem;
  text-align: center;
  color: #007bff;
  font-weight: 700;
  margin-bottom: 1rem;
}

input {
  width: 100%;
  font-size: 1rem;
  padding: 0.9rem 1.2rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  background: #fafbfc;
  transition: border 0.2s;
}

input:focus {
  border-color: #007bff;
  background: #fff;
  outline: none;
}

.btn-group {
  display: flex;
  gap: 1rem;
}

button {
  flex: 1;
  font-size: 1rem;
  padding: 0.8rem 0;
  border: none;
  border-radius: 10px;
  background: linear-gradient(90deg, #7ecbff 0%, #007bff 100%);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 18px #007bff22;
  transition: background 0.2s;
}

button:hover {
  background: linear-gradient(90deg, #4fa3e3 0%, #0056b3 100%);
}

</style>