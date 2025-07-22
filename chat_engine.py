import requests
import logging

logger = logging.getLogger(__name__)

FREE_AI_ENDPOINTS = [
    {
        "name": "HuggingFace",
        "url": "https://api-inference.huggingface.co/models/google/flan-t5-xxl",
        "headers": {},
        "payload": lambda p: {"inputs": p},
        "parser": lambda r: r.json()[0]["generated_text"]
    },
    {
        "name": "DeepAI",
        "url": "https://api.deepai.org/api/text-generator",
        "headers": {"api-key": "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"},
        "payload": lambda p: {"text": p},
        "parser": lambda r: r.json()["output"]
    }
]

def ask_chat_engine(prompt):
    """Get AI analysis with multiple fallback options"""
    for api in FREE_AI_ENDPOINTS:
        try:
            response = requests.post(
                api["url"],
                headers=api["headers"],
                json=api["payload"](prompt),
                timeout=20
            )
            if response.status_code == 200:
                return format_ai_response(api["parser"](response))
        except Exception as e:
            logger.warning(f"{api['name']} failed: {str(e)}")
            continue
    
    return "⚠️ AI services are busy. Please try again later or enable premium APIs for reliable access."

def format_ai_response(text):
    """Clean up AI response"""
    return (
        text.replace("In this image", "In the chart")
            .replace("photo", "chart")
            .replace("picture", "trading view")
            .split(".")[0] + "..."  # Shorten long responses
    )
