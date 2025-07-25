#!/data/data/com.termux/files/usr/bin/bash

echo "🔥 Update Termux & Install Paket..."
pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git unzip

echo "🐍 Setup Python environment..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Setup struktur direktori..."
mkdir -p storage/memory storage/logs modules

echo "🔐 Menulis file .env..."
cat <<EOT > .env
telegram_token=8188383319:AAEgbYSGu90EDpD-yTEg-4F60IdPofHC6rg
openrouter_api_key=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
model=deepseek/deepseek-chat-v3-0324:free
EOT

echo "📦 Menulis requirements.txt..."
cat <<EOT > requirements.txt
python-telegram-bot==20.7
openai
requests
python-dotenv
PyMuPDF
pypdf
pandas
EOT

echo "🧠 Menulis main.py..."
cat <<EOT > main.py
# KODE MAIN DISINI (AKAN GUA LANJUTKAN DI STEP BERIKUTNYA)
EOT

echo "✅ Setup selesai. Jalankan bot dengan:"
echo "     python main.py"
