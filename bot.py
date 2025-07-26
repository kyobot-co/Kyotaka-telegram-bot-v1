import logging
import time
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from commands.kick import kick
from commands.unban import unban
from commands.help_cmd import help_command
from commands.info import info
from commands.ttp import ttp
from commands.lirik import lirik
from commands.ass import ass
from commands.boobs import boobs
from commands.hboobs import hboobs
from commands.ipinfo import ipinfo
from commands.darkgen import darkgen
from commands.darkweather import darkweather
from commands.defdark import defdark
from commands.darkquote import darkquote
from commands.ping import ping
from commands.uptime import uptime
from commands.nsfw import nsfw
from commands.ai_kyo import ai_kyo
from commands.ban import ban
from commands.mute import mute
from commands.unmute import unmute
from commands.nightmode import nightmode
from commands.lock import lock
from commands.tagall import tagall

TOKEN = "TON_TOKEN"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Bienvenue dans DarkAI Bot.\nTape /help pour voir les commandes.")

async def auto_restart(app):
    while True:
        await asyncio.sleep(7200)
        logging.info("🔄 Redémarrage automatique")
        try:
            await app.shutdown()
            await app.initialize()
            await app.start()
        except Exception as e:
            logging.error(f"Erreur au redémarrage : {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.bot_data["start_time"] = time.time()

    handlers = [
        ("start", start),
        ("help", help_command),
        ("kick", kick),
        ("unban", unban),
        ("ban", ban),
        ("info", info),
        ("ipinfo", ipinfo),
        ("ttp", ttp),
        ("lirik", lirik),
        ("ass", ass),
        ("boobs", boobs),
        ("hboobs", hboobs),
        ("darkgen", darkgen),
        ("darkweather", darkweather),
        ("defdark", defdark),
        ("darkquote", darkquote),
        ("ping", ping),
        ("uptime", uptime),
        ("nsfw", nsfw),
        ("mute", mute),
        ("unmute", unmute),
        ("nightmode", nightmode),
        ("lock", lock),
        ("tagall", tagall)
    ]

    for cmd, func in handlers:
        app.add_handler(CommandHandler(cmd, func))

    app.add_handler(CommandHandler(["ai", "kyo"], ai_kyo))

    logging.info("✅ Bot prêt")
    asyncio.create_task(auto_restart(app))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())