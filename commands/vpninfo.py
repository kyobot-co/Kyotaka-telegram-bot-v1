import re
import json
import base64
from urllib.parse import urlparse
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("vpninfo"))
async def decode_vpn(client: Client, message: Message):
    try:
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("❌ Réponds à un message contenant une config VPN")

        config_text = message.reply_to_message.text
        result = "🔍 **Analyse VPN**\n\n"

        if "vmess://" in config_text:
            vmess_data = base64.b64decode(config_text.split("vmess://")[1]).decode()
            vmess_json = json.loads(vmess_data)
            result += "⚡ **Type**: VMESS\n"
            result += f"🌐 **Host**: `{vmess_json.get('add')}`\n"
            result += f"🚪 **Port**: `{vmess_json.get('port')}`\n"
            result += f"🆔 **User ID**: `{vmess_json.get('id')}`\n"
            result += f"🛡️ **Security**: `{vmess_json.get('scy', 'auto')}`\n"
            if "ps" in vmess_json:
                result += f"📝 **Description**: `{vmess_json['ps']}`\n"
                date_str = re.search(r"\d{4}-\d{2}-\d{2}", vmess_json['ps'])
                if date_str:
                    exp_date = datetime.strptime(date_str.group(), "%Y-%m-%d")
                    remaining = (exp_date - datetime.now()).days
                    result += f"⏳ **Expire dans**: {remaining} jours\n"
            result += "\n🔐 **Config complète**:\n```json\n"
            result += json.dumps(vmess_json, indent=2)

        elif "ss://" in config_text:
            ss_data = base64.b64decode(config_text.split("ss://")[1].split("#")[0]).decode()
            method, password = ss_data.split("@")[0].split(":")
            server, port = ss_data.split("@")[1].split(":")
            result += "⚡ **Type**: Shadowsocks\n"
            result += f"🔑 **Méthode**: `{method}`\n"
            result += f"🌐 **Server**: `{server}`\n"
            result += f"🚪 **Port**: `{port}`\n"
            result += "\n🔐 **Config complète**:\n```json\n"
            result += json.dumps({"server": server, "port": port, "method": method}, indent=2)

        elif "howdy://" in config_text:
            howdy_data = base64.b64decode(config_text.split("howdy://")[1]).decode()
            howdy_json = json.loads(howdy_data)
            result += "🤠 **Type**: Howdy VPN\n"
            result += f"🌐 **Server**: `{howdy_json.get('server')}`\n"
            result += f"👤 **Username**: `{howdy_json.get('username')}`\n"
            result += f"🔑 **Password**: `{howdy_json.get('password')}`\n"
            result += f"🚪 **Port**: `{howdy_json.get('port')}`\n"
            result += f"🔒 **SNI**: `{howdy_json.get('sni')}`\n"
            result += "\n🔐 **Config complète**:\n```json\n"
            result += json.dumps(howdy_json, indent=2)

        else:
            return await message.reply("❌ Format non supporté (VMESS/SS/Howdy)")

        result += "```"
        await message.reply(result, parse_mode="markdown")

    except Exception as e:
        await message.reply(f"❌ Erreur: {str(e)}")