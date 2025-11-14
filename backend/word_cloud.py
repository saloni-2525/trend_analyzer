from fastapi import APIRouter, Query
from collections import Counter
import re

router = APIRouter()

# Common English stopwords (to skip meaningless words)
STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be because been before being below
between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each
few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers
herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more
most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same
shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them
themselves then there there's these they they'd they'll they're they've this those through to too under
until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's
which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours
yourself yourselves
""".split())

# Simple text cleaning
def clean_text(text):
    text = re.sub(r"http\S+|www\S+", "", text)  # remove URLs
    text = re.sub(r"[^A-Za-z\s]", "", text)  # remove punctuation/numbers
    text = text.lower().strip()
    return text

@router.get("/topwords")
def get_top_words(keyword: str = Query(...)):
    """
    Collects text from Reddit, Twitter, News data (already stored or fetched)
    and returns top 20 most common words (excluding stopwords).
    """
    # Example: replace this section with your own DB fetch
    # Here we're just combining text from all three sources
    # You can adapt it to your structure easily
    all_texts = []

    try:
        from .db import get_db
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT text FROM combined_data
            WHERE keyword = %s
        """, (keyword,))
        rows = cursor.fetchall()
        all_texts = [row["text"] for row in rows if row.get("text")]
    except Exception as e:
        print("DB fetch error:", e)
        all_texts = []

    if not all_texts:
        return []

    # Combine all text and clean
    combined_text = " ".join(all_texts)
    cleaned = clean_text(combined_text)
    words = [w for w in cleaned.split() if w not in STOPWORDS and len(w) > 2]

    # Count top 20 words
    counter = Counter(words)
    top_words = counter.most_common(20)

    # Format output
    return [{"word": w, "count": c} for w, c in top_words]
