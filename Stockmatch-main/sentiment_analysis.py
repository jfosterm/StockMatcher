import requests
from textblob import TextBlob
from config.settings import NEWS_API_KEY
from datetime import datetime, timedelta

def get_last_two_weeks_dates():
    today = datetime.today()
    two_weeks_ago = today - timedelta(days=14)

    return two_weeks_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

# Fetch news for only the last two weeks
def fetch_news(company):
    from_date, to_date = get_last_two_weeks_dates()
    
    url = f"https://newsapi.org/v2/everything?q={company}&language=en&from={from_date}&to={to_date}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    news_data = response.json()
    
    return news_data.get("articles", [])

# Function to analyze sentiment of a news article
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns sentiment score (-1 to 1)

# Main function
def get_sentiment_for_company(ticker):
    articles = fetch_news(ticker)
    
    sentiments = []
    
    for article in articles[:10]:  # Limit to 5 articles for efficiency
        title = article.get("title", "")
        description = article.get("description", "")
        content = f"{title}. {description}"  # Combine title & description

        sentiment_score = analyze_sentiment(content)
        sentiments.append(sentiment_score)

    # Calculate average sentiment
    if sentiments:
        avg_sentiment = sum(sentiments) / len(sentiments)
        return avg_sentiment
    else:
        print("No news found.")
        return None

# Example: Analyze sentiment for Tesla
#get_sentiment_for_company("GOOGL")