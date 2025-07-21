import requests
import os
import time
import logging
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
# Updated to moondream2 model (actively maintained)
MOONDREAM_API_URL = "https://api-inference.huggingface.co/models/vikhyatk/moondream2"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def read_chart_image(image_bytes):
    """Analyze chart image using HuggingFace Moondream"""
    try:
        # First try Moondream API
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
        logger.error(f"HuggingFace API error: {str(e)}")
        try:
            # Fallback to basic OCR
            img = Image.open(BytesIO(image_bytes))
            import pytesseract
            return pytesseract.image_to_string(img)
        except:
            return "⚠️ Could not analyze chart image"
