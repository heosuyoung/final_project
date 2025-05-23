<template>
  <div class="savings-recommendation">
    <h2>예적금 상품 추천</h2>
    
    <div class="filter-section">
      <h3>검색 필터</h3>
      <div class="filter-options">
        <div class="filter-group">
          <h4>상품 유형</h4>
          <label><input type="radio" v-model="productType" value="S" checked> 적금</label>
          <label><input type="radio" v-model="productType" value="D"> 예금</label>
        </div>
        
        <div class="filter-group">
          <h4>우대조건</h4>
          <div class="condition-grid">
            <label v-for="(condition, index) in availableConditions" :key="index">
              <input type="checkbox" v-model="selectedConditions" :value="condition.value">
              {{ condition.name }}
            </label>
          </div>
        </div>
        
        <div class="filter-group">
          <h4>정렬 방식</h4>
          <select v-model="sortOption">
            <option value="rate">금리순</option>
            <option value="bank">은행순</option>
          </select>
        </div>
        
        <button @click="fetchProducts" class="search-button">검색</button>
      </div>
    </div>
    
    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <p>금융 상품 정보를 가져오는 중...</p>
    </div>
    
    <div class="results-section" v-else>
      <h3>추천 상품 ({{ filteredProducts.length }}개)</h3>
      
      <div class="product-grid">
        <div v-for="(product, index) in filteredProducts" :key="index" class="product-card">
          <div class="product-header">
            <h4>{{ product.kor_co_nm }}</h4>
            <span class="product-type">{{ product.prdt_div === 'S' ? '적금' : '예금' }}</span>
          </div>
          <h5 class="product-name">{{ product.fin_prdt_nm }}</h5>
          
          <div class="interest-rate">
            <span class="rate-label">최고금리</span>
            <span class="rate-value">{{ getMaxInterestRate(product) }}%</span>
          </div>
          
          <div class="product-details">
            <div class="detail-item">
              <span class="detail-label">가입 방법</span>
              <span class="detail-value">{{ formatJoinWay(product.join_way) }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">우대조건</span>
              <p class="detail-value special-conditions">{{ product.spcl_cnd }}</p>
            </div>
            
            <div class="detail-item" v-if="product.max_limit">
              <span class="detail-label">최대한도</span>
              <span class="detail-value">{{ formatAmount(product.max_limit) }}</span>
            </div>
          </div>
        </div>
      </div>
        <div class="no-results" v-if="filteredProducts.length === 0">
        <p>검색 조건에 맞는 상품이 없습니다. 조건을 변경해 다시 검색해보세요.</p>
      </div>
        <!-- 페이지네이션 추가 -->
      <div class="pagination" v-if="totalPages > 1">
        <button 
          :disabled="currentPage === 1" 
          @click="currentPage--" 
          class="pagination-button"
        >
          이전
        </button>
        
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        
        <button 
          :disabled="currentPage === totalPages" 
          @click="currentPage++" 
          class="pagination-button"
        >
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SavingsRecommendation',  data() {
    return {
      loading: false,
      productType: 'S', // S: 적금, D: 예금
      products: [],
      selectedConditions: [],
      sortOption: 'rate',
      currentPage: 1,
      itemsPerPage: 8, // 한 페이지에 표시할 항목 수
      availableConditions: [
        { name: '카드사용', value: 'card' },
        { name: '공과금연동', value: 'utilities' },
        { name: '급여연동', value: 'salary' },
        { name: '비대면가입', value: 'online' },
        { name: '주택청약', value: 'housing' },
        { name: '첫거래', value: 'first' },
        { name: '예적금가입', value: 'accounts' },
        { name: '재예치', value: 'redeposit' },
        { name: '입출금통장', value: 'checking' },
        { name: '은행앱사용', value: 'app' },
        { name: '기타', value: 'other' }
      ],
      API_KEY: 'e5fce6cf13c93a150983abce4b1ee7ff'
    };
  },  computed: {
    filteredProducts() {
      let result = [...this.products];
      
      // Filter by product type
      result = result.filter(product => product.prdt_div === this.productType);
      
      // Filter by selected conditions
      if (this.selectedConditions.length > 0) {
        result = result.filter(product => {
          const conditions = product.spcl_cnd?.toLowerCase() || '';
          return this.selectedConditions.some(condition => {
            switch (condition) {
              case 'card': return conditions.includes('카드') || conditions.includes('체크') || conditions.includes('신용');
              case 'utilities': return conditions.includes('공과금') || conditions.includes('관리비');
              case 'salary': return conditions.includes('급여') || conditions.includes('연금');
              case 'online': return conditions.includes('인터넷') || conditions.includes('스마트') || conditions.includes('비대면');
              case 'housing': return conditions.includes('청약') || conditions.includes('주택');
              case 'first': return conditions.includes('첫거래') || conditions.includes('신규고객');
              case 'accounts': return conditions.includes('예금') || conditions.includes('적금');
              case 'redeposit': return conditions.includes('재예치') || conditions.includes('재가입');
              case 'checking': return conditions.includes('통장') || conditions.includes('입출금');
              case 'app': return conditions.includes('앱') || conditions.includes('스마트뱅킹');
              case 'other': return true; // Allow other conditions
              default: return false;
            }
          });
        });
      }
      
      // Sort products
      result.sort((a, b) => {
        if (this.sortOption === 'rate') {
          return this.getMaxInterestRate(b) - this.getMaxInterestRate(a);
        } else if (this.sortOption === 'bank') {
          return a.kor_co_nm.localeCompare(b.kor_co_nm);
        }
        return 0;
      });
      
      // 페이지네이션을 위한 전체 상품 목록 반환 (표시할 항목만)
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return result.slice(startIndex, endIndex);
    },
      // 전체 페이지 수 계산
    totalPages() {
      // 먼저 현재 선택된 상품 유형에 따라 필터링
      let filtered = this.products.filter(product => product.prdt_div === this.productType);
      
      // 선택된 조건이 있으면 추가 필터링
      if (this.selectedConditions.length > 0) {
        filtered = filtered.filter(product => {
          const conditions = product.spcl_cnd?.toLowerCase() || '';
          return this.selectedConditions.some(condition => {
            switch (condition) {
              case 'card': return conditions.includes('카드') || conditions.includes('체크') || conditions.includes('신용');
              case 'utilities': return conditions.includes('공과금') || conditions.includes('관리비');
              case 'salary': return conditions.includes('급여') || conditions.includes('연금');
              case 'online': return conditions.includes('인터넷') || conditions.includes('스마트') || conditions.includes('비대면');
              case 'housing': return conditions.includes('청약') || conditions.includes('주택');
              case 'first': return conditions.includes('첫거래') || conditions.includes('신규고객');
              case 'accounts': return conditions.includes('예금') || conditions.includes('적금');
              case 'redeposit': return conditions.includes('재예치') || conditions.includes('재가입');
              case 'checking': return conditions.includes('통장') || conditions.includes('입출금');
              case 'app': return conditions.includes('앱') || conditions.includes('스마트뱅킹');
              case 'other': return true;
              default: return false;
            }
          });
        });
      }
      
      const totalCount = filtered.length;
      return Math.max(1, Math.ceil(totalCount / this.itemsPerPage));
    },
    
    // 현재 표시 중인 상품 범위
    displayRange() {
      const start = (this.currentPage - 1) * this.itemsPerPage + 1;
      const total = this.products.filter(product => product.prdt_div === this.productType).length;
      const end = Math.min(this.currentPage * this.itemsPerPage, total);
      return `${start}-${end} / ${total}`;
    }
  },
  mounted() {
    this.fetchProducts();
  },  methods: {    async fetchProducts() {
      this.loading = true;
      // 페이지 초기화
      this.currentPage = 1;
      
      // CORS 문제로 인해 샘플 데이터를 바로 사용
      this.useSampleData();
      
      // 로딩 상태를 끝내기 위해 타이머 설정
      setTimeout(() => {
        this.loading = false;
      }, 1000);
      
      // API 호출 부분은 주석 처리 (CORS 문제 해결 후 활성화 가능)
      /*
      try {
        // 적금 상품 가져오기
        const savingsResponse = await axios.get(`https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth=${this.API_KEY}&topFinGrpNo=020000&pageNo=1`);
        const savingsData = savingsResponse.data.result.baseList || [];
        const savingsOptions = savingsResponse.data.result.optionList || [];
        
        // 예금 상품 가져오기
        const depositResponse = await axios.get(`https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth=${this.API_KEY}&topFinGrpNo=020000&pageNo=1`);
        const depositData = depositResponse.data.result.baseList || [];
        const depositOptions = depositResponse.data.result.optionList || [];
        
        // 상품에 옵션 연결
        savingsData.forEach(product => {
          product.prdt_div = 'S'; // 적금 표시
          product.options = savingsOptions.filter(opt => 
            opt.fin_co_no === product.fin_co_no && 
            opt.fin_prdt_cd === product.fin_prdt_cd
          );
        });
        
        depositData.forEach(product => {
          product.prdt_div = 'D'; // 예금 표시
          product.options = depositOptions.filter(opt => 
            opt.fin_co_no === product.fin_co_no && 
            opt.fin_prdt_cd === product.fin_prdt_cd
          );
        });
        
        // 모든 상품 합치기
        this.products = [...savingsData, ...depositData];
      } catch (error) {
        console.error('금융 상품 데이터를 가져오는 중 오류가 발생했습니다:', error);
        // 오류 발생 시 샘플 데이터 사용
        this.useSampleData();
      } finally {
        this.loading = false;
      }
      */
    },    useSampleData() {
      // 실제 API가 작동하지 않을 경우 샘플 데이터 사용
      // JSON 파일에서 데이터 불러오기
      try {
        // 정적으로 샘플 데이터 불러오기
        import('../assets/savingsData.json')
          .then(data => {
            // 샘플 데이터 로딩 성공
            const baseList = data.default.result.baseList || [];
            const optionList = data.default.result.optionList || [];
            
            // 상품 타입 설정 (적금/예금)
            baseList.forEach(product => {
              if (!product.prdt_div) {
                // 상품명에 적금이 있는지 확인
                if (product.fin_prdt_nm?.includes('적금')) {
                  product.prdt_div = 'S';
                } else {
                  product.prdt_div = 'D';
                }
              }
              
              // 각 상품에 옵션 정보 연결
              product.options = optionList.filter(option => 
                option.fin_co_no === product.fin_co_no && 
                option.fin_prdt_cd === product.fin_prdt_cd
              );
            });
            
            this.products = baseList;
            console.log('샘플 데이터 로딩 완료:', this.products.length, '개 상품');
          })
          .catch(error => {
            console.error('샘플 데이터를 불러오는 중 오류가 발생했습니다:', error);
            this.products = [];
          });
      } catch (error) {
        console.error('샘플 데이터 불러오기 실패:', error);
        this.products = [];
      }
    },
      getMaxInterestRate(product) {
      // 상품의 최고 금리 계산 (options 배열 항목에서 intr_rate2 값을 사용)
      if (!product.options || product.options.length === 0) {
        return "0.00";
      }
      
      const maxRate = product.options.reduce((max, option) => {
        const rate = parseFloat(option.intr_rate2) || 0;
        return rate > max ? rate : max;
      }, 0);
      
      return maxRate.toFixed(2);
    },
    
    formatJoinWay(joinWay) {
      if (!joinWay) return '정보 없음';
      
      const ways = {
        '영업점': '영업점',
        '인터넷': '인터넷',
        '스마트폰': '모바일',
        '전화': '전화',
        '모집인': '모집인'
      };
      
      return joinWay.split(',')
        .map(way => {
          for (const [key, value] of Object.entries(ways)) {
            if (way.includes(key)) return value;
          }
          return way;
        })
        .join(', ');
    },
    
    formatAmount(amount) {
      if (!amount) return '제한 없음';
      
      // 금액 포맷팅 (원 단위)
      const amountNum = parseInt(amount);
      if (amountNum >= 100000000) {
        return `${(amountNum / 100000000).toFixed(1)}억원`;
      } else if (amountNum >= 10000) {
        return `${(amountNum / 10000).toFixed(0)}만원`;
      } else {
        return `${amountNum}원`;
      }
    }
  }
}
</script>

