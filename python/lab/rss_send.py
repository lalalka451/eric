import requests
from PIL import Image
import os
from urllib.parse import urlparse
import uuid
import io
import sqlite3

class db_handler():
    def __init__(self, category_name, db_name):
        self.category_name = category_name
        self.db_name = f'{category_name}_{db_name}.db'

    def create_database(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS media
                         (thread_id INTEGER, url TEXT, UNIQUE(thread_id, url))''')
            conn.commit()

    def url_exists(self, thread_id, url):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM media WHERE thread_id=? AND url=?", (thread_id, url))
            return c.fetchone() is not None

    def thread_id_exists(self, thread_id):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT 1 FROM media WHERE thread_id=?", (thread_id,))
            return c.fetchone() is not None

    def insert_url(self, thread_id, url):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO media (thread_id, url) VALUES (?, ?)", (thread_id, url))
                conn.commit()
            except sqlite3.IntegrityError:
                # URL already exists, do nothing
                pass

    def insert_url2(self, thread_id, url):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO media (thread_id, url, type) VALUES (?, ?, ?)", (thread_id, url, 3))
                conn.commit()
            except sqlite3.IntegrityError:
                # URL already exists, do nothing
                pass

    def insert_url3(self, thread_id, url, type):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO media (thread_id, url, type) VALUES (?, ?, ?)", (thread_id, url, type))
                conn.commit()
            except sqlite3.IntegrityError:
                # URL already exists, do nothing
                pass

    def set_url(self, thread_id):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                # c.execute("UPDATE media SET url = ? WHERE thread_id = ?", ('true', thread_id))
                c.execute("UPDATE media SET url = ? WHERE thread_id = ?", ('true', thread_id))
                conn.commit()
            except sqlite3.IntegrityError:
                # URL already exists, do nothing
                pass
    def set_url1(self, thread_id):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                # c.execute("UPDATE media SET url = ? WHERE thread_id = ?", ('true', thread_id))
                c.execute("UPDATE media SET url = ? WHERE thread_id = ?", ('fail', thread_id))
                conn.commit()
            except sqlite3.IntegrityError:
                # URL already exists, do nothing
                pass

    def get_twitter_user_by_type(self, type):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                c.execute("SELECT thread_id FROM media WHERE type = ? AND url != 'true'", (type,))
                return c.fetchall()
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                return None


def send_photo(client, chat, url, caption):
    """Download and send a photo to the specified Telegram chat."""
    # headers = {
    #     "Host": "www.reddit.com",
    #     "Upgrade-Insecure-Requests": "1",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "Sec-Fetch-Site": "none",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-User": "?1",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    #     "Sec-Ch-Ua-Mobile": "?0",
    #     "Sec-Ch-Ua-Platform": '"Windows"',
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
    #     "Priority": "u=0, i"
    # }
    # try:
    # Download the image
    response = requests.get(url, proxies={}, timeout=6, headers={})
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
    caption = caption

    # Send the photo
    client.send_file(
        chat,
        file=image_bytes,
        caption=caption,
        force_document=False,  # Ensure it's sent as a photo, not a document
        parse_mode='md'  # Enable Markdown parsing for backticks
    )
    print(f"Photo sent: {caption}")
    return True  # Indicate success
    # except Exception as e:
    #     print(f"Failed to send photo {url}: {e}")
    #     return False  # Indicate failure


import requests
from PIL import Image
from io import BytesIO


def send_photo_reddit(client, chat, url, caption):
    # try:
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
    caption = caption

    # Send the photo
    client.send_file(
        chat,
        file=image_bytes,
        caption=caption,
        force_document=False,  # Ensure it's sent as a photo, not a document
        parse_mode='md'  # Enable Markdown parsing for backticks
    )
    return True
    # except Exception as e:
        # print(f"Failed to send photo {url}: {e}")
        # return False  # Indicate failure