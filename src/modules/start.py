from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '7124170275:AAFzQl25c2MVQLACM8DZz7tPOvU6RscnSrk'

# Dictionary to store user ban counts
user_ban_counts = {}

app = Client("my_bot", bot_token=bot_token)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Bot started. Use /admin command to promote users to admin.")

@app.on_message(filters.command("admin"))
def admin(client, message):
    if len(message.command) == 2:
        user_id = message.command[1]
        try:
            # Promote user to admin
            client.promote_chat_member(message.chat.id, user_id, can_change_info=True, can_delete_messages=True, can_restrict_members=True, can_invite_users=True, can_pin_messages=True, can_promote_members=False)
            message.reply_text("User promoted to admin successfully.")
        except Exception as e:
            message.reply_text(f"Error promoting user to admin: {e}")
    else:
        message.reply_text("Usage: /admin <user_id>")

@app.on_message(filters.text & ~filters.command)
def handle_message(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Increment user ban count
    user_ban_counts[user_id] = user_ban_counts.get(user_id, 0) + 1

    # If user has banned 3 users within 1 hour, demote them
    if user_ban_counts[user_id] >= 3:
        try:
            # Demote user
            client.promote_chat_member(chat_id, user_id, can_change_info=False, can_delete_messages=False, can_restrict_members=False, can_invite_users=False, can_pin_messages=False, can_promote_members=False)
            message.reply_text("User demoted due to excessive bans.")
            # Reset ban count
            user_ban_counts[user_id] = 0
        except Exception as e:
            message.reply_text(f"Error demoting user: {e}")

app.run()
