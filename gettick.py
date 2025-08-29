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

# tickers_hose = client.TickerList(ticker="VNINDEX")._get_data()
# tickers_hnx = client.TickerList(ticker="HNXINDEX")._get_data()
# tickers_upcom = client.TickerList(ticker="UPCOMINDEX")._get_data()

# all_tickers = list(set(filter(lambda item: len(item) <= 3, tickers_hose + tickers_hnx)))

# print(len(all_tickers))
# print(all_tickers)

ticker_vn30 = client.TickerList(ticker="VN30")._get_data()
data = list(set(filter(lambda item: len(item) <= 3, ticker_vn30)))
print(len(data))