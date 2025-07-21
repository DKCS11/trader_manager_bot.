import requests
import os
import time
import logging

logger = logging.getLogger(__name__)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MOONDREAM_API_URL = "https://api-inference.huggingface.co/models/vikhyatk/moondream2"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def read_chart_image(image_bytes):
    """Analyze chart image using HuggingFace Moondream only"""
    try:
        response = requests.post(
            MOONDREAM_API_URL,
            headers=headers,
            data=image_bytes
        )
        
        # Handle model loading
        if response.status_code == 503:
            wait_time = response.json().get("estimated_time", 30)
            logger.info(f"Model loading, waiting {wait_time}s...")
            time.sleep(wait_time)
            return read_chart_image(image_bytes)
            
        response.raise_for_status()
        return response.json()[0]["generated_text"]
        
    except Exception as e:
        logger.error(f"Chart analysis failed: {str(e)}")
        return "⚠️ Could not analyze chart (try a clearer image)"
