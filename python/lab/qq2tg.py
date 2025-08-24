import asyncio
import websockets
import json
import logging
#'<img src="htt.*?"

logging.basicConfig(level=logging.INFO)

async def send_message(ws, message):
    await ws.send(json.dumps(message))
    logging.info(f"Sent: {message}")

async def receive_messages(ws):
    async for message in ws:
        data = json.loads(message)
        if data.get("type") == "message":
            user = data.get("user")
            content = data.get("content")
            logging.info(f"{user}: {content}")
        elif data.get("type") == "notification":
            notice = data.get("notice")
            logging.info(f"Notice: {notice}")
        # Handle other message types as needed

async def chat_client():
    websocket_url = "ws://localhost:3001"  # Replace with your chat server's WebSocket URL
    token = "71498134"  # Replace with your authentication token if needed

    while True:
        try:
            async with websockets.connect(websocket_url) as ws:
                # Authenticate if required
                auth_message = {"type": "authenticate", "token": token}
                # auth_message = {"type": "authenticate", "token": token}
                await send_message(ws, auth_message)

                # Send join message
                join_message = {"type": "join", "username": "YourName"}
                await send_message(ws, join_message)

                # Start receiving messages
                await receive_messages(ws)

        except (websockets.exceptions.ConnectionClosedError,
                websockets.exceptions.InvalidURI,
                websockets.exceptions.InvalidHandshake) as e:
            logging.error(f"Connection error: {e}")
            logging.info("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(chat_client())