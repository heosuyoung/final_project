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
          <!-- 출발지 설정 -->
        <div class="location-settings">          <div class="location-header">
            <h3>출발지 설정</h3>
          </div>
            <!-- 출발지 선택 -->
          <div class="location-selector">
            <label for="start-location">출발지</label>
            <div class="selector-content">
              <select v-model="selectedStartLocation" id="start-location" class="location-select">
                <option value="default">SSAFY 부울경 캠퍼스</option>
                <option value="custom">직접 입력</option>
                <option value="current">현재 위치</option>
              </select>
              <input 
                v-if="selectedStartLocation === 'custom'" 
                v-model="customStartLocation" 
                type="text" 
                placeholder="출발지 주소 입력" 
                class="custom-location-input" 
              />
              <button v-if="selectedStartLocation === 'custom'" @click="searchCustomLocation('start')" class="location-search-btn">
                검색
              </button>
            </div>
          </div>
            <!-- 도착지 선택 (숨김) -->
          <div class="location-selector" style="display: none;">
            <label for="end-location">도착지</label>
            <div class="selector-content">
              <select v-model="selectedEndLocation" id="end-location" class="location-select">
                <option value="custom">직접 입력</option>
                <option value="search">검색 결과에서 선택</option>
              </select>
            </div>
          </div>
          
          <!-- 교통수단 선택 -->
          <div class="transport-options">
            <h4>이동 수단 선택</h4>
            <div class="transport-buttons">
              <button 
                :class="['transport-btn', transportMode === 'car' ? 'active' : '']" 
                @click="transportMode = 'car'"
              >
                🚗 자동차
              </button>
              <button 
                :class="['transport-btn', transportMode === 'walk' ? 'active' : '']" 
                @click="transportMode = 'walk'"
              >
                🚶 도보
              </button>
              <button 
                :class="['transport-btn', transportMode === 'bike' ? 'active' : '']" 
                @click="transportMode = 'bike'"
              >
                🚲 자전거
              </button>
            </div>
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
          
          <div class="results-list">            <div 
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
              
              <!-- 예상 소요 시간 정보 -->
              <div class="travel-time" v-if="place.duration">
                <div class="travel-icon">
                  <span v-if="transportMode === 'car'">🚗</span>
                  <span v-else-if="transportMode === 'walk'">🚶</span>
                  <span v-else-if="transportMode === 'bike'">🚲</span>
                </div>
                <div class="travel-info">
                  <span class="travel-duration">{{ formatDuration(place.duration) }}</span>
                  <span class="travel-distance">{{ formatDistance(place.distance) }}</span>
                </div>
              </div>
              
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
import { ref, onMounted, computed, watch } from 'vue'
import data from '../assets/data.json'

// 데이터
const mapInfo = data.mapInfo
const bankInfo = data.bankInfo

const selectedDo = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const selectedCountries = ref([])
const searchResults = ref([]) // 검색 결과 저장

// 출발지 설정
const selectedStartLocation = ref('default')
const customStartLocation = ref('')
const transportMode = ref('car')  // 'car', 'walk', 'bike' 중 하나

// 도착지 설정
const selectedEndLocation = ref('custom')
const customEndLocation = ref('')
const customEndLocationData = ref(null)

// 출발지 정보 (기본값)
const defaultStartLocation = {
  name: 'SSAFY 부울경 캠퍼스',
  address: '부산 강서구 녹산산업중로 333',
  lat: 35.094663, // 위도
  lng: 128.855308 // 경도
}

// 실제 사용할 출발지 정보 (computed)
const startLocation = computed(() => {
  // 디버깅을 위한 로그 추가
  console.log('startLocation computed 호출됨:', {
    selectedStartLocation: selectedStartLocation.value,
    hasCustomData: !!customStartLocationData.value,
    hasCurrentData: !!currentLocationData.value
  })

  if (selectedStartLocation.value === 'default') {
    return defaultStartLocation
  } else if (selectedStartLocation.value === 'custom' && customStartLocationData.value) {
    return customStartLocationData.value
  } else if (selectedStartLocation.value === 'current' && currentLocationData.value) {
    return currentLocationData.value
  }
  return defaultStartLocation
})

// 사용자 정의 출발지 데이터
const customStartLocationData = ref(null)
// 현재 위치 데이터
const currentLocationData = ref(null)

let mapInstance = null
let markers = []
let infowindows = []
let startMarker = null      // 출발지 마커
let startInfoWindow = null  // 출발지 인포윈도우

// 컴포넌트 마운트 시 실행
onMounted(async () => {
  console.log('MapPage 컴포넌트 마운트됨')
  
  try {
    // 1. 카카오맵 API 로드
    await loadKakaoMap()
    
    // 2. 지도 초기화
    initializeMap()
    
    // 3. 출발지 마커 표시
    setStartLocationMarker()
    
    // 4. 현재 위치 가져오기 시도
    getCurrentLocation()
    
    console.log('지도 초기화 완료')
  } catch (error) {
    console.error('지도 초기화 중 오류 발생:', error)
  }
})

// 교통수단 변경 감지
watch(transportMode, () => {
  console.log('교통수단 변경됨:', transportMode.value)
  
  // 검색 결과가 있으면 경로 정보 다시 계산
  if (searchResults.value.length > 0) {
    updateRouteInfo()
  }
})

// 출발지 변경 감지
watch(startLocation, () => {
  console.log('출발지 변경됨:', startLocation.value)
  
  // 출발지 마커 업데이트
  setStartLocationMarker()
  
  // 검색 결과가 있으면 경로 정보 다시 계산
  if (searchResults.value.length > 0) {
    updateRouteInfo()
  }
}, { deep: true })

// 현재 위치 데이터 변경 감지
watch(currentLocationData, (newVal) => {
  if (newVal && selectedStartLocation.value === 'current') {
    console.log('현재 위치 데이터 변경됨:', newVal)
    
    // 기존 마커 제거
    if (startMarker) {
      startMarker.setMap(null)
    }
    
    // 새 마커 설정
    setStartLocationMarker()
    
    // 검색 결과가 있으면 거리 정보 재계산
    if (searchResults.value.length > 0) {
      updateRouteInfo()
    }
  }
}, { deep: true })

// 출발지 선택 변경 감지
watch(selectedStartLocation, () => {
  console.log('출발지 선택 변경됨:', selectedStartLocation.value)
  
  // 모든 기존 마커와 인포윈도우 제거
  if (startMarker) {
    startMarker.setMap(null);
    startMarker = null;
  }
  
  if (startInfoWindow) {
    startInfoWindow.close();
    startInfoWindow = null;
  }
  
  // 현재 위치 선택 시 현재 위치 가져오기
  if (selectedStartLocation.value === 'current') {
    getCurrentLocation()
  }
  
  // 약간의 지연 후 마커 업데이트 (위치 데이터가 업데이트될 시간을 주기 위해)
  setTimeout(() => {
    setStartLocationMarker()
    
    // 검색 결과가 있으면 경로 정보 다시 계산
    if (searchResults.value.length > 0) {
      updateRouteInfo()
    }
  }, 500)
})

// 교통수단 아이콘 얻기
const getTransportIcon = (mode) => {
  switch (mode) {
    case 'car':
      return '🚗'
    case 'walk':
      return '🚶'
    case 'bike':
      return '🚲'
    default:
      return '🚗'
  }
}

