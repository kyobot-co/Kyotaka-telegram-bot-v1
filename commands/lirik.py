import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Utilisation : /lirik <artiste> - <titre>")
        return

    query = " ".join(context.args)
    if "-" not in query:
        await update.message.reply_text("⚠️ Format : /lirik <artiste> - <titre>")
        return

    artist, title = map(str.strip, query.split("-", 1))
    await update.message.reply_text("🔍 Recherche des paroles...")

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
            async with session.get(url) as resp:
                data = await resp.json()

                if "lyrics" not in data:
                    await update.message.reply_text("❌ Paroles non trouvées")
                    return

                lyrics = data["lyrics"]
                if len(lyrics) > 4000:
                    lyrics = lyrics[:3990] + "...\n\n(Paroles coupées)"

                response = f"🎵 <b>{title}</b> - <i>{artist}</i>\n\n{lyrics}"
                await update.message.reply_text(response, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Erreur : {str(e)}")
