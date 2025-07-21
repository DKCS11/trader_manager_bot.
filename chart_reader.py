import requests
import os
import time
import logging

logger = logging.getLogger(__name__)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# List of potential vision models to try (in order)
VISION_MODELS = [
    "vikhyatk/moondream2",
    "Salesforce/blip2-opt-2.7b",
    "nlpconnect/vit-gpt2-image-captioning"
]

def read_chart_image(image_bytes):
    """Analyze chart image with multiple fallback options"""
    for model in VISION_MODELS:
        try:
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            
            response = requests.post(url, headers=headers, data=image_bytes, timeout=30)
            
            # Handle model loading
            if response.status_code == 503:
                wait_time = response.json().get("estimated_time", 30)
                logger.info(f"Model {model} loading, waiting {wait_time}s...")
                time.sleep(wait_time)
                return read_chart_image(image_bytes)
                
            response.raise_for_status()
            result = response.json()
            return result[0].get("generated_text", str(result))
            
        except Exception as e:
            logger.warning(f"Model {model} failed: {str(e)}")
            continue
    
    logger.error("All vision models failed")
    return "⚠️ Could not analyze chart (try a clearer image or different model)"
