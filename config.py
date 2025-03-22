import os
import logging
from logging.handlers import RotatingFileHandler

# =================== BOT CONFIGURATION =================== #

# Bot Username
BOT_USERNAME = os.environ.get("BOT_USERNAME", "default_bot_username")  # Not strictly required

# Permanent Heroku App URL (For Redirection)
HEROKU_APP_URL = os.environ.get("HEROKU_APP_URL", "") #  Not strictly required

# Telegram Bot Token (@Botfather)
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN") # Now required

# Telegram API Credentials (from my.telegram.org)
APP_ID = os.environ.get("APP_ID")  # Get as string initially, will convert later
API_HASH = os.environ.get("API_HASH") # Now required

# Database Configuration
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "bot13")

# Channel & Owner Details
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001973418807"))
OWNER = os.environ.get("OWNER", "iBOXTVADS")
OWNER_ID = int(os.environ.get("OWNER_ID", "6124171612"))

# Bot Working Port
PORT = int(os.environ.get("PORT", "8030"))  # Not strictly required for basic functionality

# Bot Workers (for handling multiple requests)
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Force Subscription Channels (if enabled)
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002311266823"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002311266823"))

# Tutorial Video Message ID
TUTORIAL_VIDEO_ID = os.environ.get("TUTORIAL_VIDEO_ID", "0")  # Get as string, default "0"


# Admins List
try:
    ADMINS = [OWNER_ID]  # Always include the owner as admin
    ADMINS.extend([int(x) for x in os.environ.get("ADMINS", "762308466").split()])
except ValueError:
    raise Exception("❌ ERROR: Your Admins list does not contain valid integers.")

# =================== BOT UI MESSAGES =================== #

# Start Message (Optimized for TV Show Fetching)
START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b>👋 Hello, {first}!</b>\n\n"
    "I am <b>iBOX TV File Share Bot</b>. 📺\n"
    "Click on the <b>Season</b> or <b>Episode</b> buttons sent by the admin to fetch your favorite TV shows! 🎬"
)

# Force Subscription Message (Fixed Spacing & "Try Again" Button)
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "👋 <b>Hello, {first},</b>\n\n"
    "<i>To continue using me, you must join our channels below.</i> 👇\n\n"
    "📢 <b>Join, then tap 'Try Again' to access your requested file.</b>"
)

# Custom Caption for Forwarded Files (Optional)
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# File Protection (Prevents forwarding files outside the bot)
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False").lower() == "true" else False

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

# --- Validation and Conversions ---
if not TG_BOT_TOKEN:
    raise ValueError("TG_BOT_TOKEN environment variable is not set.")
if not API_HASH:
    raise ValueError("API_HASH environment variable is not set.")
if not APP_ID:
    raise ValueError("APP_ID environment variable is not set.")
if not TUTORIAL_VIDEO_ID or TUTORIAL_VIDEO_ID == "0":
    raise ValueError("TUTORIAL_VIDEO_ID is not set or is set to '0'.")

try:
    APP_ID = int(APP_ID)  # Convert to integer *after* checking if it exists
except (ValueError, TypeError) as e:
    raise ValueError(f"APP_ID environment variable must be a valid integer. Error: {e}")

try:
    TUTORIAL_VIDEO_ID = int(TUTORIAL_VIDEO_ID)  # Convert to int *after* check
except (ValueError, TypeError) as e:
    raise ValueError(f"TUTORIAL_VIDEO_ID environment variable must be a valid integer. Error: {e}")

print("config.py loaded successfully")
print(f"TUTORIAL_VIDEO_ID: {TUTORIAL_VIDEO_ID}, Type: {type(TUTORIAL_VIDEO_ID)}")

def LOGGER(name: str) -> logging.Logger:
    """Returns a configured logger instance."""
    return logging.getLogger(name)
