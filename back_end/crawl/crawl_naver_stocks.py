import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 네이버 증권 시가총액 페이지
URL = "https://finance.naver.com/sise/sise_market_sum.naver"

# User-Agent 헤더 필수
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 원하는 항목들 선택 (종목명, 종목코드, 현재가, 시가총액, 거래량, 등락률)
def fetch_top_marketcap_stocks():
    stocks = []
    for page in range(1, 2):  # 1페이지에 약 50개 → 한 페이지만
        res = requests.get(f"{URL}?&page={page}", headers=headers)
        res.encoding = 'euc-kr'  # 네이버는 euc-kr 인코딩 사용
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table.type_2")
        rows = table.select("tr")

        for row in rows:
            cols = row.select("td")
            if len(cols) < 10:
                continue

            name_tag = cols[1].select_one("a")
            if not name_tag:
                continue

            name = name_tag.text.strip()
            href = name_tag['href']
            code = href.split("code=")[-1]

            price = cols[2].text.strip().replace(",", "")
            change_rate = cols[9].text.strip()
            market_cap = cols[6].text.strip()
            volume = cols[10].text.strip()

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

    return stocks[:30]  # 상위 30개만

# JSON 저장
def save_to_json(data, filename="stocks_top30.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{filename} 저장 완료: {len(data)}개 종목")

if __name__ == "__main__":
    stock_data = fetch_top_marketcap_stocks()
    save_to_json(stock_data)
