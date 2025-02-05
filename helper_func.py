# (©) iBOX TV

import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, ADMINS
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait


async def is_subscribed(filter, client, update):
    """Checks if a user is subscribed to required channels."""
    if not FORCE_SUB_CHANNEL and not FORCE_SUB_CHANNEL2:
        return True

    user_id = update.from_user.id
    if user_id in ADMINS:
        return True

    try:
        member1 = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL, user_id=user_id)
        member2 = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL2, user_id=user_id)
    except UserNotParticipant:
        return False

    return all(
        m.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
        for m in [member1, member2]
    )


async def encode(string):
    """Encodes text to a URL-safe Base64 format."""
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


async def decode(base64_string):
    """Decodes a Base64 URL-safe string back to its original format."""
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string


async def get_messages(client, message_ids, chat_id):
    """Fetches messages from the DB channel and auto-deletes sent files after 5 seconds."""
    messages = []
    total_messages = 0

    while total_messages < len(message_ids):
        temp_ids = message_ids[total_messages:total_messages + 200]
        try:
            msgs = await client.get_messages(chat_id=client.db_channel.id, message_ids=temp_ids)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(chat_id=client.db_channel.id, message_ids=temp_ids)
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return None  # Return None if messages couldn't be retrieved

        total_messages += len(temp_ids)
        messages.extend(msgs)

    if not messages:
        return None  # If no messages were retrieved, return None

    sent_messages = []

    for msg in messages:
        try:
            # ✅ Corrected: Send files to the correct user chat_id
            sent_msg = await msg.copy(chat_id=chat_id)
            sent_messages.append(sent_msg)
        except Exception as e:
            print(f"Error sending message: {e}")

    # ✅ Auto-delete only if messages were successfully sent
    await asyncio.sleep(5)
    for sent_msg in sent_messages:
        try:
            await sent_msg.delete()
        except:
            pass

    return messages


async def get_message_id(client, message):
    """Extracts the message ID from a forwarded message or a Telegram link."""
    if message.forward_from_chat and message.forward_from_chat.id == client.db_channel.id:
        return message.forward_from_message_id
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    return 0


def get_readable_time(seconds: int) -> str:
    """Converts seconds into a readable time format like '1d:2h:3m:4s'."""
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    time_list.reverse()
    up_time = ":".join(f"{t}{s}" for t, s in zip(time_list, time_suffix_list[-len(time_list):]))
    return up_time


subscribed = filters.create(is_subscribed)
