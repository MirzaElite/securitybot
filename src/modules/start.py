from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges
from src import app
import time
from pyrogram.errors import FloodWait

user_ban_counts = {}

@app.on_message(filters.command("start"))
async def start(bot: app, message):
    await message.reply_text("Bot started. Use /admin command to promote users to admin.")

@app.on_message(filters.command("admin"))
async def admin(bot: app, message):
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            await bot.promote_chat_member(message.chat.id, user_id, privileges=ChatPrivileges(can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True, can_promote_members=False))
            await message.reply_text("User promoted to admin successfully.")
        except Exception as e:
            await message.reply_text(f"Error promoting user to admin: {e}")
    else:
        await message.reply_text("Usage: /admin <user_id>")

@app.on_message(filters.command)
async def handle_message(bot: app, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id not in user_ban_counts:
        user_ban_counts[user_id] = {"count": 0, "last_ban": 0}

    if time.time() - user_ban_counts[user_id]["last_ban"] > 3600:  # Reset ban count if last ban was more than 1 hour ago
        user_ban_counts[user_id]["count"] = 0

    user_ban_counts[user_id]["count"] += 1
    user_ban_counts[user_id]["last_ban"] = time.time()

    if user_ban_counts[user_id]["count"] >= 3:
        try:
            await bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_delete_messages=False, can_restrict_members=False, can_invite_users=False, can_pin_messages=False, can_promote_members=False)
            await message.reply_text("User demoted due to excessive bans.")

            user_ban_counts[user_id]["count"] = 0
        except FloodWait as e:
            await message.reply_text(f"Error demoting user: {e}")
        except Exception as e:
            await message.reply_text(f"Unexpected error demoting user: {e}")
