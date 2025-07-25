import logging
import os
import requests
import json
import pandas as pd
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from modules.tools import handle_tools
from modules.file_handler import handle_file
from modules.memory import MemoryManager

# Load ENV
load_dotenv()
BOT_TOKEN = os.getenv("telegram_token")
API_KEY = os.getenv("openrouter_api_key")
MODEL = os.getenv("model")

# Logging
logging.basicConfig(level=logging.INFO)

# Memory per user
memory = MemoryManager()

# Chat Completion API
def chat_completion(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"API Error: {response.json()}"

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai aku Nayla 🤍 Siap nemenin kamu 24 jam~ Ketik apa aja ya!")

# Handle message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text

    # Tool trigger
    if handle_tools(update, context, text):
        return

    # History
    history = memory.load(user_id)
    history.append({"role": "user", "content": text})
    response = chat_completion(history)
    history.append({"role": "assistant", "content": response})
    memory.save(user_id, history)

    await update.message.reply_text(response)

# Handle file
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_file(update, context)

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
