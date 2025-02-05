# (©) Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=(
                "🎬 <b>Welcome to iBOX TV!</b>\n\n"
                "🌟 **Your Ultimate Movie & TV Show Destination**\n"
                "🔹 Stay updated with the **latest movies & series**\n"
                "🔹 Search and discover content **effortlessly**\n"
                "🔹 Get **exclusive updates & recommendations**\n\n"
                "💡 **Our Community & Updates:**\n"
                "📢 <b>Owner:</b> <a href='tg://user?id={OWNER_ID}'>iBOX TV</a>\n"
                "📺 <b>Updates:</b> <a href='https://t.me/iBOX_TV'>iBOX TV</a>\n"
                "🎥 <b>Movies Channel:</b> <a href='https://t.me/iBOXTVMOVIES'>iBOX TV FAMILY</a>\n"
                "🌍 <b>Community:</b> <a href='https://t.me/+Cze71ohH6B82ZTZk'>Search Movies</a>\n"
                "🔎 <b>Movie Search Chat:</b> <a href='https://t.me/+ESw_v3HM6nRlNTQ0'>iBOX TV</a>\n\n"
                "✨ **Enjoy a seamless movie experience with us!** 🍿🎥"
            ).format(OWNER_ID=OWNER_ID),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🎬 Explore Movies", url="https://t.me/iBOXTVMOVIES"),
                        InlineKeyboardButton("📢 Latest Updates", url="https://t.me/iBOX_TV")
                    ],
                    [
                        InlineKeyboardButton("❌ Close", callback_data="close")
                    ]
                ]
            )
        )

    elif data == "close":
        # Smooth exit with a confirmation message
        await query.message.edit_text(
            "❌ <b>Closed.</b>\n\n"
            "Need help? Use /help anytime! 🚀",
            disable_web_page_preview=True
        )

# ⋗ Telegram - @ibox_tv

# 🎉 Credit: Github - @ibox_tv
# 📢 Special Thanks to iBOX TV for support!
# 🛠 For any issues, contact @ibox_tv | Community: @ibox_tv
