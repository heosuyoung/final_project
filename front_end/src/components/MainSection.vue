<template>
  <section class="main-section">
    <div class="main-row">
      <div class="main-left">
        <div class="main-text-group">
          <div class="main-line1">금융이 쉬워지는</div>
          <div class="main-ease">EA$E</div>
          <div class="main-line2">맞춤형 서비스</div>
        </div>
      </div>
      <div class="main-right">
        <div class="main-img-bg">
          <img src="/lucky-bag.png" alt="복주머니 이모티콘" />
        </div>
      </div>
    </div>

    <!-- ✅ 관심 종목 슬라이드 추가 -->
    <FavoriteSlide />
  </section>
</template>

<script setup>
import FavoriteSlide from './FavoriteSlide.vue'
</script>

<style scoped>
.main-section {
  min-height: 50vh;
  background: #f3e3e3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0 2rem 0;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
}

.main-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  gap: 4rem;
  margin: 0 auto;
}

.main-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  height: 100%;
  padding-right: 2rem;
}

.main-text-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  gap: 0.2em;
}

.main-line1,
.main-line2 {
  font-size: 3.5rem;
  font-weight: 700;
  color: #222;
  letter-spacing: -1px;
  line-height: 1.2;
  text-align: right;
}

.main-ease {
  color: #007bff;
  font-size: 4rem;
  font-weight: 900;
  letter-spacing: 0.1em;
  margin: 0.1em 0 0.1em 0;
  line-height: 1.1;
  text-align: right;
}

.main-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  padding-left: 2rem;
}

.main-img-bg {
  background: #f3e3e3;
  border-radius: 2.5rem;
  width: 400px;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 24px #0001;
}

.main-img-bg img {
  width: 90%;
  height: 90%;
  object-fit: contain;
}

@media (max-width: 1400px) {
  .main-row {
    gap: 2rem;
  }
  .main-img-bg {
    width: 400px;
    height: 400px;
  }
  .main-line1,
  .main-line2 {
    font-size: 3rem;
  }
  .main-ease {
    font-size: 3.5rem;
  }
}

@media (max-width: 1200px) {
  .main-row {
    gap: 1.5rem;
  }
  .main-img-bg {
    width: 300px;
    height: 300px;
  }
  .main-line1,
  .main-line2 {
    font-size: 2.5rem;
  }
  .main-ease {
    font-size: 3rem;
  }
}

@media (max-width: 900px) {
  .main-row {
    flex-direction: column;
    gap: 2rem;
  }
  .main-left,
  .main-right {
    width: 100%;
    justify-content: center;
    align-items: center;
    padding-left: 0;
    padding-right: 0;
  }
  .main-text-group {
    align-items: center;
  }
  .main-line1,
  .main-line2 {
    font-size: 2rem;
    text-align: center;
  }
  .main-ease {
    font-size: 2.5rem;
    text-align: center;
  }
  .main-img-bg {
    width: 200px;
    height: 200px;
  }
}

@media (max-width: 600px) {
  .main-line1,
  .main-line2 {
    font-size: 1.5rem;
  }
  .main-ease {
    font-size: 2rem;
  }
  .main-img-bg {
    width: 150px;
    height: 150px;
  }
}
</style>
