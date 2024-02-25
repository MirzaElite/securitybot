from pyrogram import Client, filters
from pyrogram.types import Chat

import time
from pyrogram.errors import FloodWait
api_id = "29400566"
api_hash= "8fd30dc496aea7c14cf675f59b74ec6f"  
bot_token = "7124170275:AAFzQl25c2MVQLACM8DZz7tPOvU6RscnSrk"  

app = Client("sex", api_id, api_hash, bot_token)

user_ban_counts = {}

@app.on_message(filters.command("start"))
def start(bot: app, message):
    message.reply_text("Bot started. Use /admin command to promote users to admin.")

@app.on_message(filters.command("admin"))
def admin(bot: app, message):
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            bot.promote_chat_member(message.chat.id, user_id, can_change_info=True, can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True, can_promote_members=False)
            message.reply_text("User promoted to admin successfully.")
        except Exception as e:
            message.reply_text(f"Error promoting user to admin: {e}")
    else:
        message.reply_text("Usage: /admin <user_id>")

@app.on_message(filters.text)
def handle_message(bot: app, message):
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
            bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_delete_messages=False, can_restrict_members=False, can_invite_users=False, can_pin_messages=False, can_promote_members=False)
            message.reply_text("User demoted due to excessive bans.")

            user_ban_counts[user_id]["count"] = 0
        except FloodWait as e:
            message.reply_text(f"Error demoting user: {e}")
        except Exception as e:
            message.reply_text(f"Unexpected error demoting user: {e}")

app.run()
print("Bhenkelode Hogya Start Tera Bot")
