from telethon.sync import TelegramClient, events
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace these with your own values
api_id = 8170577  # Ensure this is an integer
# IMPORTANT: Replace with your actual api_hash obtained from my.telegram.org
api_hash = 'YOUR_NEW_API_HASH'

# Create a list of tuples with source and destination chat IDs
# Messages from the first ID in a tuple will be forwarded to the second ID.
# If a source ID appears multiple times, it will forward to each corresponding destination.
chat_pairs = [
    (-4934532253, -4802881170), # forward1 -> forward2
    (-4934532253, -4669831220), # forward1 -> 日记
]

# Create and start the client
# 'wanted_eric' is the session file name
client = TelegramClient('wanted_eric', api_id, api_hash)

# Define the event handler for new messages
# It listens for messages in any chat ID listed as a source in chat_pairs
@client.on(events.NewMessage(chats=[pair[0] for pair in chat_pairs]))
async def handler(event):
    """Forwards incoming messages from source chats to their configured destination chats."""
    try:
        source_chat_id = event.chat_id
        # Find ALL destination chat IDs for this source chat
        # Use a list comprehension to get all matching destinations
        destination_chat_ids = [dest for src, dest in chat_pairs if src == source_chat_id]

        logger.info(f"Message received from {source_chat_id}. Will attempt to forward to: {destination_chat_ids}")

        if destination_chat_ids:
            # Loop through each found destination and forward the message
            for destination_chat_id in destination_chat_ids:
                if destination_chat_id == -4669831220:
                    # forward *as a copy* (no forward header or author tag)
                    await client.forward_messages(
                        entity=destination_chat_id,
                        messages=event.message.id,
                        from_peer=source_chat_id,
                        drop_author=True  # <= key line
                    )
                    logger.info(f"Copied message from {source_chat_id} to {destination_chat_id} (header removed)")
                else:
                    # normal forward keeps the header
                    await event.message.forward_to(destination_chat_id)
                    logger.info(f"Forwarded message from {source_chat_id} to {destination_chat_id}")
        else:
             # This case technically shouldn't be hit if the event came from a chat in chat_pairs' sources,
             # but it's good practice for robustness.
            logger.warning(f"No destination chats found for source chat {source_chat_id}")

    except Exception as e:
        logger.error(f"Error forwarding message from chat {event.chat_id}: {e}") # Added chat_id to error log

def main():
    """Starts the Telegram client and runs the auto-forwarding logic."""
    try:
        logger.info("Starting Telegram client...")
        client.start()
        logger.info("Telegram client started successfully.")
        logger.info("Auto-forwarding bot is running...")

        # Fetch and log information about the source and destination chats for verification
        # Note: This loop runs once at startup
        for source_chat_id, destination_chat_id in chat_pairs:
            try:
                source_entity = client.get_entity(source_chat_id)
                dest_entity = client.get_entity(destination_chat_id)
                logger.info(f"Configured Pair - Source: {source_entity.title} (ID: {source_entity.id}) -> Destination: {dest_entity.title} (ID: {dest_entity.id})")
            except Exception as e:
                 logger.warning(f"Could not fetch entity for chat IDs {source_chat_id} or {destination_chat_id}: {e}")


        logger.info("Bot is now listening for new messages...")
        # Run the client until you manually stop it (e.g., with Ctrl+C)
        client.run_until_disconnected()

    except Exception as e:
        logger.error(f"An unexpected error occurred during bot execution: {e}")
    finally:
        if client.is_connected(): # Check if client is connected before disconnecting
            client.disconnect()
            logger.info("Telegram client disconnected.")
        else:
             logger.info("Telegram client was not connected.")


if __name__ == "__main__":
    main()