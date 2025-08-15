from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    help_image_url = "https://files.catbox.moe/7zi7fd.jpg"
    
    help_text = """
╔════════════════╗
       🧠 *DARK KYOTAKA HELP* 📱
╚════════════════╝

📱 *Commandes Mobile :*

┏━━━━━━━━━━━━━━━━┓
┃ /start ┃ Démarrer le bot
┃ /help  ┃ Aide mobile
┗━━━━━━━━━━━━━━━━┛

👮 *Admin*
┏━━━━━━━━━━━━━━━━┓
┃ /kick      ┃ Expulser
┃ /unban     ┃ Débannir
┃ /ban       ┃ Bannir
┃ /mute      ┃ Rendre muet
┃ /unmute    ┃ Réactiver
┃ /nightmode ┃ Mode nuit
┃ /lock      ┃ Verrouiller
┗━━━━━━━━━━━━━━━━┛

📡 *Réseau*
┏━━━━━━━━━━━━━━━━┓
┃ /ipinfo <ip> ┃ Infos IP
┗━━━━━━━━━━━━━━━━┛

🎵 *Média*
┏━━━━━━━━━━━━━━━━┓
┃ /lirik <titre> ┃ Paroles
┃ /ttp <texte>   ┃ Sticker texte
┗━━━━━━━━━━━━━━━━┛

🔞 *NSFW*
┏━━━━━━━━━━━━━━━━┓
┃ /nsfw   ┃ Menu
┃ /ass    ┃ 🍑
┃ /boobs  ┃ Aléatoire
┃ /hboobs ┃ HB content
┗━━━━━━━━━━━━━━━━┛

🎨 *Dark*
┏━━━━━━━━━━━━━━━━┓
┃ /darkgen <prompt> ┃ Génération
┃ /darkweather      ┃ Météo
┃ /darkquote        ┃ Citations
┗━━━━━━━━━━━━━━━━┛

📚 *Définitions*
┏━━━━━━━━━━━━━━━━┓
┃ /defdark <mot> ┃ Définition
┗━━━━━━━━━━━━━━━━┛

⚙️ *Divers*
┏━━━━━━━━━━━━━━━━┓
┃ /ping    ┃ Latence
┃ /uptime  ┃ Fonctionnement
┃ /info    ┃ Infos
┃ /ai      ┃ IA
┃ /tagall  ┃ Mentionner
┗━━━━━━━━━━━━━━━━┛
"""
    try:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=help_image_url,
            caption=help_text,
            parse_mode="Markdown"
        )
    except:
        await update.message.reply_text(help_text, parse_mode="Markdown")