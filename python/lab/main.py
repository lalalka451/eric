from telethon import TelegramClient, events
import asyncio

# Replace these with your own values
api_id = '8170577'
api_hash = 'f3dd83af2dea7bd46764163dde8d0b4e'
source_chat = '1843180756'      # e.g., 'sourcechannel' or -1001234567890
destination_chat = '2147469030'  # e.g., 'destinationchannel' or -1009876543210

# Create the client and connect
client = TelegramClient('auto_forward_session', api_id, api_hash)

@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    try:
        # Forward the incoming message to the destination chat
        await event.message.forward_to(destination_chat)
        print(f"Forwarded message from {source_chat} to {destination_chat}")
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    await client.start()
    print("Auto-forwarding bot is running...")
    await client.run_until_disconnected()

asyncio.run(main())