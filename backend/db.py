# backend/db.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Always load .env from the project root, no matter where this file is!
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client['trend_analyzer_db']

def get_db():
    return db

def get_results_for_keyword(keyword):
    entry = db.trends.find_one({"keyword": keyword})
    return entry["results"] if entry else []
