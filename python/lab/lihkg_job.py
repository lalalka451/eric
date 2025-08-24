import re
import requests
from telethon import TelegramClient, errors
from telethon.tl.types import InputPeerChannel, InputPeerUser
import asyncio
import os
from dotenv import load_dotenv
import logging
from urllib.parse import urlparse
import uuid
import hashlib
import io
import sqlite3
import schedule
import time

from unicodedata import category

# ------------------------ Configuration ------------------------

proxies = {
    'http': '127.0.0.1:10809',
}


# Generate a random device ID
def generate_device_id():
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    # Convert the UUID to a string and encode it
    uuid_str = str(random_uuid).encode('utf-8')
    # Create a SHA1 hash of the UUID
    sha1_hash = hashlib.sha1(uuid_str).hexdigest()
    return sha1_hash


# Load environment variables
load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
destination_chat = 4569483129
category = 'job'
category_id = 14
# Define the URL to fetch media from
global_thread_id = 3793254
MEDIA_URL = f"https://lihkg.com/api_v2/thread/{global_thread_id}/media?include_link=0"
global_thread_title = ""


# ------------------------ Helper Functions ------------------------

def is_image(url):
    """Check if the URL points to an image (excluding GIFs)."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    parsed = urlparse(url)
    return any(parsed.path.lower().endswith(ext) for ext in image_extensions)


def is_gif(url):
    """Check if the URL points to a GIF."""
    return url.lower().endswith('.gif')


def is_youtube(url):
    """Check if the URL is a YouTube link."""
    parsed = urlparse(url)
    return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc


def is_video(url):
    """Check if the URL points to a video."""
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
    parsed = urlparse(url)
    return any(parsed.path.lower().endswith(ext) for ext in video_extensions)


async def send_photo(client, chat, url):
    """Download and send a photo to the specified Telegram chat."""
    try:
        # Download the image
        response = requests.get(url)
        response.raise_for_status()

        # Extract the image filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # Generate a unique filename if none is present
            filename = f"{uuid.uuid4()}.jpg"

        # Wrap the image bytes in a BytesIO object and provide the filename
        image_bytes = io.BytesIO(response.content)
        image_bytes.name = filename  # Important for Telegram to recognize the file type

        # Send the photo
        await client.send_file(
            chat,
            file=image_bytes,
            caption=f'`{global_thread_title}\n`https://lihkg.com/thread/`{global_thread_id}/\n{url}`',
            force_document=False,  # Ensure it's sent as a photo, not a document
            parse_mode='md'  # Enable Markdown parsing for backticks
        )
        print(f"Photo sent: {global_thread_title}\n{url}")
    except Exception as e:
        print(f"Failed to send photo {url}: {e}")

"""
Downloaded GIF: 4475791 bytes
GIF sent: https://na.cx/i/f7LDG8K.gif
Downloaded GIF: 10112531 bytes
GIF sent: https://na.cx/i/jhPYkR2.gif
Downloaded GIF: 4788948 bytes
GIF sent: https://na.cx/i/eKym2Kp.gif

slow

