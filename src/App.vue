<script setup>
import Header from './components/Header.vue'
import MainSection from './components/MainSection.vue'
import StockComparisonSection from './components/StockComparisonSection.vue'
import AutoInvestmentSection from './components/AutoInvestmentSection.vue'
</script>

<template>
  <div id="app-wrapper">
    <Header />
    <main>
      <MainSection />
      <StockComparisonSection />
      <AutoInvestmentSection />
    </main>
  </div>
</template>

<style>
/* Global styles */
body, html {
  margin: 0;
  font-size: 23px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f3e3e3; /* MainSection과 동일한 핑크색으로 변경 */
  color: #333;
  line-height: 1.6;
}

#app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1;
}

/* App.vue specific styles can be scoped if needed */
</style>
