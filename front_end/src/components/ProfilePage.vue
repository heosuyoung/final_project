<template>  <div class="profile-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">내 프로필</h1>
      </div>
    </div>

    <div class="container profile-content">
      <div v-if="isLoading" class="loading-container">
        <div class="spinner"></div>
        <p>프로필 정보를 불러오는 중입니다...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <div class="error-icon">!</div>
        <p>{{ error }}</p>
      </div>
      
      <div v-else class="profile-grid">
        <!-- 왼쪽: 프로필 카드 -->
        <div class="profile-card">          <div class="profile-avatar-container">
            <div class="profile-avatar">
              <img v-if="hasProfileImage" :src="profileImage" alt="프로필 사진" />
              <div v-else class="avatar-placeholder">
                {{ userInitials }}
              </div>
              <div class="avatar-edit" v-if="!isEditing">
                <button @click="toggleFileInput" class="avatar-edit-btn" title="프로필 사진 변경">
                  <span class="material-icons">photo_camera</span>
                </button>
                <input 
                  type="file" 
                  ref="fileInput" 
                  style="display: none" 
                  accept="image/*" 
                  @change="handleImageChange"
                />
              </div>
            </div>
          </div>
          <div class="profile-summary">
            <h2 class="profile-name">{{ user.first_name || user.name || user.username }}</h2>
            <p class="profile-username">@{{ user.username }}</p>
            <p class="profile-email">{{ user.email || '이메일 미등록' }}</p>
          </div>
          <div class="profile-stats">
            <div class="stat-item">
              <div class="stat-value">{{ getTotalInvestments() | 0 }}만원</div>
              <div class="stat-label">총 투자금액</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ getFavoriteCount() | 0 }}</div>
              <div class="stat-label">관심종목</div>
            </div>
          </div>
        </div>

        <!-- 오른쪽: 정보 영역 -->
        <div class="profile-details">
          <div class="profile-section">
            <h3 class="section-title">
              <span class="section-icon material-icons">person</span>
              계정 정보
              <button v-if="!isEditing" @click="startEdit" class="edit-button">
                <span class="material-icons">edit</span> 편집
              </button>
            </h3>

            <!-- 보기 모드 -->
            <div v-if="!isEditing" class="profile-info">
              <div class="info-grid">
                <div class="info-item">
                  <div class="info-label">아이디</div>
                  <div class="info-value">{{ user.username }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">이름</div>
                  <div class="info-value">{{ user.first_name || user.name || '미등록' }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">이메일</div>
                  <div class="info-value">{{ user.email || '미등록' }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">생년월일</div>
                  <div class="info-value">{{ formatBirthDate(user.birth_date || user.birth) }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">성별</div>
                  <div class="info-value">{{ formatGender(user.gender) }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">가입일</div>
                  <div class="info-value">{{ formatJoinDate(user.date_joined) }}</div>
                </div>
              </div>
            </div>
            
            <!-- 수정 모드 -->
            <div v-else class="profile-edit-form">
              <div class="form-grid">
                <div class="form-group">
                  <label for="name">이름</label>
                  <input id="name" v-model="editForm.name" type="text" placeholder="이름을 입력하세요" />
                  <span v-if="validationErrors.name" class="validation-error">{{ validationErrors.name }}</span>
                </div>
                <div class="form-group">
                  <label for="email">이메일</label>
                  <input id="email" v-model="editForm.email" type="email" placeholder="이메일을 입력하세요" />
                  <span v-if="validationErrors.email" class="validation-error">{{ validationErrors.email }}</span>
                </div>
                <div class="form-group">
                  <label for="birth">생년월일</label>
                  <input id="birth" v-model="editForm.birth" type="text" maxlength="8" placeholder="YYYYMMDD" />
                  <span v-if="validationErrors.birth" class="validation-error">{{ validationErrors.birth }}</span>
                </div>
                <div class="form-group">
                  <label for="gender">성별</label>
                  <select id="gender" v-model="editForm.gender">
                    <option value="male">남자</option>
                    <option value="female">여자</option>
                  </select>
                </div>
              </div>
              
              <div class="form-actions">
                <button class="cancel-btn" @click="cancelEdit">취소</button>
                <button class="save-btn" @click="saveChanges">
                  <span class="material-icons">check</span> 저장하기
                </button>
              </div>
            </div>
          </div>
          
          <div class="profile-section">
            <h3 class="section-title">
              <span class="section-icon material-icons">security</span>
              계정 보안
            </h3>
            <div class="security-options">
              <button class="option-btn" @click="changePassword">
                <span class="material-icons">lock</span>
                비밀번호 변경
              </button>
              <button class="option-btn" @click="logout">
                <span class="material-icons">logout</span>
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getUserProfile, updateUserProfile, logout as authLogout, isAuthenticated } from '../services/auth.js'

const router = useRouter()
const user = ref({})
const isLoading = ref(true)
const error = ref(null)
const isEditing = ref(false)
const editForm = ref({})
const validationErrors = ref({})
const fileInput = ref(null)
const profileImage = ref('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')  // 기본 프로필 이미지

// 사용자 이니셜(첫 글자) 표시
const userInitials = computed(() => {
  const name = user.value.first_name || user.value.name || user.value.username || '';
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
})

// 프로필 이미지가 있는지 확인
const hasProfileImage = computed(() => {
  return profileImage.value && profileImage.value !== 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png';
})

// 생년월일 포맷팅 함수
const formatBirthDate = (birthDate) => {
  if (!birthDate) return '미등록'
  
  // 8자리 생년월일 포맷팅 (YYYYMMDD -> YYYY-MM-DD)
  const year = birthDate.substring(0, 4)
  const month = birthDate.substring(4, 6)
  const day = birthDate.substring(6, 8)
  
  return `${year}년 ${month}월 ${day}일`
}

// 성별 포맷팅 함수
const formatGender = (gender) => {
  if (!gender) return '미등록'
  
  // 백엔드 값을 프론트엔드 표시용으로 변환
  const genderMap = {
    'M': '남자',
    'F': '여자',
    'male': '남자',
    'female': '여자'
  }
  
  return genderMap[gender] || '미등록'
}

// 가입일 포맷팅 함수
const formatJoinDate = (dateJoined) => {
  if (!dateJoined) return '미등록'
  
  try {
    const date = new Date(dateJoined)
    return date.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  } catch (e) {
    return '미등록'
  }
}

// 총 투자금액 계산 - 실제로는 백엔드에서 가져오는 것이 좋지만 예시로 구현
const getTotalInvestments = () => {
  // 로컬 스토리지에 저장된 투자 정보가 있는지 확인
  try {
    const investments = JSON.parse(localStorage.getItem('user_investments') || '{}')
    return investments.total || 0
  } catch (e) {
    return 0
  }
}

// 관심종목 개수 - 로컬 스토리지에서 가져오기
const getFavoriteCount = () => {
  try {
    const favorites = JSON.parse(localStorage.getItem('favorite_stocks') || '[]')
    return favorites.length
  } catch (e) {
    return 0
  }
}

// 비밀번호 변경 함수
const changePassword = () => {
  // 현재 예시로만 구현 - 실제 비밀번호 변경 페이지로 라우팅
  alert('비밀번호 변경 기능은 아직 개발 중입니다.')
}

const fetchUserProfile = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    console.log('프로필 정보 로딩 시작...')
    
    // 인증 상태 확인 및 디버깅
    const authStatus = isAuthenticated() 
    console.log('인증 상태:', authStatus)
    
    if (!authStatus) {
      throw new Error('로그인이 필요합니다. 로그인 페이지로 이동합니다.');
    }
    
    // 로컬 스토리지 데이터 확인
    const rawUserData = localStorage.getItem('user')
    console.log('로컬 스토리지 사용자 데이터 존재:', !!rawUserData)
    
    // auth 서비스를 통해 사용자 프로필 정보 가져오기
    const userInfo = await getUserProfile()
    console.log('가져온 사용자 정보:', userInfo)
    
    // 데이터 검증
    if (!userInfo || typeof userInfo !== 'object' || Object.keys(userInfo).length === 0) {
      throw new Error('사용자 정보가 비어있습니다. 다시 로그인해주세요.');
    }
    
    user.value = userInfo
    
    // 프로필 이미지가 있으면 설정
    if (userInfo.profileImage) {
      profileImage.value = userInfo.profileImage
    }
    
    console.log('프로필 정보 로딩 완료')
  } catch (err) {
    console.error('Error fetching profile:', err)
    error.value = err.message || '프로필 정보를 불러오는데 실패했습니다.'
    
    // 에러가 인증 관련이면 로그인 페이지로 리다이렉트
    if (err.message.includes('로그인')) {
      alert('로그인이 필요합니다. 로그인 페이지로 이동합니다.');
      setTimeout(() => {
        router.push({
          path: '/login',
          query: { redirect: '/profile' }
        })
      }, 1000)
    }
  } finally {
    isLoading.value = false
  }
}

// 편집 모드 시작
const startEdit = () => {
  // 사용자 정보 복사
  editForm.value = { ...user.value }
  
  // 백엔드 성별 형식(M, F)을 프론트엔드 형식(male, female)으로 변환
  if (user.value.gender === 'M') {
    editForm.value.gender = 'male'
  } else if (user.value.gender === 'F') {
    editForm.value.gender = 'female'
  } else {
    editForm.value.gender = 'male' // 기본값
  }
  
  // 생년월일 필드명 변환 (birth_date -> birth)
  if (user.value.birth_date) {
    editForm.value.birth = user.value.birth_date
  }
  
  isEditing.value = true
}

// 변경 사항 취소
const cancelEdit = () => {
  validationErrors.value = {}
  isEditing.value = false
}

// 변경사항 저장
const saveChanges = async () => {
  // 폼 유효성 검사
  validationErrors.value = {}
  
  if (!editForm.value.name || editForm.value.name.trim() === '') {
    validationErrors.value.name = '이름을 입력해주세요'
  }
  
  if (editForm.value.email && !validateEmail(editForm.value.email)) {
    validationErrors.value.email = '유효한 이메일 형식이 아닙니다'
  }
  
  if (editForm.value.birth && !validateBirthDate(editForm.value.birth)) {
    validationErrors.value.birth = '생년월일은 8자리 숫자(YYYYMMDD) 형식이어야 합니다'
  }
  
  // 유효성 검사 실패 시 저장하지 않음
  if (Object.keys(validationErrors.value).length > 0) {
    return
  }
  
  isLoading.value = true
    try {
    // 백엔드 형식에 맞게 데이터 변환
    const profileData = {
      ...editForm.value,
      // birth 필드를 birth_date로 변환
      birth_date: editForm.value.birth,
      // gender 필드를 백엔드 형식(M/F)으로 변환
      gender: editForm.value.gender === 'male' ? 'M' : 'F'
    }
    
    // 프로필 업데이트 요청
    const updatedProfile = await updateUserProfile(profileData)
    user.value = updatedProfile
    isEditing.value = false
    
    // 성공 메시지 표시
    error.value = null
    
  } catch (err) {
    console.error('Profile update error:', err)
    error.value = err.message || '프로필 정보 업데이트에 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 이메일 유효성 검사
const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// 생년월일 유효성 검사
const validateBirthDate = (birth) => {
  if (!birth) return true
  
  // 8자리 숫자인지 확인
  if (!/^\d{8}$/.test(birth)) return false
  
  // 날짜 범위 확인
  const year = parseInt(birth.substring(0, 4))
  const month = parseInt(birth.substring(4, 6))
  const day = parseInt(birth.substring(6, 8))
  
  if (year < 1900 || year > new Date().getFullYear()) return false
  if (month < 1 || month > 12) return false
  if (day < 1 || day > 31) return false
  
  return true
}

// 프로필 이미지 업로드
const toggleFileInput = () => {
  fileInput.value.click()
}

// 이미지 변경 처리
const handleImageChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 이미지 파일 타입 검사
  if (!file.type.match('image.*')) {
    error.value = '이미지 파일만 업로드할 수 있습니다.'
    return
  }
  
  try {
    // FileReader로 이미지 미리보기
    const reader = new FileReader()
    reader.onload = (e) => {
      profileImage.value = e.target.result
      
      // 이미지 데이터를 사용자 프로필에 저장
      updateUserProfile({ ...user.value, profileImage: e.target.result })
        .then(updatedProfile => {
          user.value = updatedProfile
        })
        .catch(err => {
          console.error('이미지 업로드 에러:', err)
          error.value = '프로필 이미지 업데이트에 실패했습니다.'
        })
    }
    reader.readAsDataURL(file)
  } catch (err) {
    console.error('Image processing error:', err)
    error.value = '이미지 처리 중 오류가 발생했습니다.'
  }
}

const logout = () => {
  // auth 서비스를 통한 로그아웃
  authLogout()
  
  // 홈으로 리다이렉트
  router.push('/')
  
  // 페이지 새로고침으로 상태 완전히 갱신
  window.location.reload()
}

// 페이지 로드 시 프로필 정보 가져오기
onMounted(() => {
  console.log('ProfilePage 컴포넌트 마운트됨')
  
  // 인증 확인 후 프로필 가져오기
  if (isAuthenticated()) {
    console.log('인증된 사용자: 프로필 데이터 로딩 시작')
    fetchUserProfile()
  } else {
    console.log('인증되지 않은 사용자: 로그인 페이지로 리다이렉트')
    error.value = '로그인이 필요합니다. 로그인 페이지로 이동합니다.'
    
    // 즉시 리다이렉트하지 않고 에러 메시지를 잠시 보여줌
    setTimeout(() => {
      router.push('/login?redirect=/profile')
    }, 1000)
  }
})
</script>

<style scoped>
/* 전체 페이지 스타일 */
.profile-page {
  background-color: #f8f9ff;
  min-height: calc(100vh - 64px); /* 헤더 높이 제외 */
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* 페이지 헤더 스타일 */
.page-header {
  background: linear-gradient(135deg, #007bff, #00bcd4);
  padding: 3.5rem 0;
  color: white;
  margin-top: 2rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23ffffff' fill-opacity='0.1' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.5;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
  max-width: 600px;
}

/* 프로필 컨텐츠 레이아웃 */
.profile-content {
  margin-bottom: 3rem;
}

.profile-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

/* 로딩 및 에러 스타일 */
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.spinner {
  border: 4px solid rgba(0, 123, 255, 0.1);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border-left-color: #007bff;
  animation: spin 1s linear infinite;
  margin-bottom: 1.2rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  color: #e74c3c;
}

.error-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #ffe0e0;
  color: #e74c3c;
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* 프로필 카드 스타일 */
.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  padding: 2rem;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: fit-content;
}

.profile-avatar-container {
  margin-bottom: 1.5rem;
}

.profile-avatar {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.15);
  border: 5px solid #ffffff;
  background-color: #f0f7ff;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background-color: #f0f7ff;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, #4a90e2, #2e75cc);
  color: white;
  font-size: 3rem;
  font-weight: 500;
}

.avatar-edit {
  position: absolute;
  bottom: 5px;
  right: 5px;
}

.avatar-edit-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 123, 255, 0.9);
  color: white;
  border: 2px solid #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.avatar-edit-btn:hover {
  background: #0069d9;
  transform: scale(1.05);
}

.profile-summary {
  margin-bottom: 2rem;
}

.profile-name {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 0;
  margin-bottom: 0.3rem;
  color: #333;
}

.profile-username {
  font-size: 1rem;
  color: #777;
  margin: 0;
  margin-bottom: 0.8rem;
}

.profile-email {
  font-size: 0.9rem;
  color: #999;
  margin: 0;
}

.profile-stats {
  display: flex;
  width: 100%;
  border-top: 1px solid #eee;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #007bff;
  margin-bottom: 0.3rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #888;
}

/* 프로필 상세 정보 스타일 */
.profile-details {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  padding: 2rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-icon {
  font-size: 1.3rem;
  color: #007bff;
  margin-right: 0.5rem;
}

.edit-button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: all 0.2s;
}

.edit-button:hover {
  background: #f0f7ff;
}

.edit-button .material-icons {
  font-size: 1rem;
}

/* 정보 그리드 스타일 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.info-item {
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.info-label {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 0.5rem;
}

.info-value {
  font-size: 1.1rem;
  color: #333;
  font-weight: 500;
}

/* 폼 스타일 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #555;
}

.form-group input,
.form-group select {
  padding: 0.9rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #f9f9f9;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
  background-color: white;
}

.validation-error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.2rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.save-btn,
.cancel-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 5px;
}

.save-btn {
  background: #007bff;
  color: white;
  border: none;
}

.save-btn:hover {
  background: #0069d9;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
}

.cancel-btn {
  background: #f8f9fa;
  border: 1px solid #ddd;
  color: #666;
}

.cancel-btn:hover {
  background: #e9ecef;
}

/* 보안 옵션 스타일 */
.security-options {
  display: flex;
  gap: 1rem;
}

.option-btn {
  padding: 1rem;
  border-radius: 8px;
  background: #f8f9fa;
  border: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #555;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  flex: 1;
}

.option-btn:hover {
  background: #f0f7ff;
  border-color: #cce5ff;
  color: #007bff;
}

.option-btn .material-icons {
  color: #007bff;
}

/* 반응형 스타일 */
@media (max-width: 992px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-card {
    max-width: 600px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 2rem 0;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .profile-section {
    padding: 1.5rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .security-options {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .container {
    padding: 0 1rem;
  }
  
  .profile-avatar {
    width: 120px;
    height: 120px;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .save-btn, .cancel-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
