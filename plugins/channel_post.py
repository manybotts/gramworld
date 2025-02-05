# (©) iBOX TV

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, HEROKU_APP_URL, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    """Handles posts from admins and generates shareable links"""
    
    reply_text = await message.reply_text("⏳ **Generating your secure link...**", quote=True)
    
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(f"Error: {e}")
        await reply_text.edit_text("❌ **Something went wrong! Please try again.**")
        return

    # Encoding message ID for security
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"{HEROKU_APP_URL}?start={base64_string}"

    # Inline buttons for sharing the generated URL
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔗 Copy Link", url=f"https://telegram.me/share/url?url={link}")
            ]
        ]
    )

    # Sending the generated link in a clean format
    await reply_text.edit(
        f"✅ **Your link has been generated!**\n\n"
        f"🔗 **Secure Link:** `{link}`\n\n"
        f"🔄 Share this link to give access.",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    # Update the post message with a share button (if enabled)
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    """Handles new posts from the configured channel and adds a share button"""

    if DISABLE_CHANNEL_BUTTON:
        return

    # Encoding message ID for security
    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"{HEROKU_APP_URL}?start={base64_string}"

    # Inline button for sharing the generated URL
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔗 Share Post", url=f"https://telegram.me/share/url?url={link}")
            ]
        ]
    )

    # Updating the post with the share button
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(f"Error: {e}")
        pass
