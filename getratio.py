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

# All ticker
# tickers_hose = client.TickerList(ticker="VNINDEX")._get_data()
# tickers_hnx = client.TickerList(ticker="HNXINDEX")._get_data()
# tickers_upcom = client.TickerList(ticker="UPCOMINDEX")._get_data()

# all_tickers = list(set(filter(lambda item: len(item) <= 3, tickers_hose + tickers_hnx)))


cnt = 0
# df = pd.DataFrame(columns=["organizationId", "ticker", "year", "quarter", "ROA", "ROE", "EBITMargin", "ROIC", "NetRevenueGrowthYoY"])
for ticker in VN_30:
    fs_dict = client.FundamentalAnalysis().get_ratios(
        tickers=ticker,
        TimeFilter="Yearly",
        LatestYear=[2025],
        NumberOfPeriod=4,
        Consolidated=True,
        Fields=["ROA","ROE", "EBITMargin", "ROIC","NetRevenueGrowthYoY"],
    )
    df= pd.DataFrame(fs_dict)
    df.to_csv(f"csv/ratio_{ticker}.csv", index=False)
