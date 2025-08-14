from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes, CommandHandler
from datetime import datetime, timedelta

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat.get_member(update.effective_user.id).status in ['administrator', 'creator']:
        await update.message.reply_text("❌ Seuls les admins peuvent utiliser cette commande.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Réponds au message de l'utilisateur à mute.")
        return

    try:
        user = update.message.reply_to_message.from_user
        chat = update.effective_chat
        duration = int(context.args[0]) if context.args else 1
        until_date = datetime.now() + timedelta(hours=duration)

        await context.bot.restrict_chat_member(
            chat.id,
            user.id,
            ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            ),
            until_date=until_date
        )

        await update.message.reply_text(f"🔇 {user.full_name} a été mute pour {duration} heure(s).")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

def add_handler(application):
    application.add_handler(CommandHandler("mute", mute))