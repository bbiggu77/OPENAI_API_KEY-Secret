import os
import yfinance as yf
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

# ==========================================
# 내 포트폴리오
# ==========================================

PORTFOLIO = {
    "영웅문 ISA": {
        "TIGER 미국나스닥100 타겟데일리커버드콜": {
            "quantity": 107,
            "buy_price": 11823,
        },
        "KODEX 미국휴머노이드로봇": {
            "quantity": 476,
            "buy_price": 17008,
        },
        "TIGER 미국 S&P500": {
            "quantity": 587,
            "buy_price": 25200,
        },
        "KODEX 미국반도체": {
            "quantity": 224,
            "buy_price": 30912,
        },
        "ACE 글로벌반도체TOP4 PLUS": {
            "quantity": 226,
            "buy_price": 39954,
        },
        "TIGER 미국배당다우존스": {
            "quantity": 964,
            "buy_price": 12994,
        },
        "TIGER 미국필라델피아AI반도체나스닥": {
            "quantity": 567,
            "buy_price": 12942,
        },
    },

    "토스": {
        "QQQ": {
            "ticker": "QQQ",
            "quantity": 15.189109,
        },
        "SPY": {
            "ticker": "SPY",
            "quantity": 10.984652,
        },
        "VXUS": {
            "ticker": "VXUS",
            "quantity": 0.327345,
        },
        "BND": {
            "ticker": "BND",
            "quantity": 0.394316,
        },
        "VTI": {
            "ticker": "VTI",
            "quantity": 0.075456,
        },
        "VYM": {
            "ticker": "VYM",
            "quantity": 2.611044,
        },
    },
}


def get_us_market_data():
    """미국 ETF 최근 가격을 가져옵니다."""
    result = {}

    for name, info in PORTFOLIO["토스"].items():
        ticker = info["ticker"]
        quantity = info["quantity"]

        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="5d")

            if history.empty:
                result[name] = "가격 데이터 없음"
                continue

            close_prices = history["Close"].dropna()

            current_price = float(close_prices.iloc[-1])

            if len(close_prices) >= 2:
                previous_price = float(close_prices.iloc[-2])
                change_pct = (
                    (current_price - previous_price)
                    / previous_price
                    * 100
                )
            else:
                change_pct = 0

            result[name] = {
                "quantity": quantity,
                "current_price": current_price,
                "change_pct": change_pct,
                "value": current_price * quantity,
            }

        except Exception as e:
            result[name] = f"오류: {e}"

    return result


def build_portfolio_text(us_data):
    lines = []

    lines.append("=== 영웅문 ISA ===")

    for name, info in PORTFOLIO["영웅문 ISA"].items():
        quantity = info["quantity"]
        buy_price = info["buy_price"]

        lines.append(
            f"{name} | "
            f"보유 {quantity}주 | "
            f"평균매입가 {buy_price:,}원"
        )

    lines.append("")
    lines.append("=== 토스 미국 ETF ===")

    for name, data in us_data.items():

        if isinstance(data, dict):
            lines.append(
                f"{name} | "
                f"보유 {data['quantity']:.6f}주 | "
                f"현재가 ${data['current_price']:.2f} | "
                f"전일대비 {data['change_pct']:+.2f}%"
            )
        else:
            lines.append(f"{name} | {data}")

    return "\n".join(lines)


def ask_ai(portfolio_text):
    """최신 시장 정보를 검색하고 투자비서 의견을 생성합니다."""

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    instructions = """
너는 사용자의 개인 투자비서다.

사용자는 기본적으로 B형(중립형) 투자성향이다.
장기적으로 자산을 키우는 것이 목표이며,
불필요한 단타 매매는 원하지 않는다.

다만 별도의 영웅문 공격형 계좌에서
100만원으로 적극적인 투자 기회를 찾고 있다.

사용자의 핵심 포트폴리오는 미국 ETF와
AI/반도체 관련 ETF 비중이 높은 편이다.

해야 할 일:

1. 오늘의 한국 및 미국 증시 상황을 확인한다.
2. 금리, 환율, 나스닥, S&P500, 반도체지수 등
   시장에 영향을 줄 핵심 요인을 확인한다.
3. 사용자의 보유종목과 관련된 최신 뉴스가 있는지 확인한다.
4. 오늘 시장에서 상대적으로 전망이 좋은 종목을 찾는다.
5. 국내주식과 미국주식을 모두 탐색한다.
6. 단순 인기종목이 아니라 뉴스, 실적, 성장성,
   밸류에이션, 시장 분위기, 주가 흐름 등을 종합해 선별한다.
7. 하루에 여러 번 매매하는 전략은 추천하지 않는다.
8. 매수 의견을 줄 때는 반드시
   - 관심매수가
   - 1차 매수가
   - 추가매수가
   - 목표가격
   - 위험가격
   을 제시한다.
9. 확정적인 수익을 약속하지 않는다.
10. 좋은 기회가 없으면 "오늘은 관망"이라고 분명히 말한다.
11. 100만원 공격형 계좌에 대해서는
   오늘 가장 매력적인 후보 1~3개를 별도로 제시한다.
12. 최종적으로 오늘 무엇을 할지 한 문장으로 결론을 낸다.

답변은 한국어로 작성하고,
투자비서가 아침에 카카오톡으로 보내주는 것처럼
읽기 쉽게 작성한다.
"""

    prompt = f"""
현재 시각:
{datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")}

사용자의 현재 포트폴리오:

{portfolio_text}

위 정보를 바탕으로 최신 시장 정보를 웹에서 검색하여
오늘 아침 투자비서 리포트를 작성해라.

반드시 아래 형식을 사용해라.

🌅 효영님의 오늘 투자비서

① 오늘의 증시 시황
② 내 포트폴리오 점검
③ 오늘 주목할 국내주식 TOP 3
④ 오늘 주목할 미국주식 TOP 3
⑤ 100만원 공격계좌 TOP 3
⑥ 오늘의 매수/보유/관망 의견
⑦ 오늘 반드시 확인할 경제 일정
⑧ 최종 한줄 의견

가격은 가능한 한 최신 확인값을 사용하고,
뉴스의 날짜와 출처도 함께 표시해라.
"""

    response = client.responses.create(
        model="gpt-5.5",
        instructions=instructions,
        tools=[
            {
                "type": "web_search"
            }
        ],
        input=prompt,
    )

    return response.output_text


def main():
    print("=" * 70)
    print("🌅 효영님의 투자비서")
    print(
        "실행 시간:",
        datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
    )
    print("=" * 70)

    print("\n📊 미국 ETF 데이터 수집 중...")
    us_data = get_us_market_data()

    portfolio_text = build_portfolio_text(us_data)

    print("\n🤖 AI가 최신 시장 정보를 분석하고 있습니다...\n")

    try:
        report = ask_ai(portfolio_text)

        print("=" * 70)
        print(report)
        print("=" * 70)

    except Exception as e:
        print("❌ AI 분석 실패")
        print("오류:", e)


if __name__ == "__main__":
    main()
