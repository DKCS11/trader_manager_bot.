import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}

def ask_chat_engine(prompt):
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]