import urllib.parse
import aiohttp
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

MAX_TELEGRAM_CHARS = 4000
API_BASE = "https://api.lyrics.ovh/v1/{artist}/{title}"

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text("Utilisation : /lirik <artiste> - <titre>")
        return

    query = " ".join(context.args)

    if "-" in query:
        artist, title = map(str.strip, query.split("-", 1))
    else:
        await update.effective_message.reply_text("⚠️ Donne l'artiste et le titre séparés par un '-'")
        return

    try:
        await update.effective_message.reply_text("🔍 Recherche des paroles...")

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            url = API_BASE.format(
                artist=urllib.parse.quote_plus(artist),
                title=urllib.parse.quote_plus(title)
            )

            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    lyrics = data.get("lyrics", "Paroles non trouvées")

                    if len(lyrics) > MAX_TELEGRAM_CHARS:
                        lyrics = lyrics[:MAX_TELEGRAM_CHARS] + "\n[...]"

                    response = f"🎵 <b>{title}</b> - <i>{artist}</i>"

                    await update.effective_message.reply_text(
                        f"{response}\n\n<pre>{lyrics}</pre>",
                        parse_mode="HTML"
                    )
                else:
                    await update.effective_message.reply_text("❌ Aucune parole trouvée")
    except asyncio.TimeoutError:
        await update.effective_message.reply_text("⌛ Temps d'attente dépassé")
    except Exception as e:
        await update.effective_message.reply_text(f"⚠️ Erreur : {str(e)}")