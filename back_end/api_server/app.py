from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
import threading
import time
import pandas as pd

# 캐시 저장소
cache = {
    'exchange_rates': {'data': None, 'timestamp': None},
    'commodities': {'data': None, 'timestamp': None},
    'currency_history': {'data': None, 'timestamp': None},
    'commodity_history': {'data': None, 'timestamp': None},
    'index_history': {'data': None, 'timestamp': None}
}
cache_lock = threading.Lock()
CACHE_DURATION = 30  # 캐시 유효 기간을 30초로 줄임
HISTORY_CACHE_DURATION = 3600  # 시계열 데이터는 1시간 캐싱

app = Flask(__name__)
CORS(app)

def format_number(value):
    """숫자 포맷팅 함수"""
    try:
        if isinstance(value, (int, float)):
            if value >= 1000000:
                return f"{value/1000000:.2f}M"
            elif value >= 1000:
                return f"{value/1000:.2f}K"
            else:
                return f"{value:.2f}"
        return str(value)
    except:
        return str(value)

def get_historical_data(symbol, period='1mo', interval='1d'):
    """야후 파이낸스에서 히스토리컬 데이터 가져오기"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        if not hist.empty:
            return hist
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {str(e)}")
    return pd.DataFrame()

def initialize_cache():
    """서버 시작 시 캐시 초기화"""
    print("Initializing cache...")
    # 환율 데이터 초기화
    get_exchange_rates()
    # 상품 데이터 초기화
    get_commodities()
    
    # 히스토리 데이터 캐시 초기화 (백그라운드에서 실행)
    threading.Thread(target=get_currency_history).start()
    threading.Thread(target=get_commodity_history).start()
    threading.Thread(target=get_index_history).start()
    
    print("Cache initialization completed")

@app.route('/stocks')
def get_stocks():
    url = "https://finance.naver.com/sise/sise_market_sum.naver"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    res.encoding = 'euc-kr'
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.select_one("table.type_2")
    if table is None:
        print("[ERROR] 테이블을 찾을 수 없음")
        return jsonify({"error": "크롤링 실패"}), 500

    rows = table.select("tr")
    stocks = []

    for row in rows:
        cols = row.select("td")
        if len(cols) < 11:
            continue

        name_tag = cols[1].select_one("a")
        if not name_tag:
            continue

        try:
            name = name_tag.text.strip()
            code = name_tag['href'].split("code=")[-1]

            price_raw = cols[2].text.strip().replace(",", "")
            change_rate = cols[4].text.strip()
            market_cap_raw = cols[6].text.strip().replace(",", "")
            volume_raw = cols[9].text.strip().replace(",", "")

            price = format(int(price_raw), ",") if price_raw.isdigit() else price_raw
            market_cap = format(int(market_cap_raw), ",") if market_cap_raw.isdigit() else market_cap_raw
            volume = format(float(volume_raw), ",.2f") if volume_raw.replace('.', '', 1).isdigit() else volume_raw

            stock = {
                "name": name,
                "code": code,
                "price": price,
                "changeRate": change_rate,
                "marketCap": market_cap,
                "volume": volume,
                "isFavorite": False
            }
            stocks.append(stock)

        except Exception as e:
            print(f"[WARN] 파싱 오류: {e}")
            continue

    return jsonify(stocks[:30])

# 캐시 관련 함수
def get_cached_data(cache_key, fetch_func):
    """캐시된 데이터를 가져오거나 새로운 데이터를 가져와서 캐시에 저장"""
    with cache_lock:
        cache_data = cache.get(cache_key)
        current_time = time.time()
        
        # 캐시가 유효한 경우
        if (cache_data and cache_data['data'] and cache_data['timestamp'] 
            and current_time - cache_data['timestamp'] < CACHE_DURATION):
            return cache_data['data']
        
        # 새로운 데이터 가져오기
        try:
            new_data = fetch_func()
            if new_data:
                cache[cache_key] = {
                    'data': new_data,
                    'timestamp': current_time
                }
                return new_data
            elif cache_data and cache_data['data']:
                return cache_data['data']
        except Exception as e:
            print(f"Error fetching data for {cache_key}: {str(e)}")
            if cache_data and cache_data['data']:
                return cache_data['data']
            raise

@app.route('/exchange-rates')
def get_exchange_rates():
    """환율 데이터를 가져오는 엔드포인트"""
    def fetch_latest_rates():
        try:
            exchange_rates = {}
            currency_symbols = {
                'USD': 'USDKRW=X',
                'EUR': 'EURKRW=X',
                'JPY': 'JPYKRW=X',
                'CNY': 'CNYKRW=X',
                'GBP': 'GBPKRW=X',
                'AUD': 'AUDKRW=X',
                'CAD': 'CADKRW=X',
                'HKD': 'HKDKRW=X',
                'SGD': 'SGDKRW=X'
            }
            
            for currency, symbol in currency_symbols.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period='5d')  # 5일치 데이터 가져오기
                    hist = hist.dropna()  # 결측치 제거
                    
                    if not hist.empty:
                        current_rate = float(hist['Close'].iloc[-1])
                        
                        # 변동률 계산
                        if len(hist) >= 2:
                            prev_rate = float(hist['Close'].iloc[-2])
                            change = ((current_rate - prev_rate) / prev_rate) * 100
                            change_amount = current_rate - prev_rate
                        else:
                            change = 0.0
                            change_amount = 0.0
                        
                        if currency == 'JPY':
                            current_rate = current_rate / 100  # Convert to per-yen rate
                            change_amount = change_amount / 100
                        
                        exchange_rates[currency] = {
                            'rate': round(current_rate, 2),
                            'change': round(change, 2),
                            'change_amount': round(change_amount, 2),
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                except Exception as e:
                    print(f"Failed to fetch {currency}: {str(e)}")
            
            if not exchange_rates:
                raise Exception("No exchange rate data available")
                
            return exchange_rates
            
        except Exception as e:
            print(f"Error fetching exchange rates: {str(e)}")
            return None
    
    try:
        rates = get_cached_data('exchange_rates', fetch_latest_rates)
        if rates:
            return jsonify({
                'success': True,
                'data': rates,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch exchange rates',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/commodities')
def get_commodities():
    """상품 시세 데이터를 가져오는 엔드포인트"""
    def get_clean_data(hist):
        """데이터 정제 및 변동률 계산"""
        if hist.empty or len(hist) == 0:
            return None
            
        try:
            current_price = float(hist['Close'].iloc[-1])
            prev_price = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else current_price
            change = ((current_price - prev_price) / prev_price) * 100
            change_amount = current_price - prev_price
            
            return {
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_amount': round(change_amount, 2)
            }
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            return None
    def fetch_latest_commodities():
        try:
            commodities = {}
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 주요 상품(원자재/귀금속) 심볼
            commodity_symbols = {
                'Gold': 'GC=F',
                'Silver': 'SI=F',
                'Copper': 'HG=F',
                'Crude Oil': 'CL=F',
                'Natural Gas': 'NG=F'
            }
            
            # 지수 심볼 (한국 시장)
            index_symbols = {
                'KOSPI': '^KS11',
                'KOSDAQ': '^KQ11'
            }
            
            # 각 심볼별로 데이터 가져오기
            for name, symbol in {**commodity_symbols, **index_symbols}.items():
                try:
                    ticker = yf.Ticker(symbol)
                    # 더 긴 기간의 데이터를 가져와서 최근 데이터 확인
                    hist = ticker.history(period='1mo', interval='1d')
                    hist = hist.dropna()
                    
                    if not hist.empty:
                        data = get_clean_data(hist)
                        if data:
                            data['timestamp'] = timestamp
                            commodities[name] = data
                            print(f"Successfully fetched {name}: {data}")
                    else:
                        print(f"No data available for {name}")
                        
                except Exception as e:
                    print(f"Error fetching {name}: {str(e)}")
                    continue
            
            if not commodities:
                raise Exception("Failed to fetch any market data")
            
            return commodities
            
        except Exception as e:
            print(f"Error in fetch_latest_commodities: {str(e)}")
            return None
            
    try:
        # 캐시된 데이터 확인
        with cache_lock:
            current_time = time.time()
            if (cache['commodities']['data'] is not None and 
                cache['commodities']['timestamp'] is not None and 
                current_time - cache['commodities']['timestamp'] < CACHE_DURATION):
                return jsonify({
                    'success': True,
                    'data': cache['commodities']['data'],
                    'cached': True,
                    'timestamp': datetime.fromtimestamp(cache['commodities']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # 새로운 데이터 가져오기
        new_data = fetch_latest_commodities()
        if new_data:
            with cache_lock:
                cache['commodities'] = {
                    'data': new_data,
                    'timestamp': current_time
                }
            return jsonify({
                'success': True,
                'data': new_data,
                'cached': False,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            # 캐시된 데이터로 폴백
            with cache_lock:
                if cache['commodities']['data'] is not None:
                    return jsonify({
                        'success': True,
                        'data': cache['commodities']['data'],
                        'cached': True,
                        'timestamp': datetime.fromtimestamp(cache['commodities']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            return jsonify({
                'success': False,
                'error': 'Failed to fetch market data',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 500
            
    except Exception as e:
        print(f"Error in get_commodities: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/stock-analysis/<stock_code>')
def get_stock_analysis(stock_code):
    """
    특정 종목의 재무정보, 차트 데이터, 기술적 분석을 제공하는 엔드포인트
    """
    try:
        from flask import request
        
        # period 매개변수 가져오기 (기본값: 1d)
        period = request.args.get('period', '1d')
        
        # period에 따른 yfinance 매개변수 설정
        if period == '1d':
            yf_period = "1mo"
            yf_interval = "1d"
            date_format = '%m-%d'
        elif period == '1wk':
            yf_period = "6mo"
            yf_interval = "1wk"
            date_format = '%m-%d'
        elif period == '1mo':
            yf_period = "2y"
            yf_interval = "1mo"
            date_format = '%Y-%m'
        else:
            # 기본값으로 일봉
            yf_period = "1mo"
            yf_interval = "1d"
            date_format = '%m-%d'
        
        # 한국 주식의 경우 .KS 접미사 추가
        symbol = f"{stock_code}.KS"
        ticker = yf.Ticker(symbol)
        
        # 기본 정보 가져오기
        info = ticker.info
        
        # 지정된 기간과 간격으로 주가 데이터 가져오기
        hist = ticker.history(period=yf_period, interval=yf_interval)
        
        # 차트 데이터 준비
        chart_data = []
        if not hist.empty:
            for date, row in hist.iterrows():
                chart_data.append({
                    'date': date.strftime(date_format),
                    'price': round(row['Close'], 0)
                })        # 재무정보 추출 - 한국 주식의 경우 제한적인 데이터 고려
        def get_financial_value(info, keys, multiplier=1, decimal_places=1):
            """여러 키를 시도하여 재무 데이터를 가져오는 헬퍼 함수"""
            for key in keys:
                value = info.get(key)
                if value is not None and str(value).lower() != 'none' and value != 0:
                    try:
                        return round(float(value) * multiplier, decimal_places)
                    except (ValueError, TypeError):
                        continue
            return 'N/A'
        
        # 현재가와 시가총액 기반으로 일부 지표 계산
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        market_cap = info.get('marketCap')
        book_value = info.get('bookValue')
        
        # PBR 계산 (현재가 / 주당순자산)
        pbr_value = 'N/A'
        if current_price and book_value and book_value > 0:
            pbr_value = round(current_price / book_value, 2)
        elif info.get('priceToBook'):
            pbr_value = round(float(info.get('priceToBook')), 2)
        
        print(f"Debug for {stock_code}:")
        print(f"currentPrice: {current_price}")
        print(f"trailingPE: {info.get('trailingPE')}")
        print(f"priceToBook: {info.get('priceToBook')}")
        print(f"bookValue: {book_value}")
        print(f"calculated PBR: {pbr_value}")
          # 재무 데이터 구성 - N/A인 항목은 제외
        financial_data = {}
        
        # PER 추가 (유효한 값이 있을 때만)
        per_value = get_financial_value(info, ['trailingPE', 'forwardPE', 'pe', 'priceEarningsRatio'], 1, 2)
        if per_value != 'N/A':
            financial_data['per'] = per_value
        
        # PBR 추가 (유효한 값이 있을 때만)
        final_pbr = pbr_value if pbr_value != 'N/A' else get_financial_value(info, ['priceToBook', 'priceToBookRatio'], 1, 2)
        if final_pbr != 'N/A':
            financial_data['pbr'] = final_pbr
        
        # ROE 추가 (유효한 값이 있을 때만)
        roe_value = get_financial_value(info, ['returnOnEquity', 'roe'], 100, 1)
        if roe_value != 'N/A':
            financial_data['roe'] = roe_value
        
        # 부채비율 추가 (유효한 값이 있을 때만)
        debt_ratio = get_financial_value(info, ['debtToEquity', 'totalDebtToEquity'], 1, 1)
        if debt_ratio != 'N/A':
            financial_data['debtRatio'] = debt_ratio
        
        # 영업이익률 추가 (유효한 값이 있을 때만)
        operating_margin = get_financial_value(info, ['operatingMargins', 'operatingMargin'], 100, 1)
        if operating_margin != 'N/A':
            financial_data['operatingMargin'] = operating_margin
        
        # 배당수익률 추가 (유효한 값이 있을 때만)
        dividend_yield = get_financial_value(info, ['dividendYield', 'yield'], 100, 2)
        if dividend_yield != 'N/A':
            financial_data['dividendYield'] = dividend_yield
        
        # 시가총액과 현재가는 항상 포함
        financial_data['marketCap'] = market_cap if market_cap else 'N/A'
        financial_data['currentPrice'] = current_price if current_price else 'N/A'
        
        # 기술적 분석 계산
        technical_data = {}
        if not hist.empty and len(hist) >= 20:
            current_price = hist['Close'].iloc[-1]
            
            # 이동평균선 계산
            ma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            ma60 = hist['Close'].rolling(window=min(60, len(hist))).mean().iloc[-1]
            
            # RSI 계산 (간단한 버전)
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # 볼린저 밴드 계산
            bb_period = 20
            if len(hist) >= bb_period:
                ma = hist['Close'].rolling(window=bb_period).mean()
                std = hist['Close'].rolling(window=bb_period).std()
                bb_upper = ma + (std * 2)
                bb_lower = ma - (std * 2)
                
                technical_data = {
                    'rsi': round(rsi, 1),
                    'ma20': round(ma20, 0),
                    'ma60': round(ma60, 0),
                    'bollingerUpper': round(bb_upper.iloc[-1], 0),
                    'bollingerLower': round(bb_lower.iloc[-1], 0),
                    'bollingerStatus': '중간대' if bb_lower.iloc[-1] < current_price < bb_upper.iloc[-1] else 
                                    ('상단 근접' if current_price >= bb_upper.iloc[-1] * 0.98 else '하단 근접')
                }
        
        return jsonify({
            'success': True,
            'data': {
                'chart_data': chart_data,
                'financial_data': financial_data,
                'technical_data': technical_data,
                'stock_info': {
                    'name': info.get('longName', stock_code),
                    'code': stock_code,
                    'current_price': round(info.get('currentPrice', 0), 0) if info.get('currentPrice') else 'N/A',
                    'market_cap': info.get('marketCap', 'N/A'),
                    'sector': info.get('sector', 'N/A')
                }
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        print(f"주식 분석 데이터 가져오기 실패 ({stock_code}): {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

# 환율 히스토리 데이터 가져오기
@app.route('/currency-history')
def get_currency_history():
    """환율의 최근 30일 히스토리 데이터를 제공하는 엔드포인트"""
    def fetch_currency_history():
        try:
            currency_symbols = {
                'USD': 'USDKRW=X', 
                'EUR': 'EURKRW=X',
                'JPY': 'JPYKRW=X',
                'CNY': 'CNYKRW=X',
                'GBP': 'GBPKRW=X',
                'AUD': 'AUDKRW=X',
                'CAD': 'CADKRW=X', 
                'HKD': 'HKDKRW=X',
                'SGD': 'SGDKRW=X'
            }
            
            result = {}
            
            for currency, symbol in currency_symbols.items():
                hist = get_historical_data(symbol, period='30d', interval='1d')
                if not hist.empty:
                    # 날짜-가격 쌍으로 변환
                    history_data = []
                    for index, row in hist.iterrows():
                        date_str = index.strftime('%Y-%m-%d')
                        close_price = round(row['Close'], 2)
                        
                        # JPY는 100엔당 원화로 표시되므로 100으로 나눔
                        if currency == 'JPY':
                            close_price = close_price / 100
                            
                        history_data.append({
                            'date': date_str,
                            'price': close_price
                        })
                    
                    result[currency] = history_data
            
            return result
        except Exception as e:
            print(f"환율 히스토리 데이터 가져오기 실패: {str(e)}")
            return None
    
    # 캐싱된 데이터 가져오기
    with cache_lock:
        cache_data = cache.get('currency_history')
        current_time = time.time()
        
        if (cache_data and cache_data['data'] and cache_data['timestamp'] 
            and current_time - cache_data['timestamp'] < HISTORY_CACHE_DURATION):
            data = cache_data['data']
        else:
            data = fetch_currency_history()
            if data:
                cache['currency_history'] = {
                    'data': data,
                    'timestamp': current_time
                }
    
    if data:
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({
            'success': False,
            'error': "환율 히스토리 데이터를 가져오지 못했습니다.",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

# 상품(금, 은, 원유 등) 히스토리 데이터 가져오기
@app.route('/commodity-history')
def get_commodity_history():
    """상품의 최근 30일 히스토리 데이터를 제공하는 엔드포인트"""
    def fetch_commodity_history():
        try:
            commodity_symbols = {
                'Gold': 'GC=F',  # 금 선물
                'Silver': 'SI=F',  # 은 선물
                'Copper': 'HG=F',  # 구리 선물
                'Crude Oil': 'CL=F',  # WTI 원유 선물
                'Natural Gas': 'NG=F'  # 천연가스 선물
            }
            
            result = {}
            
            for commodity, symbol in commodity_symbols.items():
                hist = get_historical_data(symbol, period='30d', interval='1d')
                if not hist.empty:
                    # 날짜-가격 쌍으로 변환
                    history_data = []
                    for index, row in hist.iterrows():
                        date_str = index.strftime('%Y-%m-%d')
                        close_price = round(row['Close'], 2)
                        history_data.append({
                            'date': date_str,
                            'price': close_price
                        })
                    
                    result[commodity] = history_data
            
            return result
        except Exception as e:
            print(f"상품 히스토리 데이터 가져오기 실패: {str(e)}")
            return None
    
    # 캐싱된 데이터 가져오기
    with cache_lock:
        cache_data = cache.get('commodity_history')
        current_time = time.time()
        
        if (cache_data and cache_data['data'] and cache_data['timestamp'] 
            and current_time - cache_data['timestamp'] < HISTORY_CACHE_DURATION):
            data = cache_data['data']
        else:
            data = fetch_commodity_history()
            if data:
                cache['commodity_history'] = {
                    'data': data,
                    'timestamp': current_time
                }
    
    if data:
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({
            'success': False,
            'error': "상품 히스토리 데이터를 가져오지 못했습니다.",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

# 지수(KOSPI, KOSDAQ) 히스토리 데이터 가져오기
@app.route('/index-history')
def get_index_history():
    """지수의 최근 30일 히스토리 데이터를 제공하는 엔드포인트"""
    def fetch_index_history():
        try:
            # 야후 파이낸스의 코스피, 코스닥 심볼
            index_symbols = {
                'KOSPI': '^KS11',
                'KOSDAQ': '^KQ11'
            }
            
            result = {}
            
            for index_name, symbol in index_symbols.items():
                hist = get_historical_data(symbol, period='30d', interval='1d')
                if not hist.empty:
                    # 날짜-가격 쌍으로 변환
                    history_data = []
                    for index, row in hist.iterrows():
                        date_str = index.strftime('%Y-%m-%d')
                        close_price = round(row['Close'], 2)
                        history_data.append({
                            'date': date_str,
                            'price': close_price
                        })
                    
                    result[index_name] = history_data
            
            return result
        except Exception as e:
            print(f"지수 히스토리 데이터 가져오기 실패: {str(e)}")
            return None
    
    # 캐싱된 데이터 가져오기
    with cache_lock:
        cache_data = cache.get('index_history')
        current_time = time.time()
        
        if (cache_data and cache_data['data'] and cache_data['timestamp'] 
            and current_time - cache_data['timestamp'] < HISTORY_CACHE_DURATION):
            data = cache_data['data']
        else:
            data = fetch_index_history()
            if data:
                cache['index_history'] = {
                    'data': data,
                    'timestamp': current_time
                }
    
    if data:
        return jsonify({
            'success': True,
            'data': data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        return jsonify({
            'success': False,
            'error': "지수 히스토리 데이터를 가져오지 못했습니다.",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"error": "Not found - 프론트엔드에서 처리해야 함"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)