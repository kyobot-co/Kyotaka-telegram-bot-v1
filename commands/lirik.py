import aiohttp
import urllib.parse
from telegram import Update
from telegram.ext import ContextTypes

GENIUS_API_URL = "https://api.genius.com/search?q={query}"
GENIUS_LYRICS_URL = "https://api.genius.com/songs/{id}"
GENIUS_API_KEY = "FqKltcvASxUTv1yXKpfswwyIuXDqzorhjZEdzs3RgTqG0pLfQrfkr57E9v4xdWhXuSzVf0wEtX7gzjnEOXFWjA"
HEADERS = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
MAX_TELEGRAM_CHARS = 4000

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Utilisation : /lirik <titre chanson>")
        return

    query = " ".join(context.args)
    await update.message.reply_text("🔍 Recherche des paroles...")

    try:
        async with aiohttp.ClientSession() as session:
            search_url = GENIUS_API_URL.format(query=urllib.parse.quote_plus(query))
            async with session.get(search_url, headers=HEADERS) as resp:
                if resp.status != 200:
                    await update.message.reply_text("❌ Erreur lors de la recherche")
                    return
                data = await resp.json()
                hits = data.get("response", {}).get("hits", [])
                if not hits:
                    await update.message.reply_text("❌ Aucune chanson trouvée")
                    return

                song_id = hits[0]["result"]["id"]
                title = hits[0]["result"]["title"]
                artist = hits[0]["result"]["primary_artist"]["name"]

            # maintenant récupérer les détails (malheureusement Genius ne donne pas direct lyrics via API)
            async with session.get(GENIUS_LYRICS_URL.format(id=song_id), headers=HEADERS) as resp:
                if resp.status != 200:
                    await update.message.reply_text("❌ Impossible de récupérer les détails")
                    return
                song_data = await resp.json()
                song_url = song_data.get("response", {}).get("song", {}).get("url")

                response = f"🎵 <b>{title}</b> - <i>{artist}</i>\n\n"
                response += f"📖 [Paroles sur Genius]({song_url})"

                await update.message.reply_text(response, parse_mode="HTML", disable_web_page_preview=False)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Erreur : {str(e)}")