from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message
from datetime import datetime, timedelta

@Client.on_message(filters.command("lock") & filters.group)
async def lock(client: Client, message: Message):
    try:
        if not message.from_user:
            return
        
        user = await message.chat.get_member(message.from_user.id)
        if user.status not in ("administrator", "creator"):
            return await message.reply("❌ Admin only command.")

        args = message.command
        if len(args) < 2:
            return await message.reply("Usage: /lock [type] [hours]\nTypes: all|media|polls|invites|pin|changeinfo|webprev|stickers|gifs|games|inline")

        lock_type = args[1].lower()
        hours = int(args[2]) if len(args) > 2 and args[2].isdigit() else 2
        until_date = datetime.now() + timedelta(hours=hours)

        perms = ChatPermissions(
            can_send_messages=lock_type != "all",
            can_send_media_messages=lock_type not in ["all", "media"],
            can_send_polls=lock_type != "polls",
            can_send_other_messages=lock_type not in ["all", "stickers", "gifs", "games", "inline"],
            can_add_web_page_previews=lock_type != "webprev",
            can_change_info=lock_type != "changeinfo",
            can_invite_users=lock_type != "invites",
            can_pin_messages=lock_type != "pin"
        )

        await client.set_chat_permissions(
            message.chat.id,
            permissions=perms,
            until_date=until_date
        )

        await message.reply(f"🔒 {lock_type.capitalize()} locked for {hours} hour(s)")
        
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")