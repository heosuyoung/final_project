<template>
  <section class="news-section">
    <div class="content-container">
      <h2 class="section-title">최신 금융 뉴스</h2>
      <p class="section-desc">국내외 주요 금융 뉴스와 시장 동향을 확인하세요.</p>
      
      <div class="news-cards">
        <div class="news-card" v-for="(article, index) in newsArticles" :key="index">
          <div class="news-image" :style="{ backgroundImage: `url(${article.image})` }">
            <span class="news-tag">{{ article.category }}</span>
          </div>
          <div class="news-content">
            <h3 class="news-title">{{ article.title }}</h3>
            <p class="news-summary">{{ article.summary }}</p>
            <div class="news-meta">
              <span class="news-source">{{ article.source }}</span>
              <span class="news-date">{{ article.date }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <button class="view-more-btn">뉴스 더보기</button>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

// 뉴스 데이터
const newsArticles = ref([
  {
    title: '금리인하, 언제 시작되나… "6월 인하 없다면 9월로 연기될 수도"',
    summary: '글로벌 금융시장에서 미국 연방준비제도(Fed)의 금리인하 시점이 미뤄질 것이라는 전망이 확산하고 있습니다.',
    image: 'https://via.placeholder.com/400x200?text=금리뉴스',
    category: '경제',
    source: '한국경제',
    date: '2024-05-26'
  },
  {
    title: '인공지능(AI)주 하락세, 매수기회인가 하락 신호인가',
    summary: '엔비디아를 중심으로 한 AI 관련주들이 최근 하락세를 보이며 투자자들의 고민이 깊어지고 있습니다.',
    image: 'https://via.placeholder.com/400x200?text=AI투자',
    category: '주식',
    source: '매일경제',
    date: '2024-05-25'
  },
  {
    title: '코스피, 대형주 중심 반등... "실적 개선주 선별 투자해야"',
    summary: '국내 증시가 대형주 중심으로 반등하며 안정을 찾아가고 있으나 전문가들은 실적 개선이 확실한 종목 위주의 선별 투자가 필요하다고 조언합니다.',
    image: 'https://via.placeholder.com/400x200?text=코스피',
    category: '증시',
    source: '서울경제',
    date: '2024-05-24'
  }
]);
</script>

<style scoped>
.news-section {
  padding: 5rem 0;
  background-color: #f9fafd;
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  position: relative;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 1rem;
}

.section-desc {
  font-size: 1.1rem;
  color: #666;
  text-align: center;
  margin-bottom: 3rem;
}

.news-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.news-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.news-image {
  height: 180px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.news-tag {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(0, 123, 255, 0.85);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.news-content {
  padding: 1.5rem;
}

.news-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.8rem;
  line-height: 1.4;
}

.news-summary {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.2rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #777;
}

.news-source {
  font-weight: 600;
}

.view-more-btn {
  display: block;
  margin: 0 auto;
  padding: 0.8rem 2.5rem;
  background: linear-gradient(90deg, #007bff, #00bcd4);
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
}

/* 반응형 스타일 */
@media (max-width: 1200px) {
  .news-cards {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .news-cards {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .section-desc {
    font-size: 1rem;
  }
}
</style>
