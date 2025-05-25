<template>  <div class="savings-recommendation">
    <h1 class="main-title">예적금 상품 추천</h1>
      <!-- 상단 필터 영역 -->
    <div class="top-filter">
      <div class="filter-tabs">
        <button 
          :class="['tab-button', productType === 'S' ? 'active' : '']" 
          @click="productType = 'S'; fetchProducts()"
        >적금</button>
        <button 
          :class="['tab-button', productType === 'D' ? 'active' : '']" 
          @click="productType = 'D'; fetchProducts()"
        >예금</button>
      </div>
      
      <!-- 은행 선택 버튼 -->
      <div class="bank-filter">
        <button class="bank-select-button" @click="showBankModal = true">
          <span v-if="selectedBanks.length === banks.length">전체 은행</span>
          <span v-else-if="selectedBanks.length > 0">{{ selectedBanks.length }}개 은행 선택됨</span>
          <span v-else>은행 선택하기</span>
        </button>
      </div>
    </div>
    
    <!-- 우대조건 필터링 -->
    <div class="condition-filter">
      <div class="condition-tags">
        <button 
          v-for="(condition, index) in availableConditions" 
          :key="index"
          :class="['tag-button', selectedConditions.includes(condition.value) ? 'active' : '']"
          @click="toggleCondition(condition.value)"
        >
          {{ condition.name }}
        </button>
      </div>
    </div>    <!-- 가입 기간 및 정렬 옵션 -->    <div class="period-sort-options">
      <div class="filter-options">        <button class="filter-button" @click="showPeriodAmountModal = true">
          <span>기간-금액</span>
          <span class="filter-selected" style="color: #333;">{{ selectedPeriod === 0 ? '전체 기간' : selectedPeriod + '개월' }} · {{ formatAmount(selectedAmount) }}</span>
        </button>
        <button class="reset-filter-button" @click="resetPeriodAmountFilter">
          <span>초기화</span>
        </button>
      </div>
      <div class="sort-options">
        <button 
          :class="['sort-button', sortOption === 'maxRate' ? 'active' : '']" 
          @click="sortOption = 'maxRate'"
        >
          최고금리순
        </button>
        <button 
          :class="['sort-button', sortOption === 'baseRate' ? 'active' : '']" 
          @click="sortOption = 'baseRate'"
        >
          기본금리순
        </button>
      </div>
    </div>
    
    <!-- 로딩 표시 -->
    <div class="loading" v-if="loading">
      <div class="spinner"></div>
      <p>금융 상품 정보를 가져오는 중...</p>
    </div>
    
    <!-- 상품 목록 표시 -->
    <div class="results-section" v-else>
      <h3 class="results-title">예적금 상품 비교</h3>
      
      <div class="product-list">
        <div 
          v-for="(product, index) in filteredProducts" 
          :key="product.fin_prdt_cd"
          class="product-item"
        >
          <!-- 상위 3개 상품에 메달 표시 -->
          <div 
            v-if="index < 3" 
            :class="['medal', 
              index === 0 ? 'gold' : 
              index === 1 ? 'silver' : 
              'bronze'
            ]"
          >
            <span>{{ index + 1 }}</span>
          </div>
          
          <div class="bank-info">
            <div class="bank-logo">
              <!-- 은행별로 다른 이미지나 아이콘을 표시하려면 은행 코드(product.kor_co_nm)에 따라 다른 이미지 표시 -->
              <img 
                :src="getBankLogo(product.kor_co_nm)" 
                :alt="product.kor_co_nm" 
                class="bank-icon"
              >
            </div>
            <div class="bank-name">{{ product.kor_co_nm }}</div>
          </div>
          
          <div class="product-info">
            <h4 class="product-name">{{ product.fin_prdt_nm }}</h4>
            
            <div class="interest-rates">
              <div class="rate-box primary">
                <span class="rate-label">최고금리</span>
                <span class="rate-value">{{ getMaxInterestRate(product) }}%</span>
              </div>
              <div class="rate-box secondary">
                <span class="rate-label">기본금리</span>
                <span class="rate-value">{{ getBaseInterestRate(product) }}%</span>
              </div>
            </div>
            
            <div class="product-details">
              <div class="detail-row">
                <span class="detail-label">가입방법</span>
                <span class="detail-value">{{ formatJoinWay(product.join_way) }}</span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">우대조건</span>
                <span class="detail-value conditions-text">{{ product.spcl_cnd || '없음' }}</span>
              </div>
            </div>
            
            <button class="view-details-button">상품 상세보기</button>
          </div>
        </div>
      </div>
      
      <div class="no-results" v-if="filteredProducts.length === 0">
        <p>검색 조건에 맞는 상품이 없습니다. 조건을 변경해 다시 검색해보세요.</p>
      </div>
      
      <!-- 페이지네이션 -->
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
    
    <!-- 은행 선택 모달 -->
    <div class="modal" v-if="showBankModal">
      <div class="modal-content bank-modal">
        <div class="modal-header">
          <h3>금융사</h3>
          <button class="close-button" @click="showBankModal = false">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="bank-tabs">
            <button 
              :class="['bank-tab', bankTab === '1금융권' ? 'active' : '']" 
              @click="bankTab = '1금융권'"
            >1금융권</button>
            <button 
              :class="['bank-tab', bankTab === '2금융권' ? 'active' : '']" 
              @click="bankTab = '2금융권'"
            >2금융권</button>
          </div>
            <div class="bank-selection">
            <div class="select-all-wrapper">
              <label class="select-all">
                <input 
                  type="checkbox" 
                  :checked="isCurrentTabSelected" 
                  @click="toggleAllBanksInCurrentTab"
                >
                <span class="select-all-text">전체 선택</span>
              </label>
            </div>
            
            <div class="bank-grid">
              <div 
                v-for="bank in filteredBanks" 
                :key="bank.code" 
                class="bank-item"
              >
                <div class="bank-card" :class="{ 'selected': selectedBanks.includes(bank.code) }" @click="toggleBankSelection(bank.code)">
                  <div class="bank-logo-container">
                    <img :src="bank.logo" :alt="bank.name" class="bank-logo-img">
                  </div>
                  <div class="bank-name-text">{{ bank.name }}</div>
                  <div class="bank-check" v-if="selectedBanks.includes(bank.code)">
                    <span class="check-mark">✓</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="apply-button" @click="applyBankFilter">금융사 선택 적용하기</button>
        </div>
      </div>
    </div>    <!-- 기간-금액 선택 모달 -->
    <div class="modal" v-if="showPeriodAmountModal">
      <div class="modal-content period-amount-modal">
        <div class="modal-header">
          <h3>가입 기간</h3>
          <button class="close-button" @click="showPeriodAmountModal = false">&times;</button>
        </div>
        
        <div class="modal-body">          <!-- 가입 기간 선택 (월 단위) -->          <div class="term-selection-header">현재 선택: <span class="selected-term">{{ selectedPeriod === 0 ? '전체 기간' : selectedPeriod + '개월' }}</span></div>          <div class="term-selection">
            <button 
              class="term-button all-term-button"
              :class="{ 'active': selectedPeriod === 0 }"
              @click="selectedPeriod = 0"
              style="background-color: #f5f6fa; color: #333; border: 1px solid #e0e0e0;"
            >
              전체 기간
            </button>
            <button 
              v-for="month in depositPeriods" 
              :key="month"
              :class="['term-button', selectedPeriod === month ? 'active' : '']" 
              @click="selectedPeriod = month"
              style="background-color: #f5f6fa; color: #333; border: 1px solid #e0e0e0;"
            >
              {{ month }}개월
            </button>
          </div>
            <h3 class="amount-title">가입 금액</h3>
          
          <!-- 금액 입력 키패드 -->
          <div class="amount-keypad">
            <div class="amount-display">{{ formattedInputAmount || '0원' }}</div>
            
            <button 
              class="all-amount-button"
              @click="selectAllAmounts"
            >
              전체 금액으로 검색하기
            </button>
            
            <div class="numpad-grid">
              <button class="numpad-button" @click="appendDigit(1)">1</button>
              <button class="numpad-button" @click="appendDigit(2)">2</button>
              <button class="numpad-button" @click="appendDigit(3)">3</button>
              <button class="numpad-button" @click="appendDigit(4)">4</button>
              <button class="numpad-button" @click="appendDigit(5)">5</button>
              <button class="numpad-button" @click="appendDigit(6)">6</button>              <button class="numpad-button" @click="appendDigit(7)">7</button>
              <button class="numpad-button" @click="appendDigit(8)">8</button>
              <button class="numpad-button" @click="appendDigit(9)">9</button>              <button class="numpad-button" @click="clearLastDigit()">←</button>
              <button class="numpad-button" @click="appendDigit(0)">0</button>
              <button class="numpad-button delete-all" @click="clearInputAmount">
                <span class="delete-all-text">전체 삭제</span>
              </button>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="apply-button" @click="applyPeriodAmountFilter">적용</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios';
