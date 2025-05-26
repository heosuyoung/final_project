#!/usr/bin/env python3
"""
API 서버 테스트 스크립트
삼성전자(005930) 데이터를 가져와서 API가 정상 동작하는지 확인
"""

import requests
import json
from datetime import datetime

def test_stock_analysis_api():
    """주식 분석 API 테스트"""
    base_url = "http://localhost:5000"
    stock_code = "005930"  # 삼성전자
    
    try:
        print(f"🔍 삼성전자({stock_code}) 분석 데이터 테스트 시작...")
        print(f"📡 API 요청: {base_url}/stock-analysis/{stock_code}")
        
        response = requests.get(f"{base_url}/stock-analysis/{stock_code}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("✅ API 요청 성공!")
                print(f"📊 응답 시간: {data.get('timestamp')}")
                
                # 주식 정보
                stock_info = data['data']['stock_info']
                print(f"\n📈 주식 정보:")
                print(f"  - 종목명: {stock_info.get('name')}")
                print(f"  - 종목코드: {stock_info.get('code')}")
                print(f"  - 현재가: {stock_info.get('current_price'):,}원")
                print(f"  - 섹터: {stock_info.get('sector')}")
                
                # 재무정보
                financial = data['data']['financial_data']
                print(f"\n💰 재무정보:")
                print(f"  - PER: {financial.get('per')}")
                print(f"  - PBR: {financial.get('pbr')}")
                print(f"  - ROE: {financial.get('roe')}%")
                print(f"  - 부채비율: {financial.get('debtRatio')}%")
                print(f"  - 영업이익률: {financial.get('operatingMargin')}%")
                print(f"  - 배당수익률: {financial.get('dividendYield')}%")
                
                # 기술적 분석
                technical = data['data']['technical_data']
                print(f"\n📊 기술적 분석:")
                print(f"  - RSI: {technical.get('rsi')}")
                print(f"  - 20일 이평: {technical.get('ma20'):,}원")
                print(f"  - 60일 이평: {technical.get('ma60'):,}원")
                print(f"  - 볼린저 상단: {technical.get('bollingerUpper'):,}원")
                print(f"  - 볼린저 하단: {technical.get('bollingerLower'):,}원")
                print(f"  - 볼린저 상태: {technical.get('bollingerStatus')}")
                
                # 차트 데이터
                chart_data = data['data']['chart_data']
                print(f"\n📈 차트 데이터: {len(chart_data)}일치 데이터")
                if chart_data:
                    latest = chart_data[-1]
                    print(f"  - 최신 데이터: {latest['date']} - {latest['price']:,}원")
                
                return True
            else:
                print(f"❌ API 응답 실패: {data}")
                return False
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 연결 오류: API 서버가 실행 중인지 확인하세요")
        print("💡 API 서버 실행: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ 시간 초과: API 응답이 너무 오래 걸립니다")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

def test_basic_stocks_api():
    """기본 주식 목록 API 테스트"""
    base_url = "http://localhost:5000"
    
    try:
        print(f"\n🔍 주식 목록 API 테스트...")
        response = requests.get(f"{base_url}/stocks", timeout=10)
        
        if response.status_code == 200:
            stocks = response.json()
            print(f"✅ 주식 목록 API 성공! ({len(stocks)}개 종목)")
            
            # 삼성전자 찾기
            samsung = next((stock for stock in stocks if stock['code'] == '005930'), None)
            if samsung:
                print(f"🔍 삼성전자 발견: {samsung['name']} - {samsung['price']}원")
                return True
            else:
                print("⚠️ 삼성전자를 찾을 수 없습니다")
                return False
        else:
            print(f"❌ 주식 목록 API 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 주식 목록 API 오류: {e}")
        return False

if __name__ == "__main__":
    print("🚀 API 서버 테스트 시작")
    print("=" * 50)
    
    # 기본 API 테스트
    basic_success = test_basic_stocks_api()
    
    # 주식 분석 API 테스트
    analysis_success = test_stock_analysis_api()
    
    print("\n" + "=" * 50)
    print("📋 테스트 결과 요약:")
    print(f"  - 주식 목록 API: {'✅ 성공' if basic_success else '❌ 실패'}")
    print(f"  - 주식 분석 API: {'✅ 성공' if analysis_success else '❌ 실패'}")
    
    if basic_success and analysis_success:
        print("\n🎉 모든 API 테스트 성공!")
        print("💡 프론트엔드에서 실제 데이터를 사용할 수 있습니다.")
    else:
        print("\n⚠️ 일부 API에 문제가 있습니다.")
        print("💡 API 서버를 다시 시작해보세요: python app.py")
