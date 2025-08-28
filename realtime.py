from FiinQuantX import *
import os
import json
from dotenv import load_dotenv
import time

load_dotenv(dotenv_path=".env")




username = os.getenv("USER")
password = os.getenv("PASSWORD")

client = FiinSession(
    username=username,
    password=password,
).login()

# Events.start()

data = client.Fetch_Trading_Data(
    realtime=False,
    tickers=["HPG"],
    fields=["open", "high", "low", "close", "volume"],
    adjusted=True,
    by="1d",
    from_date="2025-07-01"
).get_data()

print(data)