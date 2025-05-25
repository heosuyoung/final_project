<template>
  <div class="map-page">
    <!-- 헤더 섹션 -->
    <div class="map-header">
      <div class="header-content">
        <h1 class="page-title">은행 찾기</h1>
        <p class="page-subtitle">주변 지역의 은행 지점을 쉽게 찾고 길찾기 서비스를 이용하세요</p>
      </div>
    </div>

    <div class="map-container">
      <!-- 검색 및 필터 섹션 -->
      <div class="search-panel">
        <h2 class="panel-title">지점 검색</h2>
        
        <!-- 출발지 정보 카드 -->
        <div class="origin-card" @click="focusOnStartLocation">
          <div class="origin-icon">🏢</div>
          <div class="origin-details">
            <h3>출발지</h3>
            <p class="location-name">SSAFY 부울경 캠퍼스</p>
            <p class="location-address">부산 강서구 녹산산업중로 333</p>
          </div>
        </div>
        
        <!-- 검색 필터 -->
        <div class="search-filters">
          <div class="filter-item">
            <label>광역시/도</label>
            <select v-model="selectedDo" @change="updateSiGunGuList" class="filter-select">
              <option disabled value="">광역시/도 선택</option>
              <option v-for="doItem in mapInfo" :key="doItem.name">{{ doItem.name }}</option>
            </select>
          </div>
          
          <div class="filter-item">
            <label>시/군/구</label>
            <select v-model="selectedSigungu" :disabled="!selectedDo" class="filter-select">
              <option disabled value="">시/군/구 선택</option>
              <option v-for="gu in selectedCountries" :key="gu">{{ gu }}</option>
            </select>
          </div>
          
          <div class="filter-item">
            <label>은행명</label>
            <select v-model="selectedBank" class="filter-select">
              <option disabled value="">은행 선택</option>
              <option v-for="bank in bankInfo" :key="bank">{{ bank }}</option>
            </select>
          </div>
        </div>
        
        <button @click="searchBanks" class="search-btn">
          <span class="search-icon">🔍</span>
          찾기
        </button>
        
        <!-- 검색 결과 섹션 -->
        <div class="search-results" v-if="searchResults.length > 0">
          <h3 class="results-title">검색 결과 <span class="result-count">{{ searchResults.length }}개</span></h3>
          
          <div class="results-list">
            <div 
              v-for="(place, index) in searchResults" 
              :key="index" 
              class="result-card"
              @click="focusOnMarker(index)"
            >
              <div class="result-header">
                <h4 class="place-name">{{ place.place_name }}</h4>
                <span class="result-index">{{ index + 1 }}</span>
              </div>
              
              <p class="place-address">{{ place.address_name }}</p>
              
              <div class="result-actions">
                <button @click.stop="showDirections(place)" class="action-btn directions-btn">
                  <span>🚗</span> 길찾기
                </button>
                <button @click.stop="focusOnMarker(index)" class="action-btn view-btn">
                  <span>🔎</span> 지도에서 보기
                </button>
              </div>
            </div>
          </div>
          
          <div class="no-results" v-if="searchResults.length === 0">
            <p>검색 결과가 없습니다. 다른 지역이나 은행을 선택해보세요.</p>
          </div>
        </div>
        
        <!-- 디지털 뱅킹 도우미 -->
        <div class="banking-helper">
          <h3>디지털 뱅킹 이용 도우미</h3>
          <div class="helper-cards">
            <div class="helper-card">
              <div class="helper-icon">📱</div>
              <h4>모바일뱅킹</h4>
              <p>언제 어디서나 간편하게 은행 업무를 처리하세요</p>
            </div>
            <div class="helper-card">
              <div class="helper-icon">💳</div>
              <h4>카드서비스</h4>
              <p>다양한 카드 혜택을 온라인에서 확인하세요</p>
            </div>
          </div>
        </div>
        
        <!-- 로컬 알림창 확인 버튼 (숨김) -->
        <button @click="handleConfirmMessage" class="confirm-button" style="display: none;">
          확인
        </button>
      </div>

      <!-- 지도 컨테이너 -->
      <div class="map-view">
        <div id="map"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import data from '../assets/data.json'

