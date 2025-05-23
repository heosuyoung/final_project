<script setup>
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'
import MainSection from './components/MainSection.vue'
import StockComparisonSection from './components/StockComparisonSection.vue'
import AutoInvestmentSection from './components/AutoInvestmentSection.vue'

const route = useRoute()
</script>

<template>
  <div :id="'app-wrapper'" :class="{ 'signup-bg-root': route.path === '/signup' || route.path === '/login' || route.path === '/profile' }">
    <Header />
    <main :class="{ 'signup-main': route.path === '/signup' || route.path === '/login' || route.path === '/profile'}">
      <router-view />
      <template v-if="route.path === '/'">
        <StockComparisonSection />
        <AutoInvestmentSection />
      </template>
    </main>
  </div>
</template>

<style>
/* Global styles */
body, html {
  margin: 0;
  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  line-height: 1.6;
}

#app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f3e3e3;
}

main {
  flex-grow: 1;
}

.signup-bg-root {
  background: #fff !important;
}

.signup-main {
  background: #fff !important;
}

/* App.vue specific styles can be scoped if needed */
</style>
