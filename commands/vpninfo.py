from telegram import Update
from telegram.ext import ContextTypes
import re
import json
import base64
from datetime import datetime

async def vpninfo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
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
            response += f"🚪 Port: `{vmess_json.get('port')}`\n"
            response += f"🆔 User ID: `{vmess_json.get('id')}`\n"
            response += f"🛡️ Security: `{vmess_json.get('scy', 'auto')}`\n"
            if "ps" in vmess_json:
                response += f"📝 Description: `{vmess_json['ps']}`\n"
                date_match = re.search(r"\d{4}-\d{2}-\d{2}", vmess_json['ps'])
                if date_match:
                    expiry_date = datetime.strptime(date_match.group(), "%Y-%m-%d")
                    days_left = (expiry_date - datetime.now()).days
                    response += f"⏳ Expire dans: {days_left} jours\n"
            response += "\n🔐 Config complète:\n```json\n"
            response += json.dumps(vmess_json, indent=2)
            response += "```"

        elif "ss://" in config:
            ss_data = base64.b64decode(config.split("ss://")[1].split("#")[0]).decode()
            method, password = ss_data.split("@")[0].split(":")
            server, port = ss_data.split("@")[1].split(":")
            response += "⚡ Type: Shadowsocks\n"
            response += f"🔑 Méthode: `{method}`\n"
            response += f"🌐 Server: `{server}`\n"
            response += f"🚪 Port: `{port}`\n"
            response += "\n🔐 Config complète:\n```json\n"
            response += json.dumps({"server": server, "port": port, "method": method}, indent=2)
            response += "```"

        elif "howdy://" in config:
            howdy_data = base64.b64decode(config.split("howdy://")[1]).decode()
            howdy_json = json.loads(howdy_data)
            response += "🤠 Type: Howdy VPN\n"
            response += f"🌐 Server: `{howdy_json.get('server')}`\n"
            response += f"👤 Username: `{howdy_json.get('username')}`\n"
            response += f"🔑 Password: `{howdy_json.get('password')}`\n"
            response += f"🚪 Port: `{howdy_json.get('port')}`\n"
            response += f"🔒 SNI: `{howdy_json.get('sni')}`\n"
            response += "\n🔐 Config complète:\n```json\n"
            response += json.dumps(howdy_json, indent=2)
            response += "```"

        else:
            await update.message.reply_text("❌ Format non supporté (VMESS/SS/Howdy)")
            return

        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as error:
        await update.message.reply_text(f"❌ Erreur: {str(error)}")