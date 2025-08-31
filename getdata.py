from FiinQuantX import FiinSession, FiinIndicator
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv
import time
import pandas as pd

# Đăng nhập
load_dotenv(dotenv_path=".env")
username = os.getenv("USER")
password = os.getenv("PASSWORD")

client = FiinSession(
    username=username,
    password=password,
).login()

# Tính ngày bắt đầu và kết thúc
to_date = datetime.now().strftime("%Y-%m-%d")
from_date = (datetime.now() - timedelta(days=3*365)).strftime("%Y-%m-%d")

tick = "VN30"

VN_30 = ['STB', 'VIC', 'DGC', 'SAB', 'ACB', 'BCM', 'MSN', 'CTG', 'GVR', 'MWG', 'VIB', 'VNM', 'HPG', 'VPB', 'VCB', 'LPB', 'TPB', 'MBB', 'HDB', 'FPT', 'VRE', 'TCB', 'BID', 'VHM', 'SHB', 'VJC', 'SSB', 'GAS', 'PLX', 'SSI']

tickers_hose = client.TickerList(ticker="VNINDEX")._get_data()
tickers_hnx = client.TickerList(ticker="HNXINDEX")._get_data()
tickers_upcom = client.TickerList(ticker="UPCOMINDEX")._get_data()

all_tickers = list(set(filter(lambda item: len(item) <= 3, tickers_hose + tickers_hnx)))

# Gọi dữ liệu lịch sử
for i in VN_30:
    event = client.Fetch_Trading_Data(
        realtime=False,
        tickers=[i],
        fields=["open", "high", "low", "close", "volume"],
        adjusted=True,
        by="1d",
        from_date=from_date,
        to_date=to_date
    )
    data = event.get_data()
    df = pd.DataFrame(data)
    print(i)
    # print(f'Ratios for {i}:')
    # df = pd.DataFrame(fs_dict)
    df.set_index(['ticker'], inplace=True)
    # print(df)
    fi = client.FiinIndicator()
    # print(dir(fi))
    df['ema20'] =+ fi.ema(df['close'], window=20)
    df['macd_signal'] = fi.macd_signal(df['close'], window_fast=12, window_slow=26, window_sign=9)
    df['macd'] = fi.macd(df['close'], window_fast=12, window_slow=26)
    df['macd_cross'] = 'neutral'

    # Golden cross (MACD cắt lên Signal)
    df.loc[(df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1)), 'macd_cross'] = 'goldencross'

    # Death cross (MACD cắt xuống Signal)
    df.loc[(df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1)), 'macd_cross'] = 'deathcross'

    df['ema_strat'] = df["close"] > df["ema20"]
    df['rsi30'] = fi.rsi(df['close'], window=30)
    df['rsi_signal'] = df['rsi30'].apply(lambda x: 'overbought' if x > 70 else ('oversold' if x < 30 else 'neutral'))
    df['sma20'] = fi.sma(df['close'], window=20)
    df['bollinger_hband'] = fi.bollinger_hband(df['close'], window=20, window_dev=2)
    df['bollinger_lband'] = fi.bollinger_lband(df['close'], window=20, window_dev=2)
    df['atr'] = fi.atr(df['high'], df['low'], df['close'], window=14)
    df['tp'] = df['high'].rolling(20).max().shift()
    df['sl'] = df['low'].rolling(20).min().shift()



    # print(df)
    df.to_csv(f"csv/data_{i}_1d.csv", index=False)

print(f"Total tickers with volume >= 200000: {cnt}")