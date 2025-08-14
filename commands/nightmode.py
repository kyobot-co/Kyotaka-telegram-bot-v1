from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes, Application
from datetime import datetime, timedelta
import asyncio

nightmode_locks = {}

async def nightmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin uniquement")
    
    if chat_id in nightmode_locks:
        return await update.message.reply_text("🔒 Le groupe est déjà verrouillé")
    
    until_time = datetime.now() + timedelta(hours=5)
    perms = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    )
    
    try:
        await context.bot.set_chat_permissions(
            chat_id=chat_id,
            permissions=perms,
            until_date=until_time
        )
        nightmode_locks[chat_id] = True
        await update.message.reply_text("🌙 Mode nuit activé pour 5 heures")
        
        await asyncio.sleep(18000)  # 5 heures en secondes
        if chat_id in nightmode_locks:
            del nightmode_locks[chat_id]
            await context.bot.send_message(chat_id, "🌞 Mode nuit désactivé")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return False
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    return any(admin.user.id == update.effective_user.id for admin in admins)

def add_nightmode_handler(application: Application):
    application.add_handler(CommandHandler("nightmode", nightmode))