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
# ------------------------ Configuration ------------------------


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
destination_chat = 4571037073

# Define the URL to fetch media from
MEDIA_URL = "https://lihkg.com/api_v2/thread/3793254/media?include_link=0"

# Define headers for the GET request
HEADERS = {
    "referer": "https://lihkg.com/thread/3793310/page/1",
}



# ------------------------ Helper Functions ------------------------

def is_image(url):
    """Check if the URL points to an image."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    parsed = urlparse(url)
    return any(parsed.path.lower().endswith(ext) for ext in image_extensions)


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

        # Send the photo
        await client.send_file(chat, file=response.content, caption=url, force_document=False)
        print(f"Photo sent: {url}")
    except Exception as e:
        print(f"Failed to send photo {url}: {e}")


async def send_message(client, chat, message):
    """Send a text message to the specified Telegram chat."""
    try:
        await client.send_message(chat, message)
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Failed to send message '{message}': {e}")


# ------------------------ Main Function ------------------------

async def main():
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

    media_urls = []
    # Fetch the media data from the API
    try:
        # Define the URL
        url = "https://lihkg.com/api_v2/thread/3793254/media?include_link=0"

        # Define the headers
        headers = {
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
            # "Cookie": "_ga=GA1.1.1408923090.1727350058; PHPSESSID=ok84r4f5f5b7gngjd5l93bg1kl; __cfruid=f0b00f51bb74f679e4c6201ba0a4a9a0bae30a34-1727595733; _cfuvid=M6wmXQ3AYfL2MtpmP2SuVD1RJtNc4wCRLMS5H2rC50Y-1727595733482-0.0.1.1-604800000; _ga_PPY9Z37CCJ=GS1.1.1727595735.3.1.1727595735.60.0.0; _ga_L8WS4GS6YR=GS1.1.1727595737.3.0.1727595737.0.0.0; __cf_bm=dgoxRaxD7_tSGwlplJ5yCOe8ix_lA8dvq_THUHiwkmw-1727597163-1.0.1.1-fTH0wx33FYvhA.ybsx3dvjVO6d6MOu6oIQ2jCzJ.6T4zEuuFUP.IjJv.CSeosN538ZMyGPId7dtKu1QewSBIlg; cf_clearance=ZQf3Ct7nrKOerXO6K0eT2_As1uDvYIybLgEzK.kgHR8-1727597165-1.2.1.1-OVtYGJB7VnZInLPErCwn1bV4_Ca_CmNo.m7.wVNtfiYQ7.B17ip6pCeGgpTOmmsCGVhfzte5x1soe17tY0vejTqJs.p7zBJCrwW1J_XdHuqgSihmR5yTi3B8Owqk0Pv4CTuO2Wsg2oKi3V.HntRiY08W_NNmi_2P7SnlST6JFzpD8VfUgAHfbgygWmVuQi0BgAdYp00emOFt4nOZe7LPzhoGCeUV9d8ZV1czDz5Rx7TBR3DtQVwzpY8jGK57brOL_skpAXfTJ7aEoCoxNlVOU.kKNhDFOHGrETuZDSmXC8arGOlzTEm6BM_6zI.SAdB4Gege6vRlZbSjyuEsEEUDG0x.tfG0B_Um8ET8Rkmd9YWNodn97rRq.AJT8OlUVmsi"
        }

        # 'url': '.*?'
        # 4571037073
        # Make the GET request
        response = requests.get(url, headers=headers, proxies={
            'http':'127.0.0.1:10809'
        })

        print(response.text.replace("\\",""))
        urls = re.findall('"url":"(.*?)"',response.text.replace("\\",""))
        media_urls = urls
        print(f"Extracted {len(media_urls)} media URLs.")
    except Exception as e:
        print(f"Failed to parse media data: {e}")
        await client.disconnect()
        return

    # Iterate over each URL and send appropriately
    for url in media_urls:
        if is_image(url):
            await send_photo(client, dest_entity, url)
        elif is_youtube(url) or is_video(url):
            await send_message(client, dest_entity, url)
        else:
            print(f"Unrecognized media type for URL: {url}")

    # Disconnect the client after processing
    await client.disconnect()
    print("Telegram client disconnected.")


# ------------------------ Entry Point ------------------------

if __name__ == "__main__":
    asyncio.run(main())