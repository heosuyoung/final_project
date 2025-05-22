<template>
  <section class="main-section">
    <div class="main-content">
      <h1 class="main-title">금융이 쉬워지는<br />맞춤형 서비스 <span class="brand">EA$E</span></h1>
      <div class="main-emoji">
        <img src="/piggy-bank.png" alt="이모티콘" />
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

.main-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
  gap: 3rem;
}

.main-title {
  font-size: 3.2rem;
  font-weight: 800;
  color: #222;
  line-height: 1.2;
  margin-bottom: 2.5rem;
  margin-top: 0;
}

.brand {
  color: #007bff;
}

.main-emoji {
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.main-emoji img {
  width: 180px;
  height: 180px;
  border-radius: 2.5rem;
  background: #fffbe7;
  box-shadow: 0 4px 24px #0001;
  object-fit: contain;
}

@media (max-width: 900px) {
  .main-title {
    font-size: 2.1rem;
  }
  .main-emoji img {
    width: 120px;
    height: 120px;
  }
}
</style> 