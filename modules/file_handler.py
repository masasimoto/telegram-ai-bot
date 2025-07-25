from modules.file_reader import read_pdf
import os
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file_path = f"downloads/{doc.file_name}"
    os.makedirs("downloads", exist_ok=True)

    file = await context.bot.get_file(doc.file_id)
    await file.download_to_drive(file_path)

    ext = file_path.split(".")[-1].lower()
    result = ""

    if ext == "txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            result = f.read()

    elif ext == "pdf":
        result = read_pdf(file_path)

    elif ext == "csv":
        df = pd.read_csv(file_path)
        result = df.head(10).to_markdown()

    else:
        await update.message.reply_text("Format belum didukung 😔 (txt/pdf/csv saja)")
        return

    await update.message.reply_text(f"[Isi File Terdeteksi]\n\n{result[:4000]}")
