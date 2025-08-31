from FiinQuantX import FiinSession
import os
import json
from dotenv import load_dotenv
import time
import pandas as pd
load_dotenv(dotenv_path=".env")

username = os.getenv("USER")
password = os.getenv("PASSWORD")

client = FiinSession(
    username=username,
    password=password,
).login()

VN_30 = ['STB', 'VIC', 'DGC', 'SAB', 'ACB', 'BCM', 'MSN', 'CTG', 'GVR', 'MWG', 'VIB', 'VNM', 'HPG', 'VPB', 'VCB', 'LPB', 'TPB', 'MBB', 'HDB', 'FPT', 'VRE', 'TCB', 'BID', 'VHM', 'SHB', 'VJC', 'SSB', 'GAS', 'PLX', 'SSI']
tickers = ["ACB","BID","VCB"]
# for tickers in wh:
for i in VN_30:
    fs_dict = client.FundamentalAnalysis().get_ratios(
        tickers=[i],
        TimeFilter="Quarterly",
        LatestYear=[2025],
        NumberOfPeriod=14,
    # Consolidated=True,
    Fields=["ROA","ROE", "EBITMargin", "ROIC","NetRevenueGrowthYoY"]
    )
    # print(i)
    # print(f'Ratios for {i}:')
    df = pd.DataFrame(fs_dict,index=[i])
    df.to_csv(f"csv/ratio_{i}.csv", index=False)


# # Keo het ve 1 file ratios
fs_dict = client.FundamentalAnalysis().get_ratios(
    tickers=tickers,
    TimeFilter="Yearly",
    LatestYear=[2025],
    NumberOfPeriod=5,
    # Consolidated=False,
Fields=["ROA","ROE", "EBITMargin", "ROIC","NetRevenueGrowthYoY"]
)

# # print(i)
# # print(f'Ratios for {i}:')
df = pd.DataFrame(fs_dict)
df.to_csv(f"csv/ratio_{tickers}.csv", index=False)



# print(df)