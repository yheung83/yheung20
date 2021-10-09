import pyupbit
import pandas
import datetime
import time

access_key = "BDsiUgCPsKUvxfyn0DaVakOT9346k8xuUqSoSCFG"
secret_key = "z62A0ojKNOgUFn1F8cmtiGZzgTdu3LpWNDxSHkhj"
upbit = pyupbit.Upbit(access_key, secret_key)

def rsi(ohlc: pandas.DataFrame, period: int = 11):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

coinlist = ["KRW-KAVA"] 
lower28 = []
higher70 = []

for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)

while(True): 
    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute1")
        now_rsi = rsi(data, 11).iloc[-1]
        print("코인명: ", coinlist[i])
        print("현재시간: ", datetime.datetime.now())
        print("RSI :", now_rsi)
        print()
        if now_rsi <= 28 :
            lower28[i] = True
        elif now_rsi >= 33 and lower28[i] == True:
            buy(coinlist[i])
            lower28[i] = False
        elif now_rsi >= 70 and higher70[i] == False:
            sell(coinlist[i])
            higher70[i] = True
        elif now_rsi <= 60 :
            higher70[i] = False
    time.sleep(0.5)
    
    def buy(coin): 
        money = upbit.get_balance("KRW")
        #cur_price = pyupbit.get_current_price(coin)
        #avg_price = upbit.get_avg_buy_price("KRW")
        #buy_profit = ((cur_price - avg_price) / avg_price) * 100
        #profit = round(buy_profit, 2)

        if money < 20000 : 
            print(upbit.buy_market_order(coin, money)) 
        elif money < 50000 : 
            print(upbit.buy_market_order(coin, money*0.4)) 
        elif money < 100000 : 
            print(upbit.buy_market_order(coin, money*0.3)) 
        else: 
            print(upbit.buy_market_order(coin, money*0.2)) 
        return 

    def sell(coin): 
        amount = upbit.get_balance(coin) 
        cur_price = pyupbit.get_current_price(coin)
        avg_price = upbit.get_avg_buy_price("KRW-KAVA")
        buy_profit = ((cur_price - avg_price) / avg_price) * 100
        profit = round(buy_profit, 2)

        total = amount * cur_price 
        if profit >= 2.0 and total < 20000 : 
            print(upbit.sell_market_order(coin, amount))
        elif profit >= 2.0 and total < 50000 :
            print(upbit.sell_market_order(coin, amount*0.4))
        elif profit >= 2.0 and total < 100000 :
            print(upbit.sell_market_order(coin, amount*0.3))
        else : 
            print(upbit.buy_market_order(coin, amount*0.2))
        return
