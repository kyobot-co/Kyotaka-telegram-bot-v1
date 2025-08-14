from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Réponds au message de la personne à débannir")
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Seuls les admins peuvent utiliser cette commande")
        return

    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        await context.bot.unban_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            only_if_banned=True
        )
        await update.message.reply_text(f"✅ {user.full_name} a été débanni du groupe")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return False
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    return any(admin.user.id == update.effective_user.id for admin in admins)

def add_unban_handler(application):
    application.add_handler(CommandHandler("unban", unban))