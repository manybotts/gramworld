# (©) iBOX TV

import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    """Handles the bot start command"""
    
    user_id = message.from_user.id
    
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except:
            pass
    
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        decoded_string = await decode(base64_string)
        argument = decoded_string.split("-")

        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return

            ids = list(range(start, end + 1)) if start <= end else list(reversed(range(end, start + 1)))

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return

        temp_msg = await message.reply("⏳ **Fetching your files...** Please wait.")
        
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("❌ **An error occurred while retrieving your files.** Please try again.")
            return

        await temp_msg.delete()

        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "", filename=msg.document.file_name)
                       if CUSTOM_CAPTION and msg.document else msg.caption.html if msg.caption else "")

            reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup

            try:
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ℹ️ About", callback_data="about"),
                 InlineKeyboardButton("🎬 iBOX TV", url="https://t.me/iBOX_TV")]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username='@' + message.from_user.username if message.from_user.username else None,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return


# =====================================================================================##

WAIT_MSG = "⏳ **Processing...** Please wait."

REPLY_ERROR = "❌ **Incorrect Usage**\n\nUse this command as a **reply** to any **Telegram message**."

# =====================================================================================##


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    """Handles users who have not joined required channels"""
    
    buttons = [
        [
            InlineKeyboardButton(text="📢 Join Channel 1", url=client.invitelink),
            InlineKeyboardButton(text="🎥 Join Channel 2", url=client.invitelink2),
        ]
    ]
    
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="🔄 Try Again",
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username='@' + message.from_user.username if message.from_user.username else None,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    """Displays the number of users using the bot"""
    
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"📊 **Total Users:** `{len(users)}`")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    """Broadcasts messages to all users"""
    
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0

        pls_wait = await message.reply("📢 **Broadcasting Message...**\n\nThis might take some time.")

        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = (
            f"📢 **Broadcast Completed**\n\n"
            f"👥 **Total Users:** `{total}`\n"
            f"✅ **Successful:** `{successful}`\n"
            f"🚫 **Blocked Users:** `{blocked}`\n"
            f"🗑️ **Deleted Accounts:** `{deleted}`\n"
            f"⚠️ **Failed Deliveries:** `{unsuccessful}`"
        )

        return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
