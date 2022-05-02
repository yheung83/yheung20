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

coinlist = ['KRW-ZRX']
lower28 = []
higher70 = []

for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)

while(True): 
    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute1")
        now_rsi = rsi(data, 11).iloc[-1]
        avg_buy_price = upbit.get_avg_buy_price('KRW-ZRX')
        now_price = pyupbit.get_current_price(coinlist) 
        print("name: ", coinlist[i])         
        print("nowtime: ", datetime.datetime.now())
        print("RSI :", now_rsi)
        print("buy_price:", avg_buy_price)
        print("now_price:", now_price)
        print()
        if now_rsi <= 28 :
            lower28[i] = True
        elif now_rsi >= 33 and lower28[i] == True :
            buy(coinlist[i])
            lower28[i] = False
        elif now_rsi >= 70 and higher70[i] == False :
            if (avg_buy_price + 15.0) <= now_price and avg_buy_price > 0 :
                amount = upbit.get_balance('KRW-ZRX') 
                cur_price = pyupbit.get_current_price('KRW-ZRX') 
                total = amount * cur_price
                if total > 5000 : 
                    print(upbit.sell_market_order('KRW-ZRX', amount))
                time.sleep(1)
            higher70[i] = True
        elif now_rsi <= 60 :
            if (avg_buy_price + 15.0) <= now_price and avg_buy_price > 0 :
                amount = upbit.get_balance('KRW-ZRX') 
                cur_price = pyupbit.get_current_price('KRW-ZRX') 
                total = amount * cur_price
                if total > 5000 : 
                    print(upbit.sell_market_order('KRW-ZRX', amount))
                time.sleep(1)
            #if (now_price + 15.0) <= avg_buy_price and avg_buy_price > 0 :
            #    amount = upbit.get_balance('KRW-ZRX') 
             #   cur_price = pyupbit.get_current_price('KRW-ZRX') 
              #  total = amount * cur_price
               # if total > 5000 : 
                #    print(upbit.sell_market_order('KRW-ZRX', amount))
              #  time.sleep(1)
            higher70[i] = False
    time.sleep(0.5)

    def buy(coinlist): 
        krw_balance = upbit.get_balance("KRW")
        krw_price = 102980
        if krw_balance > krw_price : 
            upbit.buy_market_order(ticker=coinlist, price=krw_price, )
        else:
            pass
        return
    def sell(coin): 
        amount = upbit.get_balance(coin) 
        cur_price = pyupbit.get_current_price(coin) 
        total = amount * cur_price
        if total > 5000 : 
            print(upbit.sell_market_order(coin, amount))
        return
