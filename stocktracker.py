import requests
import pandas as pd
from datetime import datetime, timedelta
import os

API_KEY = os.environ.get("API_KEY")

stock = input("Enter Stock Name to fetch data : ")

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}'
r = requests.get(url)
data = r.json().get("Time Series (Daily)", {})

df = pd.DataFrame(data)

print(df)

