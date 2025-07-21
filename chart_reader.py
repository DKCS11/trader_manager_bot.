import requests
import os
import logging
import base64

logger = logging.getLogger(__name__)

def read_chart_image(image_bytes):
    """Analyze chart image using a reliable API"""
    try:
        # Option 1: Use OpenAI's GPT-4 Vision (if you have access)
        if os.getenv("OPENAI_API_KEY"):
            return analyze_with_openai(image_bytes)
        
        # Option 2: Use a free API (example with Imagga)
        return analyze_with_imagga(image_bytes)
        
    except Exception as e:
        logger.error(f"Chart analysis failed: {str(e)}")
        return "⚠️ Could not analyze chart (service unavailable)"

def analyze_with_openai(image_bytes):
    """Use OpenAI's vision capabilities"""
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this trading chart. Describe key patterns, support/resistance levels, and trends."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"}
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def analyze_with_imagga(image_bytes):
    """Fallback to Imagga's tagging API (free tier available)"""
    api_key = os.getenv("IMAGGA_API_KEY") or "YOUR_FREE_KEY"
    response = requests.post(
        "https://api.imagga.com/v2/tags",
        auth=(api_key, ""),
        files={"image": image_bytes},
        data={"image_content": "trading chart"}
    )
    tags = [tag["tag"]["en"] for tag in response.json()["result"]["tags"][:5]]
    return "Chart features: " + ", ".join(tags)
