import requests
import os
import json
from chart_reader import read_chart_image
from chat_engine import ask_chat_engine
from trade_logic import suggest_trade

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def save_trade_log(data):
    try:
        with open("trade_memory.json", "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []
    logs.append(data)
    with open("trade_memory.json", "w") as file:
        json.dump(logs, file, indent=2)

async def process_telegram_update(update):
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")

    if "photo" in message:
        file_id = message["photo"][-1]["file_id"]
        file_info = requests.get(f"{TELEGRAM_API_URL}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]
        image_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        image_bytes = requests.get(image_url).content

        caption = read_chart_image(image_bytes)
        strategy = suggest_trade(str(caption))
        conversation_response = ask_chat_engine(f"Chart analysis: {caption}\nSuggestion: {strategy}")

        save_trade_log({"caption": caption, "strategy": strategy, "response": conversation_response})

        message_text = f"Caption: {caption}\nStrategy: {strategy}\nAI Thoughts: {conversation_response}"
        requests.get(f"{TELEGRAM_API_URL}/sendMessage", params={"chat_id": chat_id, "text": message_text})
    else:
        requests.get(f"{TELEGRAM_API_URL}/sendMessage", params={"chat_id": chat_id, "text": "Please send a chart image."})