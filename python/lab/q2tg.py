import asyncio
import re
import json
import os
import subprocess
import requests
import schedule
import time

import websockets
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.sync import TelegramClient

# Assuming you have a `db_handler` class in `rss_send.py`
from rss_send import db_handler  # Make sure this module is correctly implemented

# Load environment variables from a .env file
load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Telegram configuration
TELEGRAM_SESSION = 'justforfun_session'
TELEGRAM_CHANNEL_ID = 2238825797  # Updated as per your specification

# Database configuration
DB_NAME = 'qq'
DB_COLLECTION = 'media'

# WebSocket configuration
WEBSOCKET_URI = "ws://127.0.0.1:3001"

# Directory to save media files
MEDIA_DIR = 'media'
os.makedirs(MEDIA_DIR, exist_ok=True)


def download_file(url, path):
    """
    Downloads a file from a URL and saves it to the specified path.
    """
    # try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes
    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded: {path}")
    return True
    # except requests.RequestException as e:
    #     print(f"Failed to download {url}: {e}")
    #     return False


def merge_audio_video(video_path, audio_path, output_path):
    """
    Merges video and audio files into a single output file using FFmpeg.
    """
    try:
        # FFmpeg command to merge without re-encoding
        command = [
            r"C:\Users\fueqq\Downloads\eric\qq chat export 0.2.0\lib\ffmpeg-lgpl\ffmpeg.exe",
            '-i', video_path,
            '-i', audio_path,
            '-c', 'copy',
            output_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Merged video and audio into: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        return False





def send_photo_to_telegram(client, image_url, caption):
    """
    Sends an image from a URL to the specified Telegram chat.
    Downloads the image before sending.
    """
    # try:
    image_filename = os.path.basename(image_url)
    image_path = os.path.join(MEDIA_DIR, image_filename)

    # Download the image
    if download_file(image_url, image_path):
        client.send_file(TELEGRAM_CHANNEL_ID, image_path, caption=caption)
        print(f"Sent to Telegram: {image_path}")
        # Optionally, delete the image after sending
        os.remove(image_path)
        print(f"Deleted temporary image: {image_path}")
        return True
    else:
        print(f"Failed to download image: {image_url}")
        return False
    # except Exception as e:
        # print(f"Failed to send image to Telegram: {e}")
        # return False


def cleanup_files(*files):
    """
    Deletes the specified files from the filesystem.
    """
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted temporary file: {file}")
        except OSError as e:
            print(f"Error deleting file {file}: {e}")


def process_post(post, client, db):
    """
    Processes a single post: downloads media, merges audio and video if necessary, sends to Telegram.
    """
    try:
        # Example structure of 'post', adjust according to actual data
        caption = post.get('title', 'No Title')
        image_url = post.get('url')

        if image_url and image_url.endswith('.jpg'):
            # Check if the post is already processed
            # if db.th({'url': image_url}):
            #     print(f"Post already processed: {image_url}")
            #     return

            # Send photo to Telegram
            if send_photo_to_telegram(client, image_url, caption):
                print('ok')
                # Save to database to avoid reprocessing
                # db.insert({'url': image_url, 'caption': caption})
    except Exception as e:
        print(f"Error processing post: {e}")


async def connect_to_websocket(db):
    """
    Connects to the WebSocket and processes incoming messages.
    """
    async with websockets.connect(WEBSOCKET_URI) as websocket:
        print(f"Connected to {WEBSOCKET_URI}")

        async for message in websocket:
            try:
                received_message = json.loads(message)
                print(f"< {received_message}")

                # Extract image URLs using regex
                img_urls = re.findall(r',url=(https://.*?\.jpg)\]', str(received_message))
                print('iamurl', img_urls)
                for img_url in img_urls:
                    post = {
                        'url': img_url,
                        'title': received_message.get('title', 'No Title')
                        # Adjust according to actual message structure
                    }
                    # process_post(post, client, db)
            except json.JSONDecodeError:
                print("Received a non-JSON message.")
            except Exception as e:
                print(f"Error handling message: {e}")


def main():
    """
    Main function to connect to Telegram and start WebSocket processing.
    """
    # Initialize the database handler
    db = db_handler(DB_NAME, DB_COLLECTION)
    db.create_database()

    # # Connect to Telegram
    # try:
    #     client = TelegramClient(TELEGRAM_SESSION, api_id, api_hash)
    #     client.start()  # This will handle the authorization process
    #     print("Connected to Telegram.")
    # except Exception as e:
    #     print(f"Failed to connect Telegram client: {e}")
    #     return

    # Start the WebSocket connection
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(connect_to_websocket(db))
    except KeyboardInterrupt:
        print("WebSocket connection closed.")
    finally:
        # client.disconnect()
        print("Disconnected from Telegram.")


if __name__ == "__main__":
    main()

    # If you want to run the main function periodically, uncomment the following lines:
    # schedule.every(10).minutes.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)