// 데이터
const mapInfo = data.mapInfo
const bankInfo = data.bankInfo

const selectedDo = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const selectedCountries = ref([])
const searchResults = ref([]) // 검색 결과 저장

// 출발지 정보 (고정)
const startLocation = {
  name: 'SSAFY 부울경 캠퍼스',
  address: '부산 강서구 녹산산업중로 333',
  lat: 35.094663, // 위도
  lng: 128.855308 // 경도
}

let mapInstance = null
let markers = []
let infowindows = []
let startMarker = null      // 출발지 마커
let startInfoWindow = null  // 출발지 인포윈도우

// 시도 변경 시 시군구 갱신
const updateSiGunGuList = () => {
  const target = mapInfo.find(item => item.name === selectedDo.value)
  selectedCountries.value = target ? target.countries : []
  selectedSigungu.value = '' // 시군구 선택 초기화
}

// 특정 마커로 지도 이동 및 인포윈도우 표시
const focusOnMarker = (index) => {
  if (markers.length > index && mapInstance) {
    // 해당 마커 위치로 지도 이동
    mapInstance.setCenter(markers[index].getPosition())
    mapInstance.setLevel(3) // 확대 레벨 조정

    // 다른 인포윈도우 닫기
    infowindows.forEach(iw => iw.close())
    
    // 현재 인포윈도우 열기
    infowindows[index].open(mapInstance, markers[index])
  }
}

// 출발지(SSAFY 캠퍼스)로 지도 이동 및 인포윈도우 표시
const focusOnStartLocation = () => {
  if (mapInstance && startMarker && startInfoWindow) {
    // 출발지 위치로 지도 이동
    mapInstance.setCenter(new kakao.maps.LatLng(startLocation.lat, startLocation.lng))
    mapInstance.setLevel(3) // 확대 레벨 조정
    
    // 다른 인포윈도우 닫기 (검색 결과 인포윈도우)
    infowindows.forEach(iw => iw.close())
    
    // 출발지 인포윈도우 열기
    startInfoWindow.open(mapInstance, startMarker)
  }
}

// 경로 안내 보여주기
const showDirections = (place) => {
  console.log('길찾기 버튼 클릭됨:', place)
  
  // 카카오맵 길찾기 API 호출
  const { kakao } = window
  if (!kakao || !kakao.maps || !kakao.maps.services) {
    console.error('카카오맵 API가 로드되지 않았습니다.')
    alert('카카오맵 API가 로드되지 않아 길찾기 기능을 사용할 수 없습니다.')
    return
  }
  
  // 출발지와 도착지 좌표 설정
  const start = startLocation // 출발지 (SSAFY 부울경 캠퍼스)
  const end = {
    name: place.place_name,
    lat: place.y, 
    lng: place.x
  }
  
  // 카카오맵 길찾기 URL 생성
  // 카카오맵 웹 URL 방식 사용: https://apis.map.kakao.com/web/guide/#routeurl
  const kakaoMapUrl = `https://map.kakao.com/link/to/${end.name},${end.lat},${end.lng}/from/${start.name},${start.lat},${start.lng}`
  
  // 새 창에서 카카오맵 길찾기 열기
  window.open(kakaoMapUrl, '_blank')
  
  // 지도에 경로 표시 (선택적 기능)
  showRouteOnMap(start, end)
}

// 지도에 경로 표시하기
const showRouteOnMap = (start, end) => {
  // 이전 경로 삭제
  if (window.currentRoute) {
    window.currentRoute.setMap(null)
  }
  
  // 경로 그리기
  const linePath = [
    new kakao.maps.LatLng(start.lat, start.lng),
    new kakao.maps.LatLng(end.lat, end.lng)
  ]
  
  // 경로 선 생성
  const polyline = new kakao.maps.Polyline({
    path: linePath,
    strokeWeight: 5,
    strokeColor: '#FF0000',
    strokeOpacity: 0.7,
    strokeStyle: 'solid'
  })
  
  // 경로를 지도에 표시
  polyline.setMap(mapInstance)
  
  // 현재 경로 저장 (나중에 삭제하기 위해)
  window.currentRoute = polyline
  
  // 두 지점이 모두 보이게 지도 중심 및 레벨 조정
  const bounds = new kakao.maps.LatLngBounds()
  bounds.extend(new kakao.maps.LatLng(start.lat, start.lng))
  bounds.extend(new kakao.maps.LatLng(end.lat, end.lng))
  mapInstance.setBounds(bounds)
}

