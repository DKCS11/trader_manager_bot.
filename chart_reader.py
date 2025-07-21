import requests
import os
import logging

logger = logging.getLogger(__name__)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MOONDREAM_API_URL = "https://api-inference.huggingface.co/models/vikhyatk/moondream1.0"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def read_chart_image(image_bytes):
    """Extract text from chart image."""
    try:
        response = requests.post(
            MOONDREAM_API_URL,
            headers=headers,
            data=image_bytes
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        logger.error(f"HuggingFace API error: {str(e)}")
        return f"⚠️ Chart reading failed: {str(e)}"
