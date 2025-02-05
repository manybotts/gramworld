# (©) iBOX TV

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, HEROKU_APP_URL
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    """Handles batch link creation from the DB Channel"""
    
    while True:
        try:
            first_message = await client.ask(
                text=(
                    "📥 **Batch Link Creation**\n\n"
                    "📌 **Step 1:** Forward the **first message** from your DB Channel **(with quotes)**\n"
                    "📌 Or send the **DB Channel Post link**\n\n"
                    "⏳ **Waiting for your input...**"
                ),
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(
                "❌ **Error:**\n\n"
                "🚫 This forwarded post **is not from my DB Channel**, or the **link is invalid**.\n"
                "🔄 Please try again!",
                quote=True
            )
            continue

    while True:
        try:
            second_message = await client.ask(
                text=(
                    "📥 **Batch Link Creation**\n\n"
                    "📌 **Step 2:** Forward the **last message** from your DB Channel **(with quotes)**\n"
                    "📌 Or send the **DB Channel Post link**\n\n"
                    "⏳ **Waiting for your input...**"
                ),
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(
                "❌ **Error:**\n\n"
                "🚫 This forwarded post **is not from my DB Channel**, or the **link is invalid**.\n"
                "🔄 Please try again!",
                quote=True
            )
            continue

    # Encode and generate batch link
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"{HEROKU_APP_URL}?start={base64_string}"

    # Inline button for sharing
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔗 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    await second_message.reply_text(
        f"✅ **Batch Link Created Successfully!**\n\n"
        f"🔗 **Access Link:** <code>{link}</code>\n\n"
        f"🔄 Share this link with others to grant access.",
        quote=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    """Handles single message link generation"""
    
    while True:
        try:
            channel_message = await client.ask(
                text=(
                    "📥 **Generate a Secure Link**\n\n"
                    "📌 Forward a **message from the DB Channel (with quotes)**\n"
                    "📌 Or send the **DB Channel Post link**\n\n"
                    "⏳ **Waiting for your input...**"
                ),
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply(
                "❌ **Error:**\n\n"
                "🚫 This forwarded post **is not from my DB Channel**, or the **link is invalid**.\n"
                "🔄 Please try again!",
                quote=True
            )
            continue

    # Encode and generate single message link
    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"{HEROKU_APP_URL}?start={base64_string}"

    # Inline button for sharing
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔗 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    await channel_message.reply_text(
        f"✅ **Your Secure Link is Ready!**\n\n"
        f"🔗 **Access Link:** <code>{link}</code>\n\n"
        f"🔄 Share this link to grant access.",
        quote=True,
        reply_markup=reply_markup
    )
