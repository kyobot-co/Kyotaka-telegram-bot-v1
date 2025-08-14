from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        return
    
    for member in update.message.new_chat_members:
        try:
            if member.is_bot:  
                continue
                
            user_name = member.full_name
            group_name = update.effective_chat.title
            
            
            photo = await context.bot.get_user_profile_photos(member.id, limit=1)
            
            welcome_msg = (
                f"🌑 *Bienvenue dans l'Ombre, {user_name}*\n\n"
                f"Tu pénètres dans *{group_name}*\n"
                f"Un lieu où seuls les vrais persistent...\n\n"
                f"© KYOTAKA SYSTEM"
            )
            
            if photo.photos:
                await update.effective_chat.send_photo(
                    photo=photo.photos[0][-1].file_id,
                    caption=welcome_msg,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.effective_chat.send_message(
                    text=welcome_msg,
                    parse_mode=ParseMode.MARKDOWN
                )
                
        except Exception:
            pass  

def add_handler(application):
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))