"""
async def send_gif(client, chat, url):
    """Download and send a GIF to the specified Telegram chat."""
    try:
        # Download the GIF
        response = requests.get(url)
        response.raise_for_status()

        print(f"Downloaded GIF: {len(response.content)} bytes")

        # Extract the GIF filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # Generate a unique filename if none is present
            filename = f"{uuid.uuid4()}.gif"

        # Wrap the GIF bytes in a BytesIO object and provide the filename
        gif_bytes = io.BytesIO(response.content)
        gif_bytes.name = filename  # Important for Telegram to recognize the file type

        # Send the GIF without a caption and without parse_mode
        await client.send_file(
            chat,
            file=gif_bytes,
            caption=f'`{global_thread_title}\n`https://lihkg.com/thread/`{global_thread_id}/\n{url}`',
            force_document=False
            # parse_mode='md'  # Remove parse_mode for now
        )
        print(f"GIF sent: {url}")
    except Exception as e:
        print(f"Failed to send GIF {url}: {e}")


async def send_message(client, chat, message):
    """Send a text message to the specified Telegram chat with caption."""
    try:
        # Prepare the caption with the global title and thread URL
        caption = f'{global_thread_title}\n`https://lihkg.com/thread/{global_thread_id}/`\n\n{message}'

        # Send the message with the caption
        await client.send_message(chat, caption, parse_mode='md')
        print(f"Message sent: {caption}")
    except Exception as e:
        print(f"Failed to send message '{message}': {e}")


# ... existing imports and helper functions ...
def get_headers():
    return {
        "referer": "https://lihkg.com/thread/3793310/page/1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "X-Li-Device-Type": "browser",
        "X-Li-Device": generate_device_id(),
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i",
        "Connection": "keep-alive",
        # Add the cookie here if needed
        # "Cookie": "your_cookie_here"
    }


# ------------------------ Database Functions ------------------------

def create_database():
    conn = sqlite3.connect(f'{category}_lihkg_media.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media
                 (thread_id INTEGER, url TEXT, UNIQUE(thread_id, url))''')
    conn.commit()
    conn.close()

def url_exists(thread_id, url):
    conn = sqlite3.connect(f'{category}_lihkg_media.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM media WHERE thread_id=? AND url=?", (thread_id, url))
    result = c.fetchone() is not None
    conn.close()
    return result

def insert_url(thread_id, url):
    conn = sqlite3.connect(f'{category}_lihkg_media.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO media (thread_id, url) VALUES (?, ?)", (thread_id, url))
        conn.commit()
    except sqlite3.IntegrityError:
        # URL already exists, do nothing
        pass
    conn.close()


async def process_thread(thread_id):
    global global_thread_id, global_thread_title
    global_thread_id = thread_id
    MEDIA_URL = f"https://lihkg.com/api_v2/thread/{global_thread_id}/media?include_link=0"

    media_urls = []
    # Fetch the media data from the API
    try:
        # Define the URLs
        url = MEDIA_URL
        title_url = f"https://lihkg.com/api_v2/thread/{global_thread_id}/page/1?order=reply_time"

        headers = get_headers()
        title_response = requests.get(title_url, headers=headers, proxies=proxies)
        title_response.raise_for_status()
        title = title_response.json()['response']['title']
        print(title,url)
        # Programmatically handle Unicode-encoded strings
        global_thread_title = title.encode('utf-8').decode('utf-8')

        # Make the GET request with proxy if needed
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()

        # Clean the response text and extract URLs
        clean_text = response.text.replace("\\", "")
        media_urls = re.findall('"url":"(.*?)"', clean_text)
        print(f"Extracted {len(media_urls)} media URLs.")
    except Exception as e:
        print(f"Failed to parse media data: {e}")
        return
    if not media_urls:
        print(f"No media URLs found for thread {global_thread_id}.")
        return
    # Initialize the Telegram client
    client = TelegramClient('auto_forward_session', api_id, api_hash)

    try:
        await client.start()
        print("Telegram client started successfully.")
    except errors.RPCError as e:
        print(f"Failed to start Telegram client: {e}")
        return

    # Get the destination chat entity
    try:
        dest_entity = await client.get_entity(destination_chat)
        print(f"Destination chat: {destination_chat}")
    except Exception as e:
        print(f"Failed to get destination chat '{destination_chat}': {e}")
        await client.disconnect()
        return


    # Iterate over each URL and send appropriately
    for url in media_urls:
        if not url_exists(thread_id, url):
            if is_image(url):
                await send_photo(client, dest_entity, url)
            elif is_youtube(url) or is_video(url):
                await send_message(client, dest_entity, url)
            else:
                print(f"Unrecognized media type for URL: {url}")
            
            # Insert the URL into the database after sending
            insert_url(thread_id, url)
        else:
            print(f"URL already processed: {url}")

    # Disconnect the client after processing
    await client.disconnect()
    print("Telegram client disconnected.")

# Modify the main function to be non-async
def main():
    asyncio.run(async_main())

# Rename the existing main function to async_main
async def async_main():
    # Create the database and table if they don't exist
    create_database()

    url = f"https://lihkg.com/api_v2/thread/category?cat_id={category_id}&page=1&count=60"
    headers = get_headers()
    response = requests.get(url, headers=headers, proxies=proxies)
    thread_ids = list(set(re.findall(r"thread_id': (\d+)", str(response.json()))))
    print(thread_ids)

    for thread_id in thread_ids:
        await process_thread(thread_id)


# ------------------------ Entry Point ------------------------

if __name__ == "__main__":
    main()
    # Schedule the main function to run every 15 minutes
    schedule.every(15).minutes.do(main)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)