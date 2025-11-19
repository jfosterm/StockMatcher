import requests
from config.settings import fmp_api_key

def fetch_stocks_from_api():
    """
    Fetch a list of stocks with a market cap greater than $1 billion from the FMP API.
    """
    url = f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1e9&apikey={fmp_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns a list of stocks
    else:
        print("Failed to fetch stocks from FMP API")
        return []
    
def fetch_stock_from_api(ticker):
    """
    Fetch stock data for a single ticker from the FMP API.
    :param ticker: Stock ticker symbol.
    :return: Stock data.
    """
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={fmp_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns stock data
    else:
        print(f"Failed to fetch data for {ticker}")
        return None