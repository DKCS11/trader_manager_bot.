import requests
import logging
import time

logger = logging.getLogger(__name__)

# List of free API endpoints to try (in order)
VISION_APIS = [
    {
        "name": "DeepAI",
        "url": "https://api.deepai.org/api/image-captioning",
        "headers": {"api-key": "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"},
        "payload": lambda img: {"image": img},
        "parser": lambda r: r.json()["output"]
    },
    {
        "name": "HuggingFace",
        "url": "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
        "headers": {},
        "payload": lambda img: img,
        "parser": lambda r: r.json()[0]["generated_text"]
    }
]

def read_chart_image(image_bytes):
    """Analyze chart using multiple free API options"""
    for api in VISION_APIS:
        try:
            response = requests.post(
                api["url"],
                headers=api["headers"],
                data=api["payload"](image_bytes),
                timeout=15
            )
            if response.status_code == 200:
                return api["parser"](response)
            time.sleep(2)  # Delay between API tries
        except Exception as e:
            logger.warning(f"{api['name']} failed: {str(e)}")
            continue
    
    # Final fallback analysis
    return enhanced_fallback_analysis(image_bytes)

def enhanced_fallback_analysis(image_bytes):
    """Improved analysis without external APIs"""
    try:
        # Check basic image characteristics
        size_kb = len(image_bytes) / 1024
        
        if size_kb < 10:
            return "Image too small for proper analysis (min 10KB recommended)"
        elif size_kb > 500:
            return "Large image received (please crop to chart area)"
            
        # Basic format detection
        if image_bytes.startswith(b'\xFF\xD8'):
            details = "High-quality JPEG (enable APIs for full analysis)"
        elif image_bytes.startswith(b'\x89PNG'):
            details = "PNG image (enable APIs for full analysis)"
        else:
            details = "Image received (format not recognized)"
            
        return f"{details}\n• Size: {size_kb:.1f} KB\n• Send clearer chart for better analysis"
    except Exception:
        return "Chart image received (analysis unavailable)"
