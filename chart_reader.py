import requests
import os
import logging
import base64

logger = logging.getLogger(__name__)

def read_chart_image(image_bytes):
    """Analyze trading charts using free APIs with fallbacks"""
    try:
        # Try the free NLP Connect API first
        result = analyze_with_nlpconnect(image_bytes)
        if result: return result
        
        # Fallback to basic analysis
        return basic_image_analysis(image_bytes)
        
    except Exception as e:
        logger.error(f"Chart analysis failed: {str(e)}")
        return "⚠️ Could not analyze chart (try a clearer image)"

def analyze_with_nlpconnect(image_bytes):
    """Free image captioning API (no key needed)"""
    response = requests.post(
        "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning",
        headers={"Authorization": "Bearer hf_xxxxxxxx"},  # Optional public token
        data=image_bytes,
        timeout=15
    )
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    return None

def basic_image_analysis(image_bytes):
    """Fallback analysis without external APIs"""
    try:
        # Simple checks that don't require image processing
        if len(image_bytes) < 1024:
            return "Image too small for analysis"
            
        if image_bytes.startswith(b'\xFF\xD8'):
            return "JPEG image detected (enable APIs for full analysis)"
        elif image_bytes.startswith(b'\x89PNG'):
            return "PNG image detected (enable APIs for full analysis)"
            
        return "Chart image received (enable APIs for analysis)"
    except Exception:
        return "Received image data (analysis unavailable)"
