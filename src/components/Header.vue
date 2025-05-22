<template>
  <header :class="{ 'header': true, 'scrolled-or-hovered': isHeaderScrolled || isHeaderHovered }"
    @mouseover="handleMouseOver"
    @mouseout="handleMouseOut">
    <div class="header-inner">
      <div class="logo-area">
        <img src="/dollar-logo.png" alt="Logo" class="logo-img" />
        <span class="logo-text">EA$E</span>
      </div>
      <nav class="nav">
        <ul>
          <li><a href="#">상품추천</a></li>
          <li><a href="#">관심종목정보 검색</a></li>
          <li><a href="#">현물가격변동(환율)</a></li>
          <li><a href="#">주변은행검색</a></li>
        </ul>
      </nav>
      <div class="auth-buttons">
        <button class="login">로그인</button>
        <button class="signup">회원가입</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isHeaderScrolled = ref(false);
const isHeaderHovered = ref(false);

const handleScroll = () => {
  isHeaderScrolled.value = window.scrollY > 50; // 50px 이상 스크롤 시 변경
};

const handleMouseOver = () => {
  isHeaderHovered.value = true;
};

const handleMouseOut = () => {
  isHeaderHovered.value = false;
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
  z-index: 1000;
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
  width: 100vw;
  min-width: 1200px;
  max-width: 100vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  margin: 0;
  padding: 0 48px;
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
  border: 1.5px solid #111;
  background: #fff;
  color: #111;
  padding: 0.8rem 2.2rem;
  border-radius: 24px;
  font-size: 1.15rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.signup {
  background: #007bff;
  border-color: #007bff;
  color: #fff;
}

.login:hover {
  background: #f5f5f5;
}

.signup:hover {
  background: #0056b3;
  border-color: #0056b3;
}

@media (max-width: 1400px) {
  .header-inner {
    min-width: 0;
    padding: 0 16px;
  }
  .nav ul {
    gap: 32px;
  }
  .login, .signup {
    padding: 0.8rem 1.2rem;
  }
}
</style> 