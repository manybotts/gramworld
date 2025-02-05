# (©) iBOX TV - UI & UX Improved Version

from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import asyncio
from datetime import datetime
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="iBOX_Bot",
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

        self.LOGGER(__name__).info("🚀 Starting iBOX TV Bot... Please wait!")
        
        # ✅ Force Subscription Setup
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
                self.LOGGER(__name__).info(f"📢 Force Sub Channel 1 Linked: {link}")
            except Exception as e:
                self.LOGGER(__name__).error(f"❌ Failed to fetch Force Sub Channel 1: {e}")
                self.LOGGER(__name__).info("📌 Make sure the bot is an admin and has 'Invite via Link' permission.")
                sys.exit()

        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
                self.LOGGER(__name__).info(f"📢 Force Sub Channel 2 Linked: {link}")
            except Exception as e:
                self.LOGGER(__name__).error(f"❌ Failed to fetch Force Sub Channel 2: {e}")
                self.LOGGER(__name__).info("📌 Make sure the bot is an admin and has 'Invite via Link' permission.")
                sys.exit()

        # ✅ Database Channel Setup
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="✅ iBOX TV Bot Test Message.")
            await test.delete()
            self.LOGGER(__name__).info(f"📦 Connected to Database Channel: {db_channel.title}")
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ ERROR: Cannot connect to DB Channel {CHANNEL_ID}. Details: {e}")
            self.LOGGER(__name__).info("📌 Make sure the bot is an admin in the channel!")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"✅ iBOX TV Bot is LIVE and Ready to Serve!")
        self.username = usr_bot_me.username

        # ✅ Web Server Setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("🔴 iBOX TV Bot Stopped. See you again!")
