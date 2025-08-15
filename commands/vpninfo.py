from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import re
import json
import base64
from datetime import datetime

async def vpninfo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        await update.message.reply_text("❌ Commande invalide")
        return

    config = update.message.text.split(' ', 1)[1] if len(update.message.text.split()) > 1 else None
    
    if not config:
        await update.message.reply_text("⚠️ Usage: /vpninfo <lien_config>")
        return

    response = ""
    try:
        if "vmess://" in config:
            vmess_data = base64.b64decode(config.split("vmess://")[1]).decode()
            vmess_json = json.loads(vmess_data)
            response += f"🌐 Host: `{vmess_json.get('add')}`\n"
            # ... (reprends le reste de ton code existant)
            
            await update.message.reply_text(response, parse_mode="Markdown")
            
        elif "ss://" in config:
            # ... (adaptation similaire pour Shadowsocks)
            
        elif "howdy://" in config:
            # ... (adaptation similaire pour Howdy)
            
        else:
            await update.message.reply_text("❌ Format non supporté (VMESS/SS/Howdy)")

    except Exception as error:
        await update.message.reply_text(f"❌ Erreur: {str(error)}")

def register_handlers(app):
    app.add_handler(CommandHandler("vpninfo", vpninfo_handler))
