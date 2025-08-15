import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from gtts import gTTS
from pydub import AudioSegment
import edge_tts
import asyncio

CHARACTER_VOICES = {
    "madara": "ja-JP-NanamiNeural",
    "sasuke": "ja-JP-KeitaNeural",
    "naruto": "ja-JP-DaichiNeural",
    "itachi": "ja-JP-NaokiNeural"
}

@Client.on_message(filters.command("voice"))
async def character_voice(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("Format: /voice <texte> - <personnage>\nEx: /voice Salut sombre mortel - madara")
            return

        parts = " ".join(message.command[1:]).split("-", 1)
        if len(parts) != 2:
            await message.reply_text("Format invalide. Utilise: /voice <texte> - <personnage>")
            return

        text = parts[0].strip()
        character = parts[1].strip().lower()

        if character not in CHARACTER_VOICES:
            await message.reply_text(f"Personnage non supporté. Choisis parmi: {', '.join(CHARACTER_VOICES.keys())}")
            return

        voice = CHARACTER_VOICES[character]
        communicate = edge_tts.Communicate(text, voice)
        output_file = f"voice_{message.id}.mp3"
        
        await communicate.save(output_file)
        await message.reply_voice(output_file)
        os.remove(output_file)

    except Exception as e:
        await message.reply_text(f"Erreur: {str(e)}")
        if os.path.exists(output_file):
            os.remove(output_file)

def add_voice_handler(client):
    client.add_handler(character_voice)