// 모든 기존 마커와 인포윈도우 제거 함수
const clearMarkers = () => {
  markers.forEach(marker => marker.setMap(null))
  infowindows.forEach(infowindow => infowindow.close())
  markers = []
  infowindows = []
}

// 지도 로딩
const loadKakaoMap = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      console.log('Kakao Maps API가 이미 로드되어 있습니다.')
      resolve()
      return
    }

    console.log('Kakao Maps API 로드 시작')
    // .env 파일에서 API 키 가져오기
    const apiKey = import.meta.env.VITE_KAKAO_API_KEY 
    
    // API 키 유효성 검증
    if (!apiKey) {
      console.error('API 키가 로드되지 않았습니다. .env 파일을 확인해주세요.')
      alert('.env 파일의 VITE_KAKAO_API_KEY가 설정되지 않았습니다.')
      reject(new Error('API 키가 없음'))
      return
    }
    
    // 이미 존재하는 스크립트 제거 (중복 로딩 방지)
    const existingScript = document.querySelector('script[src*="dapi.kakao.com"]')
    if (existingScript) {
      document.head.removeChild(existingScript)
    }
    
    const script = document.createElement('script')
    // 반드시 services, drawing, clusterer 라이브러리 포함
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&autoload=false&libraries=services,clusterer,drawing`
    script.async = true // 비동기 로드
    
    script.onload = () => {
      console.log('Kakao Maps 스크립트 로드 완료, Maps API 초기화 시작')
      window.kakao.maps.load(() => {
        console.log('Kakao Maps API 초기화 완료')
        resolve()
      })
    }
    
    script.onerror = (e) => {
      console.error('Kakao Maps 스크립트 로드 실패', e)
      console.error('카카오 개발자 사이트에서 http://localhost:5179 도메인이 등록되어 있는지 확인하세요.')
      alert('카카오 지도를 불러오는데 실패했습니다. 개발자 도구에서 자세한 오류를 확인해주세요.')
      reject(e)
    }
    
    document.head.appendChild(script)
    console.log('Kakao Maps 스크립트 태그 추가됨')
    
    // localhost 알림창 대응
    window.addEventListener('message', function(event) {
      if (event.data && typeof event.data === 'string' && event.data.includes('지역의 은행')) {
        console.log('알림 메시지 감지:', event.data)
        // 확인 버튼을 자동으로 클릭하는 로직
        const confirmButton = document.querySelector('.confirm-button')
        if (confirmButton) {
          confirmButton.click()
        }
      }
    })
  })
}

// 검색 함수
const searchBanks = () => {
  console.log('searchBanks 실행됨') // 클릭 작동 확인용

  if (!window.kakao || !window.kakao.maps) {
    console.error('카카오맵이 아직 로드되지 않았습니다.')
    return
  }

  // 선택 값 확인
  console.log('[선택된 값들]', {
    do: selectedDo.value,
    sigungu: selectedSigungu.value,
    bank: selectedBank.value
  })

  // 모든 값이 선택되었는지 확인
  if (!selectedDo.value || !selectedSigungu.value || !selectedBank.value) {
    alert('모든 항목(광역시/도, 시/군/구, 은행)을 선택해주세요.')
    return
  }

  const geocoder = new kakao.maps.services.Geocoder()
  const query = `${selectedDo.value} ${selectedSigungu.value} ${selectedBank.value}`

  console.log('[검색 쿼리]', query)

  // 키워드 검색 서비스 사용
  const places = new kakao.maps.services.Places()
  
  // 마커와 인포윈도우 초기화
  clearMarkers()

  // 키워드로 장소 검색
  places.keywordSearch(query, function(result, status) {
    console.log('[키워드 검색 결과]', result)
    console.log('[키워드 검색 상태]', status)
    
    if (status === kakao.maps.services.Status.OK) {
      // 검색 결과 저장
      searchResults.value = result
      
      // 첫번째 결과의 위치로 맵 이동 (확대 레벨 조정)
      const firstCoords = new kakao.maps.LatLng(result[0].y, result[0].x)
      mapInstance.setCenter(firstCoords)
      mapInstance.setLevel(4) // 적절한 확대 레벨로 설정
      
      // 검색된 모든 은행에 마커 표시
      result.forEach((place, index) => {
        const coords = new kakao.maps.LatLng(place.y, place.x)
        
        // 마커 생성 (인덱스 레이블 추가)
        const marker = new kakao.maps.Marker({
          map: mapInstance,
          position: coords,
          title: place.place_name
        })
        markers.push(marker)
        
        // 인포윈도우 생성
        const infoContent = `
          <div class="custom-info-window">
            <div class="info-title">${place.place_name}</div>
            <div class="info-address">${place.address_name}</div>
            <button onclick="window.showDirectionsFromMap && window.showDirectionsFromMap(${index})" class="info-button">
              길찾기
            </button>
          </div>
        `
        
        const infowindow = new kakao.maps.InfoWindow({
          content: infoContent,
          removable: true
        })
        infowindows.push(infowindow)
        
        // 마커 클릭시 인포윈도우 표시
        kakao.maps.event.addListener(marker, 'click', function() {
          // 다른 인포윈도우 닫기
          infowindows.forEach(iw => iw.close())
          // 현재 인포윈도우 열기
          infowindow.open(mapInstance, marker)
        })
        
        // 첫번째 마커에 인포윈도우 자동 열기
        if (index === 0) {
          infowindow.open(mapInstance, marker)
        }
      })
      
      // 인포윈도우 내 버튼으로 길찾기할 수 있도록 전역함수 설정
      window.showDirectionsFromMap = (index) => {
        if (searchResults.value && searchResults.value.length > index) {
          showDirections(searchResults.value[index])
        }
      }
      
    } else {
      // Geocoder로 주소 검색 시도 (대안으로)
      geocoder.addressSearch(query, function (result, status) {
        console.log('[주소 검색 결과]', result)
        console.log('[주소 검색 상태]', status)

        if (status === kakao.maps.services.Status.OK) {
          const coords = new kakao.maps.LatLng(result[0].y, result[0].x)

          if (!mapInstance) {
            mapInstance = new kakao.maps.Map(document.getElementById('map'), {
              center: coords,
              level: 3
            })
          } else {
            mapInstance.setCenter(coords)
          }

          const marker = new kakao.maps.Marker({
            map: mapInstance,
            position: coords
          })

          const infowindow = new kakao.maps.InfoWindow({
            content: `<div style="padding:10px;">${selectedBank.value}</div>`,
            removable: true
          })

          infowindow.open(mapInstance, marker)
        } else {
          alert('해당 지역의 은행 정보를 찾을 수 없습니다.')
          searchResults.value = [] // 결과 초기화
        }
      })
    }
  })
}

// 로컬 알림창 확인 버튼 처리 함수
const handleConfirmMessage = () => {
  console.log('알림창 확인 버튼 클릭됨')
  // 필요한 경우 추가 작업 수행
}

// 지도 초기화
onMounted(async () => {
  try {
    console.log('MapPage 마운트됨, 카카오맵 로드 시작')
    
    // 카카오맵 API 로드
    await loadKakaoMap()
    console.log('카카오맵 API가 로드되었습니다.')
    
    const container = document.getElementById('map')
    if (!container) {
      console.error('map 요소를 찾을 수 없습니다.')
      return
    }
    
    // 지도 초기화 (출발지 기준)
    const options = {
      center: new window.kakao.maps.LatLng(startLocation.lat, startLocation.lng), // 출발지(녹산산업중로 333)
      level: 3  // 확대 레벨
    }
    
    try {
      console.log('지도 초기화 시작')
      mapInstance = new kakao.maps.Map(container, options)
      console.log('지도 초기화 완료')
      console.log('지도 객체:', mapInstance ? '생성됨' : '생성 실패')
      
      // 지도 로드 확인
      if (mapInstance) {
        // 지도 객체에 이벤트 리스너 추가
        kakao.maps.event.addListener(mapInstance, 'tilesloaded', function() {
          console.log('지도 타일 로딩 완료!')
        })
        
        // 출발지 마커 추가
        startMarker = new kakao.maps.Marker({
          map: mapInstance,
          position: new kakao.maps.LatLng(startLocation.lat, startLocation.lng),
          title: startLocation.name,
          // 출발지 마커 이모티콘을 더 눈에 띄는 큰 파란색 마커로 변경
          image: new kakao.maps.MarkerImage(
            // 큰 파란색 마커 이미지
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png', 
            new kakao.maps.Size(40, 42), 
            { offset: new kakao.maps.Point(20, 42) }
          )
        })
        
        // 출발지 인포윈도우 - 더 눈에 띄게 디자인 변경
        startInfoWindow = new kakao.maps.InfoWindow({
          content: `<div class="custom-start-info">
                     <div class="start-title">${startLocation.name}</div>
                     <div class="start-address">${startLocation.address}</div>
                     <div class="start-label">출발지</div>
                   </div>`,
          removable: true // 닫기 버튼 표시
        })
        
        // 마커 클릭 시 출발지 정보 표시
        kakao.maps.event.addListener(startMarker, 'click', function() {
          startInfoWindow.open(mapInstance, startMarker)
        })
        
        // 초기에는 출발지 인포윈도우 표시
        startInfoWindow.open(mapInstance, startMarker)
      }
    } catch (mapError) {
      console.error('지도 객체 생성 실패:', mapError)
      alert('지도 객체 생성 실패. 새로고침 후 다시 시도해보세요.')
    }
    
    // 초기 데이터 확인용 로그
    console.log('지도 정보:', mapInfo.length, '개 지역')
    console.log('은행 정보:', bankInfo.length, '개 은행')
    
  } catch (e) {
    console.error('카카오맵 로딩 실패:', e)
    alert('카카오맵 로딩에 실패했습니다. 개발자 도구의 콘솔에서 자세한 오류를 확인하세요.')
  }
})
</script>

<style scoped>
.map-page {
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
  background-color: #f8f9ff;
}

/* 헤더 스타일 */
.map-header {
  background: linear-gradient(135deg, #4e54c8 0%, #8f94fb 100%);
  padding: 5rem 0 3rem;
  color: white;
  text-align: center;
  margin-bottom: 2rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-title {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  font-size: 1.2rem;
  font-weight: 400;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

/* 지도 컨테이너 레이아웃 */
.map-container {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 250px);
  padding: 0 1rem 2rem;
}

/* 검색 패널 */
.search-panel {
  width: 380px;
  min-width: 320px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  margin-right: 1.5rem;
  height: fit-content;
  max-height: calc(100vh - 250px);
  overflow-y: auto;
  z-index: 10;
}

.panel-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #333;
}

/* 출발지 카드 스타일 */
.origin-card {
  display: flex;
  align-items: center;
  background-color: #f0f8ff;
  padding: 1.2rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 4px solid #4e54c8;
}

.origin-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.origin-icon {
  font-size: 2rem;
  margin-right: 1rem;
  color: #4e54c8;
}

.origin-details h3 {
  font-size: 0.9rem;
  color: #666;
  margin: 0 0 0.3rem;
}

.location-name {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 0 0.2rem;
  color: #4e54c8;
}

.location-address {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

/* 검색 필터 스타일 */
.search-filters {
  margin-bottom: 1.5rem;
}

.filter-item {
  margin-bottom: 1rem;
}

.filter-item label {
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.9rem;
  color: #555;
  font-weight: 500;
}

.filter-select {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  background-color: #f8f9ff;
  font-size: 0.95rem;
  transition: all 0.3s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23555' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 30px;
}

.filter-select:focus {
  outline: none;
  border-color: #8f94fb;
  box-shadow: 0 0 0 3px rgba(143, 148, 251, 0.2);
}

.filter-select:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
  opacity: 0.7;
}

/* 검색 버튼 */
.search-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(90deg, #4e54c8, #8f94fb);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  margin-bottom: 1.5rem;
}

.search-btn:hover {
  box-shadow: 0 4px 15px rgba(78, 84, 200, 0.3);
  transform: translateY(-2px);
}

.search-btn:active {
  transform: translateY(0);
}

.search-icon {
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

/* 검색 결과 스타일 */
.search-results {
  margin-top: 2rem;
  border-top: 1px solid #eee;
  padding-top: 1.5rem;
}

.results-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.result-count {
  font-size: 0.9rem;
  background-color: #f0f0f0;
  padding: 0.2rem 0.8rem;
  border-radius: 20px;
  color: #555;
  font-weight: 500;
}

.results-list {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.result-card {
  background-color: white;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.result-card:hover {
  border-color: #8f94fb;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.place-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.result-index {
  background-color: #4e54c8;
  color: white;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 0.8rem;
  font-weight: 700;
}

.place-address {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0 1rem;
}

.result-actions {
  display: flex;
  gap: 0.8rem;
}

.action-btn {
  flex: 1;
  font-size: 0.85rem;
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  transition: all 0.2s;
}

.directions-btn {
  background-color: #4e54c8;
  color: white;
}

.directions-btn:hover {
  background-color: #3f43a1;
}

.view-btn {
  background-color: #f0f0f0;
  color: #333;
}

.view-btn:hover {
  background-color: #e0e0e0;
}

.no-results {
  text-align: center;
  padding: 2rem 1rem;
  color: #666;
  background-color: #f8f9ff;
  border-radius: 8px;
}

/* 디지털 뱅킹 도우미 섹션 */
.banking-helper {
  margin-top: 2rem;
  border-top: 1px solid #eee;
  padding-top: 1.5rem;
}

.banking-helper h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.helper-cards {
  display: flex;
  gap: 1rem;
}

.helper-card {
  flex: 1;
  background: linear-gradient(145deg, #f8f9ff, #ffffff);
  border-radius: 10px;
  padding: 1.2rem;
  text-align: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.helper-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.helper-icon {
  font-size: 2rem;
  margin-bottom: 0.8rem;
}

.helper-card h4 {
  font-size: 1rem;
  margin: 0 0 0.5rem;
  color: #4e54c8;
}

.helper-card p {
  font-size: 0.8rem;
  color: #666;
  margin: 0;
}

/* 지도 뷰 스타일 */
.map-view {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  position: relative;
}

#map {
  width: 100%;
  height: 100%;
  min-height: 600px;
}

/* 인포윈도우 커스텀 스타일 (전역 스타일로 설정해야 함) */
:global(.custom-info-window) {
  padding: 10px;
  width: 220px;
  text-align: center;
  border-radius: 8px;
  overflow: hidden;
}

:global(.info-title) {
  font-weight: bold;
  font-size: 16px;
  color: #4e54c8;
  margin-bottom: 5px;
}

:global(.info-address) {
  font-size: 13px;
  color: #666;
  margin-bottom: 10px;
}

:global(.info-button) {
  background-color: #4e54c8;
  color: white;
  border: none;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

:global(.info-button:hover) {
  background-color: #3f43a1;
}

:global(.custom-start-info) {
  padding: 10px;
  width: 220px;
  text-align: center;
  border-radius: 8px;
  overflow: hidden;
}

:global(.start-title) {
  font-weight: bold;
  font-size: 16px;
  color: #3366cc;
  margin-bottom: 5px;
}

:global(.start-address) {
  font-size: 13px;
  color: #666;
  margin-bottom: 5px;
}

:global(.start-label) {
  font-size: 11px;
  color: white;
  background-color: #3366cc;
  padding: 3px 10px;
  border-radius: 10px;
  display: inline-block;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .map-container {
    flex-direction: column;
  }
  
  .search-panel {
    width: 100%;
    margin-right: 0;
    margin-bottom: 1.5rem;
    max-height: none;
  }
  
  .map-view {
    height: 500px;
  }
  
  #map {
    min-height: 500px;
  }
}

@media (max-width: 768px) {
  .map-header {
    padding: 4rem 0 2rem;
  }
  
  .page-title {
    font-size: 2.2rem;
  }
  
  .helper-cards {
    flex-direction: column;
  }
  
  .map-view {
    height: 400px;
  }
  
  #map {
    min-height: 400px;
  }
}

@media (max-width: 480px) {
  .result-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
