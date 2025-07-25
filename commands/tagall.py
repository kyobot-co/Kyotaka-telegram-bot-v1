from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio

@Client.on_message(filters.command("tagall") & filters.group)
async def tag_all(_, message: Message):
    if not message.from_user or not message.from_user.id:
        return
    user = await message.chat.get_member(message.from_user.id)
    if not user.status in ("administrator", "creator"):
        return await message.reply("Seuls les admins peuvent utiliser cette commande.")
    
    limit = 30 
    mentions = []
    async for member in message.chat.iter_members():
        if not member.user.is_bot:
            mentions.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
        if len(mentions) == limit:
            try:
                await message.reply(" ".join(mentions))
                await asyncio.sleep(2)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            mentions = []

    if mentions:
        await message.reply(" ".join(mentions))