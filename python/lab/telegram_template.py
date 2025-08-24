import time
import schedule
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from rss_send import *
from dotenv import load_dotenv
import os

load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

db_handle = db_handler('twitter', 'media')
db_handle.create_database()
channel_id = 2280520430

import subprocess

import requests
import os


# Create a directory to save media files
MEDIA_DIR = 'media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)


def download_file(url, path):
    """
    Downloads a file from a URL and saves it to the specified path.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {path}")
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False


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


def send_video_to_telegram(client, file_path, caption):
    """
    Sends a video file to the specified Telegram chat.
    """
    try:
        client.send_file(channel_id, file_path, caption=caption)
        print(f"Sent to Telegram: {file_path}")
        return True
    except RPCError as e:
        print(f"Failed to send video to Telegram: {e}")
        return False


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


def send_photo_to_telegram(client, image_url, caption):
    """
    Sends an image from a URL to the specified Telegram chat.
    Downloads the image before sending.
    """
    try:
        image_filename = os.path.basename(image_url)
        image_path = os.path.join(MEDIA_DIR, image_filename)

        # Download the image
        if download_file(image_url, image_path):
            client.send_file(channel_id, image_path, caption=caption)
            print(f"Sent to Telegram: {image_path}")
            # Optionally, delete the image after sending
            os.remove(image_path)
            print(f"Deleted temporary image: {image_path}")
            return True
        else:
            print(f"Failed to download image: {image_url}")
            return False
    except Exception as e:
        print(f"Failed to send image to Telegram: {e}")
        return False


def process_post(post, client):
    """
    Processes a single Reddit post: downloads media, merges audio and video if necessary, sends to Telegram.
    """


def main():
    global channel_id, db_handle
    """
    Main function to connect to Telegram and process Reddit posts.
    """
    # Connect to Telegram
    try:
        client = TelegramClient('auto_forward_session', api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print("Telegram client is not authorized. Please authorize the client.")
            # Handle authorization if necessary
            # For example, send a code request and input the code manually
            # client.send_code_request(phone)
            # code = input('Enter the code: ')
            # client.sign_in(phone, code)
            return
    except Exception as e:
        print(f"Failed to connect Telegram client: {e}")
        return

    db_handle = db_handler('reddit', 'media')
    db_handle.create_database()
    channel_id = 2262601777  # asmongold

    # Disconnect Telegram client
    client.disconnect()


if __name__ == "__main__":
    main()
    schedule.every(10).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
