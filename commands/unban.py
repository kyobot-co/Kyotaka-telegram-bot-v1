from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes, CommandHandler
from datetime import datetime, timedelta

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérification admin
    if not update.effective_chat.get_member(update.effective_user.id).status in ['administrator', 'creator']:
        await update.message.reply_text("❌ Seuls les admins peuvent utiliser cette commande.")
        return
    
    # Vérification reply
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Réponds au message de l'utilisateur à unmute.")
        return

    try:
        user = update.message.reply_to_message.from_user
        chat = update.effective_chat
        
        # Rétablit TOUTES les permissions
        await context.bot.restrict_chat_member(
            chat.id,
            user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,  # Garde cette permission désactivée si voulu
                can_invite_users=True,
                can_pin_messages=False
            ),
            until_date=datetime.now() + timedelta(seconds=1)  # Contourne un bug Telegram
        )
        
        await update.message.reply_text(f"🔊 {user.full_name} a été unmute.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

def add_handler(application):
    application.add_handler(CommandHandler("unmute", unmute))
