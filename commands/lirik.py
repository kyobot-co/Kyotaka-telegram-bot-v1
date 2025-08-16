import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

async def lirik(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Utilisation : /lirik <titre ou artiste>")
        return

    query = " ".join(context.args)
    await update.message.reply_text("🔍 Recherche des paroles...")

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://some-random-api.com/lyrics?title={query}"
            async with session.get(url) as resp:
                data = await resp.json()

                if "lyrics" not in data:
                    await update.message.reply_text("❌ Paroles non trouvées")
                    return

                title = data.get("title", "Inconnu")
                artist = data.get("author", "Inconnu")
                lyrics = data["lyrics"]

                if len(lyrics) > 4000:
                    lyrics = lyrics[:3990] + "...\n\n(Paroles coupées)"

                response = f"🎵 <b>{title}</b> - <i>{artist}</i>\n\n{lyrics}"
                await update.message.reply_text(response, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Erreur : {str(e)}")
