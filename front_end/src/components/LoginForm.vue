<template>
  <div class="login-form">
    <h2>로그인</h2>
    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />
    <div class="btn-group">
      <button @click="handleLogin" :disabled="isLoading">{{ isLoading ? '로그인 중...' : '로그인' }}</button>
      <button @click="register" :disabled="isLoading">회원가입</button>
    </div>
    
    <div class="social-login">
      <div class="divider">
        <span>또는</span>
      </div>
      <button class="social-btn google" @click="handleGoogleLogin" :disabled="socialLoading">
        <img src="/google-logo.png" alt="Google" />
        Google로 로그인
      </button>
      <button class="social-btn kakao" @click="handleKakaoLogin" :disabled="socialLoading">
        <img src="/kakao-logo.png" alt="Kakao" />
        카카오로 로그인
      </button>
    </div>
    <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
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
const socialLoading = ref(false)
const errorMsg = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMsg.value = '아이디와 비밀번호를 모두 입력해주세요.'
    return
  }

  errorMsg.value = ''
  isLoading.value = true
  try {
    // 서버 API를 통해 로그인 처리
    console.log('로그인 시도:', username.value)
    const result = await login(username.value, password.value)
    
    // 로그인 성공 메시지 표시
    alert('로그인 성공!')

    if (typeof window !== 'undefined') {
      localStorage.setItem('username', username.value)
    }
      // URL에서 redirect 쿼리 파라미터 확인
    const redirect = router.currentRoute.value.query.redirect
    
    // 로그인 결과 확인
    console.log('로그인 성공 결과:', result)
    
    // 로컬 스토리지 확인 (서버에서 저장된 토큰과 사용자 데이터)
    console.log('인증 토큰 존재:', !!localStorage.getItem('token'))
    console.log('사용자 데이터 존재:', !!localStorage.getItem('user'))
    
    // 이미 로그인 성공 알림을 표시했으므로 이동만 처리
    if (redirect === '/profile') {
      // 프로필 페이지로 직접 이동 (새로고침으로 처리)
      window.location.href = redirect
    } else if (redirect) {
      // 리다이렉트 경로로 이동 후 새로고침
      router.push(redirect)
      setTimeout(() => window.location.reload(), 100)
    } else {
      // 홈으로 이동 후 새로고침
      router.push('/')
      setTimeout(() => window.location.reload(), 100)
    }
  } catch (e) {
    console.error('로그인 오류:', e)
    // 오류 발생 시 즉시 피드백 제공
    errorMsg.value = e.message || '로그인 실패'
  } finally {
    isLoading.value = false
  }
}

const register = () => {
  router.push('/signup')
}

const handleSocialLogin = (provider, url) => {
  try {
    socialLoading.value = true
    errorMsg.value = ''
    
    // 로그인 시도 전 현재 경로를 세션 스토리지에 저장 (복귀를 위해)
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.setItem('login_redirect', router.currentRoute.value.fullPath)
      // 로그인 제공자 정보 저장
      sessionStorage.setItem('login_provider', provider.toLowerCase())
    }
    
    console.log(`${provider} 로그인 시도 중...`)
    
    // 소셜 로그인 URL로 리디렉션
    window.location.href = url
  } catch (error) {
    console.error(`${provider} 로그인 오류:`, error)
    errorMsg.value = `${provider} 로그인 중 오류가 발생했습니다.`
    socialLoading.value = false
  }
}

const handleGoogleLogin = () => {
  // Google OAuth 로그인 처리
  handleSocialLogin('Google', "http://localhost:8000/oauth/login/google-oauth2/")
}

const handleKakaoLogin = () => {
  // Kakao OAuth 로그인 처리 - 직접 처리 방식
  try {
    socialLoading.value = true
    errorMsg.value = ''
    
    // 로그인 시도 전 현재 경로를 세션 스토리지에 저장 (복귀를 위해)
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.setItem('login_redirect', router.currentRoute.value.fullPath)
      // 카카오 로그인 표시
      sessionStorage.setItem('login_provider', 'kakao')
    }
    
    console.log('카카오 로그인 시도 중... (직접 처리 방식)')
    
    // 직접 구현한 카카오 로그인 엔드포인트로 리디렉션
    // 이 엔드포인트는 백엔드에서 카카오 인증 코드를 직접 처리하고
    // 프론트엔드에 완성된 토큰을 제공합니다
    const kakaoAuthUrl = "https://kauth.kakao.com/oauth/authorize"
    const client_id = "06a3d74ba43b6ca0c2ab80015a8ad417"
    const redirect_uri = "http://localhost:8000/accounts/kakao/callback/"
    
    const kakaoUrl = `${kakaoAuthUrl}?client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&response_type=code`
    
    // 카카오 로그인 페이지로 이동
    window.location.href = kakaoUrl
  } catch (error) {
    console.error('카카오 로그인 오류:', error)
    errorMsg.value = '카카오 로그인 중 오류가 발생했습니다.'
    socialLoading.value = false
  }
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

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
  box-shadow: none;
}

.social-login {
  width: 100%;
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1rem 0;
  color: #999;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid #ddd;
}

.divider span {
  padding: 0 1rem;
  font-size: 0.9rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 0.8rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.social-btn img {
  width: 1.5rem;
  height: 1.5rem;
}

.google {
  background: white;
  color: #444;
  border: 1px solid #ddd;
}

.google:hover {
  background: #f5f5f5;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.kakao {
  background: #FEE500;
  color: #000;
  border: none;
}

.kakao:hover {
  background: #f2d900;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.error-message {
  color: #d9534f;
  font-size: 0.9rem;
  margin-top: 1rem;
  text-align: center;
  background-color: #f9f2f2;
  padding: 0.5rem;
  border-radius: 6px;
}
</style>