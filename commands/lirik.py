import aiohttp
import urllib.parse
from telegram import Update
from telegram.ext import ContextTypes

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
            search_url = f"https://api.genius.com/search?q={urllib.parse.quote_plus(query)}"
            async with session.get(search_url, headers=HEADERS) as resp:
                data = await resp.json()

                if resp.status != 200 or "response" not in data:
                    await update.message.reply_text("❌ Erreur lors de la recherche")
                    return

                hits = data["response"].get("hits", [])
                if not hits:
                    await update.message.reply_text("❌ Aucune chanson trouvée")
                    return

                song = hits[0]["result"]
                title = song["title"]
                artist = song["primary_artist"]["name"]
                song_url = song["url"]

                response = f"🎵 <b>{title}</b> - <i>{artist}</i>\n\n"
                response += f"📖 [Paroles ici]({song_url})"

                await update.message.reply_text(response, parse_mode="HTML", disable_web_page_preview=False)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Erreur : {str(e)}")
