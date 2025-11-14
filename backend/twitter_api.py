import requests
from dotenv import load_dotenv
import os

# Always load .env from the project root, no matter where this file is!
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def fetch_twitter_data(keyword, max_results=10):
    """
    Fetch recent tweets containing the keyword using Twitter API v2.
    Returns a list of dicts with at least "text" field.
    """
    endpoint_url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }
    params = {
        "query": f"{keyword}",
        "tweet.fields": "id,text,author_id,created_at",
        "max_results": max_results
    }
    response = requests.get(endpoint_url, headers=headers, params=params)
    print("status:", response.status_code, response.text)

    data = response.json()
    tweets = []
    for tweet in data.get("data", []):
        tweets.append({
            "id": tweet["id"],
            "text": tweet["text"],
            "author_id": tweet["author_id"],
            "created_at": tweet["created_at"]
        })
    return tweets

# For debugging/testing
if __name__ == "__main__":
    tweets = fetch_twitter_data("python", max_results=5)
    for t in tweets:
        print(t["text"])
