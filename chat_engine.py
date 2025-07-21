import requests
import os
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://your-render-url.onrender.com",
    "X-Title": "Trader Manager Bot"
}

def ask_chat_engine(prompt):  # Make sure this matches your import
    """Query OpenRouter AI with error handling"""
    try:
        payload = {
            "model": "google/gemma-7b-it:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
        
    except Exception as e:
        logger.error(f"AI service error: {str(e)}")
        return "⚠️ AI analysis is currently unavailable"
