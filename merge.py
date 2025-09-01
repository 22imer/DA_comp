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


VN_30 = ['STB', 'VIC', 'DGC', 'SAB', 'ACB', 'BCM', 'MSN', 'CTG', 'GVR', 'MWG', 'VIB', 'VNM', 'HPG', 'VPB', 'VCB', 'LPB', 'TPB', 'MBB', 'HDB', 'FPT', 'VRE', 'TCB', 'BID', 'VHM', 'SHB', 'VJC', 'SSB', 'GAS', 'PLX', 'SSI']

tickers_hose = client.TickerList(ticker="VNINDEX")._get_data()
tickers_hnx = client.TickerList(ticker="HNXINDEX")._get_data()
tickers_upcom = client.TickerList(ticker="UPCOMINDEX")._get_data()

all_tickers = list(set(filter(lambda item: len(item) <= 3, tickers_hose + tickers_hnx + tickers_upcom)))


for i in VN_30:
    data = pd.read_csv(f"csv/data_{i}_1d.csv")
    ratio = pd.read_csv(f"csv/ratio_{i}.csv")

    merged = pd.merge(data, ratio, on=["ticker", "year", "quarter"], how="inner")

    merged.to_csv(f"csv/input_{i}.csv", index=False)

