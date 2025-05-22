<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <div class="profile-avatar">
          <img :src="profileImage" alt="프로필 사진" />
          <div class="avatar-edit" v-if="!isEditing">
            <button @click="toggleFileInput" class="avatar-edit-btn">
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
        <h1>내 프로필</h1>
      </div>
      
      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        로딩 중...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else>
        <!-- 보기 모드 -->
        <div v-if="!isEditing" class="profile-info">
          <div class="info-row">
            <span class="label">아이디:</span>
            <span class="value">{{ user.username }}</span>
          </div>
          <div class="info-row">
            <span class="label">이름:</span>
            <span class="value">{{ user.name }}</span>
          </div>
          <div class="info-row">
            <span class="label">이메일:</span>
            <span class="value">{{ user.email || '등록된 이메일이 없습니다.' }}</span>
          </div>
          <div class="info-row">
            <span class="label">생년월일:</span>
            <span class="value">{{ formatBirthDate(user.birth) }}</span>
          </div>
          <div class="info-row">
            <span class="label">성별:</span>
            <span class="value">{{ user.gender === 'male' ? '남자' : '여자' }}</span>
          </div>
        
          <button class="edit-btn" @click="startEdit">프로필 수정</button>
        </div>
        
        <!-- 수정 모드 -->
        <div v-else class="profile-edit-form">
          <div class="form-group">
            <label>이름:</label>
            <input v-model="editForm.name" type="text" />
            <span v-if="validationErrors.name" class="validation-error">{{ validationErrors.name }}</span>
          </div>
          <div class="form-group">
            <label>이메일:</label>
            <input v-model="editForm.email" type="email" />
            <span v-if="validationErrors.email" class="validation-error">{{ validationErrors.email }}</span>
          </div>
          <div class="form-group">
            <label>생년월일 (YYYYMMDD):</label>
            <input v-model="editForm.birth" type="text" maxlength="8" />
            <span v-if="validationErrors.birth" class="validation-error">{{ validationErrors.birth }}</span>
          </div>
          <div class="form-group">
            <label>성별:</label>
            <select v-model="editForm.gender">
              <option value="male">남자</option>
              <option value="female">여자</option>
            </select>
          </div>
          
          <div class="edit-buttons">
            <button class="save-btn" @click="saveChanges">저장</button>
            <button class="cancel-btn" @click="cancelEdit">취소</button>
          </div>
        </div>
      </div>
      <button class="logout-btn" @click="logout">로그아웃</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
const profileImage = ref('/profile-default.jpg')  // 기본 프로필 이미지

const formatBirthDate = (birthDate) => {
  if (!birthDate) return '등록된 생년월일이 없습니다.'
  
  // 8자리 생년월일 포맷팅 (YYYYMMDD -> YYYY-MM-DD)
  const year = birthDate.substring(0, 4)
  const month = birthDate.substring(4, 6)
  const day = birthDate.substring(6, 8)
  
  return `${year}년 ${month}월 ${day}일`
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
  editForm.value = { ...user.value }
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
    // 프로필 업데이트 요청
    const updatedProfile = await updateUserProfile(editForm.value)
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
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem 0;
}

.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 2.5rem 3rem;
  width: 100%;
  max-width: 600px;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.profile-avatar {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 1rem;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-edit {
  position: absolute;
  bottom: 0;
  right: 0;
}

.avatar-edit-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.avatar-edit-btn:hover {
  background: #0069d9;
}

h1 {
  color: #007bff;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  text-align: center;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1rem;
  color: #666;
}

.spinner {
  border: 4px solid rgba(0, 123, 255, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #007bff;
  animation: spin 1s linear infinite;
  margin: 0 auto;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  color: #e74c3c;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  padding: 0.8rem 0;
  border-bottom: 1px solid #eee;
}

.label {
  flex: 0 0 100px;
  font-weight: 600;
  color: #555;
}

.value {
  flex: 1;
  color: #333;
}

.edit-btn {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.8rem;
  width: 100%;
  margin-top: 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.edit-btn:hover {
  background: #0069d9;
}

.profile-edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #555;
}

.form-group input,
.form-group select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.validation-error {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.2rem;
}

.edit-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.save-btn,
.cancel-btn {
  padding: 0.8rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  flex: 1;
  transition: all 0.2s;
}

.save-btn {
  background: #007bff;
  color: white;
}

.save-btn:hover {
  background: #0069d9;
}

.cancel-btn {
  background: #f8f9fa;
  border: 1px solid #ddd;
  color: #666;
}

.cancel-btn:hover {
  background: #f1f3f5;
}

.logout-btn {
  display: block;
  width: 100%;
  padding: 0.8rem;
  margin-top: 2rem;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #f1f3f5;
  color: #007bff;
}

@media (max-width: 768px) {
  .profile-card {
    padding: 1.5rem 2rem;
  }
  
  .info-row {
    flex-direction: column;
    gap: 0.3rem;
  }
  
  .label {
    flex: none;
  }
  
  .edit-buttons {
    flex-direction: column;
  }
}
</style>
