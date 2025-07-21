from fastapi import FastAPI, Request, HTTPException
import os
import logging
from telegram_bot import process_telegram_update

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/debug")
async def debug():
    """Endpoint to verify environment variables."""
    return {
        "TELEGRAM_BOT_TOKEN": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "HUGGINGFACE_API_KEY": bool(os.getenv("HUGGINGFACE_API_KEY")),
        "OPENROUTER_API_KEY": bool(os.getenv("OPENROUTER_API_KEY")),
    }

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "active", "service": "Trader Manager Bot"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle Telegram updates."""
    try:
        data = await request.json()
        logger.info(f"Incoming update: {data}")
        await process_telegram_update(data)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