// 현재 위치 가져오기
const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    console.error('이 브라우저에서는 위치 정보를 지원하지 않습니다.')
    alert('현재 브라우저에서는 위치 정보 기능을 사용할 수 없습니다.')
    // 출발지를 기본값으로 되돌림
    selectedStartLocation.value = 'default'
    return
  }
  
  // 기존 마커 제거
  if (startMarker) {
    startMarker.setMap(null)
    startMarker = null
  }
  
  if (startInfoWindow) {
    startInfoWindow.close()
    startInfoWindow = null
  }
  
  // 중요: 이미 위치 정보 가져오기가 진행 중인지 확인 (중복 실행 방지)
  if (window._gettingLocation) {
    console.log('이미 위치 정보를 가져오는 중입니다.')
    return
  }
  
  window._gettingLocation = true
  
  // 로딩 메시지 표시 (alert 대신 콘솔로만 출력하도록 변경)
  const loadingMessage = '현재 위치를 가져오는 중입니다...'
  console.log(loadingMessage)
  // alert 대화상자는 제거하고 콘솔로만 표시
  
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      
      // 현재 위치 정보 저장
      currentLocationData.value = {
        name: '내 현재 위치',
        address: '현재 위치 (GPS)',
        lat: latitude,
        lng: longitude
      }
      
      console.log('현재 위치 정보 업데이트됨:', currentLocationData.value)
      
      // 지도 이동 및 마커 업데이트
      if (mapInstance && selectedStartLocation.value === 'current') {
        // 맵 이동
        mapInstance.setCenter(new kakao.maps.LatLng(latitude, longitude))
        
        // 마커 업데이트 (새 위치에 맞게)
        setStartLocationMarker()
        
        // 작업 완료 메시지 (alert 제거, 콘솔로만 출력)
        console.log('현재 위치로 출발지가 설정되었습니다.')
        
        // 검색 결과가 있으면 경로 정보 다시 계산
        if (searchResults.value.length > 0) {
          // 기존 검색 결과에 대한 거리 및 시간 정보 업데이트
          updateRouteInfo()
        }
      }
      
      // 위치 가져오기 상태 초기화
      window._gettingLocation = false
    },    (error) => {
      console.error('위치 정보를 가져오는데 실패했습니다:', error)
      let errorMessage = '위치 정보를 가져오는데 실패했습니다.';
      
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage = '위치 정보 액세스 권한이 거부되었습니다. 브라우저 주소창 옆의 자물쇠/정보 아이콘을 클릭하여 위치 권한을 허용해주세요.';
          break;
        case error.POSITION_UNAVAILABLE:
          errorMessage = '위치 정보를 사용할 수 없습니다. 인터넷 연결을 확인해주세요.';
          break;
        case error.TIMEOUT:
          errorMessage = '위치 정보 요청 시간이 초과되었습니다. 다시 시도해주세요.';
          break;
      }
      
      // 위치 오류 메시지 표시
      alert(errorMessage);
      
      // 오류 발생 시 기본 위치로 되돌림
      selectedStartLocation.value = 'default'
      setStartLocationMarker() // 기본 위치로 마커 재설정
      
      // 위치 가져오기 상태 초기화
      window._gettingLocation = false
    },
    {
      enableHighAccuracy: false, // 높은 정확도를 끄고 속도 중심으로 변경
      timeout: 8000,  // 타임아웃 시간 감소
      maximumAge: 60000    // 1분 이내의 캐시된 위치 허용
    }
  )
}

// 지도 초기화 함수
const initializeMap = () => {
  const container = document.getElementById('map')
  
  // 지도 옵션 설정 - 드래그 가능, 휠 확대/축소 가능 (옵션 명시적 설정)
  const options = {
    center: new kakao.maps.LatLng(startLocation.value.lat, startLocation.value.lng),
    level: 3,
    draggable: true,
    scrollwheel: true,
    disableDoubleClick: false,  // 더블 클릭 줌 활성화
    draggable: true  // 명시적인 재설정
  }
  
  // 지도 생성 전 컨테이너 스타일 확인 및 설정
  if (container) {
    // 컨테이너 스타일에 pointer-events: auto 추가
    container.style.pointerEvents = 'auto';
    container.style.touchAction = 'auto';
  }
  
  // 지도 생성 - 명시적인 옵션 적용
  mapInstance = new kakao.maps.Map(container, options)
  
  // 문제 해결: 강제로 드래그 가능 속성 설정
  mapInstance.setDraggable(true)
  mapInstance.setZoomable(true)
  
  // 지도 이벤트 리스너 추가
  kakao.maps.event.addListener(mapInstance, 'dragend', function() {
    console.log('지도 이동 완료:', mapInstance.getCenter().toString())
  })
  
  kakao.maps.event.addListener(mapInstance, 'zoom_changed', function() {
    console.log('지도 줌 레벨 변경:', mapInstance.getLevel())
  })
  
  // 강제로 클릭, 드래그 이벤트를 다시 활성화하는 트릭 적용
  mapInstance.relayout();
  
  // 명시적으로 지도 드래그 및 줌 가능하도록 다시 설정 (카카오맵 이벤트 발생 후)
  setTimeout(() => {
    if(mapInstance) {
      mapInstance.setDraggable(true)
      mapInstance.setZoomable(true)
      console.log('지도 드래그 및 줌 기능 재활성화됨')
      // 레이아웃 재조정 (중요: 지도 요소의 제약 사항 해제에 도움)
      mapInstance.relayout();
    }
  }, 500)
  
  // 추가 타이머로 두 번째 설정 시도 (일부 환경에서 필요)
  setTimeout(() => {
    if(mapInstance) {
      mapInstance.setDraggable(true)
      mapInstance.setZoomable(true)
      mapInstance.relayout();
    }
  }, 2000)
  
  console.log('지도 객체 생성됨:', mapInstance)
}

