from telethon import TelegramClient, events, errors
from telethon.tl.types import Channel, User, Chat
import asyncio
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
source_chat = os.getenv('SOURCE_CHAT')
destination_chat = os.getenv('DESTINATION_CHAT')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the client and connect
client = TelegramClient('4chan_session', api_id, api_hash)
#+85292172500
#+85253402943
#+85292031488
async def get_all_chats():
    chats = []
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, (Channel, User, Chat)):
            entity_type = type(dialog.entity).__name__
            chats.append({
                'id': dialog.id,
                'name': dialog.name,
                'type': entity_type
            })
    return chats

async def validate_chat(chat_id):
    try:
        entity = await client.get_entity(chat_id)
        return entity
    except ValueError as e:
        logger.error(f"Invalid chat ID: {chat_id}. Error: {e}")
        return None

@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    try:
        # Forward the incoming message to the destination chat
        await client.forward_messages(destination_chat, event.message)
        logger.info(f"Forwarded message from {source_chat} to {destination_chat}")
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
    except errors.RPCError as rpc_err:
        logger.error(f"RPC Error: {rpc_err}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

async def main():
    await client.start()
    
    # Get all chats
    logger.info("Fetching all chats:")
    chats = await get_all_chats()
    
    # Display all chats
    for chat in chats:
        logger.info(f"{chat['type']}: {chat['name']} (ID: {chat['id']})")
    
    # Validate source and destination chats
    source_entity = await validate_chat(source_chat)
    destination_entity = await validate_chat(destination_chat)
    
    if not source_entity or not destination_entity:
        logger.error("Invalid source or destination chat. Please update your .env file with correct chat IDs.")
        return
    
    logger.info(f"Source chat: {source_entity.id} ({source_entity.title if hasattr(source_entity, 'title') else 'User'})")
    logger.info(f"Destination chat: {destination_entity.id} ({destination_entity.title if hasattr(destination_entity, 'title') else 'User'})")
    
    logger.info("Auto-forwarding bot is ready to run. Press Ctrl+C to stop.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())