import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

GENIUS_TOKEN = "FqKltcvASxUTv1yXKpfswwyIuXDqzorhjZEdzs3RgTqG0pLfQrfkr57E9v4xdWhXuSzVf0wEtX7gzjnEOXFWjA"
MAX_TELEGRAM_CHARS = 4000

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_message.reply_text("Utilisation : /lirik <titre chanson>")
        return

    query = " ".join(context.args)

    try:
        await update.effective_message.reply_text("🔍 Recherche des paroles...")

        headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            search_url = f"https://api.genius.com/search?q={query}"
            async with session.get(search_url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text("❌ Erreur lors de la recherche")
                    return
                data = await resp.json()
                hits = data.get("response", {}).get("hits", [])
                if not hits:
                    await update.effective_message.reply_text("❌ Aucun résultat trouvé")
                    return
                song = hits[0]["result"]
                title = song.get("title", query)
                artist = song.get("primary_artist", {}).get("name", "")
                lyrics_url = song.get("url")

            async with session.get(lyrics_url) as resp:
                if resp.status != 200:
                    await update.effective_message.reply_text("❌ Paroles introuvables")
                    return
                html = await resp.text()

        import re
        match = re.search(r'<div class="lyrics">.*?<p>(.*?)</p>', html, re.S)
        if match:
            lyrics = re.sub(r'<.*?>', '', match.group(1)).strip()
        else:
            lyrics = "Paroles non trouvées"

        if len(lyrics) > MAX_TELEGRAM_CHARS:
            lyrics = lyrics[:MAX_TELEGRAM_CHARS] + "\n[...]"

        response = f"🎵 <b>{title}</b> - <i>{artist}</i>\n\n<pre>{lyrics}</pre>"
        await update.effective_message.reply_text(response, parse_mode="HTML")

    except Exception as e:
        await update.effective_message.reply_text(f"⚠️ Erreur : {str(e)}")