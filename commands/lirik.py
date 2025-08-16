import aiohttp
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
import urllib.parse

MAX_TELEGRAM_CHARS = 4000
API_BASE = "https://api.vagalume.com.br/search.php?art={artist}&mus={title}&extra=lyrics"

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or "-" not in " ".join(context.args):
        await update.effective_message.reply_text("Utilisation : /lirik <artiste> - <titre>")
        return

    artist, title = map(str.strip, " ".join(context.args).split("-", 1))
    await update.effective_message.reply_text("🔍 Recherche des paroles...")

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            url = API_BASE.format(
                artist=urllib.parse.quote_plus(artist),
                title=urllib.parse.quote_plus(title)
            )
            async with session.get(url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text("❌ Aucune parole trouvée")
                    return
                data = await resp.json()
                mus = data.get("mus")
                if not mus:
                    await update.effective_message.reply_text("❌ Aucune parole trouvée")
                    return
                lyrics = mus[0].get("text", "")
                if not lyrics:
                    await update.effective_message.reply_text("❌ Aucune parole trouvée")
                    return
                if len(lyrics) > MAX_TELEGRAM_CHARS:
                    lyrics = lyrics[:MAX_TELEGRAM_CHARS] + "\n[...]"
                response = f"🎵 <b>{title}</b> - <i>{artist}</i>"
                await update.effective_message.reply_text(f"{response}\n\n<pre>{lyrics}</pre>", parse_mode="HTML")
    except asyncio.TimeoutError:
        await update.effective_message.reply_text("⌛ Temps d'attente dépassé")
    except Exception as e:
        await update.effective_message.reply_text(f"⚠️ Erreur : {str(e)}")