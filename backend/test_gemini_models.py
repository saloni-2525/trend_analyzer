import google.generativeai as genai
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# List all models available for your key
print("Available models:")
for m in genai.list_models():
    print(m.name)
