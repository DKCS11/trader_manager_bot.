import requests
import os
import json
import logging
from chart_reader import read_chart_image
from chat_engine import ask_chat_engine
from trade_logic import suggest_trade

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def save_trade_log(data):
    """Save trade data to JSON file."""
    try:
        with open("trade_memory.json", "a+") as file:
            file.seek(0)
            logs = json.load(file) if file.read() else []
        logs.append(data)
        with open("trade_memory.json", "w") as file:
            json.dump(logs, file, indent=2)
    except Exception as e:
        logger.error(f"Failed to save trade log: {str(e)}")

async def process_telegram_update(update):
    """Process Telegram message or photo."""
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        
        if not chat_id:
            return

        if "photo" in message:
            # Handle photo
            file_id = message["photo"][-1]["file_id"]
            file_info = requests.get(f"{TELEGRAM_API_URL}/getFile?file_id={file_id}").json()
            file_path = file_info["result"]["file_path"]
            image_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
            image_bytes = requests.get(image_url).content

            caption = read_chart_image(image_bytes)
            strategy = suggest_trade(str(caption))
            conversation_response = ask_chat_engine(
                f"Chart analysis: {caption}\nSuggestion: {strategy}"
            )

            save_trade_log({
                "caption": caption,
                "strategy": strategy,
                "response": conversation_response
            })

            message_text = (
                f"📊 Chart Analysis:\n{caption}\n\n"
                f"🔮 Trade Suggestion:\n{strategy}\n\n"
                f"🤖 AI Insights:\n{conversation_response}"
            )
        else:
            message_text = "Please send a chart image for analysis."

        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": message_text}
        )
    except Exception as e:
        logger.error(f"Update processing failed: {str(e)}")
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": f"⚠️ Error: {str(e)}"}
        )
