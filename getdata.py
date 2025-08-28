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
# Gọi dữ liệu lịch sử
event = client.Fetch_Trading_Data(
    realtime=False,
    tickers=[tick],
    fields=["open", "high", "low", "close", "volume"],
    adjusted=True,
    by="1d",
    from_date=from_date,
    to_date=to_date
)

data = event.get_data()
df = pd.DataFrame(data)
print(df)

df.to_csv(f"data_{tick}.csv", index=False)