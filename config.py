from os import getenv
from dotenv import load_dotenv

load_dotenv()

#Necessary Variables 
API_ID = int(getenv("API_ID", "29400566"))
API_HASH = getenv("API_HASH", "8fd30dc496aea7c14cf675f59b74ec6f")
BOT_TOKEN = getenv("BOT_TOKEN", "7124170275:AAFzQl25c2MVQLACM8DZz7tPOvU6RscnSrk") #Put your bot token here
