import requests
import logging

logger = logging.getLogger(__name__)

def ask_chat_engine(prompt):
    """Free AI analysis using Hugging Face endpoints"""
    try:
        # Try the free Mistral API
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
            headers={"Authorization": "Bearer hf_xxxxxxxx"},  # Optional public token
            json={"inputs": prompt},
            timeout=20
        )
        
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
            
        return "⚠️ Free AI service is currently overloaded"
        
    except Exception as e:
        logger.error(f"AI service error: {str(e)}")
        return "⚠️ AI analysis is temporarily unavailable"
