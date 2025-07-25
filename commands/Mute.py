from telegram import ChatPermissions
from telegram.ext import CommandHandler
from datetime import timedelta, datetime

async def mute(update, context):
    if not update.message.reply_to_message:
        await update.message.reply_text("Réponds au message de la personne à mute.")
        return
    user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    bot = context.bot
    try:
        duration = int(context.args[0])
    except (IndexError, ValueError):
        duration = 60
    until_date = datetime.utcnow() + timedelta(hours=duration)
    await bot.restrict_chat_member(
        chat_id=chat.id,
        user_id=user.id,
        permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
        ),
        until_date=until_date
    )
    await update.message.reply_text(f"{user.full_name} est mute pour {duration} heure(s).")

app.add_handler(CommandHandler("mute", mute))