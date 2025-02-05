# (©) iBOX TV

import os
import logging
from logging.handlers import RotatingFileHandler

# =================== BOT CONFIGURATION =================== #

# Bot Username
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")

# Permanent Heroku App URL (For Redirection)
HEROKU_APP_URL = os.environ.get("HEROKU_APP_URL", "https://your-app.herokuapp.com")

# Telegram Bot Token (@BotFather)
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Telegram API Credentials (from my.telegram.org)
APP_ID = int(os.environ.get("APP_ID", "5166878"))
API_HASH = os.environ.get("API_HASH", "fdafb41f9a67f40e34a6c67f47730a92")

# Database Configuration
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "bot13")

# Channel & Owner Details
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001973418807"))
OWNER = os.environ.get("OWNER", "iBOXTVADS")
OWNER_ID = int(os.environ.get("OWNER_ID", "6124171612"))

# Bot Working Port
PORT = int(os.environ.get("PORT", "8030"))

# Bot Workers (for handling multiple requests)
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Force Subscription Channels (if enabled)
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002311266823"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002311266823"))

# Admins List
try:
    ADMINS = [OWNER_ID]  # Always include the owner as admin
    ADMINS.extend([int(x) for x in os.environ.get("ADMINS", "762308466").split()])
except ValueError:
    raise Exception("❌ ERROR: Your Admins list does not contain valid integers.")

# =================== BOT UI MESSAGES =================== #

# Welcome Message
START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b>👋 Hello {first},\n\n"
    "I am a file storage bot for iBOX TV 🎬. "
    "I help users store and retrieve files effortlessly using special links.</b>"
)

# Force Subscription Message
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "👋 Hello {first},\n\n"
    "<b>To continue using me, you must join our channels below 👇</b>\n"
    "📢 Join and then click **Reload** to access your requested file."
)

# Custom Caption for Forwarded Files (Optional)
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# File Protection (Prevents forwarding files outside the bot)
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False").lower() == "true"

# Disable Share Button for Channel Posts
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False").lower() == "true"

# Bot Stats Message
BOT_STATS_TEXT = "<b>📊 BOT UPTIME:</b>\n{uptime}"

# Unauthorized Access Response
USER_REPLY_TEXT = "🚫 **Permission Denied!** Only bot owners can execute this command."

# =================== LOGGING CONFIGURATION =================== #

LOG_FILE_NAME = "filesharingbot.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    """Returns a configured logger instance."""
    return logging.getLogger(name)
