from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
import asyncio
import datetime

nightmode_active = {}

async def nightmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if not user or not user.id:
        return

    if not user.id in [admin.user.id for admin in await context.bot.get_chat_administrators(chat_id)]:
        return await update.message.reply_text("❌ Tu dois être admin pour activer ce mode.")

    if not context.args:
        return await update.message.reply_text("⏳ Utilise `/nightmode on` ou `/nightmode off`")

    cmd = context.args[0].lower()

    if cmd == "on":
        nightmode_active[chat_id] = True
        await update.message.reply_text("🌙 Mode nuit activé.\nLe groupe fermera à 22h et rouvrira à 6h.")
    elif cmd == "off":
        nightmode_active[chat_id] = False
        await update.message.reply_text("🌞 Mode nuit désactivé.")
    else:
        await update.message.reply_text("❗ Option inconnue. Utilise `on` ou `off`.")

async def nightmode_scheduler(app):
    while True:
        now = datetime.datetime.now().time()
        for chat_id, active in nightmode_active.items():
            if not active:
                continue

            if now.hour == 22 and now.minute == 0:
                perms = ChatPermissions(can_send_messages=False)
                await app.bot.set_chat_permissions(chat_id, permissions=perms)
                await app.bot.send_message(chat_id, "🌌 Le groupe est fermé pour la nuit. Réouverture à 6h.")
                await asyncio.sleep(60)
            elif now.hour == 6 and now.minute == 0:
                perms = ChatPermissions(can_send_messages=True)
                await app.bot.set_chat_permissions(chat_id, permissions=perms)
                await app.bot.send_message(chat_id, "🌅 Bonjour ! Le groupe est de nouveau ouvert.")
                await asyncio.sleep(60)
        await asyncio.sleep(30)