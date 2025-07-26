from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message

@Client.on_message(filters.command("lock") & filters.group)
async def lock(client: Client, message: Message):
    if not message.from_user or not message.from_user.id in [admin.user.id async for admin in message.chat.get_members(filter="administrators")]:
        return
    if len(message.command) < 2:
        await message.reply_text("Usage: /lock [all/photos/videos/links/stickers]")
        return
    typ = message.command[1].lower()
    perms = {
        "all": ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False),
        "photos": ChatPermissions(can_send_media_messages=False),
        "videos": ChatPermissions(can_send_media_messages=False),
        "links": ChatPermissions(can_add_web_page_previews=False),
        "stickers": ChatPermissions(can_send_other_messages=False),
    }
    if typ not in perms:
        await message.reply_text("Type invalide.")
        return
    await message.chat.set_permissions(perms[typ])
    await message.reply_text(f"{typ} verrouillé.")