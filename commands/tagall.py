from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import asyncio

@Client.on_message(filters.command("tagall") & filters.group)
async def tagall(client: Client, message: Message):
    try:
        user = await message.chat.get_member(message.from_user.id)
        if user.status not in ("administrator", "creator"):
            return await message.reply("❌ Commande réservée aux admins.")

        await message.delete()

        members = []
        count = 0
        async for member in client.get_chat_members(message.chat.id):
            if not member.user.is_bot:
                if member.user.username:
                    members.append(f"@{member.user.username}")
                else:
                    members.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
                count += 1

        if count == 0:
            return await message.reply("❌ Aucun membre à taguer.")

        header = f"🏷 **Mention de tous les membres** ({count})\n\n"
        chunks = [members[i:i + 7] for i in range(0, len(members), 7)]

        for chunk in chunks:
            try:
                text = header + " ".join(chunk)
                if message.reply_to_message:
                    await client.send_message(
                        message.chat.id,
                        text,
                        reply_to_message_id=message.reply_to_message.message_id
                    )
                else:
                    await client.send_message(message.chat.id, text)
                await asyncio.sleep(5)
            except FloodWait as e:
                await asyncio.sleep(e.x + 2)
            except Exception:
                continue

    except Exception as e:
        await message.reply(f"⚠️ Erreur: {str(e)}")