import yfinance as yf
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

# 토스 계좌의 미국 ETF
PORTFOLIO = {
    "QQQ": 15.189109,
    "SPY": 10.984652,
    "VXUS": 0.327345,
    "BND": 0.394316,
    "VTI": 0.075456,
    "VYM": 2.611044,
}


def get_current_price(ticker_symbol):
    """Yahoo Finance에서 최근 가격을 가져옵니다."""
    ticker = yf.Ticker(ticker_symbol)

    history = ticker.history(period="5d")

    if history.empty:
        raise ValueError(f"{ticker_symbol} 가격 데이터를 가져오지 못했습니다.")

    return float(history["Close"].dropna().iloc[-1])


def main():
    now = datetime.now(KST)

    print("=" * 45)
    print("🌅 효영님의 투자비서")
    print("실행 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 45)

    total_value = 0

    for ticker, quantity in PORTFOLIO.items():
        try:
            price = get_current_price(ticker)
            value = price * quantity
            total_value += value

            print(
                f"{ticker:5s} | "
                f"수량 {quantity:>10.6f} | "
                f"현재가 ${price:>10.2f} | "
                f"평가금액 ${value:>10.2f}"
            )

        except Exception as e:
            print(f"{ticker}: 오류 - {e}")

    print("-" * 45)
    print(f"토스 미국 ETF 평가금액: ${total_value:,.2f}")
    print("=" * 45)


if __name__ == "__main__":
    main()import yfinance as yf
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

# ==============================
# 토스 계좌 - 미국 ETF
# ==============================
US_PORTFOLIO = {
    "QQQ": 15.189109,
    "SPY": 10.984652,
    "VXUS": 0.327345,
    "BND": 0.394316,
    "VTI": 0.075456,
    "VYM": 2.611044,
}

# ==============================
# 영웅문 ISA - 국내 ETF
# ==============================
KOREA_PORTFOLIO = {
    "TIGER 미국나스닥100 타겟데일리커버드콜": {
        "code": "486290",
        "quantity": 107,
        "buy_price": 11823,
    },
    "KODEX 미국휴머노이드로봇": {
        "code": "0038A0",
        "quantity": 476,
        "buy_price": 17008,
    },
    "TIGER 미국 S&P500": {
        "code": "360750",
        "quantity": 587,
        "buy_price": 25200,
    },
    "KODEX 미국반도체": {
        "code": "390390",
        "quantity": 224,
        "buy_price": 30912,
    },
    "ACE 글로벌반도체TOP4 Plus": {
        "code": "446770",
        "quantity": 226,
        "buy_price": 39954,
    },
    "TIGER 미국배당다우존스": {
        "code": "458730",
        "quantity": 964,
        "buy_price": 12994,
    },
    "TIGER 미국필라델피아AI반도체나스닥": {
        "code": "497570",
        "quantity": 567,
        "buy_price": 12942,
    },
}


def get_us_price(ticker_symbol):
    """Yahoo Finance에서 최근 미국 ETF 종가를 가져옵니다."""
    ticker = yf.Ticker(ticker_symbol)
    history = ticker.history(period="5d")

    if history.empty:
        raise ValueError(f"{ticker_symbol} 가격 데이터를 가져오지 못했습니다.")

    return float(history["Close"].dropna().iloc[-1])


def main():
    now = datetime.now(KST)

    print("=" * 60)
    print("🌅 효영님의 투자비서")
    print("실행 시간:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    # ------------------------------
    # 미국 ETF
    # ------------------------------
    print("\n🇺🇸 토스 미국 ETF")

    total_us_value = 0

    for ticker, quantity in US_PORTFOLIO.items():
        try:
            price = get_us_price(ticker)
            value = price * quantity
            total_us_value += value

            print(
                f"{ticker:5s} | "
                f"수량 {quantity:>10.6f} | "
                f"현재가 ${price:>10.2f} | "
                f"평가금액 ${value:>10.2f}"
            )

        except Exception as e:
            print(f"{ticker}: 오류 - {e}")

    print("-" * 60)
    print(f"미국 ETF 평가금액: ${total_us_value:,.2f}")

    # ------------------------------
    # 국내 ETF
    # ------------------------------
    print("\n🇰🇷 영웅문 ISA 국내 ETF")
    print("국내 ETF 가격 연동 준비 완료")
    print("-" * 60)

    for name, info in KOREA_PORTFOLIO.items():
        quantity = info["quantity"]
        buy_price = info["buy_price"]

        print(
            f"{name} | "
            f"코드 {info['code']} | "
            f"수량 {quantity} | "
            f"매입가 {buy_price:,}원"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()
