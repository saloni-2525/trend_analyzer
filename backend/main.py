# backend/main.py
from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .db import get_db, get_results_for_keyword
from .reddit_api import fetch_reddit_data
from .twitter_api import fetch_twitter_data
from .news_api import fetch_news_data
from .sentiment import analyze_sentiment
from .summary_gen import generate_summary, generate_overall_summary
from .word_cloud import router as wordcloud_router

app = FastAPI(title="Trend Analyzer API")
app.include_router(wordcloud_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Trend Analyzer Backend Running!"}


#  Endpoint 1: Fetch latest trend data from Reddit, Twitter, and News
@app.get("/trend/{keyword}")
def get_trend(keyword: str):
    # Fetch data
    reddit_comments = fetch_reddit_data(keyword)
    # tweets = fetch_twitter_data(keyword)
    news_articles = fetch_news_data(keyword)

    results = []

    # Reddit
    for item in reddit_comments:
        text = item.get("body", "")
        sentiment = analyze_sentiment(text)
        summary = generate_summary(text, max_words=50)
        results.append({
            "source": "reddit",
            "text": text,
            "sentiment": sentiment,
            "summary": summary
        })

    # Twitter
    for tweet in tweets:
        text = tweet.get("text", "")
        sentiment = analyze_sentiment(text)
        summary = generate_summary(text, max_words=50)
        results.append({
            "source": "twitter",
            "text": text,
            "sentiment": sentiment,
            "summary": summary
        })

    # News
    for article in news_articles:
        text = article.get("description", "") or article.get("title", "")
        sentiment = analyze_sentiment(text)
        summary = generate_summary(text, max_words=50)
        results.append({
            "source": "news",
            "title": article.get("title"),
            "text": text,
            "url": article.get("url"),
            "sentiment": sentiment,
            "summary": summary
        })

    # Store in MongoDB
    db = get_db()
    db.trends.insert_one({
        "keyword": keyword,
        "results": results,
        "created_at": datetime.utcnow()
    })

    return {"keyword": keyword, "results": results}


#  Endpoint 2: Fetch historical searches for a keyword
@app.get("/trend_history/{keyword}")
def get_trend_history(keyword: str, limit: int = Query(10)):
    """
    Returns the historical trends for a keyword, newest first.
    """
    db = get_db()
    history = list(db.trends.find({"keyword": keyword}).sort("created_at", -1).limit(limit))

    # Convert ObjectId and datetime for JSON
    for doc in history:
        doc["_id"] = str(doc["_id"])
        doc["created_at"] = doc["created_at"].isoformat()

    return {"keyword": keyword, "history": history}


#  Endpoint 3: Generate an overall summary combining all sources
@app.get("/trend_summary/{keyword}")
def get_trend_summary(keyword: str):
    # Try to get existing results
    results = get_results_for_keyword(keyword)

    # If no data found, fetch fresh data
    if not results:
        print(f"No existing data for '{keyword}', fetching new data...")
        reddit_comments = fetch_reddit_data(keyword)
        # tweets = fetch_twitter_data(keyword)
        news_articles = fetch_news_data(keyword)

        results = []

        # Reddit
        for item in reddit_comments:
            text = item.get("body", "")
            sentiment = analyze_sentiment(text)
            summary = generate_summary(text, max_words=50)
            results.append({
                "source": "reddit",
                "text": text,
                "sentiment": sentiment,
                "summary": summary
            })

        # Twitter
        for tweet in tweets:
            text = tweet.get("text", "")
            sentiment = analyze_sentiment(text)
            summary = generate_summary(text, max_words=50)
            results.append({
                "source": "twitter",
                "text": text,
                "sentiment": sentiment,
                "summary": summary
            })

        # News
        for article in news_articles:
            text = article.get("description", "") or article.get("title", "")
            sentiment = analyze_sentiment(text)
            summary = generate_summary(text, max_words=50)
            results.append({
                "source": "news",
                "title": article.get("title"),
                "text": text,
                "url": article.get("url"),
                "sentiment": sentiment,
                "summary": summary
            })

        # Save to DB
        db = get_db()
        db.trends.insert_one({
            "keyword": keyword,
            "results": results,
            "created_at": datetime.utcnow()
        })

    # Generate overall summary from all sources
    print(f"[DEBUG] Generating summary for keyword: {keyword}")
    print(f"[DEBUG] Total items fetched: {len(results)}")

    for i, r in enumerate(results[:5]): 
     print(f"[DEBUG] Sample {i+1}: Source={r.get('source')}, Text={r.get('text')[:100]}")
    summary = generate_overall_summary(results, keyword)
    return {"keyword": keyword, "overall_summary": summary}
