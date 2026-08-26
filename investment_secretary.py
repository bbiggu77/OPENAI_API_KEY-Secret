import yfinance as yf
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")


def get_korea_price(ticker):
    """Yahoo Finance에서 한국 ETF의 최근 가격을 가져옵니다."""
    stock = yf.Ticker(ticker)
    history = stock.history(period="5d")

    if history.empty:
        raise ValueError(f"{ticker} 가격 데이터를 가져오지 못했습니다.")

    return float(history["Close"].dropna().iloc[-1])


def main():
    now = datetime.now(KST)

    print("=" * 50)
    print("🇰🇷 국내 ETF 가격 테스트")
    print("실행 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)

    ticker = "0038A0.KS"

    try:
        price = get_korea_price(ticker)

        print()
        print("KODEX 미국휴머노이드로봇")
        print("종목코드 : 0038A0")
        print(f"현재가   : {price:,.0f}원")
        print()
        print("✅ 국내 ETF 가격 수집 성공")

    except Exception as e:
        print()
        print("❌ 가격 수집 실패")
        print("오류:", e)

    print("=" * 50)


if __name__ == "__main__":
    main()
