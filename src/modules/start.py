from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from src import app
import time
from pyrogram.errors import FloodWait

user_ban_counts = {}
admin_ban_counts = {}

@app.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply_text("Bot started. Use /admin command to promote users to admin.")

@app.on_message(filters.command("admin"))
async def admin(bot, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        try:
            await bot.promote_chat_member(
                message.chat.id,
                user_id,
                can_change_info=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False
            )
            await message.reply_text("User promoted to admin successfully.")
        except Exception as e:
            await message.reply_text(f"Error promoting user to admin: {e}")
    else:
        await message.reply_text("Usage: /admin <user_id>")

@app.on_message(filters.command("demote"))
async def demote(bot, message):
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            await bot.promote_chat_member(
                message.chat.id,
                user_id,
                can_manage_chat=False
            )
            await message.reply_text("Admin demoted successfully.")
        except Exception as e:
            await message.reply_text(f"Error demoting admin: {e}")
    else:
        await message.reply_text("Usage: /demote <user_id>")

@app.on_message(filters.command("kick"))
async def kick(bot, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            await bot.kick_chat_member(message.chat.id, user_id)
            await message.reply_text("User kicked successfully.")
        except Exception as e:
            await message.reply_text(f"Error kicking user: {e}")
    else:
        await message.reply_text("Reply to a user's message to kick them.")

@app.on_message(filters.command("ban"))
async def ban(bot, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            await bot.kick_chat_member(message.chat.id, user_id)
            await message.reply_text("User banned successfully.")
        except Exception as e:
            await message.reply_text(f"Error banning user: {e}")
    else:
        await message.reply_text("Reply to a user's message to ban them.")

@app.on_message(filters.command)
async def handle_message(bot, message):
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
            await bot.promote_chat_member(
                chat_id,
                user_id,
                can_manage_chat=False
            )
            await message.reply_text("User demoted due to excessive bans.")

            user_ban_counts[user_id]["count"] = 0
        except FloodWait as e:
            await message.reply_text(f"Error demoting user: {e}")
        except Exception as e:
            await message.reply_text(f"Unexpected error demoting user: {e}")

    # Admin demotion check
    if user_id in admin_ban_counts:
        if time.time() - admin_ban_counts[user_id]["last_ban"] > 3600:
            admin_ban_counts[user_id]["count"] = 0
        admin_ban_counts[user_id]["count"] += 1
        admin_ban_counts[user_id]["last_ban"] = time.time()

        if admin_ban_counts[user_id]["count"] >= 3:
            try:
                await bot.promote_chat_member(
                    chat_id,
                    user_id,
                    can_manage_chat=False
                )
                await message.reply_text("Admin demoted due to excessive bans.")

                admin_ban_counts[user_id]["count"] = 0
            except FloodWait as e:
                await message.reply_text(f"Error demoting admin: {e}")
            except Exception as e:
                await message.reply_text(f"Unexpected error demoting admin: {e}")
    else:
        admin_ban_counts[user_id] = {"count": 0, "last_ban": 0}
