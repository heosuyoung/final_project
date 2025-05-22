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
              style="width: 100%; padding: 10px; background-color: orange; color: white; border: none; font-weight: bold;">
        찾기
      </button>
    </div>

    <!-- 지도: 나머지 전체 채움 -->
    <div id="map" style="flex-grow: 1;"></div>
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

let mapInstance = null

// 시도 변경 시 시군구 갱신
const updateSiGunGuList = () => {
  const target = mapInfo.find(item => item.name === selectedDo.value)
  selectedCountries.value = target ? target.countries : []
}

// 지도 로딩
const loadKakaoMap = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_API_KEY}&autoload=false&libraries=services`
    script.onload = () => window.kakao.maps.load(resolve)
    script.onerror = reject
    document.head.appendChild(script)
  })
}

// ✅ 검색 함수 (alert + console 확인)
const searchBanks = () => {
  alert('searchBanks 실행됨') // 클릭 작동 확인용

  if (!window.kakao || !window.kakao.maps) {
    console.error('카카오맵이 아직 로드되지 않았습니다.')
    return
  }

  const geocoder = new kakao.maps.services.Geocoder()
  const query = `${selectedDo.value} ${selectedSigungu.value} ${selectedBank.value}`

  console.log('[검색 쿼리]', query)

  geocoder.addressSearch(query, function (result, status) {
    console.log('[검색 결과]', result)
    console.log('[상태]', status)

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

// 지도 초기화
onMounted(async () => {
  try {
    await loadKakaoMap()
    const container = document.getElementById('map')
    const options = {
      center: new window.kakao.maps.LatLng(37.5665, 126.9780),
      level: 3
    }
    mapInstance = new kakao.maps.Map(container, options)
  } catch (e) {
    console.error('카카오맵 로딩 실패:', e)
  }
})
</script>
