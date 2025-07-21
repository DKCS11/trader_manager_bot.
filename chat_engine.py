import requests
import os
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Ordered list of models to try
MODELS = [
    {"name": "gpt-3.5-turbo", "free": False},
    {"name": "google/gemma-7b-it:free", "free": True},
    {"name": "anthropic/claude-instant-v1", "free": False}
]

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://your-render-url.onrender.com",
    "X-Title": "Trader Manager Bot"
}

def ask_chat_engine(prompt):
    """Query AI with multiple fallback options"""
    for model in MODELS:
        try:
            if model["free"] and not OPENROUTER_API_KEY:
                continue
                
            payload = {
                "model": model["name"],
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 402 and model["free"]:
                continue  # Skip if free model requires payment
                
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.warning(f"Model {model['name']} failed: {str(e)}")
            continue
    
    logger.error("All AI models failed")
    return "⚠️ AI analysis is currently unavailable"
