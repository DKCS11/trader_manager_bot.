import os

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
    STRATEGY = "ES_SCALPER"  # Options: ES_SCALPER, SWING_TRADER
    RISK_PER_TRADE = 0.02    # 2% risk per trade
