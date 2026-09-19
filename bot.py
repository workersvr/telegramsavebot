import os import json from datetime import datetime, timezone
from telegram import Update from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
DATA_FILE = "users.json"
def load_users(): if not os.path.exists(DATA_FILE): return {}
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
except Exception:
    return {}
def save_users(users): with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(users, f, ensure_ascii=False, indent=2)
async def save_user(update: Update): user = update.effective_user
if not user:
    return

users = load_users()
user_id = str(user.id)

users[user_id] = {
    "id": user.id,
    "username": user.username,
    "name": user.full_name,
    "saved_at": datetime.now(timezone.utc).isoformat()
}

save_users(users)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): await save_user(update)
if update.effective_message:
    await update.effective_message.reply_text(
        "შენახული ხარ ✅"
    )
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE): users = load_users()
if not users:
    await update.message.reply_text("ჯერ არავინ არის შენახული.")
    return

lines = []

for user in users.values():
    username = (
        f"@{user['username']}"
        if user.get("username")
        else "username არ აქვს"
    )

    lines.append(
        f"{username}\n"
        f"სახელი: {user.get('name', '-')}\n"
        f"ID: {user['id']}\n"
    )

text = "შენახული მომხმარებლები:\n\n" + "\n".join(lines)

await update.message.reply_text(text[:4000])
def main(): token = os.environ.get("BOT_TOKEN")
if not token:
    raise RuntimeError("BOT_TOKEN არ არის მითითებული.")

app = Application.builder().token(token).build()

app.add_handler(CommandHandler("list", list_users))
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("Bot started...")
app.run_polling()
if name == "main": main()
