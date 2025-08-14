from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio

@Client.on_message(filters.command("tagall") & filters.group)
async def tagall(client, message: Message):
    try:
        if not message.from_user:
            return
        
        user = await message.chat.get_member(message.from_user.id)
        if user.status not in ("administrator", "creator"):
            return await message.reply("❌ Admin only command.")
        
        await message.delete()
        
        members = []
        async for member in client.get_chat_members(message.chat.id):
            if not member.user.is_bot and member.user.username:
                members.append(f"@{member.user.username}")
            elif not member.user.is_bot:
                members.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
        
        chunks = [members[i:i + 5] for i in range(0, len(members), 5)]
        
        for chunk in chunks:
            try:
                await client.send_message(
                    message.chat.id,
                    " ".join(chunk),
                    reply_to_message_id=message.reply_to_message_id if message.reply_to_message else None
                )
                await asyncio.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                continue
                
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")