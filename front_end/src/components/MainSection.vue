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
  </section>
</template>

<script>
export default {
  name: 'MainSection',
};
</script>

<style scoped>
.main-section {
  min-height: 60vh;
  background: #f3e3e3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5rem 0 3rem 0;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
}

.main-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 2200px;
  gap: 16rem;
  margin: 0 auto;
}

.main-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  height: 100%;
}

.main-text-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  gap: 0.2em;
}

.main-line1, .main-line2 {
  font-size: 5rem;
  font-weight: 700;
  color: #222;
  letter-spacing: -1px;
  line-height: 1.2;
  text-align: right;
}

.main-ease {
  color: #007bff;
  font-size: 5.5rem;
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
  justify-content: flex-end;
  height: 100%;
}

.main-img-bg {
  background: #f3e3e3;
  border-radius: 2.5rem;
  width: 800px;
  height: 800px;
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

@media (max-width: 1200px) {
  .main-row {
    gap: 2rem;
  }
  .main-img-bg {
    width: 220px;
    height: 220px;
  }
}

@media (max-width: 900px) {
  .main-row {
    flex-direction: column;
    gap: 2rem;
  }
  .main-left, .main-right {
    width: 100%;
    justify-content: center;
    align-items: center;
  }
  .main-text-group {
    align-items: center;
  }
  .main-line1, .main-line2 {
    font-size: 1.3rem;
    text-align: center;
  }
  .main-ease {
    font-size: 1.5rem;
    text-align: center;
  }
  .main-img-bg {
    width: 120px;
    height: 120px;
  }
}
</style> 