// 출발지 마커 표시 함수
const setStartLocationMarker = () => {
  if (!mapInstance || !startLocation.value) {
    console.error('지도가 초기화되지 않았거나 출발지 정보가 없습니다.');
    return;
  }
  
  console.log('출발지 마커 설정:', startLocation.value);
  
  // 모든 기존 마커 및 인포윈도우 정리 (중요: 이전 마커가 제대로 제거되지 않는 문제 해결)
  // 기존 마커 제거
  if (startMarker) {
    startMarker.setMap(null);
    startMarker = null;
  }
  
  // 인포윈도우 제거
  if (startInfoWindow) {
    startInfoWindow.close();
    startInfoWindow = null;
  }
  
  // 이동할 좌표
  const startPosition = new kakao.maps.LatLng(startLocation.value.lat, startLocation.value.lng);
  
  // 마커 이미지 설정 - 더 큰 별모양 마커로 변경 (크기 증가)
  const markerImage = new kakao.maps.MarkerImage(
    'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png',
    new kakao.maps.Size(35, 45),  // 더 크게
    { offset: new kakao.maps.Point(17, 45) }
  );
  
  // 마커 생성 (zIndex 높게 설정하여 항상 위에 표시)
  startMarker = new kakao.maps.Marker({
    position: startPosition,
    map: mapInstance,
    image: markerImage,
    zIndex: 100,  // 다른 마커보다 앞에 표시
    title: startLocation.value.name
  });
  
  // 인포윈도우 생성 - 스타일 개선
  startInfoWindow = new kakao.maps.InfoWindow({
    content: `<div class="custom-start-info" style="padding: 12px; min-width: 220px; text-align: center; box-shadow: 0 3px 12px rgba(0,0,0,0.15); border-radius: 10px;">
      <div class="start-title" style="font-size: 16px; font-weight: bold; color: #333; margin-bottom: 8px;">${startLocation.value.name}</div>
      <div class="start-address" style="font-size: 13px; color: #444; margin: 6px 0;">${startLocation.value.address}</div>
      <div class="start-label" style="display: inline-block; background-color: #4285f4; color: white; padding: 4px 10px; border-radius: 5px; font-size: 13px; font-weight: 600;">출발지</div>
    </div>`,
    removable: true
  });
  
  // 마커 클릭 시 인포윈도우 표시
  kakao.maps.event.addListener(startMarker, 'click', function() {
    startInfoWindow.open(mapInstance, startMarker);
  });
    // 자동으로 인포윈도우 표시
  startInfoWindow.open(mapInstance, startMarker);
  
  // 지도 중심 이동 및 확대 레벨 조정
  mapInstance.setCenter(startPosition);
  mapInstance.setLevel(3);  // 적절한 확대 레벨 지정
  
  // 명시적으로 지도가 움직일 수 있도록 설정
  mapInstance.setDraggable(true);
  mapInstance.setZoomable(true);
  
  console.log('출발지 마커 설정 완료, 지도 이동/줌 활성화');
}

