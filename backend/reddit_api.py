import praw
from dotenv import load_dotenv
import os

# Always load .env from the project root, no matter where this file is!
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")


# Initialize PRAW Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def fetch_reddit_data(keyword, subreddit="all", limit=5, comment_limit=5):
    """
    Fetch recent Reddit submissions matching a keyword from a subreddit,
    and extract top-level comments from each.
    Returns a list of { "body": comment_text, ... } dicts.
    """
    results = []
    for submission in reddit.subreddit(subreddit).search(keyword, limit=limit):
        submission.comments.replace_more(limit=0)  # Flatten comment tree
        # Get up to 'comment_limit' top-level comments
        for comment in submission.comments[:comment_limit]:
            if hasattr(comment, "body"):
                results.append({
                    "body": comment.body,
                    "submission_title": submission.title,
                    "url": submission.url,
                    "score": submission.score,
                    "author": str(comment.author) if comment.author else "unknown"
                })
    return results

# For testing/debugging
if __name__ == "__main__":
    comments = fetch_reddit_data("python web scraping", limit=2)
    for c in comments:
        print(c["body"][:120])  # Print first 120 chars of each comment
