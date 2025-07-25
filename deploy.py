import os, time
from sys import argv

if len(argv) < 3:
    print("❌ Usage: python deploy.py --token <TELEGRAM_TOKEN> --api_key <OPENROUTER_API_KEY>")
    exit()

telegram_token = argv[argv.index("--token") + 1]
openrouter_api_key = argv[argv.index("--api_key") + 1]

print("🚀 Generating .env and pushing to GitHub repo...")

# Generate .env content
with open(".env", "w") as f:
    f.write(f"telegram_token={telegram_token}\n")
    f.write(f"openrouter_api_key={openrouter_api_key}\n")

# Inisialisasi git dan push
os.system("git init")
os.system("git remote remove origin 2>/dev/null")
os.system("git remote add origin https://github.com/masasimoto/telegram-ai-bot.git")
os.system("git add .")
os.system("git commit -m 'Auto deploy from Termux 🚀'")
os.system("git branch -M main")
os.system("git push -f origin main")

print("✅ Sukses push ke GitHub. Railway akan auto-deploy.")