<style scoped>
.savings-recommendation {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
}

h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

h3 {
  font-size: 22px;
  margin-bottom: 15px;
  color: #444;
}

.filter-section {
  background-color: #f7f9fc;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 30px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #555;
}

.condition-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 8px;
}

input[type="radio"],
input[type="checkbox"] {
  margin-right: 6px;
}

select {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.search-button {
  background-color: #4a6bdc;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
  margin-top: 20px;
}

.search-button:hover {
  background-color: #3a55b4;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #4a6bdc;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.product-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.product-header h4 {
  font-size: 18px;
  color: #333;
  margin: 0;
}

.product-type {
  background-color: #f0f4ff;
  color: #4a6bdc;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.product-name {
  font-size: 16px;
  margin: 8px 0;
  color: #555;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.interest-rate {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f7f9fc;
  padding: 10px;
  border-radius: 5px;
  margin: 15px 0;
}

.rate-label {
  font-size: 14px;
  color: #666;
}

.rate-value {
  font-size: 20px;
  font-weight: bold;
  color: #ff6b6b;
}

.product-details {
  margin-top: 15px;
}

.detail-item {
  margin-bottom: 10px;
}

.detail-label {
  display: block;
  font-size: 13px;
  color: #888;
  margin-bottom: 3px;
}

.detail-value {
  font-size: 14px;
  color: #444;
}

.special-conditions {
  max-height: 80px;
  overflow-y: auto;
  padding-right: 5px;
  font-size: 13px;
  line-height: 1.4;
}

.no-results {
  text-align: center;
  padding: 40px;
  background-color: #f7f9fc;
  border-radius: 10px;
  color: #666;
}

/* 미디어 쿼리 */
@media (max-width: 768px) {
  .filter-options {
    flex-direction: column;
  }
  
  .product-grid {
    grid-template-columns: 1fr;
  }
}

/* 페이지네이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  padding: 10px 0;
}

.pagination-button {
  background-color: #4a6bdc;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.pagination-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination-button:hover:not(:disabled) {
  background-color: #3451b2;
}

.page-info {
  margin: 0 15px;
  font-size: 14px;
  color: #666;
}
</style>
