import requests
import os
import pandas as pd
from config.settings import fmp_api_key

def get_volume_change(ticker):
    url = f"https://financialmodelingprep.com/api/v3/historical-chart/1day/{ticker}?apikey={fmp_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) >= 2:
            latest_volume = data[0]['volume']
            prev_volume = data[1]['volume']
            return round(((latest_volume - prev_volume) / prev_volume) * 100, 2)
    return 0  # Default if data is unavailable

# Add volume change to stock dataset
stocks['volume_change'] = stocks['ticker'].apply(get_volume_change)
print(stocks)
