from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

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

@app.route('/exchange-rates')
def get_exchange_rates():
    """
    yfinance를 사용하여 실시간 환율 데이터를 가져오는 엔드포인트
    """
    try:
        # 주요 환율 심볼 정의 (Yahoo Finance 형식)
        currency_symbols = {
            'USD': 'KRW=X',  # USD/KRW
            'EUR': 'EURKRW=X',  # EUR/KRW
            'JPY': 'JPYKRW=X',  # JPY/KRW (100엔 기준)
            'CNY': 'CNYKRW=X',  # CNY/KRW
            'GBP': 'GBPKRW=X',  # GBP/KRW
            'AUD': 'AUDKRW=X',  # AUD/KRW
            'CAD': 'CADKRW=X',  # CAD/KRW
            'HKD': 'HKDKRW=X',  # HKD/KRW
            'SGD': 'SGDKRW=X'   # SGD/KRW
        }
        
        exchange_rates = {}
        
        for currency, symbol in currency_symbols.items():
            try:
                # yfinance를 사용하여 데이터 가져오기
                ticker = yf.Ticker(symbol)
                
                # 최근 2일간 데이터 가져오기 (현재가와 전일 대비 변동 계산용)
                hist = ticker.history(period="2d", interval="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    
                    # 전일 대비 변동 계산
                    if len(hist) >= 2:
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        change_percent = (change / prev_price) * 100
                    else:
                        change = 0
                        change_percent = 0
                    
                    # 특별 처리: JPY는 100엔 기준으로 표시
                    if currency == 'JPY':
                        current_price = current_price * 100
                        change = change * 100
                    
                    exchange_rates[currency] = {
                        'rate': f"{current_price:.2f}",
                        'change': round(change_percent, 2),
                        'change_amount': f"{change:.2f}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                else:
                    # 데이터를 가져올 수 없는 경우 기본값 설정
                    exchange_rates[currency] = {
                        'rate': '0.00',
                        'change': 0.00,
                        'change_amount': '0.00',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'error': 'Data not available'
                    }
                    
            except Exception as e:
                print(f"환율 데이터 가져오기 실패 ({currency}): {str(e)}")
                # 오류 발생 시 기본값 설정
                exchange_rates[currency] = {
                    'rate': '0.00',
                    'change': 0.00,
                    'change_amount': '0.00',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'error': str(e)
                }
        
        return jsonify({
            'success': True,
            'data': exchange_rates,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        print(f"전체 환율 데이터 가져오기 실패: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/commodities')
def get_commodities():
    """
    yfinance를 사용하여 실시간 상품(원자재) 가격 데이터를 가져오는 엔드포인트
    """
    try:
        # 주요 상품 심볼 정의
        commodity_symbols = {
            'gold': 'GC=F',      # 금 선물
            'silver': 'SI=F',    # 은 선물
            'copper': 'HG=F',    # 구리 선물
            'crude_oil': 'CL=F', # 원유 선물
            'natural_gas': 'NG=F' # 천연가스 선물
        }
        
        commodities = {}
        
        for commodity, symbol in commodity_symbols.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d", interval="1d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    
                    if len(hist) >= 2:
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        change_percent = (change / prev_price) * 100
                    else:
                        change = 0
                        change_percent = 0
                    
                    commodities[commodity] = {
                        'price': f"{current_price:.2f}",
                        'change': round(change_percent, 2),
                        'change_amount': f"{change:.2f}",
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                else:
                    commodities[commodity] = {
                        'price': '0.00',
                        'change': 0.00,
                        'change_amount': '0.00',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'error': 'Data not available'
                    }
                    
            except Exception as e:
                print(f"상품 데이터 가져오기 실패 ({commodity}): {str(e)}")
                commodities[commodity] = {
                    'price': '0.00',
                    'change': 0.00,
                    'change_amount': '0.00',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'error': str(e)
                }
        
        return jsonify({
            'success': True,
            'data': commodities,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        print(f"전체 상품 데이터 가져오기 실패: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')        }), 500

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"error": "Not found - 프론트엔드에서 처리해야 함"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
