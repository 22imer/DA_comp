from FiinQuantX import FiinSession
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
# for i in VN_30:
    # event = client.Fetch_Trading_Data(
    #     realtime=False,
    #     tickers=[i],
    #     fields=["open", "high", "low", "close", "volume"],
    #     adjusted=True,
    #     by="1d",
    #     from_date=from_date,
    #     to_date=to_date
    # )
    # data = event.get_data()
    # df = pd.DataFrame(data)

    # df.to_csv(f"csv/data_{i}_1d.csv", index=False)

for i in all_tickers:
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

    df.to_csv(f"csv/data_{i}_1d.csv", index=False)