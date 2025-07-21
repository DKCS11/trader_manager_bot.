import requests
import os

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise Exception("HUGGINGFACE_API_KEY environment variable is missing!")

MOONDREAM_API_URL = "https://api-inference.huggingface.co/models/vikhyatk/moondream1.0"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def read_chart_image(image_bytes):
    response = requests.post(MOONDREAM_API_URL, headers=headers, files={"file": image_bytes})
    return response.json()
   
