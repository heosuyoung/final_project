<template>
  <div style="display: flex; height: calc(100vh - 90px); margin-top: 90px;">
    <!-- 검색창 왼쪽에 고정 -->
    <div style="width: 280px; min-width: 260px; padding: 24px; background-color: #f7f7f7;">
      <h3 style="margin-bottom: 16px;">은행 찾기</h3>

      <select v-model="selectedDo" @change="updateSiGunGuList"
              style="width: 100%; margin-bottom: 12px; padding: 6px;">
        <option disabled value="">광역시/도 선택</option>
        <option v-for="doItem in mapInfo" :key="doItem.name">{{ doItem.name }}</option>
      </select>

      <select v-model="selectedSigungu" :disabled="!selectedDo"
              style="width: 100%; margin-bottom: 12px; padding: 6px;">
        <option disabled value="">시/군/구 선택</option>
        <option v-for="gu in selectedCountries" :key="gu">{{ gu }}</option>
      </select>

      <select v-model="selectedBank" style="width: 100%; margin-bottom: 16px; padding: 6px;">
        <option disabled value="">은행 선택</option>
        <option v-for="bank in bankInfo" :key="bank">{{ bank }}</option>
      </select>

      <button @click="searchBanks"
              style="width: 100%; padding: 10px; background-color: orange; color: white; border: none; font-weight: bold; margin-bottom: 16px;">
        찾기
      </button>
      
      <!-- 출발지 정보 표시 -->
      <div style="margin-bottom: 16px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;">
        <h4 style="margin-bottom: 8px;">출발지</h4>
        <p style="margin: 0; font-size: 14px;">부산 강서구 녹산산업중로 333</p>
      </div>
      
      <!-- 검색 결과 표시 영역 -->
      <div v-if="searchResults.length > 0" style="margin-top: 16px;">
        <h4 style="margin-bottom: 8px;">검색 결과</h4>
        <div v-for="(place, index) in searchResults" :key="index" 
             style="padding: 10px; margin-bottom: 8px; background-color: #eee; border-radius: 4px;">
          <p style="font-weight: bold; margin: 0 0 5px 0;">{{ place.place_name }}</p>
          <p style="font-size: 12px; margin: 0 0 5px 0;">{{ place.address_name }}</p>
          <div style="display: flex; gap: 8px;">
            <button @click="showDirections(place)" 
                    style="padding: 5px; background-color: #4285f4; color: white; border: none; border-radius: 4px;">
              길찾기
            </button>
            <button @click="focusOnMarker(index)"
                    style="padding: 5px; background-color: #34a853; color: white; border: none; border-radius: 4px;">
              위치 보기
            </button>
          </div>
        </div>
      </div>
      
      <!-- 로컬 알림창 확인 버튼 -->
      <button @click="handleConfirmMessage" class="confirm-button" style="display: none;">
        확인
      </button>
    </div>

    <!-- 지도: 나머지 전체 채움 -->
    <div id="map" style="flex-grow: 1; min-height: 400px; height: 100%;"></div>
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
  name: '부산 강서구 녹산산업중로 333',
  lat: 35.094663, // 위도
  lng: 128.855308 // 경도
}

let mapInstance = null
let markers = []
let infowindows = []

// 시도 변경 시 시군구 갱신
const updateSiGunGuList = () => {
  const target = mapInfo.find(item => item.name === selectedDo.value)
  selectedCountries.value = target ? target.countries : []
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
  const start = startLocation // 출발지 (녹산산업중로 333)
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

// ✅ 검색 함수 (alert + console 확인)
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
        
        // 마커 생성
        const marker = new kakao.maps.Marker({
          map: mapInstance,
          position: coords
        })
        markers.push(marker)
        
        // 인포윈도우 생성
        const infoContent = `
          <div style="padding:5px; width:200px; text-align:center;">
            <strong>${place.place_name}</strong><br>
            <span style="font-size:12px; color:#888;">${place.address_name}</span><br>
            <button onclick="window.showDirectionsFromMap && window.showDirectionsFromMap(${index})" 
                    style="margin-top:5px; padding:3px 8px; background:#4285f4; color:white; border:none; border-radius:3px; cursor:pointer;">
              길찾기
            </button>
          </div>
        `
        
        const infowindow = new kakao.maps.InfoWindow({
          content: infoContent
        })
        infowindows.push(infowindow)
        
        // 마커 클릭시 인포윈도우 표시
        kakao.maps.event.addListener(marker, 'click', function() {
          // 다른 인포윈도우 닫기
          infowindows.forEach(iw => iw.close())
          // 현재 인포윈도우 열기
          infowindow.open(mapInstance, marker)
        })
        
        // 첫번째 마커는 기본적으로 인포윈도우 열기
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
            content: `<div style="padding:5px;">${selectedBank.value}</div>`
          })

          infowindow.open(mapInstance, marker)
        } else {
          alert('해당 지역의 은행 정보를 찾을 수 없습니다.')
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
        const startMarker = new kakao.maps.Marker({
          map: mapInstance,
          position: new kakao.maps.LatLng(startLocation.lat, startLocation.lng),
          title: '출발지',
          // 출발지 마커 이미지 설정 (파란색 마커로 표시)
          image: new kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/blue_b.png', 
            new kakao.maps.Size(36, 39), 
            { offset: new kakao.maps.Point(13, 39) }
          )
        })
        
        // 출발지 인포윈도우
        const startInfoWindow = new kakao.maps.InfoWindow({
          content: `<div style="padding:5px; width:180px; text-align:center;">
                     <strong>출발지</strong><br>
                     <span style="font-size:12px; color:#888;">${startLocation.name}</span>
                   </div>`
        })
        
        // 마커 클릭 시 출발지 정보 표시
        kakao.maps.event.addListener(startMarker, 'click', function() {
          startInfoWindow.open(mapInstance, startMarker)
        })
        
        // 초기에 출발지 인포윈도우 표시
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
