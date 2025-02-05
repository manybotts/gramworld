# (©) iBOX TV - Auto Delete Handler

import asyncio

async def auto_delete_messages(client, chat_id, message_ids, delay=5):
    """
    Deletes messages after a specified delay.

    :param client: The bot client instance
    :param chat_id: The chat ID where messages were sent
    :param message_ids: A list of message IDs to delete
    :param delay: Time in seconds before deletion (default: 5 seconds)
    """
    await asyncio.sleep(delay)  # Wait before deleting
    for msg_id in message_ids:
        try:
            await client.delete_messages(chat_id, msg_id)
        except Exception as e:
            print(f"⚠️ Error deleting message {msg_id}: {e}")
