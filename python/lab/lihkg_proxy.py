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

# ------------------------ Configuration ------------------------

proxies = {
    'http': '127.0.0.1:10809',
    'https': '127.0.0.1:10809',
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

# Define multiple categories
categories = [
    # {'name': 'anime', 'id': 8, 'chat_id': 4569483129},
    # {'name': 'love', 'id': 30, 'chat_id': 4530610594},
    # {'name': 'water', 'id': 1, 'chat_id': 4579672695},
    # {'name': 'work', 'id': 14, 'chat_id': 4595270883},
    # {'name': 'news', 'id': 5, 'chat_id': 4571037073},

    {'name': 'water', 'id': 1, 'chat_id': 2400257786},
    {'name': 'anime', 'id': 8, 'chat_id': 2400438813},
    {'name': 'news', 'id': 5, 'chat_id': 2405192502},
    {'name': 'love', 'id': 30, 'chat_id': 2417674433},
    {'name': 'work', 'id': 14, 'chat_id': 2280520430},
    # Add more categories as needed
]

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

# ------------------------ Processing Functions ------------------------
def get_proxy_uri():
    while True:
        proxy_uri = requests.get('http://localhost:5000/fetch_random').text
        if len(proxy_uri) == 0:
            print('暂时没有可用代理')
            time.sleep(5)  # Wait before trying again
            continue

        if not proxy_uri.startswith('http'):
            return proxy_uri

def get_proxy():
    proxy_uri = get_proxy_uri()
    print('获取到的代理是：' + proxy_uri)
    proxies = {proxy_uri.split(':')[0]: proxy_uri}
    # proxies = {'http'}
    return proxies

def process_thread(client, category, thread_id):
    thread_title = ""
    media_urls = []
    MEDIA_URL = f"https://lihkg.com/api_v2/thread/{thread_id}/media?include_link=0"

    # Fetch the media data from the API
    try:
        # Define the URLs
        url = MEDIA_URL
        title_url = f"https://lihkg.com/api_v2/thread/{thread_id}/page/1?order=reply_time"

        headers = get_headers()
        title_response = requests.get(title_url, headers=headers, proxies=get_proxy())
        title_response.raise_for_status()
        title = title_response.json()['response']['title']
        print(f"Processing Thread ID: {thread_id}, Title: {title}")

        # Programmatically handle Unicode-encoded strings
        thread_title = title.encode('utf-8').decode('utf-8')

        # Make the GET request with proxy if needed
        response = requests.get(url, headers=headers, proxies=get_proxy())
        response.raise_for_status()

        # Clean the response text and extract URLs
        clean_text = response.text.replace("\\", "")
        media_urls = re.findall('"url":"(.*?)"', clean_text)
        print(f"Extracted {len(media_urls)} media URLs for thread {thread_id}.")
    except Exception as e:
        print(f"Failed to parse media data for thread {thread_id}: {e}")
        return

    if not media_urls:
        print(f"No media URLs found for thread {thread_id}.")
        return

    # Get the destination chat entity
    try:
        # No need to get_entity since we're using chat_id directly
        chat = category['chat_id']
        print(f"Destination chat for category '{category['name']}': {chat}")
    except Exception as e:
        print(f"Failed to get destination chat '{category['chat_id']}': {e}")
        return

    # Iterate over each URL and send appropriately
    for url in media_urls:
        if not url_exists(category['name'], thread_id, url):
            upload_success = False  # Initialize upload success flag
            # url = 'https://na.cx/i/3LkwM3w.webp'
            if is_image(url):
                upload_success = send_photo(client, chat, url, thread_title, thread_id)
            # elif is_gif(url):
            #     upload_success = send_gif(client, chat, url, thread_title, thread_id)
            elif is_youtube(url) or is_video(url):
                upload_success = send_message(client, chat, url, thread_title, thread_id)
            else:
                print(f"Unrecognized media type for URL: {url}")
            if upload_success:
                # Insert the URL into the database after successful upload
                insert_url(category['name'], thread_id, url)
            else:
                print(f"Upload failed for URL: {url}. Not inserting into the database.")
        else:
            print(f"URL already processed: {url}")

def process_category(category, client, page):
    category_name = category['name']
    category_id = category['id']
    chat_id = category['chat_id']

    print(f"Starting processing for category: {category_name} (ID: {category_id})")

    # Create the database for this category
    create_database(category_name)

    # Define the URL to fetch threads for this category
    threads_url = f"https://lihkg.com/api_v2/thread/category?cat_id={category_id}&page={page}&count=60"
    print('threads_url:',threads_url)
    headers = get_headers()
    try:
        response = requests.get(threads_url, headers=headers, proxies=get_proxy())
        response.raise_for_status()
        # Extract thread IDs using regex
        thread_ids = list(set(re.findall(r'"thread_id":\s*(\d+)', response.text)))
        print(f"Found {len(thread_ids)} threads in category '{category_name}'.")
    except Exception as e:
        print(f"Failed to fetch threads for category '{category_name}': {e}")
        return

    # Initialize the Telegram client
    try:
        client.start()
        print(f"Telegram client started for category '{category_name}'.")
    except RPCError as e:
        print(f"Failed to start Telegram client for category '{category_name}': {e}")
        return

    # Process each thread in the category
    for thread_id in thread_ids:
        process_thread(client, category, thread_id)

    # Disconnect the client after processing
    client.disconnect()
    print(f"Telegram client disconnected for category '{category_name}'.")

def main():
    # Initialize a single Telegram client
    client = TelegramClient('auto_forward_session', api_id, api_hash)
    try:
        client.connect()
        if not client.is_user_authorized():
            print("Client is not authorized. Please authorize the client.")
            # Handle authorization if necessary
            return
    except RPCError as e:
        print(f"Failed to connect Telegram client: {e}")
        return

    for category in categories:
        for i in range(1,3):
            process_category(category, client,i)

    # Disconnect the client after all categories are processed
    client.disconnect()
    print("Telegram client disconnected after processing all categories.")

# ------------------------ Entry Point ------------------------

if __name__ == "__main__":
    # Initial run
    main()

    # Schedule the main function to run every 15 minutes
    # schedule.every(15).minutes.do(main)
    schedule.every(30).minutes.do(main)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)