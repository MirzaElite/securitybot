import asyncio
import logging
import time

from pyrogram import Client, filters 
from pyrogram.errors import PeerIdInvalid, ChannelInvalid, FloodWait
from pyrogram.types import BotCommand

from config import API_ID, API_HASH, BOT_TOKEN
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

app = Client(
    "Eval",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

boot = time.time()
async def eval_bot():
    try:
        await app.start()
        print(1)
    except FloodWait as ex:
        LOGGER.warning(ex)
        await asyncio.sleep(ex.value)
    print(2)
asyncio.get_event_loop().run_until_complete(eval_bot())
