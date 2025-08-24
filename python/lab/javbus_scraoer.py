import json
import random
import requests
import re
from telethon import TelegramClient
from telethon.errors import RPCError
import schedule
import time
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


load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Define the category
category = {'name': 'javbus', 'id': 2, 'chat_id': 2380209463}

def fetch_thread_content(url):
    headers = {
        "Host": "www.javbus.com",
        "Cookie": "4fJN_2132_saltkey=dkQRPlpD; 4fJN_2132_lastvisit=1727346606; age=verified; existmag=mag; dv=1; 4fJN_2132_visitedfid=2; 4fJN_2132_onlineusernum=7439; 4fJN_2132_sendmail=1; 4fJN_2132_sid=afCb7x; 4fJN_2132_lastact=1727848640%09forum.php%09forumdisplay; 4fJN_2132_st_t=0%7C1727848640%7Cb9d94f8409868d94503297b2056f3827; 4fJN_2132_forum_lastvisit=D_2_1727848640",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.text
        # print(content)
        regexs = re.findall(r'class="s">(.*?)</a>[\S\W\n]+?<a href=".*?tid=(\d+)&amp',content)
        # print(regexs)
        return regexs
    else:
        return None

def fetch_thread_images(tid):
    url = f"https://www.javbus.com/forum/forum.php?mod=viewthread&tid={tid}&extra=page%3D1"
    headers = {
        "Host": "www.javbus.com",
        "Cookie": "4fJN_2132_saltkey=dkQRPlpD; 4fJN_2132_lastvisit=1727346606; age=verified; existmag=mag; dv=1; 4fJN_2132_visitedfid=2; 4fJN_2132_onlineusernum=7439; 4fJN_2132_sendmail=1; 4fJN_2132_sid=afCb7x; 4fJN_2132_lastact=1727848640%09forum.php%09forumdisplay; 4fJN_2132_st_t=0%7C1727848640%7Cb9d94f8409868d94503297b2056f3827; 4fJN_2132_forum_lastvisit=D_2_1727848640",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.text
        pattern = r'" class="zoom" src="(.*?)"'
        matches = re.findall(pattern, content)
        return matches
    else:
        return None
    


def send_gif_javbus(client, chat, url, thread_title, thread_id):
    """Download and send a GIF to the specified Telegram chat."""
    try:
        headers = {
            "Host": "forum.javcdn.cc",
            "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.javbus.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
            "Priority": "u=0, i"
        }
        url = url.replace('forum','cloud')
        # Download the GIF
        response = requests.get(url, proxies={}, headers=headers)
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
        caption = f'{thread_title}\n`https://www.javbus.com/forum/forum.php?mod=viewthread&tid={thread_id}/`\n`{url}`'

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

def send_photo_javbus(client, chat, url, thread_title, thread_id):
    """Download and send a photo to the specified Telegram chat."""
    headers = {
        "Host": "forum.javcdn.cc",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.javbus.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=0, i"
    }
    try:
        # Download the image
        response = requests.get(url, proxies={},headers=headers, timeout=6)
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
        caption = f'{thread_title}\n`https://www.javbus.com/forum/forum.php?mod=viewthread&tid={thread_id}/`\n`{url}`'

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

def process_thread(client, thread_id, thread_title):
    images = fetch_thread_images(thread_id)
    if images:
        chat = category['chat_id']
        for image_url in images:
            if url_exists('', thread_id, image_url):
                print(f"Upload URL exists: {image_url}")
                continue
            if image_url.endswith('.gif'):
                upload_success = send_gif_javbus(client, chat, image_url, thread_title, thread_id)
            else:
                upload_success = send_photo_javbus(client, chat, image_url, thread_title, thread_id)
            
            if upload_success:
                insert_url(category['name'], thread_id, image_url)
            else:
                print(f"Upload failed for URL: {image_url}. Not inserting into the database.")
    else:
        print(f"No images found or failed to fetch images for thread {thread_id}")
        

def create_database(category_name):
    conn = sqlite3.connect(f'javbus.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media
                 (thread_id INTEGER, url TEXT, UNIQUE(thread_id, url))''')
    conn.commit()
    conn.close()
create_database('')

def url_exists(category_name, thread_id, url):
    conn = sqlite3.connect(f'javbus.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM media WHERE thread_id=? AND url=?", (thread_id, url))
    result = c.fetchone() is not None
    conn.close()
    return result

def thread_Id_exists(category_name, thread_id):
    conn = sqlite3.connect(f'javbus.db')
    c = conn.cursor()
    c.execute("SELECT 1 FROM media WHERE thread_id="+thread_id)
    result = c.fetchone() is not None
    conn.close()
    return result

def insert_url(category_name, thread_id, url):
    conn = sqlite3.connect(f'javbus.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO media (thread_id, url) VALUES (?, ?)", (thread_id, url))
        conn.commit()
    except sqlite3.IntegrityError:
        # URL already exists, do nothing
        pass
    conn.close()

def main():
    client = TelegramClient('javbus_session', api_id, api_hash)
    try:
        client.start()
        if not client.is_user_authorized():
            print("Client is not authorized. Please authorize the client.")
            return
        base_urls = [
            'https://www.javbus.com/forum/forum.php?mod=forumdisplay&fid=2',
            'https://www.javbus.com/forum/forum.php?mod=forumdisplay&fid=36'
        ]
        urls = [f"{url}&page={page}" for url in base_urls for page in range(1, 10)]

        for url in urls:
            thread_info = fetch_thread_content(url)
            if thread_info:
                for title, tid in thread_info:
                    print(f"Processing TID: {tid}, Title: {title}")
                    print(f"https://www.javbus.com/forum/forum.php?mod=viewthread&tid={tid}")
                    process_thread(client, tid, title)
            else:
                print("Failed to fetch thread information")

    except Exception as e:
        print(f"Failed to connect Telegram client: {e}")
    finally:
        client.disconnect()
        print("Telegram client disconnected after processing all threads.")
    client.disconnect()

if __name__ == "__main__":
    main()
    schedule.every(60).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
