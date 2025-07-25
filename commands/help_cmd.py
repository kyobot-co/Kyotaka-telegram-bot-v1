from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    help_text = """
🧠 *Commandes disponibles :*

/start – Démarrer le bot
/help – Afficher cette aide

👮 *Admin*
/kick – Expulser un membre
/unban – Débannir un utilisateur
/ban – Bannir un utilisateur
/mute – Rendre muet un membre
/unmute – Réactiver un membre
/nightmode – Activer/Désactiver le mode nuit du groupe
/lock – Verrouiller temporairement le groupe

📡 *Réseau*
/ipinfo <ip> – Obtenir des infos sur une adresse IP

🎵 *Média*
/lirik <titre> – Obtenir les paroles d’une chanson
/ttp <texte> – Générer un sticker texte

🔞 *NSFW*
/nsfw – Menu NSFW
/ass – Image NSFW de fesses 🍑
/boobs – Image NSFW aléatoire
/hboobs – Image NSFW hboobs

🎨 *Dark & Fun*
/darkgen <prompt> – Génère une image dark
/darkweather <ville> – Météo version dark
/darkquote – Citation dark aléatoire

📚 *Définitions*
/defdark <mot> – Définition automatique version dark

⚙️ *Divers*
/ping – Vérifier la latence du bot
/uptime – Durée de fonctionnement du bot
/info – Informations générales
/ai ou /kyo <question> – Pose une question à l’IA
/tagall – Mentionner tous les membres du groupe
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")