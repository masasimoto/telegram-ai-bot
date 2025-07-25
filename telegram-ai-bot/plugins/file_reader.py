
import os
async def handle_file(update):
    file = await update.message.document.get_file()
    path = f"storage/{update.message.document.file_name}"
    await file.download_to_drive(path)
    with open(path, "r") as f:
        content = f.read()
    await update.message.reply_text(f"📄 Isi file:\n\n{content[:3000]}")

