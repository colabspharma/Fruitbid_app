#!/bin/zsh
# =========================================================
# 🧹 normalize_folder.sh — Clean + Launch FruitBidApp
# =========================================================

echo "🧹 Cleaning up FruitBidApp folder..."

# Disable history expansion (!)
setopt NO_BANG_HIST

# Remove junk/temp files
rm -f .DS_Store
rm -f *.pyc
rm -f *~
rm -f ._*
rm -f .!*.db
rm -f *.db-journal
rm -f app_web_backup.py
rm -f *_backup.py
find . -type d -name "__pycache__" -exec rm -rf {} +

# Restore normal shell behavior
unsetopt NO_BANG_HIST

echo "✅ Cleanup complete!"

# =========================================================
# 🚀 Launch Streamlit App
# =========================================================
APP_DIR="/Users/km/Desktop/c_bid/fruitbidapp"
echo "📂 Moving into $APP_DIR..."
cd "$APP_DIR" || { echo "❌ Could not enter app directory"; exit 1; }

echo "🌿 Activating virtual environment..."
source /Users/km/Desktop/c_bid/venv/bin/activate

echo "🚀 Launching FruitBid App..."
# Run Streamlit and capture the local URL
streamlit run app_web.py > streamlit.log 2>&1 &

sleep 3  # give Streamlit a moment to start

# Try to find the URL in the log
URL=$(grep -o 'http://localhost:[0-9]*' streamlit.log | head -1)

if [ -n "$URL" ]; then
  echo "🌐 App is running at: $URL"
  echo "Opening in browser..."
  open "$URL"
else
  echo "⚠️ Could not detect Streamlit URL automatically."
  echo "Please check the logs: streamlit.log"
fi
