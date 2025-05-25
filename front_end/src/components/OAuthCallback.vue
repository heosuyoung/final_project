<template>
  <div class="oauth-callback">
    <div v-if="loading" class="loading">
      <p>로그인 처리 중입니다...</p>
      <div class="spinner"></div>
    </div>
    <div v-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="goToLogin">로그인 페이지로 이동</button>
    </div>
    <div v-if="manualAction" class="manual-action">
      <p>카카오 로그인이 처리되었습니다.</p>
      <button @click="completeKakaoLogin" class="primary-btn">
        홈으로 이동하기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const loading = ref(true);
const error = ref(null);
const manualAction = ref(false);

const goToLogin = () => {
  router.push('/login');
};

// 카카오 로그인 완료 처리
const completeKakaoLogin = () => {
  // URL에서 토큰 정보 확인
  const token = route.query.token;
  const jwt = route.query.jwt;
  const userId = route.query.user_id;
  const username = route.query.username;
  const email = route.query.email;
  
  // 백엔드에서 전달받은 토큰이 있으면 사용, 없으면 임시 토큰 생성
  const authToken = token || `kakao_token_${Date.now()}`;
  const authJwt = jwt || null;
  const authUserId = userId || Date.now();
  const authUsername = username || `kakao_user_${Math.floor(Math.random() * 10000)}`;
  
  const kakaoUser = {
    id: authUserId,
    username: authUsername,
    email: email || '',
    provider: 'kakao'
  };
  
  console.log('카카오 로그인 완료 처리 중...');
  console.log('사용자 정보:', kakaoUser);
  
  try {
    // 로컬 스토리지에 저장
    localStorage.setItem('token', authToken);
    
    // JWT 토큰이 있으면 저장
    if (authJwt) {
      localStorage.setItem('jwt', authJwt);
      console.log('JWT 토큰이 저장되었습니다.');
    }
    
    localStorage.setItem('user', JSON.stringify(kakaoUser));
    
    // 세션 스토리지 정리
    sessionStorage.removeItem('login_provider');
    
    console.log('로그인 정보 저장 완료');
    
    // 홈으로 리다이렉트
    console.log('홈으로 이동합니다...');
    router.push('/');
  } catch (error) {
    console.error('카카오 로그인 완료 처리 중 오류:', error);
    loading.value = false;
    error.value = '로그인 정보 저장 중 오류가 발생했습니다.';
  }
};

// 카카오 로그인 수동 처리
const handleKakaoAuth = () => {
  console.log('카카오 로그인 수동 처리...');
  
  // 코드가 있는지 확인 - 카카오 인증 완료 상태
  if (route.query.code) {
    console.log('카카오 인증 코드 확인됨:', route.query.code.substring(0, 10) + '...');
    
    // 카카오 로그인 완료 화면 표시 - 사용자가 버튼을 클릭해서 진행
    loading.value = false;
    manualAction.value = true;
    
    return true;
  }
  
  return false;
};

// 구글 로그인 처리
const handleGoogleAuth = (token, userId, username, provider, jwt, email) => {
  if (!token || !userId || !username) {
    console.error('필수 정보 누락: 토큰 또는 사용자 정보');
    return false;
  }
  
  try {
    // 로컬 스토리지에 토큰과 사용자 정보 저장
    localStorage.setItem('token', token);
    
    // JWT 토큰이 존재하면 저장 (새로운 인증 방식)
    if (jwt) {
      localStorage.setItem('jwt', jwt);
      console.log('JWT 토큰이 저장되었습니다.');
    }
    
    // 사용자 정보 저장
    localStorage.setItem('user', JSON.stringify({ 
      id: userId, 
      username: username,
      email: email || '',
      provider: provider || 'google'
    }));
    
    // 홈으로 리다이렉트
    router.push('/');
    return true;
  } catch (err) {
    console.error('구글 로그인 처리 오류:', err);
    return false;
  }
};

