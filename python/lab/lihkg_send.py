import random
import re
import requests
from telethon.sync import TelegramClient
from PIL import Image
from telethon.errors import RPCError
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
import codecs

# Generate a random device ID
def generate_device_id():
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    # Convert the UUID to a string and encode it
    uuid_str = str(random_uuid).encode('utf-8')
    # Create a SHA1 hash of the UUID
    sha1_hash = hashlib.sha1(uuid_str).hexdigest()
    return sha1_hash

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

def get_headers():
    return {
        "referer": f"https://lihkg.com/thread/{random.randint(22, 66666)}/page/1",
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

def create_database(category_name):
    conn = sqlite3.connect(f'{category_name}_lihkg_media.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media
                 (thread_id INTEGER, url TEXT, UNIQUE(thread_id, url))''')
    conn.commit()
    conn.close()

def url_exists(category_name, thread_id, url):
    conn = sqlite3.connect(f'{category_name}_lihkg_media.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM media WHERE thread_id=? AND url=?", (thread_id, url))
    result = c.fetchone() is not None
    conn.close()
    return result

def thread_Id_exists(category_name, thread_id):
    conn = sqlite3.connect(f'{category_name}_lihkg_media.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM media WHERE thread_id="+thread_id)
    result = c.fetchone() is not None
    conn.close()
    return result

def insert_url(category_name, thread_id, url):
    conn = sqlite3.connect(f'{category_name}_lihkg_media.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO media (thread_id, url) VALUES (?, ?)", (thread_id, url))
        conn.commit()
    except sqlite3.IntegrityError:
        # URL already exists, do nothing
        pass
    conn.close()

# ------------------------ Sending Functions ------------------------


def send_photo(client, chat, url, thread_title, thread_id):
    """Download and send a photo to the specified Telegram chat."""
    try:
        # Download the image
        response = requests.get(url, proxies={}, timeout=6)
        response.raise_for_status()

        # Extract the image filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # Generate a unique filename if none is present
            filename = f"{uuid.uuid4()}.jpg"

        # Wrap the image bytes in a BytesIO object
        image_bytes = io.BytesIO(response.content)

        # Check if the file is a .webp and convert it to .png
        if filename.lower().endswith('.webp'):
            try:
                image = Image.open(image_bytes)
                converted_image_bytes = io.BytesIO()
                image.save(converted_image_bytes, format='PNG')
                converted_image_bytes.name = filename[:-5] + '.png'  # Change extension to .png
                converted_image_bytes.seek(0)  # Reset pointer to start
                image_bytes = converted_image_bytes
            except Exception as convert_error:
                print(f"Failed to convert .webp to .png for {url}: {convert_error}")
                # Optionally, you can choose to send the original .webp if conversion fails
                image_bytes.name = filename  # Keep original name
        else:
            image_bytes.name = filename  # Keep original name for non-webp images

        # Prepare the caption with the thread title and thread URL
        caption = f'{thread_title}\n`https://lihkg.com/thread/{thread_id}/`\n`{url}`'

        # Send the photo
        client.send_file(
            chat,
            file=image_bytes,
            caption=caption,
            force_document=False,  # Ensure it's sent as a photo, not a document
            parse_mode='md'  # Enable Markdown parsing for backticks
        )
        print(f"Photo sent: {thread_title}\n{url}")
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to send photo {url}: {e}")
        return False  # Indicate failure

def send_youtube_photo(client, chat, url, caption):
    """Download and send a photo to the specified Telegram chat."""
    try:
        # Download the image
        response = requests.get(url, proxies={}, timeout=6)
        response.raise_for_status()

        # Extract the image filename from the URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # Generate a unique filename if none is present
            filename = f"{uuid.uuid4()}.jpg"

        # Wrap the image bytes in a BytesIO object
        image_bytes = io.BytesIO(response.content)

        # Check if the file is a .webp and convert it to .png
        if filename.lower().endswith('.webp'):
            try:
                image = Image.open(image_bytes)
                converted_image_bytes = io.BytesIO()
                image.save(converted_image_bytes, format='PNG')
                converted_image_bytes.name = filename[:-5] + '.png'  # Change extension to .png
                converted_image_bytes.seek(0)  # Reset pointer to start
                image_bytes = converted_image_bytes
            except Exception as convert_error:
                print(f"Failed to convert .webp to .png for {url}: {convert_error}")
                # Optionally, you can choose to send the original .webp if conversion fails
                image_bytes.name = filename  # Keep original name
        else:
            image_bytes.name = filename  # Keep original name for non-webp images

        # Send the photo
        client.send_file(
            chat,
            file=image_bytes,
            caption=caption,
            force_document=False,  # Ensure it's sent as a photo, not a document
            parse_mode='md'  # Enable Markdown parsing for backticks
        )
        print(f"Photo sent: {url}")
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to send photo {url}: {e}")
        return False  # Indicate failure

def send_gif(client, chat, url, thread_title, thread_id):
    """Download and send a GIF to the specified Telegram chat."""
    try:
        # Download the GIF
        response = requests.get(url, proxies={})
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

        # Prepare the caption with the thread title and thread URL
        caption = f'{thread_title}\n`https://lihkg.com/thread/{thread_id}/`\n`{url}`'

        # Send the GIF
        client.send_file(
            chat,
            file=gif_bytes,
            caption=caption,
            force_document=False
        )
        print(f"GIF sent: {url}")
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to send GIF {url}: {e}")
        return False  # Indicate failure

def send_message(client, chat, message, thread_title, thread_id):
    """Send a text message to the specified Telegram chat with caption."""
    try:
        # Prepare the message with the thread title and thread URL
        full_message = f'{thread_title}\n`https://lihkg.com/thread/{thread_id}/`\n\n{message}'

        # Send the message
        client.send_message(chat, full_message, parse_mode='md')
        print(f"Message sent: {full_message}")
        return True  # Indicate success
    except Exception as e:
        print(f"Failed to send message '{message}': {e}")
        return False  # Indicate failure