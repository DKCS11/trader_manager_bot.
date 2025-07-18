from fastapi import FastAPI, Request
from telegram_bot import process_telegram_update

app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    await process_telegram_update(data)
    return {"status": "ok"}