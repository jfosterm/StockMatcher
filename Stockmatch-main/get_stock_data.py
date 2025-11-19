import requests
from config.settings import fmp_api_key
import pandas as pd
from services.fmp_services import fetch_stock_from_api

def get_stock_data(tickers):
    """
    Fetch stock data for a list of tickers from the FMP API.
    :param tickers: List of stock tickers.
    :return: DataFrame with stock data.
    """
    stock_data = []
    for ticker in tickers:
            data = fetch_stock_from_api(ticker)
            if data:  # Ensure data is not empty
                stock_data.append({
                    "ticker": ticker,
                    "price": data[0]["price"],
                    "change": data[0]["change"],
                    "change_perc": data[0]["changesPercentage"]
                })
            else:
                print(f"Failed to fetch data for {ticker}")
    return pd.DataFrame(stock_data)  # Return a DataFrame