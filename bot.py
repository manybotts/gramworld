# (©) iBOX TV

from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT
import asyncio
from auto_delete import auto_delete_messages  # ✅ Import auto-delete function without circular import

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # ✅ Setup Force Subscription Channels
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as e:
                self.LOGGER(__name__).warning(f"⚠️ Error: {e}")
                self.LOGGER(__name__).warning("❌ Force Sub Channel Error! Bot Stopped.")
                sys.exit()

        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as e:
                self.LOGGER(__name__).warning(f"⚠️ Error: {e}")
                self.LOGGER(__name__).warning("❌ Force Sub Channel 2 Error! Bot Stopped.")
                sys.exit()

        # ✅ Verify DB Channel Access
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(f"⚠️ Error: {e}")
            self.LOGGER(__name__).warning(f"❌ Ensure bot is an admin in the DB Channel {CHANNEL_ID}")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"✅ Bot Running Successfully! Created by iBOX TV")
        self.username = usr_bot_me.username

        # ✅ Web Server Setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("🚫 Bot Stopped.")

    async def send_temp_file(self, chat_id, msg):
        """✅ Sends a file and auto-deletes it after 5 seconds"""
        sent_msg = await msg.copy(chat_id=chat_id)
        await auto_delete_messages(self, chat_id, [sent_msg.id], delay=5)  # ✅ Auto-delete applied
