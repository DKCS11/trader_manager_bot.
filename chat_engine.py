import requests
import os
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://your-render-url.onrender.com",  # Replace with your URL
    "X-Title": "Trader Manager Bot"
}

FREE_MODEL = "google/gemma-7b-it:free"
PAID_MODEL = "gpt-4"

def ask_chat_engine(prompt):
    """Query OpenRouter AI with fallback to free model"""
    try:
        payload = {
            "model": PAID_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        
        # If payment required, try free model
        if response.status_code == 402:
            logger.info("Falling back to free model")
            payload["model"] = FREE_MODEL
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
            
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
        
    except Exception as e:
        logger.error(f"OpenRouter API error: {str(e)}")
        return "⚠️ AI analysis is currently unavailable"
