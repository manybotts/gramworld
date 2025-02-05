# (©) iBOX TV

from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import asyncio
from datetime import datetime
from collections import defaultdict
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT

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
        self.pending_deletes = defaultdict(list)  # ✅ Queue for messages to delete

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(f"⚠️ Error: {e}")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"✅ Bot Running Successfully! Created by iBOX TV")
        self.username = usr_bot_me.username

        # ✅ Start background deletion task
        asyncio.create_task(self.process_delete_queue())

        # ✅ Web Server Setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("🚫 Bot Stopped.")

    async def send_temp_file(self, chat_id, msg):
        """✅ Sends a file and schedules it for auto-deletion after exactly 5 seconds"""
        try:
            sent_msg = await msg.copy(chat_id=chat_id)

            # ✅ Store message ID and the exact deletion time (current time + 5 sec)
            delete_time = datetime.now().timestamp() + 5  # Calculate future timestamp
            self.pending_deletes[chat_id].append((sent_msg.message_id, delete_time))

        except Exception as e:
            self.LOGGER(__name__).warning(f"⚠️ Error sending file: {e}")

    async def process_delete_queue(self):
        """✅ Background task that accurately deletes messages at the correct time"""
        while True:
            now = datetime.now().timestamp()
            for chat_id, messages in list(self.pending_deletes.items()):
                messages_to_delete = [
                    msg_id for msg_id, delete_time in messages if now >= delete_time
                ]

                if messages_to_delete:
                    try:
                        await self.delete_messages(chat_id, messages_to_delete)
                        self.pending_deletes[chat_id] = [
                            (msg_id, delete_time) for msg_id, delete_time in self.pending_deletes[chat_id]
                            if msg_id not in messages_to_delete
                        ]
                    except Exception as e:
                        self.LOGGER(__name__).warning(f"⚠️ Error deleting messages in chat {chat_id}: {e}")

            await asyncio.sleep(1)  # ✅ Check every second for accuracy
