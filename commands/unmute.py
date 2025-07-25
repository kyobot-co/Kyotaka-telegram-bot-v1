from telegram import ChatPermissions

async def unmute(update, context):
    if not update.message.reply_to_message:
        await update.message.reply_text("Réponds au message de la personne à unmute.")
        return

    user = update.message.reply_to_message.from_user
    chat = update.effective_chat
    bot = context.bot

    await bot.restrict_chat_member(
        chat_id=chat.id,
        user_id=user.id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False,
        ),
    )

    await update.message.reply_text(f"{user.full_name} peut maintenant parler.")

app.add_handler(CommandHandler("unmute", unmute))