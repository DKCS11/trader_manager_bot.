import requests

# Your bot token (replace if regenerated)
BOT_TOKEN = "7960553174:AAE2UcsTyALD69ThMM_Bi2Vuxs9Z1GvLsLc"

# Your deployed app's webhook URL
WEBHOOK_URL = "https://elliottwavebot.onrender.com/webhook"

# Construct full Telegram API URL
url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

# Send request
response = requests.get(url, params={"url": WEBHOOK_URL})

# Print the result
print("✅ Webhook setup response:")
print(response.status_code)
print(response.json())
