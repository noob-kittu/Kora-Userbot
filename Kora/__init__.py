import os
import re
import logging
from logging import getLogger
from telethon import TelegramClient
from telethon.sessions import StringSession



logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

LOGGER = getLogger(__name__)


CMD_HELP = {}

# Telegram App KEY and HASH
API_KEY = 2191715
API_HASH = "f8f5367907ae63115bbdce3524b87671"

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", "")

# Logging channel/group ID configuration.
BOTLOG = int(os.environ.get("BOTLOG_CHATID", ""))

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = os.environ.get("PM_AUTO_BAN", "True")

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL", default=None)

# Default .alive logo
ALIVE_LOGO = os.environ.get("ALIVE_LOGO") or "https://telegra.ph/file/b8a7689c29e999c60292a.jpg"






if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("koraUserbot", API_KEY, API_HASH)
