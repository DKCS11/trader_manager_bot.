import requests
import os
import logging
import base64

logger = logging.getLogger(__name__)

def read_chart_image(image_bytes):
    """Analyze trading chart with multiple fallback options"""
    try:
        # 1. First try free API (Imagga)
        if os.getenv("IMAGGA_API_KEY"):
            return analyze_with_imagga(image_bytes)
            
        # 2. Try local analysis if no APIs available
        return analyze_locally(image_bytes)
        
    except Exception as e:
        logger.error(f"Chart analysis failed: {str(e)}")
        return "⚠️ Could not analyze chart (try a clearer image)"

def analyze_with_imagga(image_bytes):
    """Free tier API (500 calls/month)"""
    api_key = os.getenv("IMAGGA_API_KEY")
    response = requests.post(
        "https://api.imagga.com/v2/tags",
        auth=(api_key, ""),
        files={"image": image_bytes},
        params={"image_content": "trading chart"},
        timeout=10
    )
    response.raise_for_status()
    tags = [tag["tag"]["en"] for tag in response.json()["result"]["tags"][:5]]
    return "Chart features: " + ", ".join(tags)

def analyze_locally(image_bytes):
    """Basic analysis without external APIs or Pillow"""
    try:
        # Extremely lightweight analysis (no Pillow required)
        file_size = len(image_bytes)
        header = image_bytes[:24]
        
        # Detect basic image type from magic numbers
        if header.startswith(b'\xff\xd8'):
            img_type = "JPEG"
        elif header.startswith(b'\x89PNG'):
            img_type = "PNG"
        else:
            img_type = "Unknown"
            
        return (
            f"Basic Analysis:\n"
            f"• File Size: {file_size:,} bytes\n"
            f"• Image Type: {img_type}\n"
            f"• Enable APIs for detailed analysis"
        )
    except Exception as e:
        return f"⚠️ Basic analysis failed: {str(e)}"