// 마커 표시 함수
const displayMarkers = () => {
  // 기존 마커 제거
  clearMarkers()
  
  if (!searchResults.value.length || !mapInstance) return
  
  // 검색 결과의 모든 위치를 포함하는 경계 설정
  const bounds = new kakao.maps.LatLngBounds()
  
  // 출발지도 경계에 추가 (항상 출발지를 포함하도록)
  bounds.extend(new kakao.maps.LatLng(startLocation.value.lat, startLocation.value.lng))
  
  // 검색된 모든 은행에 마커 표시
  searchResults.value.forEach((place, index) => {
    const coords = new kakao.maps.LatLng(place.y, place.x)
    // 마커 위치를 경계에 추가
    bounds.extend(coords)
    
    // 마커 이미지 설정 (인덱스 추가)
    const markerImage = new kakao.maps.MarkerImage(
      'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png',
      new kakao.maps.Size(36, 37),
      {
        offset: new kakao.maps.Point(13, 37),
        spriteSize: new kakao.maps.Size(36, 691),
        spriteOrigin: new kakao.maps.Point(0, (index % 10) * 46 + 10)
      }
    )
    
    // 마커 생성 (인덱스 레이블 추가)
    const marker = new kakao.maps.Marker({
      map: mapInstance,
      position: coords,
      title: place.place_name,
      image: markerImage
    })
    markers.push(marker)
    
    // 인포윈도우 생성 - 시간과 거리 정보가 제대로 표시되도록 수정
    let durationText = '시간 정보 없음'
    let distanceText = ''
    
    if (place.duration !== undefined && place.duration !== null) {
      durationText = formatDuration(place.duration)
    }
    
    if (place.distance !== undefined && place.distance !== null) {
      distanceText = formatDistance(place.distance)
    }
    
    const infoContent = `
      <div class="custom-info-window">
        <div class="info-title">${place.place_name}</div>
        <div class="info-address">${place.address_name}</div>
        <div class="info-travel-time">
          ${getTransportIcon(transportMode.value)} ${durationText} (${distanceText})
        </div>
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
      // 출발지 인포윈도우 닫기
      if (startInfoWindow) {
        startInfoWindow.close()
      }
      // 현재 인포윈도우 열기
      infowindow.open(mapInstance, marker)
    })
    
    // 첫번째 마커에 인포윈도우 자동 열기
    if (index === 0) {
      infowindow.open(mapInstance, marker)
    }
  })
  
  // 모든 마커가 보이도록 지도 범위 설정
  // 약간의 패딩을 추가하여 모든 마커가 잘 보이게 함
  mapInstance.setBounds(bounds, 50, 50, 50, 50)
  
  // 사용자가 지도를 이동할 수 있도록 확실히 설정
  mapInstance.setDraggable(true)
  mapInstance.setZoomable(true)
  
  // 인포윈도우 내 버튼으로 길찾기할 수 있도록 전역함수 설정
  window.showDirectionsFromMap = (index) => {
    if (searchResults.value && searchResults.value.length > index) {
      showDirections(searchResults.value[index])
    }
  }
}

// 검색 결과 경로 정보 업데이트
const updateRouteInfo = async () => {
  if (!searchResults.value.length) return
  
  // 기존 마커 제거
  clearMarkers()
  
  try {
    // 모든 검색 결과에 대해 소요 시간 및 거리 재계산
    const updatedResults = await Promise.all(
      searchResults.value.map(async (place) => {
        try {
          const routeInfo = await calculateRouteInfo(
            { lat: startLocation.value.lat, lng: startLocation.value.lng },
            { lat: parseFloat(place.y), lng: parseFloat(place.x) }
          );
          
          return {
            ...place,
            duration: routeInfo.duration,
            distance: routeInfo.distance
          }
        } catch (err) {
          console.error('경로 계산 중 오류:', err)
          return place
        }
      })
    )
    
    // 소요 시간 기준으로 정렬
    updatedResults.sort((a, b) => {
      if (!a.duration) return 1
      if (!b.duration) return -1
      return a.duration - b.duration
    })
    
    // 검색 결과 업데이트
    searchResults.value = updatedResults
    
    // 마커 다시 표시
    displayMarkers()
  } catch (error) {
    console.error('경로 정보 업데이트 중 오류:', error)
  }
}

// 현재 위치 가져오기
const getUserCurrentLocation = () => {
  if (!navigator.geolocation) {
    console.error('이 브라우저에서는 위치 정보를 지원하지 않습니다.')
    return
  }
  
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      
      // 현재 위치 정보 저장
      currentLocationData.value = {
        name: '현재 위치',
        address: '현재 위치',
        lat: latitude,
        lng: longitude
      }
      
      console.log('현재 위치 정보 업데이트됨:', currentLocationData.value)
    },
    (error) => {
      console.error('위치 정보를 가져오는데 실패했습니다:', error)
    }
  )
}

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

// 출발지로 지도 이동 및 인포윈도우 표시
const focusOnStartLocation = () => {
  if (mapInstance && startMarker && startInfoWindow) {
    // 출발지 위치로 지도 이동
    mapInstance.setCenter(new kakao.maps.LatLng(startLocation.value.lat, startLocation.value.lng))
    mapInstance.setLevel(3) // 확대 레벨 조정
    
    // 다른 인포윈도우 닫기 (검색 결과 인포윈도우)
    infowindows.forEach(iw => iw.close())
    
    // 출발지 인포윈도우 열기
    
    // 인포윈도우 내용 업데이트
    startInfoWindow.setContent(`<div class="custom-start-info">
      <div class="start-title">${startLocation.value.name}</div>
      <div class="start-address">${startLocation.value.address}</div>
      <div class="start-label">출발지</div>
    </div>`)
    
    startInfoWindow.open(mapInstance, startMarker)
  }
}

// 경로 안내 보여주기
const showDirections = async (place) => {
  console.log('길찾기 버튼 클릭됨:', place)
  
  // 카카오맵 길찾기 API 호출
  const { kakao } = window
  if (!kakao || !kakao.maps || !kakao.maps.services) {
    console.error('카카오맵 API가 로드되지 않았습니다.')
    alert('카카오맵 API가 로드되지 않아 길찾기 기능을 사용할 수 없습니다.')
    return
  }
  
  // 출발지와 도착지 좌표 설정
  const start = startLocation.value // 출발지 (선택된 출발지)
  const end = {
    name: place.place_name,
    lat: place.y, 
    lng: place.x
  }
  
  // 경로 정보 계산
  try {
    const routeInfo = await calculateRouteInfo(
      { lat: start.lat, lng: start.lng },
      { lat: parseFloat(end.lat), lng: parseFloat(end.lng) }
    );
    
    // 소요 시간 및 거리 정보를 사용자에게 표시
    const durationText = formatDuration(routeInfo.duration)
    const distanceText = formatDistance(routeInfo.distance)
    
    // 길찾기 정보를 표시 (알림)
    const modeText = {
      'car': '자동차',
      'walk': '도보',
      'bike': '자전거'
    }
    
    // 출발 - 도착 정보와 소요 시간 표시
    alert(`${start.name}에서 ${end.name}까지 ${modeText[transportMode.value]} 경로입니다.\n소요 시간: ${durationText}\n이동 거리: ${distanceText}`)
  } catch (error) {
    console.error('경로 계산 중 오류 발생:', error)
  }
  
  // 교통수단에 따라 다른 URL 파라미터 사용
  let routeMode = 'car' // 기본값 자동차
  
  // 카카오맵에서는 car만 공식 지원, 나머지는 다른 방식으로 구현 필요
  if (transportMode.value === 'walk') {
    routeMode = 'foot' // 비공식 파라미터 (작동하지 않을 수 있음)
  } else if (transportMode.value === 'bike') {
    routeMode = 'bike' // 비공식 파라미터 (작동하지 않을 수 있음)
  }
  
  // 카카오맵 길찾기 URL 생성
  // 카카오맵 웹 URL 방식 사용: https://apis.map.kakao.com/web/guide/#routeurl
  let kakaoMapUrl = `https://map.kakao.com/link/to/${end.name},${end.lat},${end.lng}/from/${start.name},${start.lat},${start.lng}`
  
  // 교통수단 정보 추가 (비공식 파라미터)
  if (transportMode.value !== 'car') {
    kakaoMapUrl += `?routeMode=${routeMode}`
  }
    // 새 창에서 카카오맵 길찾기 열기 (사용자가 원하면 새 창 열도록 확인)
  if (confirm('카카오맵에서 상세 경로를 확인하시겠습니까?')) {
    window.open(kakaoMapUrl, '_blank');
  }
  
  // 지도에 경로 표시
  showRouteOnMap(start, end);
};  // 지도에 경로 표시하기
const showRouteOnMap = (start, end) => {
  const { kakao } = window;
  if (!kakao || !kakao.maps || !mapInstance) {
    console.error('카카오맵 API가 로드되지 않았거나 지도가 초기화되지 않았습니다.');
    return;
  }

  // 이전 경로 삭제
  if (window.currentRoute) {
    if (Array.isArray(window.currentRoute)) {
      window.currentRoute.forEach(route => route.setMap(null));
    } else {
      window.currentRoute.setMap(null);
    }
    window.currentRoute = null;
  }
  
  if (window.currentRouteMarkers) {
    window.currentRouteMarkers.forEach(marker => marker.setMap(null));
    window.currentRouteMarkers = [];
  }
  
  // 교통수단에 따라 색상 및 스타일 변경
  let strokeColor, strokeStyle;
  
  switch(transportMode.value) {
    case 'car':
      strokeColor = '#3366FF'; // 파란색
      strokeStyle = 'solid';
      break;
    case 'walk':
      strokeColor = '#00C73C'; // 녹색
      strokeStyle = 'shortdash';
      break;
    case 'bike':
      strokeColor = '#FF3366'; // 붉은색
      strokeStyle = 'dashdot';
      break;
    default:
      strokeColor = '#3366FF';
      strokeStyle = 'solid';
  }
  
  console.log('경로 그리기:', start, end);
  
  // 두 지점이 모두 보이게 지도 중심 및 레벨 조정
  const bounds = new kakao.maps.LatLngBounds();
  bounds.extend(new kakao.maps.LatLng(start.lat, start.lng));
  bounds.extend(new kakao.maps.LatLng(end.lat, end.lng));
  
  // 경로 검색 시도 (Directions Service API 사용)
  try {
    // 로딩 메시지 표시 (선택적)
    console.log('도로 경로 검색 중...');
    
    // 경로 검색 시작
    if (kakao.maps.services && kakao.maps.services.Directions) {
      // Directions 서비스 객체 생성
      const directionService = new kakao.maps.services.Directions();
        // 카카오맵 API 요청 형식에 맞게 옵션 수정
      const options = {
        // 출발지 - 카카오맵 API는 x(경도), y(위도) 형식 사용
        origin: {
          x: start.lng,
          y: start.lat
        },
        // 도착지
        destination: {
          x: end.lng,
          y: end.lat
        },
        // 경유지 (없음)
        waypoints: [],
        // 교통수단 설정
        // 1: 자동차, 3: 도보
        roadType: transportMode.value === 'walk' ? 3 : 1
      };
      
      // 올바른 함수명 사용: route가 아닌 getRoutes
      directionService.getRoutes(options, function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
          console.log('경로 검색 성공:', result);
          
          // 경로 데이터 추출
          const routes = [];
          
          // 경로 정보 (첫 번째 경로만 사용)
          if (result.routes && result.routes.length > 0) {
            const routeInfo = result.routes[0];
            
            // 섹션별 경로 그리기
            if (routeInfo.sections) {
              window.currentRoute = [];
              
              routeInfo.sections.forEach((section, idx) => {
                // 경로 좌표 배열 생성
                const path = section.roads.flatMap(road => {
                  return road.vertexes.map((vertex, i) => {
                    // 버텍스는 [경도, 위도] 배열로 되어있음 -> LatLng 객체로 변환
                    if (i % 2 === 0 && i + 1 < road.vertexes.length) {
                      return new kakao.maps.LatLng(road.vertexes[i+1], road.vertexes[i]);
                    }
                    return null;
                  }).filter(Boolean); // null 제거
                });
                
                // 경로마다 다른 색상 변화를 주기 위한 계산
                const sectionColor = adjustColor(strokeColor, idx * 0.1);
                
                // 폴리라인 생성
                const polyline = new kakao.maps.Polyline({
                  path: path,
                  strokeWeight: 5,
                  strokeColor: sectionColor,
                  strokeOpacity: 0.8,
                  strokeStyle: strokeStyle
                });
                
                // 지도에 표시
                polyline.setMap(mapInstance);
                
                // 나중에 제거할 수 있도록 저장
                window.currentRoute.push(polyline);
              });
              
              // 전체 경로가 보이도록 지도 범위 조정
              // 여기서 경로의 모든 점을 고려하여 범위를 업데이트
              routeInfo.sections.forEach(section => {
                section.roads.forEach(road => {
                  for (let i = 0; i < road.vertexes.length; i += 2) {
                    if (i + 1 < road.vertexes.length) {
                      bounds.extend(new kakao.maps.LatLng(road.vertexes[i+1], road.vertexes[i]));
                    }
                  }
                });
              });
            }
          } else {
            // 경로 정보가 없는 경우 직선 경로로 폴백
            fallbackToStraightLine();
          }
          
          // 지도 범위 설정
          mapInstance.setBounds(bounds, 50);
        } else {
          // 검색 실패 시 직선 경로로 폴백
          console.warn('경로 검색 실패, 직선 경로로 대체합니다:', status);
          fallbackToStraightLine();
        }
      });
    } else {
      console.warn('카카오맵 Direction 서비스를 사용할 수 없습니다, 직선 경로로 대체합니다');
      fallbackToStraightLine();
    }
  } catch (error) {
    console.error('경로 검색 중 오류:', error);
    // 오류 발생 시 직선 경로로 폴백
    fallbackToStraightLine();
  }
  
  // 직선 경로로 표시하는 폴백 함수
  function fallbackToStraightLine() {
    console.log('직선 경로로 표시합니다');
    // 간단한 직선 경로로 표시
    const linePath = [
      new kakao.maps.LatLng(start.lat, start.lng),
      new kakao.maps.LatLng(end.lat, end.lng)
    ];
    
    // 경로 선 생성
    const polyline = new kakao.maps.Polyline({
      path: linePath,
      strokeWeight: 5,
      strokeColor: strokeColor,
      strokeOpacity: 0.8,
      strokeStyle: strokeStyle
    });
    
    // 경로를 지도에 표시
    polyline.setMap(mapInstance);
    
    // 현재 경로 저장 (나중에 삭제하기 위해)
    window.currentRoute = polyline;
  }
  
  // 색상 조정 함수 (경로 각 섹션마다 약간 다른 색상 적용)
  function adjustColor(color, factor) {
    // 16진수 색상을 RGB로 변환
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);
    
    // 색상 조정 (약간 더 밝게)
    const newR = Math.min(255, Math.round(r + (255 - r) * factor));
    const newG = Math.min(255, Math.round(g + (255 - g) * factor));
    const newB = Math.min(255, Math.round(b + (255 - b) * factor));
    
    // RGB를 16진수로 변환
    return '#' + 
      newR.toString(16).padStart(2, '0') + 
      newG.toString(16).padStart(2, '0') + 
      newB.toString(16).padStart(2, '0');
  }
  
  // 출발지 마커 표시
  const startMarkerImage = new kakao.maps.MarkerImage(
    'https://t1.daumcdn.net/mapjsapi/images/marker_green.png',
    new kakao.maps.Size(30, 44),
    { offset: new kakao.maps.Point(15, 44) }
  )
  
  const startMarker = new kakao.maps.Marker({
    position: new kakao.maps.LatLng(start.lat, start.lng),
    image: startMarkerImage,
    map: mapInstance
  })
  
  // 출발지 인포윈도우 생성
  const startInfoWindow = new kakao.maps.InfoWindow({
    content: `<div style="padding:5px;width:150px;text-align:center;">
      <div style="font-weight:bold;margin-bottom:3px;">${start.name}</div>
      <div style="color:blue;">출발지</div>
    </div>`,
    removable: true
  })
  
  // 출발지 마커 클릭시 인포윈도우 표시
  kakao.maps.event.addListener(startMarker, 'click', function() {
    startInfoWindow.open(mapInstance, startMarker)
  })
  
  // 도착지 마커 표시
  const endMarkerImage = new kakao.maps.MarkerImage(
    'https://t1.daumcdn.net/mapjsapi/images/marker_red.png',
    new kakao.maps.Size(30, 44),
    { offset: new kakao.maps.Point(15, 44) }
  )
  
  const endMarker = new kakao.maps.Marker({
    position: new kakao.maps.LatLng(end.lat, end.lng),
    image: endMarkerImage,
    map: mapInstance
  })
  
  // 도착지 인포윈도우 생성
  const endInfoWindow = new kakao.maps.InfoWindow({
    content: `<div style="padding:5px;width:150px;text-align:center;">
      <div style="font-weight:bold;margin-bottom:3px;">${end.name}</div>
      <div style="color:red;">도착지</div>
    </div>`,
    removable: true
  })
  
  // 도착지 마커 클릭시 인포윈도우 표시
  kakao.maps.event.addListener(endMarker, 'click', function() {
    endInfoWindow.open(mapInstance, endMarker)
  })
  
  // 도착지 인포윈도우 자동 표시 (중요: 도착지 정보를 바로 보여주기 위해)
  endInfoWindow.open(mapInstance, endMarker)
  
  // 마커 저장 (나중에 삭제하기 위해)
  window.currentRouteMarkers = [startMarker, endMarker]
  
  // 지도 범위 설정 (두 마커가 모두 보이게)
  mapInstance.setBounds(bounds)
}

