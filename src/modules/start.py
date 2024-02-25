from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

from src import app 

user_ban_counts = {}

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Bot started. Use /admin command to promote users to admin.")

@app.on_message(filters.command("admin"))
def admin(client, message):
    if len(message.command) == 2:
        user_id = message.command[1]
        try:

            client.promote_chat_member(message.chat.id, user_id, can_change_info=True, can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True, can_promote_members=False)
            message.reply_text("User promoted to admin successfully.")
        except Exception as e:
            message.reply_text(f"Error promoting user to admin: {e}")
    else:
        message.reply_text("Usage: /admin <user_id>")

@app.on_message(filters.text)
def handle_message(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id


    user_ban_counts[user_id] = user_ban_counts.get(user_id, 0) + 1

    if user_ban_counts[user_id] >= 3:
        try:

            client.promote_chat_member(chat_id, user_id, can_change_info=False, can_delete_messages=False, can_restrict_members=False, can_invite_users=False, can_pin_messages=False, can_promote_members=False)
            message.reply_text("User demoted due to excessive bans.")

            user_ban_counts[user_id] = 0
        except Exception as e:
            message.reply_text(f"Error demoting user: {e}")

app.run()
