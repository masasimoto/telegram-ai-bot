from telegram import Update
from telegram.ext import ContextTypes
import os
import requests

async def show_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    model = os.environ.get("model", "default")
    await update.message.reply_text(f"🤖 Model aktif sekarang:\n`{model}`", parse_mode="Markdown")

async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Format salah. Contoh:\n`/setmodel mistralai/mistral-7b-instruct`", parse_mode="Markdown")
        return

    new_model = " ".join(context.args)
    os.environ["model"] = new_model

    with open(".env", "r") as f:
        lines = f.readlines()
    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("model="):
                f.write(f"model={new_model}\n")
            else:
                f.write(line)

    await update.message.reply_text(f"✅ Model berhasil diganti ke:\n`{new_model}`", parse_mode="Markdown")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api_key = os.environ.get("api_key", "")[:20] + "..." if os.environ.get("api_key") else "❌ Tidak ada API key"
    model = os.environ.get("model", "❌ Tidak ditemukan")
    
    headers = {
        "Authorization": f"Bearer {os.environ.get('api_key')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Halo"}]
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
        if "choices" in r.json():
            status = "✅ Berhasil respons"
        else:
            status = f"⚠️ Error: {r.json().get('message')}"
    except Exception as e:
        status = f"❌ Error: {str(e)}"

    await update.message.reply_text(f"""🔍 STATUS BOT:

🔑 API key: {api_key}
🧠 Model: `{model}`
📡 Respons: {status}
""", parse_mode="Markdown")
