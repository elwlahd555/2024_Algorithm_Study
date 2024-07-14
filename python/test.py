import time
import pyupbit
import datetime

access = "r2DJZiHi4rCqx8fzDpax5DCMPqtOJOIxBhRwGUxr"
secret = "mQij2OUVlkRWPxirttVCHr20iABqThFmBajh1h9w"


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]["close"] + (df.iloc[0]["high"] - df.iloc[0]["low"]) * k
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df["close"].rolling(15).mean().iloc[-1]
    return ma15


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b["currency"] == ticker:
            if b["balance"] is not None:
                return float(b["balance"])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = 0
checkETC = 0
checkXRP = 0
checkBCH = 0

# 자동매매 시작
while True:
    try:
        if checkETC + checkXRP + checkBCH == 0:
            krw = get_balance("KRW")

        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            # ETC
            target_price = get_target_price("KRW-ETC", 0.7)
            ma15 = get_ma15("KRW-ETC")
            current_price = get_current_price("KRW-ETC")
            if krw > 5000:
                if target_price < current_price:
                    if checkETC < 1:
                        upbit.buy_market_order("KRW-ETC", krw * 0.15)
                        checkETC = 1
                    if checkETC < 2 and ma15 < current_price:
                        upbit.buy_market_order("KRW-ETC", krw * 0.25)
                        checkETC = 2

            # XRP
            target_price = get_target_price("KRW-XRP", 0.7)
            ma15 = get_ma15("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if krw > 5000:
                if target_price < current_price:
                    if checkXRP < 1:
                        upbit.buy_market_order("KRW-XRP", krw * 0.1)
                        checkXRP = 1
                    if checkXRP < 2 and ma15 < current_price:
                        upbit.buy_market_order("KRW-XRP", krw * 0.2)
                        checkXRP = 2

            # BCH
            target_price = get_target_price("KRW-BCH", 0.7)
            ma15 = get_ma15("KRW-BCH")
            current_price = get_current_price("KRW-BCH")
            if krw > 5000:
                if target_price < current_price:
                    if checkBCH < 1:
                        upbit.buy_market_order("KRW-BCH", krw * 0.1)
                        checkBCH = 1
                    if checkBCH < 2 and ma15 < current_price:
                        upbit.buy_market_order("KRW-BCH", krw * 0.2)
                        checkBCH = 2

        else:
            etc = get_balance("ETC")
            if etc > 0.1:
                upbit.sell_market_order("KRW-ETC", etc)

            xrp = get_balance("XRP")
            if xrp > 5:
                upbit.sell_market_order("KRW-XRP", xrp)

            bch = get_balance("BCH")
            if bch > 0.02:
                upbit.sell_market_order("KRW-BCH", bch)
            checkETC = 0
            checkXRP = 0
            checkBCH = 0
            krw = 0

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)


