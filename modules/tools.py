import os
from telegram import Update

admin_id = "7791283642"

def handle_tools(update: Update, context, text):
    if text.startswith("/reset"):
        from_user = update.message.from_user.id
        user_path = f"user_memory/{from_user}.json"
        if os.path.exists(user_path):
            os.remove(user_path)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Memory direset!")
        return True

    if text.startswith("/broadcast") and str(update.message.from_user.id) == admin_id:
        msg = text.replace("/broadcast", "").strip()
        for uid_file in os.listdir("user_memory"):
            uid = uid_file.replace(".json", "")
            try:
                context.bot.send_message(chat_id=int(uid), text=f"[Broadcast Admin]\n\n{msg}")
            except:
                pass
        return True

    if text.startswith("/model"):
        model = text.split(" ", 1)[-1]
        with open(".env", "r") as f:
            lines = f.readlines()
        with open(".env", "w") as f:
            for line in lines:
                if line.startswith("model="):
                    f.write(f"model={model}\n")
                else:
                    f.write(line)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Model diganti ke: `{model}`", parse_mode="Markdown")
        return True

    return False
