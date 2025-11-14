📊 **Trend Analyzer – AI-Powered Multi-Source Trend & Sentiment Explorer**

Trend Analyzer is an AI-driven system that collects real-time data from Reddit, News, and Twitter, analyzes sentiment, generates short AI summaries for each post/article, and produces a final overall trend summary using an LLM.

It also stores all searches in MongoDB and lets users retrieve history, word clouds, and summaries for any keyword.

🚀 **Features**
🔍 Multi-Source Data Collection

For any keyword, the system fetches:

🔸 Reddit comments

🔸 News articles

🔸 Tweets

🧠 **AI-Based Processing**

Every post/article is passed through:

✔ Sentiment analysis

✔ Short AI-generated summary (per post)

✔ Combined overall AI-generated summary (all sources)

📦 **Backend Services**

The FastAPI backend provides:

/trend/{keyword} → Fetch fresh data + store in DB

/trend_summary/{keyword} → Fetch or generate overall summary

/trend_history/{keyword} → Get past searches

🗃 **MongoDB Storage**

Every trend fetch is stored with:

{
  keyword,
  results: [
    { source, text, sentiment, summary, ... }
  ],
  created_at
}

🎯 **Summaries You Get**

1. Per-post summary → 50-word micro-summary
2. Full combined summary → LLM-generated theme-level summary

🛠️ **Tech Stack**
**Backend**

Python

FastAPI

NLTK / VADER sentiment

LLM models for summary (Gemini/OpenRouter/OpenAI)

Requests

PyMongo

**Database**

MongoDB (cloud/local)

**Frontend**

HTML, CSS, JS

🔥 **API Endpoints**
1️⃣ Fetch Fresh Trend Data
GET /trend/{keyword}

This endpoint:

Fetches Reddit comments

Fetches News articles

Fetches Tweets

Performs sentiment analysis

Generates per-post summaries

Saves everything in MongoDB

Sample Response
{
  "keyword": "AI",
  "results": [
    {
      "source": "reddit",
      "text": "...",
      "sentiment": "positive",
      "summary": "Short AI summary..."
    },
    {
      "source": "news",
      "title": "AI is transforming business...",
      "text": "...",
      "sentiment": "neutral",
      "summary": "Short AI summary..."
    }
  ]
}

2️⃣ Get Historical Trend Data
GET /trend_history/{keyword}?limit=10

Returns all previous searches for the keyword, sorted latest-first.

Example:

{
  "keyword": "AI",
  "history": [
    { "_id": "...", "created_at": "...", "results": [...] }
  ]
}

3️⃣ Get Overall Combined Summary
GET /trend_summary/{keyword}

This endpoint:

Tries to retrieve the latest stored results

If not found → automatically fetches fresh data

Generates a full overall summary combining all sources

Returns high-level insights for that keyword

Sample Output
{
  "keyword": "AI",
  "overall_summary": "AI is trending due to major LLM updates, industry adoption, and discussions on ethics..."
}

🔄 **Workflow**
User enters a keyword → Backend does:

🔎 Fetch Reddit comments

🗞 Fetch News articles

🐦 Fetch Tweets

🧠 Run sentiment analysis on every item

✍️ Generate short summary per item

💾 Save results to MongoDB

📤 Return data to frontend

When summary is needed →

/trend_summary/{keyword} loads the latest results

If no previous results → fetches fresh

Generates a single Overall Summary using:

generate_overall_summary(results, keyword)

▶️ How to Run the Project

1️⃣ Clone the Repository
git clone https://github.com/your-username/trend-analyzer.git
cd trend-analyzer/backend

2️⃣ Create Virtual Environment
python -m venv env
source env/bin/activate  # Windows: env\\Scripts\\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the FastAPI Backend
uvicorn main:app --reload

5️⃣ Start Frontend (if using)
cd frontend
npm install
npm start

✨ **Future Enhancements**

Add livestreaming trending graphs

Add Twitter API full integration

Add YouTube trending & comments

Add auto-scheduling using n8n / Make

Add RAG-based context summaries

👤 **Author**

Saloni Jain
AI/ML Developer | Generative AI | Automation

⭐ **Support**

If you like this project, consider giving it a star ⭐ on GitHub!
