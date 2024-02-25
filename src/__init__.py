import asyncio
import logging
import time

from pyrogram import Client
from pyrogram.types import BotCommand

from config import API_ID, API_HASH, BOT_TOKEN, LOG_ID

# Configure logging
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# Create the Pyrogram Client instance
app = Client(
    "Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

# Define the bot commands
bot_commands = [
    BotCommand("start", "Starts The Bot"),
    BotCommand("admin", "Promote the user")
]

async def start_bot():
    try:
        await app.start()
    except Exception as e:
        LOGGER.warning(f"Failed to start the bot: {e}")
        return
    
    LOGGER.info(f"Bot started as {app.me.first_name}")
    
    try:
        await app.send_message(
            chat_id=LOG_ID,
            text=f"<u><b>» {app.me.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{app.me.id}</code>\nɴᴀᴍᴇ : {app.me.first_name}\nᴜsᴇʀɴᴀᴍᴇ : @{app.me.username}"
        )
    except Exception as e:
        LOGGER.warning(f"Failed to send start message to log chat: {e}")
    
    try:
        await app.set_bot_commands(bot_commands)
    except Exception as e:
        LOGGER.warning(f"Failed to set bot commands: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
