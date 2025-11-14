import google.generativeai as genai
from dotenv import load_dotenv
import os
import traceback

# Load environment variables from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded GEMINI_API_KEY:", API_KEY)

# Configure Gemini
genai.configure(api_key=API_KEY)

#  Function 1: Summarize individual text (used for each post/tweet/article)
def generate_summary(text, max_words=50):
    prompt = f"Summarize the following text in {max_words} words or less:\n\n{text}"
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        print("Error generating summary:", e)
        words = text.split()
        return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")


#  Function 2: Generate overall summary (Reddit + Twitter + News)
def generate_overall_summary(results, keyword):
    # Build a readable combined text for Gemini
    input_text = f"Public sentiment and discussion data for the keyword '{keyword}':\n\n"
    for item in results:
        src = item.get("source", "unknown").capitalize()
        text = item.get("text", "")[:300]  # Limit to 300 chars per entry to avoid token overload
        sent = item.get("sentiment", {})
        input_text += (
            f"{src}: \"{text}\" "
            f"(Positive: {sent.get('pos', 0)}, Neutral: {sent.get('neu', 0)}, Negative: {sent.get('neg', 0)})\n"
        )

    prompt = f"""
    You are an expert trend analyst and journalist.
    Analyze the following data collected from Reddit, Twitter, and News sources about the topic '{keyword}'.

    Write a concise yet detailed 3–5 sentence summary that:
    - Highlights the overall tone or mood (positive, neutral, or negative)
    - Describes the major themes and public opinions
    - Notes any differences between Reddit, Twitter, and News coverage
    - Mentions how recent news might have influenced discussions
    - Ends with a one-line takeaway summarizing the public trend or sentiment.

    Keep it analytical and balanced, as if writing for a professional insights dashboard.

    Data:
    {input_text}
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error generating overall summary:", str(e))
        traceback.print_exc()
        return "Summary generation failed."
    except Exception as e:
     print("[ERROR] Summary generation failed:", e)
    return "Summary generation failed."
