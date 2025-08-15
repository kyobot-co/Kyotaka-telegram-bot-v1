from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import edge_tts
import asyncio
import os

CHARACTER_VOICES = {
    "madara": "ja-JP-NanamiNeural",
    "sasuke": "ja-JP-KeitaNeural",
    "naruto": "ja-JP-DaichiNeural",
    "itachi": "ja-JP-NaokiNeural"
}

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("Format: /voice <texte> - <personnage>\nEx: /voice Salut sombre mortel - madara")
            return

        parts = " ".join(context.args).split("-", 1)
        if len(parts) != 2:
            await update.message.reply_text("Format invalide. Utilise: /voice <texte> - <personnage>")
            return

        text = parts[0].strip()
        character = parts[1].strip().lower()

        if character not in CHARACTER_VOICES:
            await update.message.reply_text(f"Personnage non supporté. Choisis parmi: {', '.join(CHARACTER_VOICES.keys())}")
            return

        voice = CHARACTER_VOICES[character]
        communicate = edge_tts.Communicate(text, voice)
        output_file = f"voice_{update.message.message_id}.mp3"
        
        await communicate.save(output_file)
        await update.message.reply_voice(voice=open(output_file, "rb"))
        os.remove(output_file)

    except Exception as e:
        await update.message.reply_text(f"Erreur: {str(e)}")
        if os.path.exists(output_file):
            os.remove(output_file)

def register_handlers(app):
    app.add_handler(CommandHandler("voice", voice_handler))