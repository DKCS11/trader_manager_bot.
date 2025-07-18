# Trader Manager Bot

AI-powered futures trading assistant using FastAPI, Hugging Face Moondream, OpenRouter AI, and Telegram.

## Features

- Chart reading using Hugging Face Moondream API.
- Trade suggestions based on chart analysis.
- Conversation and insights via OpenRouter API.
- Telegram bot interface for easy interaction.
- JSON-based trade logging.

## Setup

1. Create a Telegram bot and get the `TELEGRAM_BOT_TOKEN`.
2. Get your `HUGGINGFACE_API_KEY` from huggingface.co.
3. Get your `OPENROUTER_API_KEY` from openrouter.ai.
4. Add these as environment variables on Render.

## Deploy

- Push this repo to GitHub.
- Import the repo to Render.com.
- It auto-deploys using `render.yaml`.

## Usage

- Send a chart image to your Telegram bot.
- Receive analysis, trade suggestion, and AI explanation.