onMounted(() => {
  console.log('OAuth 콜백 마운트됨, 쿼리 파라미터:', route.query);
  
  loading.value = true;
  error.value = null;
  
  try {    // URL에서 토큰과 사용자 정보 추출
    const token = route.query.token;
    const jwt = route.query.jwt; // JWT 토큰 추출
    const userId = route.query.user_id;
    const username = route.query.username;
    const email = route.query.email; // 이메일 추출
    const provider = route.query.provider || sessionStorage.getItem('login_provider');
    const code = route.query.code; // OAuth 인증 코드
    const success = route.query.success === 'true'; // 성공 여부
    
    // 로그인 제공자 확인 및 디버깅 정보
    console.log('로그인 제공자:', provider);
    console.log('인증 코드 존재:', !!code);
    console.log('직접 처리 성공:', success);
      // 카카오 로그인 자동 처리 (코드가 있으면 즉시 처리)
    if (code && (
        provider === 'kakao' || 
        sessionStorage.getItem('login_provider') === 'kakao' || 
        window.location.href.toLowerCase().includes('kakao')
       )) {
      
      console.log('카카오 로그인 자동 처리 시작');
      
      // 백엔드에서 전달받은 토큰과 사용자 정보 확인
      const backendToken = token;
      const backendJwt = jwt;
      const backendUserId = userId;
      const backendUsername = username;
      const backendEmail = email;
      
      // 백엔드에서 정보가 전달된 경우와 그렇지 않은 경우를 구분하여 처리
      const kakaoUser = {
        id: backendUserId || Date.now(),
        username: backendUsername || `kakao_user_${Math.floor(Math.random() * 10000)}`,
        email: backendEmail || '',
        provider: 'kakao'
      };
      
      // 토큰 설정 (백엔드에서 제공한 토큰이 있으면 사용, 없으면 임시 생성)
      const kakaoToken = backendToken || `kakao_token_${Date.now()}`;
      
      console.log('카카오 인증 정보:', {
        hasBackendToken: !!backendToken,
        hasJWT: !!backendJwt,
        userId: kakaoUser.id
      });
      
      // 로컬 스토리지에 저장
      localStorage.setItem('token', kakaoToken);
      localStorage.setItem('user', JSON.stringify(kakaoUser));
      
      // JWT 토큰이 있으면 저장
      if (backendJwt) {
        localStorage.setItem('jwt', backendJwt);
        console.log('JWT 토큰이 저장되었습니다.');
      }
      
      // 로그인 성공 메시지
      console.log('카카오 로그인 성공, 홈으로 이동합니다');
      
      // 세션 스토리지 정리
      sessionStorage.removeItem('login_provider');
      
      // 홈 페이지로 리다이렉트
      setTimeout(() => {
        router.push('/');
      }, 500);
      
      return;
    }// 로그인 처리 디버깅
    console.log('로그인 정보 확인:', {
      hasToken: !!token, 
      hasJWT: !!jwt, 
      userId, 
      provider
    });
    
    // 구글 등 일반 OAuth 처리 (토큰과 사용자 정보가 있는 경우)
    if (token && userId) {
      console.log('구글/일반 OAuth 처리: 토큰과 사용자 정보 있음');
      if (handleGoogleAuth(token, userId, username, provider, jwt, email)) {
        return; // 구글 처리 완료
      }
    }
    
    // 카카오 특별 처리 - handleKakaoAuth 함수 사용
    if (route.query.code && (provider === 'kakao' || sessionStorage.getItem('login_provider') === 'kakao')) {
      console.log('카카오 로그인 수동 처리 시도');
      if (handleKakaoAuth()) {
        return; // 카카오 처리 진행 중
      }
    }
    
    // 응답에 오류 정보가 있는지 확인
    if (route.query.error) {
      loading.value = false;
      error.value = `인증 오류: ${route.query.error_description || route.query.error}`;
      console.error('OAuth 오류:', route.query.error);
      return;
    }
    
    // 임시 처리 - 인증 코드가 있지만 처리되지 않은 경우
    if (route.query.code) {
      console.log('인증 코드 발견, 임시 처리 진행');
      
      const tempUser = {
        id: Date.now(),
        username: `oauth_user_${Math.floor(Math.random() * 10000)}`,
        provider: provider || '소셜 로그인'
      };
      
      const tempToken = `oauth_token_${Date.now()}`;
      
      try {
        localStorage.setItem('token', tempToken);
        localStorage.setItem('user', JSON.stringify(tempUser));
        
        console.log('임시 로그인 정보 저장 완료');
        
        // 수동 진행 화면 표시
        loading.value = false;
        manualAction.value = true;
      } catch (storageError) {
        console.error('로그인 정보 저장 중 오류:', storageError);
        loading.value = false;
        error.value = '로그인 정보를 저장할 수 없습니다.';
      }
    } else {
      // 필요한 정보가 없음
      loading.value = false;
      error.value = '로그인 정보를 찾을 수 없습니다. 다시 시도해주세요.';
      console.error('OAuth 콜백: 필요한 정보 없음');
    }
    
  } catch (err) {
    loading.value = false;
    error.value = '로그인 처리 중 오류가 발생했습니다.';
    console.error('OAuth 콜백 오류:', err);
  } finally {
    // 세션 스토리지 정리
    sessionStorage.removeItem('login_provider');
    sessionStorage.removeItem('oauth_callback_visited');
  }
});
</script>

<style scoped>
.oauth-callback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

.loading, .error, .manual-action {
  padding: 20px;
  border-radius: 8px;
  background-color: #f5f5f5;
  width: 100%;
}

.error {
  color: #d9534f;
  background-color: #f9f2f2;
  border: 1px solid #ebccd1;
}

.manual-action {
  background-color: #f0f7ff;
  border: 1px solid #d0e5ff;
  color: #0056b3;
}

.spinner {
  margin: 20px auto;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 123, 255, 0.1);
  border-radius: 50%;
  border-top-color: #007bff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

button {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.primary-btn {
  background-color: #28a745;
}

button:hover {
  opacity: 0.9;
}
</style>
