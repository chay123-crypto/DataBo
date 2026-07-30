import os
import json
import threading
from agent import run_agent
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram import Update
import asyncio
import traceback
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
print("DEBUG KEY:", os.environ.get("CEREBRAS_API_KEY"))
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
web_app = Flask(__name__)

@web_app.route('/')
def health():
    return "Bot is running", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    chat_id = update.message.chat_id
    history = context.chat_data.setdefault("history", [])
    history.append({'role': 'user', 'content': message})
    try:
        result_json = await run_agent(history)
    except Exception as e:
        traceback.print_exc()
        result_json = json.dumps({"answer": None, "log_url": "", "error": str(e)})
    history.append({"role": "assistant", "content": result_json})
    await update.message.reply_text(result_json)

def main():
    # start the web server in a background thread first
    threading.Thread(target=run_web, daemon=True).start()

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
