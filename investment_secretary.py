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
    main()
