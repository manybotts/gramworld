from auto_delete import auto_delete_messages  # Import the auto-delete function

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    """Handles deep links and deletes sent files after 5 seconds"""

    user_id = message.from_user.id
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

        message_ids = []

        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "", filename=msg.document.file_name)
                       if CUSTOM_CAPTION and msg.document else msg.caption.html if msg.caption else "")

            reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup

            try:
                sent_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )

                message_ids.append(sent_msg.id)  # Store message ID for deletion

            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )

                message_ids.append(sent_msg.id)  # Store message ID for deletion

            except:
                pass

        # ✅ Trigger auto-delete after sending the files
        await auto_delete_messages(client, message.chat.id, message_ids, delay=5)

        return
