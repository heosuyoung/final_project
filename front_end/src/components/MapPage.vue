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
        <div class="location-settings">
          <div class="location-header">
            <h3>출발지와 도착지 설정</h3>
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

// 출발지 정보 (기본값)
const defaultStartLocation = {
  name: 'SSAFY 부울경 캠퍼스',
  address: '부산 강서구 녹산산업중로 333',
  lat: 35.094663, // 위도
  lng: 128.855308 // 경도
}

// 실제 사용할 출발지 정보 (computed)
const startLocation = computed(() => {
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
  const start = startLocation.value // 출발지 (선택된 출발지)
  const end = {
    name: place.place_name,
    lat: place.y, 
    lng: place.x
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
  
  // 새 창에서 카카오맵 길찾기 열기
  window.open(kakaoMapUrl, '_blank')
  
  // 지도에 경로 표시
  showRouteOnMap(start, end)
}

// 지도에 경로 표시하기
const showRouteOnMap = (start, end) => {
  // 이전 경로 삭제
  if (window.currentRoute) {
    window.currentRoute.setMap(null)
  }
  
  if (window.currentRouteMarkers) {
    window.currentRouteMarkers.forEach(marker => marker.setMap(null))
    window.currentRouteMarkers = []
  }
  
  // 교통수단에 따라 색상 및 스타일 변경
  let strokeColor, strokeStyle
  
  switch(transportMode.value) {
    case 'car':
      strokeColor = '#3366FF' // 파란색
      strokeStyle = 'solid'
      break
    case 'walk':
      strokeColor = '#00C73C' // 녹색
      strokeStyle = 'shortdash'
      break
    case 'bike':
      strokeColor = '#FF3366' // 붉은색
      strokeStyle = 'dashdot'
      break
    default:
      strokeColor = '#3366FF'
      strokeStyle = 'solid'
  }
  
  // 카카오 길찾기 API로 실제 경로 가져오기 시도
  const directions = new kakao.maps.services.Directions()
  
  directions.route({
    origin: new kakao.maps.LatLng(start.lat, start.lng),
    destination: new kakao.maps.LatLng(end.lat, end.lng),
    waypoints: [],
    priority: 'RECOMMEND'
  }, (result, status) => {
    // 두 지점이 모두 보이게 지도 중심 및 레벨 조정
    const bounds = new kakao.maps.LatLngBounds()
    bounds.extend(new kakao.maps.LatLng(start.lat, start.lng))
    bounds.extend(new kakao.maps.LatLng(end.lat, end.lng))
    
    if (status === kakao.maps.services.Status.OK && result.routes && result.routes.length > 0) {
      // 자동차 경로일 경우 API 결과 사용
      const route = result.routes[0]
      
      // 경로 그리기
      const linePath = []
      
      // 경로의 각 구간(sections)에 대한 처리
      route.sections.forEach(section => {
        // 각 구간의 경로(roads)에 대한 처리
        section.roads.forEach(road => {
          // 각 경로에 포함된 node(좌표점)에 대한 처리
          road.vertexes.forEach((vertex, index) => {
            // 위도(lat)와 경도(lng)로 변환
            // vertexes 배열의 짝수 인덱스는 경도(lng), 홀수 인덱스는 위도(lat)
            if (index % 2 === 0 && index + 1 < road.vertexes.length) {
              const lng = vertex
              const lat = road.vertexes[index + 1]
              
              const latLng = new kakao.maps.LatLng(lat, lng)
              linePath.push(latLng)
              bounds.extend(latLng)
            }
          })
        })
      })
      
      // 경로 선 생성
      const polyline = new kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 5,
        strokeColor: strokeColor,
        strokeOpacity: 0.8,
        strokeStyle: strokeStyle
      })
      
      // 경로를 지도에 표시
      polyline.setMap(mapInstance)
      
      // 현재 경로 저장 (나중에 삭제하기 위해)
      window.currentRoute = polyline
      
    } else {
      console.log('길찾기 API 호출 실패 또는 결과 없음. 직선 경로로 표시합니다.')
      
      // API 호출 실패시 직선 경로로 표시
      const linePath = [
        new kakao.maps.LatLng(start.lat, start.lng),
        new kakao.maps.LatLng(end.lat, end.lng)
      ]
      
      // 경로 선 생성
      const polyline = new kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 5,
        strokeColor: strokeColor,
        strokeOpacity: 0.8,
        strokeStyle: strokeStyle
      })
      
      // 경로를 지도에 표시
      polyline.setMap(mapInstance)
      
      // 현재 경로 저장 (나중에 삭제하기 위해)
      window.currentRoute = polyline
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
    
    // 마커 저장 (나중에 삭제하기 위해)
    window.currentRouteMarkers = [startMarker, endMarker]
    
    // 지도 범위 설정
    mapInstance.setBounds(bounds)
  })
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

// 소요 시간 형식화
const formatDuration = (seconds) => {
  if (!seconds) return '시간 정보 없음'
  
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (hours > 0) {
    return `${hours}시간 ${minutes}분`
  } else {
    return `${minutes}분`
  }
}

