import requests
import os
import logging
import base64
from openai import OpenAI  # Updated import

logger = logging.getLogger(__name__)

def read_chart_image(image_bytes):
    """Analyze chart image using available APIs"""
    try:
        # Option 1: Use OpenAI's GPT-4 Vision
        if os.getenv("OPENAI_API_KEY"):
            return analyze_with_openai(image_bytes)
        
        # Option 2: Use free API (Imagga)
        return analyze_with_imagga(image_bytes)
        
    except Exception as e:
        logger.error(f"Chart analysis failed: {str(e)}")
        return "⚠️ Could not analyze chart (service unavailable)"

def analyze_with_openai(image_bytes):
    """Use OpenAI's vision capabilities (v1.0.0+ syntax)"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this trading chart for trends, patterns, and potential trades."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def analyze_with_imagga(image_bytes):
    """Fallback to Imagga's tagging API"""
    api_key = os.getenv("IMAGGA_API_KEY") or "free_credential"  # Replace with your key
    response = requests.post(
        "https://api.imagga.com/v2/tags",
        auth=(api_key, ""),
        files={"image": image_bytes},
        params={"image_content": "trading chart"}
    )
    tags = [tag["tag"]["en"] for tag in response.json()["result"]["tags"][:5]]
    return "Key elements: " + ", ".join(tags)
