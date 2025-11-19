import random
import pandas as pd
from sentiment_analysis import get_sentiment_for_company as get_stock_news_sentiment
from momentum_analysis import get_stock_momentum
from get_stock_data import get_stock_data
from config.settings import fmp_api_key
import requests
from services.fmp_services import fetch_stocks_from_api, fetch_stock_from_api


def filter_stocks(stocks, min_market_cap=1e9, sector="Technology"):
    """
    Filter stocks by market cap and sector.
    :param stocks: List of stocks from FMP API.
    :param min_market_cap: Minimum market cap in dollars (default: $1 billion).
    :param sector: Sector to filter by (default: Technology).
    :return: Filtered list of stocks.
    """
    filtered_stocks = []
    print(f"Total stocks received: {len(stocks)}")  # Debug print
    for stock in stocks:
        print(f"Checking stock: {stock.get('symbol')}")  # Debug print
        print(f"Market Cap: {stock.get('marketCap')}, Sector: {stock.get('sector')}")  # Debug print
        if stock.get("marketCap", 0) >= min_market_cap and stock.get("sector") == sector:
            filtered_stocks.append(stock)
            print(f"Added {stock.get('symbol')} to filtered stocks.")  # Debug print
    print(f"Total filtered stocks: {len(filtered_stocks)}")  # Debug print
    return filtered_stocks

def score_stock(ticker):
    sentiment = get_stock_news_sentiment(ticker)
    momentum = get_stock_momentum(ticker)
    return round((sentiment * 50) + (momentum * 50), 2)

def recommend_stock(liked_tickers, disliked_tickers, exploration_rate=0.3):
    # Fetch all stocks from FMP API
    all_stocks = fetch_stocks_from_api()
    
    # Filter stocks by market cap and sector
    filtered_stocks = filter_stocks(all_stocks, min_market_cap=1e9, sector="Technology")
    
    # Extract tickers from filtered stocks
    tickers = [stock["symbol"] for stock in filtered_stocks]
    if not tickers:
        return "No stocks found."
    
    # Get stock data for the filtered tickers
    stocks = get_stock_data(tickers)
    
    # Ensure stocks is not None
    if stocks is None or stocks.empty:
        return "No stocks found or failed to fetch stock data."

    # Exclude liked and disliked tickers
    unseen_stocks = stocks[~stocks['ticker'].isin(liked_tickers + disliked_tickers)]

    if unseen_stocks.empty:
        return "No new stocks to recommend!"

    if random.random() < exploration_rate:
        return unseen_stocks.sample(1)['ticker'].values[0]

    unseen_stocks['ai_score'] = unseen_stocks['ticker'].apply(score_stock)
    return unseen_stocks.sort_values('ai_score', ascending=False).iloc[0]['ticker']