// 거리 형식화
const formatDistance = (meters) => {
  if (!meters) return ''
  
  if (meters >= 1000) {
    return `${(meters / 1000).toFixed(1)}km`
  } else {
    return `${meters}m`
  }
}

// 검색 함수
const searchBanks = async () => {
  console.log('searchBanks 실행됨') // 클릭 작동 확인용

  if (!window.kakao || !window.kakao.maps) {
    console.error('카카오맵이 아직 로드되지 않았습니다.')
    return
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
      try {
        // 검색 결과에 소요 시간 및 거리 정보 추가
        const resultsWithRouteInfo = await Promise.all(
          result.map(async (place) => {
            try {
              const routeInfo = await calculateRouteInfo(
                { lat: startLocation.value.lat, lng: startLocation.value.lng },
                { lat: parseFloat(place.y), lng: parseFloat(place.x) }
              )
              
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
        
        // 첫번째 결과의 위치로 맵 이동 (확대 레벨 조정)
        const firstCoords = new kakao.maps.LatLng(resultsWithRouteInfo[0].y, resultsWithRouteInfo[0].x)
        mapInstance.setCenter(firstCoords)
        mapInstance.setLevel(4) // 적절한 확대 레벨로 설정
        
        // 검색된 모든 은행에 마커 표시
        resultsWithRouteInfo.forEach((place, index) => {
          const coords = new kakao.maps.LatLng(place.y, place.x)
          
          // 마커 생성 (인덱스 레이블 추가)
          const marker = new kakao.maps.Marker({
            map: mapInstance,
            position: coords,
            title: place.place_name
          })
          markers.push(marker)
          
          // 인포윈도우 생성
          const durationText = place.duration ? formatDuration(place.duration) : '시간 정보 없음'
          const distanceText = place.distance ? formatDistance(place.distance) : ''
          
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

// 교통수단 아이콘 얻기
const getTransportIcon = (mode) => {
  switch (mode) {
    case 'car': return '🚗'
    case 'walk': return '🚶'
    case 'bike': return '🚲'
    default: return '🚗'
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
  const address = type === 'start' ? customStartLocation.value : ''
  
  if (!address) {
    alert('주소를 입력해주세요.')
    return
  }
  
  // 주소로 좌표 검색
  geocoder.addressSearch(address, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const coords = new kakao.maps.LatLng(result[0].y, result[0].x)
      
      if (type === 'start') {
        customStartLocationData.value = {
          name: address,
          address: result[0].address_name || address,
          lat: parseFloat(result[0].y),
          lng: parseFloat(result[0].x)
        }
        
        // 지도 이동
        if (mapInstance) {
          mapInstance.setCenter(coords)
          mapInstance.setLevel(3)
          
          // 기존 출발지 마커 업데이트
          if (startMarker) {
            startMarker.setPosition(coords)
            
            // 인포윈도우 내용 업데이트
            if (startInfoWindow) {
              startInfoWindow.setContent(`<div class="custom-start-info">
                <div class="start-title">${address}</div>
                <div class="start-address">${result[0].address_name || ''}</div>
                <div class="start-label">출발지</div>
              </div>`)
              startInfoWindow.open(mapInstance, startMarker)
            }
          }
        }
        
        console.log('출발지 설정 완료:', customStartLocationData.value)
      }
    } else {
      alert('주소 검색에 실패했습니다. 정확한 주소를 입력해주세요.')
    }
  })
}

// 현재 위치 가져오기
const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        
        // 좌표로 주소 검색
        const geocoder = new kakao.maps.services.Geocoder()
        geocoder.coord2Address(lng, lat, (result, status) => {
          if (status === kakao.maps.services.Status.OK) {
            const addressName = result[0].address.address_name || '현재 위치'
            
            currentLocationData.value = {
              name: '현재 위치',
              address: addressName,
              lat: lat,
              lng: lng
            }
            
            // 지도 이동
            if (mapInstance) {
              const coords = new kakao.maps.LatLng(lat, lng)
              mapInstance.setCenter(coords)
              mapInstance.setLevel(3)
              
              // 기존 출발지 마커 업데이트
              if (startMarker) {
                startMarker.setPosition(coords)
                
                // 인포윈도우 내용 업데이트
                if (startInfoWindow) {
                  startInfoWindow.setContent(`<div class="custom-start-info">
                    <div class="start-title">현재 위치</div>
                    <div class="start-address">${addressName}</div>
                    <div class="start-label">출발지</div>
                  </div>`)
                  startInfoWindow.open(mapInstance, startMarker)
                }
              }
            }
            
            console.log('현재 위치 설정 완료:', currentLocationData.value)
          }
        })
      },
      (error) => {
        console.error('위치 정보를 가져오는데 실패했습니다:', error)
        alert('위치 정보를 가져오는데 실패했습니다. 브라우저 설정에서 위치 접근 권한을 허용해주세요.')
      }
    )
  } else {
    alert('이 브라우저에서는 위치 정보 기능을 지원하지 않습니다.')
  }
}

// 출발지 선택 변경 감지
watch(selectedStartLocation, (newValue) => {
  if (newValue === 'current') {
    getCurrentLocation()
  }
})

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
