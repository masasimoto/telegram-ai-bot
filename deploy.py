import os
import time

# Token & API key dari argumen
from sys import argv

if len(argv) < 3:
    print("❌ Usage: python deploy.py --token <TELEGRAM_TOKEN> --api_key <OPENROUTER_API_KEY>")
    exit()

telegram_token = argv[argv.index("--token") + 1]
openrouter_api_key = argv[argv.index("--api_key") + 1]

print("🚀 Railway Auto Deploy Started...")

# Simpan ke .env
with open(".env", "w") as f:
    f.write(f"telegram_token={telegram_token}\n")
    f.write(f"openrouter_api_key={openrouter_api_key}\n")

# Railway init + deploy
print("🔧 Inisialisasi Railway Project...")
os.system("railway init --yes")
time.sleep(2)
print("⬆️ Upload ke Railway...")
os.system("railway up")

print("✅ DONE! Bot kamu sudah dideploy ke Railway.")
