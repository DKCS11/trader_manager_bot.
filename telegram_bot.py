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
    """Save trade data to JSON file with error handling"""
    try:
        with open("trade_memory.json", "a+") as file:
            file.seek(0)
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                logs = []
            logs.append(data)
            file.seek(0)
            file.truncate()
            json.dump(logs, file, indent=2)
    except Exception as e:
        logger.error(f"Failed to save trade log: {str(e)}")

async def process_telegram_update(update):
    """Process incoming Telegram messages"""
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        
        if not chat_id:
            return

        if "photo" in message:
            # Get highest resolution photo available
            file_id = message["photo"][-1]["file_id"]
            
            # Get file path from Telegram
            file_response = requests.get(
                f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
            )
            file_response.raise_for_status()
            file_path = file_response.json()["result"]["file_path"]
            
            # Download image
            image_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status()
            image_bytes = image_response.content

            # Analyze image
            caption = read_chart_image(image_bytes)
            strategy = suggest_trade(str(caption))
            ai_response = ask_chat_engine(
                f"Analyze this trading chart description: {caption}\n"
                "Provide 2-3 sentence trading advice in simple terms."
            )

            # Save results
            save_trade_log({
                "chat_id": chat_id,
                "caption": caption,
                "strategy": strategy,
                "ai_response": ai_response,
                "timestamp": message.get("date")
            })

            # Format response
            response_text = f"""
📈 Chart Analysis:
{caption}

💡 Trading Suggestion:
{strategy}

🤖 AI Insights:
{ai_response}

💡 Pro Tip: For best results:
• Use clear, cropped charts
• Include volume indicators
• Avoid screenshots of screens
"""
        else:
            response_text = """
📊 Please send a clear image of your trading chart.

For best results:
1. Crop to the relevant price area
2. Use candlestick or bar charts
3. Include volume if possible

I'll analyze:
• Trends and patterns
• Support/resistance levels
• Potential trade setups
"""

        # Send response
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": response_text,
                "parse_mode": "Markdown"
            }
        )
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "⚠️ Network error. Please try again later."
            }
        )
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "⚠️ System error. Our team has been notified."
            }
        )
