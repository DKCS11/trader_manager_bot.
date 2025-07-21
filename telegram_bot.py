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
    try:
        with open("trade_memory.json", "a+") as file:
            file.seek(0)
            logs = json.load(file) if file.read() else []
            logs.append(data)
            file.seek(0)
            json.dump(logs, file, indent=2)
    except Exception as e:
        logger.error(f"Failed to save trade log: {str(e)}")

async def process_telegram_update(update):
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        
        if not chat_id:
            return

        if "photo" in message:
            # Get highest resolution photo
            file_id = message["photo"][-1]["file_id"]
            file_info = requests.get(
                f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
            ).json()
            
            file_path = file_info["result"]["file_path"]
            image_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
            
            # Download image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Analyze image
            caption = read_chart_image(image_response.content)
            strategy = suggest_trade(str(caption))
            ai_response = ask_chat_engine(
                f"Analyze this trading chart:\n{caption}\n\nSuggested strategy: {strategy}\n"
                "Provide concise trading advice in 2-3 sentences."
            )
            
            # Save and respond
            save_trade_log({
                "caption": caption,
                "strategy": strategy,
                "ai_response": ai_response
            })
            
            response_text = (
                "📈 Chart Analysis:\n"
                f"{caption}\n\n"
                "💡 Trading Suggestion:\n"
                f"{strategy}\n\n"
                "🤖 AI Insights:\n"
                f"{ai_response}"
            )
            
        else:
            response_text = "Please send a chart image for analysis."

        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": response_text}
        )
        
    except Exception as e:
        logger.error(f"Telegram processing error: {str(e)}")
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": f"⚠️ Error: {str(e)}"}
        )
