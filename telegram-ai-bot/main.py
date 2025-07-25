
import os, json, logging, requests
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tools.ttsmaker import ttsmaker_speak
from tools.unit_converter import convert_units
from tools.web_search import search_web
from plugins.file_reader import handle_file
from tools.persona_manager import get_persona, set_persona

load_dotenv()
TELEGRAM_TOKEN = os.getenv("telegram_token")
api_key = os.getenv("openrouter_api_key")
model = os.getenv("model", "openchat/openchat-3.5")
logging.basicConfig(level=logging.INFO)

def load_memory(user_id):
    path = f"storage/memory/{user_id}.json"
    return json.load(open(path)) if os.path.exists(path) else []

def save_memory(user_id, memory):
    os.makedirs(f"storage/memory", exist_ok=True)
    json.dump(memory[-20:], open(f"storage/memory/{user_id}.json", "w"))

def log_chat(user_id, msg):
    os.makedirs("storage/logs", exist_ok=True)
    with open(f"storage/logs/{user_id}.txt", "a") as f:
        f.write(msg + "\\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hai! Aku siap nemenin kamu 24 jam 🤍\\nGunakan /persona untuk pilih karakter~")

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    audio_url = ttsmaker_speak(text)
    await update.message.reply_voice(audio_url) if audio_url else await update.message.reply_text("Gagal bikin suara 😢")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    result = convert_units(query)
    await update.message.reply_text(result)

async def persona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        new_p = " ".join(context.args)
        set_persona(update.effective_user.id, new_p)
        await update.message.reply_text(f"✅ Persona diganti jadi: {new_p}")
    else:
        current = get_persona(update.effective_user.id)
        await update.message.reply_text(f"Persona kamu sekarang:\\n\\n{current}")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_file(update)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    memory = load_memory(user_id)
    persona = get_persona(user_id)
    memory.append({"role": "system", "content": persona})
    memory.append({"role": "user", "content": message})
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": memory}
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"AI error: {str(e)}"
    memory.append({"role": "assistant", "content": reply})
    save_memory(user_id, memory)
    log_chat(user_id, f"{user_id}: {message}")
    log_chat(user_id, f"BOT: {reply}")
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("voice", voice))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("persona", persona))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

