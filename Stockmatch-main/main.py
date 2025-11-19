from recommendation import recommend_stock

liked_tickers = ['AAPL']
disliked_tickers = ['TSLA']

next_stock = recommend_stock(liked_tickers, disliked_tickers)
print(f"Next recommended stock: {next_stock}")