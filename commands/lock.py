from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions

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

UNLOCKED_PERMS = {
    "links": {"invite_links": True},
    "photos": {"can_send_media_messages": True},
    "videos": {"can_send_media_messages": True},
    "stickers": {"can_send_other_messages": True},
    "all": {
        "can_send_messages": True,
        "can_send_media_messages": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
    },
}

@Client.on_message(filters.command("lock") & filters.group)
async def lock_cmd(client, m: Message):
    admins = [member.user.id async for member in client.get_chat_members(m.chat.id, filter="administrators")]
    if not m.from_user or m.from_user.id not in admins:
        return await m.reply_text("Tu n'es pas admin.")
    if len(m.command) < 2:
        return await m.reply_text("Usage: /lock [links/photos/videos/stickers/all]")
    typ = m.command[1].lower()
    if typ not in LOCKED_PERMS:
        return await m.reply_text("Type invalide.")
    await client.set_chat_permissions(m.chat.id, ChatPermissions(**LOCKED_PERMS[typ]))
    await m.reply_text(f"🔒 {typ} verrouillé.")

@Client.on_message(filters.command("unlock") & filters.group)
async def unlock_cmd(client, m: Message):
    admins = [member.user.id async for member in client.get_chat_members(m.chat.id, filter="administrators")]
    if not m.from_user or m.from_user.id not in admins:
        return await m.reply_text("Tu n'es pas admin.")
    if len(m.command) < 2:
        return await m.reply_text("Usage: /unlock [links/photos/videos/stickers/all]")
    typ = m.command[1].lower()
    if typ not in UNLOCKED_PERMS:
        return await m.reply_text("Type invalide.")
    await client.set_chat_permissions(m.chat.id, ChatPermissions(**UNLOCKED_PERMS[typ]))
    await m.reply_text(f"🔓 {typ} déverrouillé.")