// 모든 기존 마커와 인포윈도우 제거 함수
const clearMarkers = () => {
  // 검색 결과 마커 제거
  markers.forEach(marker => marker.setMap(null))
  infowindows.forEach(infowindow => infowindow.close())
  
  // 배열 초기화
  markers = []
  infowindows = []
  
  // 기존 라인 제거
  if (window.currentRoute) {
    window.currentRoute.setMap(null)
    window.currentRoute = null
  }
  
  // 기존 경로 마커 제거
  if (window.currentRouteMarkers) {
    window.currentRouteMarkers.forEach(marker => marker.setMap(null))
    window.currentRouteMarkers = []
  }
  
  console.log('모든 마커와 인포윈도우가 제거되었습니다.')
}

// 지도 로딩
const loadKakaoMap = () => {
  return new Promise((resolve, reject) => {
    // 이미 로드된 경우
    if (window.kakao && window.kakao.maps) {
      console.log('Kakao Maps API가 이미 로드되어 있습니다.');
      // 중요: 이미 로드되었더라도 명시적으로 맵을 다시 초기화
      window.kakao.maps.load(() => {
        console.log('기존 Kakao Maps API 재초기화 완료');
        resolve();
      });
      return;
    }

    console.log('Kakao Maps API 로드 시작');
    // .env 파일에서 API 키 가져오기
    const apiKey = import.meta.env.VITE_KAKAO_API_KEY;
    
    // API 키 유효성 검증    
    if (!apiKey) {
      console.error('API 키가 로드되지 않았습니다. .env 파일을 확인해주세요.');
      alert('.env 파일의 VITE_KAKAO_API_KEY가 설정되지 않았습니다.');
      reject(new Error('API 키가 없음'));
      return;
    }
    
    // 중요: 기존 스크립트 제거 전에 전역 객체 초기화
    if (window.kakao) {
      try {
        delete window.kakao;
      } catch (e) {
        console.warn('kakao 객체 초기화 실패:', e);
      }
    }
      // 기존 스크립트 제거
    const existingScript = document.querySelector('script[src*="dapi.kakao.com"]');
    if (existingScript) {
      document.head.removeChild(existingScript);
    }
    
    // 새 스크립트 생성
    const script = document.createElement('script');
    // 반드시 services, drawing, clusterer 라이브러리 포함 + 경로 찾기를 위해 라이브러리에 services 명시적 포함
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${apiKey}&autoload=false&libraries=services,clusterer,drawing`;
    script.async = true; // 비동기 로드
    script.defer = false; // defer 비활성화로 로드 우선순위 높임
    
    script.onload = () => {
      console.log('Kakao Maps 스크립트 로드 완료, Maps API 초기화 시작');
      
      // 명시적 타임아웃 추가 (일부 환경에서 초기화 지연 문제 해결)
      setTimeout(() => {
        try {
          window.kakao.maps.load(() => {
            console.log('Kakao Maps API 초기화 완료');
            
            // DOM 완전히 로드된 후 해상도
            requestAnimationFrame(() => {
              resolve();
            });
          });
        } catch (e) {
          console.error('Kakao Maps 초기화 중 오류:', e);
          reject(e);
        }
      }, 100);
    };
    
    script.onerror = (e) => {
      console.error('Kakao Maps 스크립트 로드 실패', e);
      console.error('카카오 개발자 사이트에서 http://localhost:5179 도메인이 등록되어 있는지 확인하세요.');
      alert('카카오 지도를 불러오는데 실패했습니다. 개발자 도구에서 자세한 오류를 확인해주세요.');
      reject(e);
    };
    
    // 스크립트를 head의 맨 앞에 삽입 (로딩 우선순위)
    const head = document.head || document.getElementsByTagName('head')[0];
    if (head.firstChild) {
      head.insertBefore(script, head.firstChild);
    } else {
      head.appendChild(script);
    }
    
    console.log('Kakao Maps 스크립트 태그 추가됨');
    
    // localhost 알림창 대응
    window.addEventListener('message', function(event) {
      if (event.data && typeof event.data === 'string' && event.data.includes('지역의 은행')) {
        console.log('알림 메시지 감지:', event.data);
        // 확인 버튼을 자동으로 클릭하는 로직
        const confirmButton = document.querySelector('.confirm-button');
        if (confirmButton) {
          confirmButton.click();
        }
      }
    });
  });
};

// 소요 시간 형식화
const formatDuration = (seconds) => {
  if (!seconds) return '시간 정보 없음';
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (hours > 0) {
    return `${hours}시간 ${minutes}분`;
  } else {
    return `${minutes}분`;
  }
};

// 거리 형식화
const formatDistance = (meters) => {
  if (!meters) return '';
    if (meters >= 1000) {
    return `${(meters / 1000).toFixed(1)}km`;
  } else {
    return `${meters}m`;
  }
};

// 검색 함수
const searchBanks = async () => {
  console.log('searchBanks 실행됨'); // 클릭 작동 확인용

  if (!window.kakao || !window.kakao.maps) {
    console.error('카카오맵이 아직 로드되지 않았습니다.');
    return;
  }

  // 선택 값 확인
  console.log('[선택된 값들]', {
    do: selectedDo.value,
    sigungu: selectedSigungu.value,
    bank: selectedBank.value,
    transportMode: transportMode.value
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
  places.keywordSearch(query, async function(result, status) {
    console.log('[키워드 검색 결과]', result)
    console.log('[키워드 검색 상태]', status)
      if (status === kakao.maps.services.Status.OK) {
      try {        // 검색 결과에 소요 시간 및 거리 정보 추가
        const resultsWithRouteInfo = await Promise.all(
          result.map(async (place) => {
            try {
              const routeInfo = await calculateRouteInfo(
                { lat: startLocation.value.lat, lng: startLocation.value.lng },
                { lat: parseFloat(place.y), lng: parseFloat(place.x) }
              );
              
              return {
                ...place,
                duration: routeInfo.duration,
                distance: routeInfo.distance
              }
            } catch (err) {
              console.error('경로 계산 중 오류:', err)
              return place
            }
          })
        )
        
        // 소요 시간 기준으로 정렬
        resultsWithRouteInfo.sort((a, b) => {
          if (!a.duration) return 1
          if (!b.duration) return -1
          return a.duration - b.duration
        })
          // 검색 결과 저장
        searchResults.value = resultsWithRouteInfo
        
        // 마커 표시
        displayMarkers()
      } catch (err) {
        console.error('검색 결과 처리 중 오류:', err)
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
    
    // 컨테이너 스타일 확인 및 설정 (중요: 포인터 이벤트 보장)
    container.style.pointerEvents = 'auto';
    container.style.touchAction = 'auto';
    
    // 지도 초기화 (출발지 기준) - 명시적으로 모든 옵션 설정
    const options = {
      center: new window.kakao.maps.LatLng(startLocation.value.lat, startLocation.value.lng), // 출발지(녹산산업중로 333)
      level: 3,  // 확대 레벨
      draggable: true,  // 드래그 가능 명시적 설정
      scrollwheel: true,  // 스크롤 가능 명시적 설정
      disableDoubleClick: false,  // 더블클릭 줌 가능
      tileAnimation: true  // 타일 애니메이션 활성화
    }
    
    try {
      console.log('지도 초기화 시작')
      
      // 지도 생성 전 이전 인스턴스 제거 (메모리 누수 방지 및 충돌 방지)
      if (mapInstance) {
        mapInstance = null;
      }
      
      // 지도 생성
      mapInstance = new kakao.maps.Map(container, options);
      console.log('지도 초기화 완료');
      
      // 명시적으로 드래그 및 줌 가능 설정
      mapInstance.setDraggable(true);
      mapInstance.setZoomable(true);
      
      console.log('지도 객체:', mapInstance ? '생성됨' : '생성 실패');
      
      // 지도 로드 확인
      if (mapInstance) {
        // 지도에 특별 이벤트 핸들러 추가 (드래그 시작/종료 시 커서 변경) - 사용자 피드백 개선
        kakao.maps.event.addListener(mapInstance, 'dragstart', function() {
          container.classList.add('dragging');
        });
        
        kakao.maps.event.addListener(mapInstance, 'dragend', function() {
          container.classList.remove('dragging');
          console.log('지도 이동 완료:', mapInstance.getCenter().toString());
        });
        
        // 지도 객체에 이벤트 리스너 추가
        kakao.maps.event.addListener(mapInstance, 'tilesloaded', function() {
          console.log('지도 타일 로딩 완료!');
          
          // 타일 로딩 완료 후에도 다시 한번 드래그와 줌 가능하도록 설정
          setTimeout(() => {
            if (mapInstance) {
              // 중요: 레이아웃 재조정 후 드래그 가능 설정
              mapInstance.relayout();
              mapInstance.setDraggable(true);
              mapInstance.setZoomable(true);
              
              // CSS 스타일 직접 조작 (fallback)
              const mapElement = document.querySelector('.map_default');
              if (mapElement) {
                mapElement.style.pointerEvents = 'auto';
              }
            }
          }, 500);
        });
        
        // 추가 이벤트 리스너: 마우스 인식 확인용 (디버깅용)
        kakao.maps.event.addListener(mapInstance, 'click', function(mouseEvent) {
          console.log('지도 클릭됨:', mouseEvent.latLng.toString());
        });
        
        // 출발지 마커 추가
        startMarker = new kakao.maps.Marker({
          map: mapInstance,
          position: new kakao.maps.LatLng(startLocation.value.lat, startLocation.value.lng),
          title: startLocation.value.name,
          // 출발지 마커 이모티콘을 더 눈에 띄는 큰 파란색 마커로 변경
          image: new kakao.maps.MarkerImage(
            // 큰 파란색 마커 이미지
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png', 
            new kakao.maps.Size(40, 42), 
            { offset: new kakao.maps.Point(20, 42) }
          )
        });
        
        // 출발지 인포윈도우 - 더 눈에 띄게 디자인 변경
        startInfoWindow = new kakao.maps.InfoWindow({
          content: `<div class="custom-start-info">
                     <div class="start-title">${startLocation.value.name}</div>
                     <div class="start-address">${startLocation.value.address}</div>
                     <div class="start-label">출발지</div>
                   </div>`,
          removable: true // 닫기 버튼 표시
        });
        
        // 마커 클릭 시 출발지 정보 표시
        kakao.maps.event.addListener(startMarker, 'click', function() {
          startInfoWindow.open(mapInstance, startMarker);
        });
        
        // 초기에는 출발지 인포윈도우 표시
        startInfoWindow.open(mapInstance, startMarker);
        
        // 추가 타이머: 지도 설정 보장
        setTimeout(() => {
          mapInstance.relayout();
          mapInstance.setDraggable(true);
          mapInstance.setZoomable(true);
        }, 1500);
      }
    } catch (mapError) {
      console.error('지도 객체 생성 실패:', mapError);
      alert('지도 객체 생성 실패. 새로고침 후 다시 시도해보세요.');
    }
    
    // 초기 데이터 확인용 로그
    console.log('지도 정보:', mapInfo.length, '개 지역');
    console.log('은행 정보:', bankInfo.length, '개 은행');
  } catch (e) {
    console.error('카카오맵 로딩 실패:', e);
    alert('카카오맵 로딩에 실패했습니다. 개발자 도구의 콘솔에서 자세한 오류를 확인하세요.');
  }
});  // 경로 정보 계산 함수 (소요 시간, 거리)
  const calculateRouteInfo = (start, end) => {
    return new Promise((resolve, reject) => {
      const { kakao } = window
      if (!kakao || !kakao.maps) {
        reject(new Error('카카오맵 API가 로드되지 않았습니다.'))
        return
      }
      
      // 먼저 카카오맵 Direction API를 사용하여 실제 경로 정보 가져오기 시도
      if (kakao.maps.services && kakao.maps.services.Directions) {
        try {
          // Directions 서비스 객체 생성
          const directionService = new kakao.maps.services.Directions();
          
          // 옵션 설정 - 카카오맵 API 형식에 맞게 수정
          const options = {
            origin: {
              x: start.lng,
              y: start.lat
            },
            destination: {
              x: end.lng,
              y: end.lat
            },
            waypoints: [], // 경유지 (없음)
            // 교통수단별 설정: 1=자동차, 3=도보
            roadType: transportMode.value === 'walk' ? 3 : 1
          };
          
          // 경로 검색 요청 - getRoutes 함수 사용
          directionService.getRoutes(options, function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
              console.log('실제 경로 계산 성공:', result);
              
              // 경로 정보 가져오기
              if (result.routes && result.routes.length > 0) {
                const route = result.routes[0];
                
                // 총 거리와 소요 시간 가져오기
                let totalDistance = 0;
                let totalDuration = 0;
                
                // 모든 섹션의 거리와 시간을 합산
                if (route.sections) {
                  route.sections.forEach(section => {
                    totalDistance += section.distance;
                    totalDuration += section.duration;
                  });
                  
                  resolve({
                    distance: totalDistance,
                    duration: totalDuration
                  });
                  return;
                }
              }
              
              // 경로는 찾았지만 정보가 부족한 경우 기존 계산 방식으로 폴백
              fallbackToHaversine();
            } else {
              console.warn('실제 경로 계산 실패, 직선 거리 계산법으로 대체합니다:', status);
              fallbackToHaversine();
            }
          });
        } catch (error) {
          console.error('경로 계산 중 오류:', error);
          fallbackToHaversine();
        }
      } else {
        // Directions 서비스를 사용할 수 없는 경우 대체 방법 사용
        fallbackToHaversine();
      }
      
      // 직선 거리를 이용한 대체 계산 방법
      function fallbackToHaversine() {
        // 직선 거리 계산으로 대체
        const lineDistance = calculateLineDistance(start, end);
        
        // 교통수단별 대략적 소요 시간 계산 (초 단위)
        let approxDuration;
        switch(transportMode.value) {
          case 'car':
            // 자동차 평균 시속 40km/h (도시 내 교통을 고려)
            approxDuration = (lineDistance / 40000) * 3600;
            break;
          case 'walk':
            // 도보 평균 시속 4km/h
            approxDuration = (lineDistance / 4000) * 3600;
            break;
          case 'bike':
            // 자전거 평균 시속 15km/h
            approxDuration = (lineDistance / 15000) * 3600;
            break;
          default:
            approxDuration = (lineDistance / 40000) * 3600;
        }
        
        resolve({
          distance: lineDistance,
          duration: Math.round(approxDuration)
        });
      }
    });
  }
  // 두 좌표 사이의 직선 거리 계산 (미터 단위) - Haversine 공식 사용
  const calculateLineDistance = (point1, point2) => {
    if (!point1 || !point2) return 0;
    
    // null 체크 추가
    if (point1.lat === undefined || point1.lng === undefined || 
        point2.lat === undefined || point2.lng === undefined) {
      console.error('잘못된 좌표 정보:', point1, point2);
      return 0;
    }
    
    try {
      const R = 6371e3; // 지구 반경 (미터)
      const φ1 = parseFloat(point1.lat) * Math.PI / 180; // 위도1 (라디안)
      const φ2 = parseFloat(point2.lat) * Math.PI / 180; // 위도2 (라디안)
      const Δφ = (parseFloat(point2.lat) - parseFloat(point1.lat)) * Math.PI / 180; // 위도 차이
      const Δλ = (parseFloat(point2.lng) - parseFloat(point1.lng)) * Math.PI / 180; // 경도 차이
      
      const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                Math.cos(φ1) * Math.cos(φ2) *
                Math.sin(Δλ/2) * Math.sin(Δλ/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      
      const distance = Math.round(R * c); // 미터 단위 거리 (반올림)
      console.log(`거리 계산: ${point1.lat},${point1.lng} -> ${point2.lat},${point2.lng} = ${distance}m`);
      return distance;
    } catch (error) {
      console.error('거리 계산 중 오류:', error);
      return 0;
    }
  }

// 사용자 정의 위치 검색
const searchCustomLocation = (type) => {
  if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
    console.error('카카오맵 API가 로드되지 않았습니다.')
    alert('카카오맵 API가 로드되지 않아 위치 검색 기능을 사용할 수 없습니다.')
    return
  }
  
  const geocoder = new kakao.maps.services.Geocoder()
  const address = customStartLocation.value
  
  if (!address) {
    alert('주소를 입력해주세요.')
    return
  }
  
  console.log('출발지 위치 검색 요청:', address)
  
  // 기존 마커 제거
  if (startMarker) {
    startMarker.setMap(null)
    startMarker = null
  }
  
  if (startInfoWindow) {
    startInfoWindow.close()
    startInfoWindow = null
  }
  
  // 주소로 좌표 검색
  geocoder.addressSearch(address, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const coords = new kakao.maps.LatLng(result[0].y, result[0].x)
      
      // 출발지 저장
      customStartLocationData.value = {
        name: address,
        address: result[0].address_name || address,
        lat: parseFloat(result[0].y),
        lng: parseFloat(result[0].x)
      }
      
      console.log('출발지 설정 완료:', customStartLocationData.value)
      
      // 지도 이동 (반드시 먼저 수행)
      mapInstance.setCenter(coords)
      mapInstance.setLevel(3) // 적절한 확대 레벨로 설정
      
      // 출발지만 변경된 경우 마커 업데이트
      setStartLocationMarker()
      
      // 확인 메시지
      alert(`출발지가 "${address}"(으)로 설정되었습니다.`)
      
      // 검색 결과가 있으면 경로 정보 다시 계산
      if (searchResults.value.length > 0) {
        // 약간의 딜레이를 주어 UI 업데이트 후 계산하도록 함
        setTimeout(() => {
          updateRouteInfo()
        }, 300)
      }
    } else {
      alert('주소 검색에 실패했습니다. 올바른 주소인지 확인해주세요.')
      // 검색 실패 시 기본 위치로 되돌리기
      customStartLocation.value = ''
    }
  })
}
</script>

<style scoped>
.map-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.map-header {
  background: linear-gradient(135deg, #1a73e8, #4285f4);
  color: white;
  padding: 2rem 0;
  text-align: center;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1rem;
  opacity: 0.9;
}

.map-container {
  display: grid;
  grid-template-columns: 360px 1fr;
  height: calc(100vh - 108px);
  overflow: hidden;
}

/* 검색 패널 */
.search-panel {
  background: white;
  padding: 1.5rem;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 10;
}

.panel-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
}

/* 위치 설정 */
.location-settings {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #f8f9ff;
  border-radius: 10px;
  border: 1px solid #e0e6f2;
}

.location-header {
  margin-bottom: 1rem;
}

.location-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1a73e8;
}

.location-selector {
  margin-bottom: 1.2rem;
}

.location-selector label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #555;
}

.selector-content {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.location-select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  background-color: white;
}

.custom-location-input {
  flex-grow: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.location-search-btn {
  padding: 0.5rem 1rem;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  margin-top: 0.5rem;
}

.location-search-btn:hover {
  background-color: #3367d6;
}

/* 교통수단 선택 */
.transport-options {
  margin-bottom: 1rem;
}

.transport-options h4 {
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #555;
}

.transport-buttons {
  display: flex;
  gap: 0.5rem;
}

.transport-btn {
  flex: 1;
  padding: 0.6rem 0;
  border: 1px solid #ddd;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.transport-btn:hover {
  background-color: #e9ecef;
}

.transport-btn.active {
  background-color: #4285f4;
  color: white;
  border-color: #4285f4;
}

/* 검색 필터 */
.search-filters {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-item:first-child {
  grid-column: 1 / -1;
}

.filter-item label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #555;
}

.filter-select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  background-color: white;
}

.search-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  transition: background-color 0.2s;
}

.search-btn:hover {
  background-color: #3367d6;
}

/* 검색 결과 */
.search-results {
  margin-bottom: 1.5rem;
}

.results-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.result-count {
  font-size: 0.9rem;
  font-weight: 400;
  color: #666;
}

.results-list {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.result-card {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #eaeef5;
}

.result-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.place-name {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.result-index {
  background-color: #4285f4;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
}

.place-address {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.8rem;
}

.travel-time {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.8rem;
  padding: 0.5rem;
  background-color: #f5f7fa;
  border-radius: 6px;
}

.travel-icon {
  font-size: 1.1rem;
}

.travel-info {
  flex: 1;
}

.travel-duration {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
  margin-right: 0.5rem;
}

.travel-distance {
  font-size: 0.85rem;
  color: #666;
}

.result-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  cursor: pointer;
  transition: all 0.2s;
}

.directions-btn {
  background-color: #4285f4;
  color: white;
}

.directions-btn:hover {
  background-color: #3367d6;
}

.view-btn {
  background-color: #f5f5f5;
  color: #333;
}

.view-btn:hover {
  background-color: #e9ecef;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 0.9rem;
}

/* 지도 뷰 */
.map-view {
  height: 100%;
  position: relative;
  z-index: 1; /* 명시적으로 z-index 설정 */
  pointer-events: auto; /* 포인터 이벤트 명시적 활성화 */
}

#map {
  width: 100%;
  height: 100%;
  pointer-events: auto !important; /* 포인터 이벤트 강제 활성화 */
  touch-action: auto !important; /* 터치 액션 활성화 */
  cursor: grab; /* 드래그 가능한 커서 표시 */
}

/* 지도 컨테이너가 드래그 중일 때 커서 변경 */
#map.dragging {
  cursor: grabbing;
}

/* 도우미 섹션 */
.banking-helper {
  margin-top: 2rem;
  padding: 1.2rem;
  background-color: #f8f9ff;
  border-radius: 10px;
  border: 1px solid #e0e6f2;
}

.banking-helper h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.helper-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.helper-card {
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.helper-icon {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.helper-card h4 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.helper-card p {
  font-size: 0.85rem;
  color: #666;
}

/* 인포윈도우 커스텀 스타일 */
:deep(.custom-info-window) {
  padding: 0.8rem;
  width: 200px;
  font-size: 0.9rem;
}

:deep(.info-title) {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  color: #333;
}

:deep(.info-address) {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
}

:deep(.info-travel-time) {
  font-size: 0.9rem;
  color: #4285f4;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

:deep(.info-button) {
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.4rem;
  width: 100%;
  font-size: 0.85rem;
  cursor: pointer;
}

:deep(.info-button:hover) {
  background-color: #3367d6;
}

:deep(.custom-start-info),
:deep(.custom-end-info) {
  padding: 0.7rem;
  width: 180px;
  font-size: 0.9rem;
}

:deep(.start-title),
:deep(.end-title) {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

:deep(.start-address),
:deep(.end-address) {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.3rem;
}

:deep(.start-label),
:deep(.end-label) {
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  display: inline-block;
}

:deep(.start-label) {
  background-color: #e6f4ea;
  color: #1b7b44;
}

:deep(.end-label) {
  background-color: #fce8e6;
  color: #c5221f;
}

/* 반응형 조정 */
@media (max-width: 992px) {
  .map-container {
    grid-template-columns: 1fr;
    grid-template-rows: 50% 50%;
    height: auto;
    min-height: 80vh;
  }
  
  .search-panel {
    order: 2;
  }
  
  .map-view {
    order: 1;
    height: 50vh;
  }
}

@media (max-width: 576px) {
  .search-filters {
    grid-template-columns: 1fr;
  }
  
  .helper-cards {
    grid-template-columns: 1fr;
  }
}
</style>
