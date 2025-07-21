import os

@app.get("/debug")
async def debug():
    return {
        "TELEGRAM_BOT_TOKEN": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "HUGGINGFACE_API_KEY": bool(os.getenv("HUGGINGFACE_API_KEY")),
        "OPENROUTER_API_KEY": bool(os.getenv("OPENROUTER_API_KEY")),
    }
from fastapi import FastAPI, Request
from telegram_bot import process_telegram_update

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "alive"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    await process_telegram_update(data)
    return {"status": "ok"}
