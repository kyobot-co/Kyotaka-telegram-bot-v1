from pyrogram import Client, filters
from pyrogram.enums import ChatPermissions
from pyrogram.types import Message

LOCKED_PERMS = {
    "links": {"invite_links": False},
    "photos": {"can_send_media_messages": False},
    "videos": {"can_send_media_messages": False},
    "stickers": {"can_send_other_messages": False},
    "all": {
        "can_send_messages": False,
        "can_send_media_messages": False,
        "can_send_other_messages": False,
        "can_add_web_page_previews": False,
    },
}

@Client.on_message(filters.command("lock") & filters.group)
async def lock(client: Client, message: Message):
    if not message.from_user or not message.from_user.id in [admin.user.id async for admin in message.chat.get_members(filter="administrators")]:
        return
    if len(message.command) < 2:
        await message.reply_text("Usage: /lock [links/photos/videos/stickers/all]")
        return
    typ = message.command[1].lower()
    if typ not in LOCKED_PERMS:
        await message.reply_text("Type invalide.")
        return
    await message.chat.set_permissions(ChatPermissions(**LOCKED_PERMS[typ]))
    await message.reply_text(f"{typ} verrouillé.")