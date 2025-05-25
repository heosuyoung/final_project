from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"error": "Not found - 프론트엔드에서 처리해야 함"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
