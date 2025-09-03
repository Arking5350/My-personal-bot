import os
import json
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========= CONFIG =========
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL", None)  # optional
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
DATA_FILE = "files_db.json"

# ========= INIT =========
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ========= STORAGE =========
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ========= START =========
@app.on_message(filters.command("start"))
async def start(client, message):
    btn = [
        [InlineKeyboardButton("⚡ Help", callback_data="help")],
        [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{FORCE_CHANNEL}" if FORCE_CHANNEL else "https://t.me")]
    ]
    await message.reply_text(
        "👋 Hello! I am your bot.\nUse /help to see features.",
        reply_markup=InlineKeyboardMarkup(btn)
    )

# ========= HELP =========
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text("📖 Commands:\n/start - Welcome\n/help - This menu")

# ========= CALLBACK HANDLER =========
@app.on_callback_query()
async def callbacks(client, callback):
    if callback.data == "help":
        await callback.message.edit_text(
            "📖 Help Menu:\n/start - Start Bot\n/help - This help",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
            )
        )
    elif callback.data == "back":
        await callback.message.edit_text(
            "👋 Hello! I am your bot.\nUse /help to see features."
        )

# ========= RUN =========
print("✅ Bot started...")
app.run()
