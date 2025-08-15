import logging
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from commands.kick import add_handler as add_kick_handler
from commands.unban import add_handler as add_unban_handler
from commands.help_cmd import add_handler as add_help_handler
from commands.info import add_handler as add_info_handler
from commands.ttp import add_handler as add_ttp_handler
from commands.lirik import add_handler as add_lirik_handler
from commands.ass import add_handler as add_ass_handler
from commands.boobs import add_handler as add_boobs_handler
from commands.hboobs import add_handler as add_hboobs_handler
from commands.ipinfo import add_handler as add_ipinfo_handler
from commands.darkgen import add_handler as add_darkgen_handler
from commands.darkweather import add_handler as add_darkweather_handler
from commands.defdark import add_handler as add_defdark_handler
from commands.darkquote import add_handler as add_darkquote_handler
from commands.ping import add_handler as add_ping_handler
from commands.uptime import add_handler as add_uptime_handler
from commands.nsfw import add_handler as add_nsfw_handler
from commands.ai_kyo import add_handler as add_ai_kyo_handler
from commands.ban import add_handler as add_ban_handler
from commands.mute import add_handler as add_mute_handler
from commands.unmute import add_handler as add_unmute_handler
from commands.nightmode import add_handler as add_nightmode_handler
from commands.lock import add_handler as add_lock_handler
from commands.tagall import add_handler as add_tagall_handler
from commands.welcome import add_handler as add_welcome_handler
from commands.vpninfo import add_handler as add_vpninfo_handler
from commands.voice import add_handler as add_voice_handler
import time
import os

TOKEN = os.getenv("TELEGRAM_TOKEN", "7640665785:AAHMvh2nZy9Gwa4K42rubSU_8QBtBekoWoc")
PORT = int(os.environ.get("PORT", 10000))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot Telegram DarkAI en ligne et actif 24/7"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Bienvenue dans DarkAI Bot.\nTape /help pour voir les commandes.")

async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.bot_data["start_time"] = time.time()

    add_kick_handler(application)
    add_unban_handler(application)
    add_help_handler(application)
    add_info_handler(application)
    add_ttp_handler(application)
    add_lirik_handler(application)
    add_ass_handler(application)
    add_boobs_handler(application)
    add_hboobs_handler(application)
    add_ipinfo_handler(application)
    add_darkgen_handler(application)
    add_darkweather_handler(application)
    add_defdark_handler(application)
    add_darkquote_handler(application)
    add_ping_handler(application)
    add_uptime_handler(application)
    add_nsfw_handler(application)
    add_ai_kyo_handler(application)
    add_ban_handler(application)
    add_mute_handler(application)
    add_unmute_handler(application)
    add_nightmode_handler(application)
    add_lock_handler(application)
    add_tagall_handler(application)
    add_vpninfo_handler(application)
    add_welcome_handler(application)
    add_voice_handler(application)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Bot démarré et en écoute...")

    while True:
        await asyncio.sleep(3600)

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    bot_thread = threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True)

    flask_thread.start()
    bot_thread.start()

    flask_thread.join()
    bot_thread.join()