import './term-amount-styles.css';

export default {
  name: 'SavingsRecommendation',
  props: {
    limitCount: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      loading: false,
      productType: 'S', // S: 적금, D: 예금
      products: [],
      
      // 은행 관련
      showBankModal: false,
      bankTab: '1금융권',
      selectedBanks: [],
      
      // 우대조건 필터
      selectedConditions: [],        // 가입 기간 및 금액
      showAmountModal: false,
      showPeriodAmountModal: false,
      selectedPeriod: 0, // 기본 전체 기간
      selectedAmount: 0, // 기본 전체 금액
      inputAmount: '',
      
      // 정렬 및 페이지네이션
      sortOption: 'maxRate',
      currentPage: 1,
      itemsPerPage: 10,
      
      // API 키
      API_KEY: '066c9d4565f78a0a09c1d34543f461e7', // 업데이트된 API 키
      
      // 필터 옵션 데이터
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
        { name: '마케팅동의', value: 'marketing' }
      ],
      
      availablePeriods: [
        { label: '6개월', value: 6 },
        { label: '12개월', value: 12 },
        { label: '24개월', value: 24 },
        { label: '36개월', value: 36 }
      ],
      
      depositPeriods: [6, 12, 24, 36],
      
      // 은행 목록 데이터
      banks: [
        // 1금융권 은행들
        { code: 'kb', name: 'KB국민은행', logo: 'https://cdn.banksalad.com/icons/widgets/kbbank.png', type: '1금융권' },
        { code: 'shinhan', name: '신한은행', logo: 'https://cdn.banksalad.com/icons/widgets/shinhan.png', type: '1금융권' },
        { code: 'woori', name: '우리은행', logo: 'https://cdn.banksalad.com/icons/widgets/woori.png', type: '1금융권' },
        { code: 'hana', name: '하나은행', logo: 'https://cdn.banksalad.com/icons/widgets/hana.png', type: '1금융권' },
        { code: 'ibk', name: 'IBK기업은행', logo: 'https://cdn.banksalad.com/icons/widgets/ibkbank.png', type: '1금융권' },
        { code: 'nh', name: 'NH농협은행', logo: 'https://cdn.banksalad.com/icons/widgets/nhbank.png', type: '1금융권' },
        { code: 'sc', name: 'SC제일은행', logo: 'https://cdn.banksalad.com/icons/widgets/standardchartered.png', type: '1금융권' },
        { code: 'kdb', name: 'KDB산업은행', logo: 'https://cdn.banksalad.com/icons/widgets/kdb.png', type: '1금융권' },
        { code: 'suhyup', name: '수협은행', logo: 'https://cdn.banksalad.com/icons/widgets/suhyup.png', type: '1금융권' },
        { code: 'citi', name: '시티은행', logo: 'https://cdn.banksalad.com/icons/widgets/citi.png', type: '1금융권' },
        { code: 'dgb', name: 'DGB대구은행', logo: 'https://cdn.banksalad.com/icons/widgets/dgb.png', type: '1금융권' },
        { code: 'bnk', name: 'BNK부산은행', logo: 'https://cdn.banksalad.com/icons/widgets/bnk.png', type: '1금융권' },
        { code: 'kjb', name: '광주은행', logo: 'https://cdn.banksalad.com/icons/widgets/kjb.png', type: '1금융권' },
        { code: 'jbbank', name: '전북은행', logo: 'https://cdn.banksalad.com/icons/widgets/jbbank.png', type: '1금융권' },
        { code: 'kbank', name: '케이뱅크', logo: 'https://cdn.banksalad.com/icons/widgets/kbank.png', type: '1금융권' },
        { code: 'kakao', name: '카카오뱅크', logo: 'https://cdn.banksalad.com/icons/widgets/kakaobank.png', type: '1금융권' },
        
        // 2금융권 (저축은행 등)
        { code: 'jt', name: 'JT친애저축은행', logo: 'https://cdn.banksalad.com/icons/widgets/jtchinae.png', type: '2금융권' },
        { code: 'sbi', name: 'SBI저축은행', logo: 'https://cdn.banksalad.com/icons/widgets/sbi.png', type: '2금융권' },
        { code: 'welcomeb', name: '웰컴저축은행', logo: 'https://cdn.banksalad.com/icons/widgets/welcome.png', type: '2금융권' },
        { code: 'oksb', name: 'OK저축은행', logo: 'https://cdn.banksalad.com/icons/widgets/oksavings.png', type: '2금융권' }
      ]
    };
  },
    computed: {
    // 은행 탭에 따른 필터링된 은행 목록
    filteredBanks() {
      return this.banks.filter(bank => bank.type === this.bankTab);
    },
    
    // 현재 탭의 모든 은행이 선택되었는지 여부
    isCurrentTabSelected() {
      const banksInCurrentTab = this.banks.filter(bank => bank.type === this.bankTab).map(b => b.code);
      return banksInCurrentTab.every(code => this.selectedBanks.includes(code));
    },
    
    // 모든 은행이 선택되었는지 여부
    isAllSelected() {
      return this.selectedBanks.length === this.banks.length;
    },
    
    // 입력된 금액 포맷팅
    formattedInputAmount() {
      if (!this.inputAmount) return '0원';
      return this.inputAmount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '원';
    },
    
    // 전체 상품 중에서 필터링된 상품 목록
    filteredProducts() {
      let result = [...this.products];
      
      // 상품 유형에 따른 필터링
      result = result.filter(product => product.prdt_div === this.productType);
      
      // 선택된 은행이 있는 경우에만 은행 필터링
      if (this.selectedBanks.length > 0) {
        result = result.filter(product => {
          // 은행 코드로 변환하는 로직이 필요
          const bankCode = this.getBankCodeFromName(product.kor_co_nm);
          return this.selectedBanks.includes(bankCode);
        });
      }
      
      // 선택된 조건이 있는 경우 우대조건 필터링
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
              case 'marketing': return conditions.includes('동의') || conditions.includes('마케팅');
              default: return false;
            }
          });
        });
      }
      
      // 정렬 옵션에 따른 정렬
      result.sort((a, b) => {
        if (this.sortOption === 'maxRate') {
          return this.getMaxInterestRate(b) - this.getMaxInterestRate(a);
        } else if (this.sortOption === 'baseRate') {
          return this.getBaseInterestRate(b) - this.getBaseInterestRate(a);
        }
        return 0;
      });
      
      // 페이지네이션
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return result.slice(startIndex, endIndex);
    },
    
    // 전체 페이지 수 계산
    totalPages() {
      // 기본 필터링 (상품 유형, 은행, 우대조건)
      let filtered = [...this.products];
      
      // 상품 유형에 따른 필터링
      filtered = filtered.filter(product => product.prdt_div === this.productType);
      
      // 선택된 은행이 있는 경우 은행 필터링
      if (this.selectedBanks.length > 0) {
        filtered = filtered.filter(product => {
          const bankCode = this.getBankCodeFromName(product.kor_co_nm);
          return this.selectedBanks.includes(bankCode);
        });
      }
      
      // 선택된 조건이 있는 경우 우대조건 필터링
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
              case 'marketing': return conditions.includes('동의') || conditions.includes('마케팅');
              default: return false;
            }
          });
        });
      }
      
      const totalCount = filtered.length;
      return Math.max(1, Math.ceil(totalCount / this.itemsPerPage));
    }
  },
    mounted() {
    // 컴포넌트 마운트 시 데이터 로딩 (은행은 선택하지 않은 상태로 시작)
    this.selectedBanks = []; // 모든 은행을 보여주기 위해 비어있는 배열로 시작
    this.fetchProducts();
  },
  
  methods: {
    // 모든 은행 선택하기
    selectAllBanks() {
      this.selectedBanks = this.banks.map(bank => bank.code);
    },
    
    // 상품 데이터 가져오기
    async fetchProducts() {
      this.loading = true;
      // 페이지 초기화
      this.currentPage = 1;
      
      // 백엔드 API 호출
      const apiUrl = 'http://localhost:8000/boards/api/savings/';
      
      // 선택된 조건을 적절한 형식으로 변환
      const conditionValues = this.selectedConditions.map(condition => {
        // 조건 값 변환
        switch(condition) {
          case 'card': return '카드';
          case 'utilities': return '공과금';
          case 'salary': return '급여';
          case 'online': return '비대면';
          case 'housing': return '주택청약';
          case 'first': return '첫거래';
          case 'accounts': return '예적금';
          case 'redeposit': return '재예치';
          case 'checking': return '입출금';
          case 'app': return '앱';
          case 'marketing': return '동의';
          default: return condition;
        }
      });
      
      // API 요청 파라미터 구성
      const params = {
        type: this.productType === 'S' ? 'savings' : 'deposit',
        sort: this.sortOption,
        conditions: conditionValues
      };
      
      try {
        const response = await axios.get(apiUrl, { params });
        console.log('백엔드 API 응답 데이터:', response.data);
        
        if (Array.isArray(response.data)) {
          this.products = response.data.map(product => ({
            ...product,
            prdt_div: params.type === 'savings' ? 'S' : 'D'
          }));
          console.log('상품 데이터 로딩 완료:', this.products.length, '개 상품');
        } else {
          console.error('API에서 예상한 형식의 데이터를 반환하지 않았습니다');
          // 오류 시 샘플 데이터 사용
          this.useSampleData();
        }
      } catch (error) {
        console.error('금융 상품 데이터를 가져오는 중 오류가 발생했습니다:', error);
        // 오류 발생 시 샘플 데이터 사용
        this.useSampleData();
      } finally {
        setTimeout(() => {
          this.loading = false;
        }, 500);
      }
    },
    
    // 샘플 데이터 사용
    useSampleData() {
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
    
    // 상품의 최고 금리 계산
    getMaxInterestRate(product) {
      if (!product.options || product.options.length === 0) {
        return 0;
      }
      
      // 선택된 가입 기간에 해당하는 금리만 필터링
      let options = product.options;
      
      // 기간이 선택된 경우에만 필터링 적용
      if (this.selectedPeriod && this.selectedPeriod !== 0) {
        options = options.filter(option => {
          const saveTerm = parseInt(option.save_trm) || 0;
          return saveTerm === this.selectedPeriod;
        });
        
        // 필터링된 옵션이 없으면 전체 옵션 사용
        if (options.length === 0) {
          options = product.options;
        }
      }
      
      const maxRate = options.reduce((max, option) => {
        const rate = parseFloat(option.intr_rate2) || 0;
        return rate > max ? rate : max;
      }, 0);
      
      return maxRate;
    },
    
    // 상품의 기본 금리 계산
    getBaseInterestRate(product) {
      if (!product.options || product.options.length === 0) {
        return 0;
      }
      
      // 선택된 가입 기간에 해당하는 금리만 필터링
      let options = product.options;
      
      // 기간이 선택된 경우에만 필터링 적용
      if (this.selectedPeriod && this.selectedPeriod !== 0) {
        options = options.filter(option => {
          const saveTerm = parseInt(option.save_trm) || 0;
          return saveTerm === this.selectedPeriod;
        });
        
        // 필터링된 옵션이 없으면 전체 옵션 사용
        if (options.length === 0) {
          options = product.options;
        }
      }
      
      const baseRate = options.reduce((max, option) => {
        const rate = parseFloat(option.intr_rate) || 0;
        return rate > max ? rate : max;
      }, 0);
      
      return baseRate.toFixed(2);
    },
    
    // 가입 방법 포맷팅
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
    
    // 금액 포맷팅
    formatAmount(amount) {
      if (!amount || amount === 0) return '전체 금액';
      
      // 금액 포맷팅 (원 단위)
      const amountNum = parseInt(amount);
      if (amountNum >= 100000000) {
        return `${(amountNum / 100000000).toFixed(1)}억원`;
      } else if (amountNum >= 10000) {
        return `${(amountNum / 10000).toFixed(0)}만원`;
      } else {
        return `${amountNum}원`;
      }
    },
    
    // 은행명으로부터 은행 코드 얻기
    getBankCodeFromName(name) {
      const bank = this.banks.find(b => name.includes(b.name) || b.name.includes(name));
      return bank ? bank.code : 'unknown';
    },
    
    // 은행 코드로부터 로고 URL 얻기
    getBankLogo(name) {
      const bankCode = this.getBankCodeFromName(name);
      const bank = this.banks.find(b => b.code === bankCode);
      
      // 기본 로고 이미지
      const defaultLogo = 'https://cdn.banksalad.com/icons/widgets/etc.png';
      
      return bank ? bank.logo : defaultLogo;
    },
      // 현재 탭의 모든 은행 선택/해제 토글
    toggleAllBanksInCurrentTab() {
      const banksInCurrentTab = this.banks.filter(bank => bank.type === this.bankTab).map(b => b.code);
      
      if (this.isCurrentTabSelected) {
        // 현재 탭의 모든 은행 선택 해제
        this.selectedBanks = this.selectedBanks.filter(code => !banksInCurrentTab.includes(code));
      } else {
        // 현재 탭의 모든 은행 선택
        const newSelection = [...this.selectedBanks];
        banksInCurrentTab.forEach(code => {
          if (!newSelection.includes(code)) {
            newSelection.push(code);
          }
        });
        this.selectedBanks = newSelection;
      }
    },
    
    // 개별 은행 선택/해제 토글
    toggleBankSelection(bankCode) {
      const index = this.selectedBanks.indexOf(bankCode);
      if (index === -1) {
        // 선택되지 않은 은행 선택
        this.selectedBanks.push(bankCode);
      } else {
        // 이미 선택된 은행 해제
        this.selectedBanks.splice(index, 1);
      }
    },
    
    // 모든 은행 선택 토글 메서드
    toggleAllBanksSelection() {
      if (this.isAllSelected) {
        this.selectedBanks = [];
      } else {
        this.selectAllBanks();
      }
      this.fetchProducts();
    },
    
    // 은행 선택 필터 적용
    applyBankFilter() {
      this.showBankModal = false;
      this.fetchProducts();
    },
    
    // 금액 키패드에 숫자 추가
    appendDigit(digit) {
      if (this.inputAmount.length < 10) { // 최대 10자리 제한
        this.inputAmount += digit.toString();
      }
    },
    
    // 금액 키패드에서 마지막 숫자 제거
    clearLastDigit() {
      this.inputAmount = this.inputAmount.slice(0, -1);
    },
    
    // 전체 금액 초기화
    clearInputAmount() {
      this.inputAmount = '';
    },
    
    // 금액 필터 적용
    applyAmountFilter() {
      if (this.inputAmount) {
        this.selectedAmount = parseInt(this.inputAmount);
      }
      this.showAmountModal = false;
    },
      // 기간-금액 필터 적용
    applyPeriodAmountFilter() {
      if (this.inputAmount) {
        this.selectedAmount = parseInt(this.inputAmount);
      } else {
        // 금액 미선택 시 0으로 설정하여 전체 금액 검색
        this.selectedAmount = 0;
      }
      this.showPeriodAmountModal = false;
      this.fetchProducts();
    },
    
    // 기간-금액 필터 초기화
    resetPeriodAmountFilter() {
      this.selectedPeriod = 0; // 기간 미선택(전체 기간)으로 초기화
      this.selectedAmount = 0; // 금액 미선택(전체 금액)으로 초기화
      this.inputAmount = '';
      this.fetchProducts();
    },
    
    // 우대조건 토글
    toggleCondition(condition) {
      const index = this.selectedConditions.indexOf(condition);
      if (index === -1) {
        this.selectedConditions.push(condition);
      } else {
        this.selectedConditions.splice(index, 1);
      }
      
      // 조건 변경 시 데이터 다시 불러오기
      this.fetchProducts();
    },
    
    // 현재 탭의 모든 은행 선택/해제 토글
    toggleAllBanksInCurrentTab() {
      const banksInCurrentTab = this.filteredBanks.map(b => b.code);
      
      if (this.isCurrentTabSelected) {
        // 현재 탭의 모든 은행 선택 해제
        this.selectedBanks = this.selectedBanks.filter(code => !banksInCurrentTab.includes(code));
      } else {
        // 현재 탭의 모든 은행 선택
        this.selectedBanks = [...new Set([...this.selectedBanks, ...banksInCurrentTab])];
      }
    },
    
    // 은행 선택 토글
    toggleBankSelection(bankCode) {
      const index = this.selectedBanks.indexOf(bankCode);
      if (index === -1) {
        this.selectedBanks.push(bankCode);
      } else {
        this.selectedBanks.splice(index, 1);
      }
    },
    
    // 전체 금액 선택
    selectAllAmounts() {
      this.selectedAmount = 0;
      this.inputAmount = '';
    },
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
  color: #333;
}

.main-title {
  font-size: 28px;
  margin: 20px 0 25px 0;
  color: #333;
  font-weight: 700;
  padding-top: 25px;
}

/* 상단 필터 영역 */
.top-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-tabs {
  display: flex;
  gap: 10px;
}

.tab-button {
  padding: 8px 20px;
  border-radius: 20px;
  background-color: #f5f6fa;
  border: none;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-button.active {
  background-color: #00c853;
  color: white;
}

.bank-select-button {
  padding: 8px 20px;
  border-radius: 20px;
  background-color: #f5f6fa;
  border: none;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
}

/* 조건 필터 영역 */
.condition-filter {
  margin-bottom: 20px;
}

.condition-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-button {
  padding: 8px 15px;
  border-radius: 20px;
  background-color: white;
  border: 1px solid #e0e0e0;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-button.active {
  background-color: #e8f5e9;
  border-color: #00c853;
  color: #00c853;
}

/* 가입 기간 및 정렬 옵션 */
.period-sort-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-options {
  display: flex;
  gap: 8px;
}

.filter-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  border-radius: 8px;
  background-color: white;
  border: 1px solid #e0e0e0;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-button:hover {
  border-color: #00c853;
}

.reset-filter-button {
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  font-size: 12px;
  cursor: pointer;
  margin-left: 8px;
  transition: all 0.2s;
}

.reset-filter-button:hover {
  background-color: #e0e0e0;
}

.filter-selected {
  margin-top: 5px;
  font-weight: 600;
  color: #00c853;
}

.sort-options {
  display: flex;
  gap: 10px;
}

.sort-button {
  padding: 8px 15px;
  border-radius: 5px;
  background-color: white;
  border: 1px solid #e0e0e0;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-button.active {
  background-color: #00c853;
  color: white;
  border-color: #00c853;
}

/* 상품 결과 영역 */
.results-title {
  font-size: 22px;
  margin-bottom: 20px;
  font-weight: 700;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.product-item {
  display: flex;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 20px;
  position: relative;
}

/* 메달 표시 */
.medal {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  color: white;
  font-size: 14px;
}

.gold {
  background-color: #ffd700;
}

.silver {
  background-color: #c0c0c0;
}

.bronze {
  background-color: #cd7f32;
}

/* 은행 정보 영역 */
.bank-info {
  width: 120px;
  padding-right: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-right: 1px solid #eeeeee;
}

.bank-logo {
  width: 60px;
  height: 60px;
  margin-bottom: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.bank-icon {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.bank-name {
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  color: #555;
}

/* 상품 정보 영역 */
.product-info {
  flex-grow: 1;
  padding-left: 20px;
}

.product-name {
  font-size: 18px;
  margin-bottom: 15px;
  font-weight: 600;
}

.interest-rates {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.rate-box {
  width: 130px;
  height: 80px;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.primary {
  background-color: #e8f5e9;
}

.secondary {
  background-color: #f5f6fa;
}

.rate-label {
  font-size: 14px;
  color: #555;
}

.rate-value {
  font-size: 24px;
  font-weight: bold;
  color: #00c853;
}

.secondary .rate-value {
  color: #555;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 15px;
}

.detail-row {
  display: flex;
  gap: 10px;
}

.detail-label {
  font-size: 14px;
  color: #888;
  min-width: 70px;
}

.detail-value {
  font-size: 14px;
  color: #555;
}

.conditions-text {
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
}

.view-details-button {
  padding: 8px 15px;
  border-radius: 5px;
  background-color: #f5f6fa;
  border: 1px solid #e0e0e0;
  color: #555;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-start;
}

.view-details-button:hover {
  background-color: #00c853;
  border-color: #00c853;
  color: white;
}

/* 모달 스타일 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #888;
}

.modal-body {
  padding: 20px;
  flex-grow: 1;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.apply-button {
  padding: 10px 20px;
  background-color: #00c853;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  width: 100%;
}

/* 은행 선택 모달 스타일 */
.bank-tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.bank-tab {
  padding: 12px 20px;
  background-color: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  color: #888;
}

.bank-tab.active {
  border-bottom: 2px solid #00c853;
  color: #00c853;
  font-weight: 600;
}

.select-all-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.select-all {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  cursor: pointer;
}

.select-all-text {
  font-weight: 500;
}

.bank-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.bank-item {
  display: flex;
  justify-content: center;
}

.bank-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 10px;
  border-radius: 10px;
  border: 1px solid #eee;
  cursor: pointer;
  position: relative;
  width: 100%;
  transition: all 0.2s;
}

.bank-card.selected {
  border-color: #00c853;
  background-color: #e8f5e9;
}

.bank-logo-container {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.bank-check {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  background-color: #00c853;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 12px;
}

.bank-logo-img {
  max-width: 70%;
  max-height: 70%;
  object-fit: contain;
}

.bank-name-text {
  font-size: 12px;
  text-align: center;
  color: #555;
}

/* 금액 선택 모달 스타일 */
.period-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.period-item {
  padding: 10px;
  text-align: center;
  border: 1px solid #eee;
  border-radius: 5px;
  cursor: pointer;
}

.period-item.active {
  background-color: #00c853;
  color: white;
  border-color: #00c853;
}

.amount-title {
  font-size: 16px;
  margin-bottom: 15px;
  font-weight: 600;
}

.amount-keypad {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.amount-display {
  height: 50px;
  background-color: #f5f6fa;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 15px;
  font-size: 18px;
  font-weight: 600;
}

.keypad-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.key-button {
  height: 50px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.numpad-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(4, 1fr);
  grid-gap: 10px;
}

.numpad-button {
  padding: 15px 0;
  font-size: 18px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.numpad-button:hover {
  background-color: #f5f5f5;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  padding: 10px 0;
}

.pagination-button {
  background-color: #f5f6fa;
  color: #555;
  border: 1px solid #e0e0e0;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.pagination-button:disabled {
  background-color: #f5f6fa;
  color: #bbb;
  cursor: not-allowed;
}

.page-info {
  margin: 0 15px;
  font-size: 14px;
  color: #555;
}

/* 로딩 스타일 */
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
  border: 4px solid rgba(0, 200, 83, 0.1);
  border-radius: 50%;
  border-top-color: #00c853;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 미디어 쿼리 */
@media (max-width: 768px) {
  .top-filter {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .product-item {
    flex-direction: column;
  }
  
  .bank-info {
    width: 100%;
    padding-right: 0;
    padding-bottom: 15px;
    border-right: none;
    border-bottom: 1px solid #eee;
    flex-direction: row;
    margin-bottom: 15px;
  }
  
  .bank-logo {
    margin-right: 15px;
    margin-bottom: 0;
  }
  
  .product-info {
    padding-left: 0;
  }
  
  .interest-rates {
    flex-direction: column;
  }
  
  .bank-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
