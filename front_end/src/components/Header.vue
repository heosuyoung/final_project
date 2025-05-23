<template>
  <header :class="{ 'header': true, 'scrolled-or-hovered': isHeaderScrolled || isHeaderHovered }"
    @mouseover="handleMouseOver"
    @mouseout="handleMouseOut">
    <div class="header-inner">
      <div class="logo-area">
        <a class="logo-link" @click.prevent="goHome" href="/">
        <img src="/dollar-logo.png" alt="Logo" class="logo-img" />
        <span class="logo-text">EA$E</span>
        </a>
      </div>
      <nav class="nav">
        <ul>
          <li><a href="#">예적금 추천</a></li>
          <li><a href="#">주식 검색</a></li>
          <li><a href="#" @click.prevent="goToCommodities">현물가격변동(환율)</a></li>
          <li><a href="#" @click.prevent="goToMap">주변은행검색</a></li>
        </ul>
      </nav>
      <div class="auth-buttons">
        <template v-if="isLoggedIn">
          <button class="profile" @click="goToProfile">내 프로필</button>
          <button class="logout" @click="logout">로그아웃</button>
        </template>
        <template v-else>
          <button class="login" @click="goToLogin">로그인</button>
          <button class="signup" @click="goToSignup">회원가입</button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { isAuthenticated, logout as authLogout } from '../services/auth.js';

const isHeaderScrolled = ref(false);
const isHeaderHovered = ref(false);
const router = useRouter();
const route = useRoute();

// 로그인 상태를 ref로 관리
const authState = ref(isAuthenticated());

// 로그인 상태 확인 (computed로 참조)
const isLoggedIn = computed(() => {
  return authState.value;
});

// 라우트 변경 시 인증 상태 다시 확인 (중요: 로그인/로그아웃 후 상태 업데이트)
watch(() => route.path, () => {
  authState.value = isAuthenticated();
});

const handleScroll = () => {
  isHeaderScrolled.value = window.scrollY > 50; // 50px 이상 스크롤 시 변경
};

const handleMouseOver = () => {
  isHeaderHovered.value = true;
};

const handleMouseOut = () => {
  isHeaderHovered.value = false;
};

const goToSignup = () => {
  router.push('/signup');
};

const goHome = () => {
  router.push('/');
};

const goToLogin = () => {
  router.push('/login');
};

const goToProfile = () => {
  router.push('/profile');
};

const logout = () => {
  authLogout();
  authState.value = false; // 즉시 상태 업데이트
  router.push('/');
};

// ✅ 추가된 함수: 주변은행검색으로 이동
const goToMap = () => {
  router.push('/map');
};

// ✅ 추가된 함수: 현물가격변동(환율) 페이지로 이동
const goToCommodities = () => {
  router.push('/commodities');
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.header {
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  background: #f3e3e3;
  border-bottom: none;
  transition: background 0.3s, border-bottom 0.3s;
  padding: 0;
  height: 90px;
  display: flex;
  align-items: center;
  color: #111;
}

.header.scrolled-or-hovered {
  background: rgba(255,255,255,0.97);
  border-bottom: 1.5px solid #222;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.header-inner {
  width: 100%;
  max-width: 100vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  margin: 0;
  padding: 0 5%;
  box-sizing: border-box;
  gap: 0;
}

.logo-area,
.auth-buttons {
  flex-shrink: 0;
  overflow: visible;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-img {
  width: 32px;
  height: 32px;
  display: block;
}

.logo-text {
  font-size: 1.7rem;
  font-weight: 700;
  color: #111;
  display: inline-block;
  letter-spacing: 2px;
}

.nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav ul {
  display: flex;
  gap: 56px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav a {
  color: #111;
  text-decoration: none;
  font-size: 1.25rem;
  font-weight: 600;
  transition: color 0.2s;
  position: relative;
  padding: 30px 0;
}

.nav a:hover {
  color: #e57373;
}

.auth-buttons {
  display: flex;
  gap: 20px;
}

.login, .signup {
  border: none;
  padding: 0.8rem 2.2rem;
  border-radius: 24px;
  font-size: 1.15rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
}

.login {
  background: #f8dede;
  color: #222;
  border: 1.5px solid #e7bcbc;
  margin-right: 2px;
}

.login:hover {
  background: #f3e3e3;
  color: #007bff;
  box-shadow: 0 4px 16px #e7bcbc44;
}

.signup {
  background: linear-gradient(90deg, #7ecbff 0%, #007bff 100%);
  color: #fff;
  margin-left: 2px;
  box-shadow: 0 2px 12px #007bff22;
}

.signup:hover {
  background: linear-gradient(90deg, #4fa3e3 0%, #0056b3 100%);
  color: #fff;
  box-shadow: 0 4px 24px #007bff33;
}

.profile {
  background: #e3f2fd;
  color: #0056b3;
  border: 1.5px solid #0056b3;
  margin-right: 2px;
}

.profile:hover {
  background: #bbdefb;
  color: #004080;
  box-shadow: 0 4px 16px #007bff22;
}

.logout {
  background: #f5f5f5;
  color: #555;
  border: 1.5px solid #ddd;
  margin-left: 2px;
}

.logout:hover {
  background: #eeeeee;
  color: #e57373;
  border-color: #e57373;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  cursor: pointer;
}

@media (max-width: 1400px) {
  .header-inner {
    padding: 0 16px;
  }
  .nav ul {
    gap: 20px;
  }
  .login, .signup {
    padding: 0.7rem 1rem;
    font-size: 1rem;
  }
}

@media (max-width: 900px) {
  .header {
    height: auto;
    padding: 10px 0;
  }
  .header-inner {
    flex-direction: column;
    padding: 10px;
  }
  .nav {
    margin: 10px 0;
  }
  .nav ul {
    gap: 15px;
    padding: 0;
  }
  .auth-buttons {
    margin-top: 10px;
  }
  .login, .signup {
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
  }
}
</style>
