import requests
from config.settings import fmp_api_key

def get_stock_momentum(ticker): # Get the momentum of a stock
    url = f"https://financialmodelingprep.com/api/v3/historical-chart/1day/{ticker}?apikey={fmp_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        prices = [day['close'] for day in data[:10]]

        if len(prices) < 10:
            return 0  # Not enough data

        return round(((prices[0] - prices[-1]) / prices[-1]) * 100, 2) # Percentage change
    return 0  # Error fetching data