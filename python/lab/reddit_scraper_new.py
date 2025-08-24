import re
import urllib

import requests
from lxml import etree
from telethon.errors import RPCError
import re
import urllib
from telethon.sync import TelegramClient

import requests
from lxml import etree
from telethon.errors import RPCError

from rss_send import *
from dotenv import load_dotenv
import os

from rss_send import *
from dotenv import load_dotenv
import os

load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

channel_id = 2262601777
db_handle = db_handler('reddit', 'media')
db_handle.create_database()


import subprocess

import praw
import requests
import os
import re
import ffmpeg

# Replace these with the values from your Reddit app
reddit = praw.Reddit(
    client_id='AJ8IpOAc2yFLdn2R5SbhuA',
    client_secret='g3c0y22tSigQhyIMCyflFpsOfrgLEg',
    username='Left-Effort-7573',
    password='a13579246810A@',
    user_agent='testscript by u/Left-Effort-7573'
)

# Select subreddit
subreddit = reddit.subreddit('asmongold')

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
    permalink = post.permalink
    title = post.title
    url = post.url

    print(f"Processing post: {title}")

    if post.is_video and post.media and 'reddit_video' in post.media:
        video_url = post.media['reddit_video'].get('fallback_url')
        # Check if the post has already been processed
        if db_handle.url_exists(permalink, video_url):
            print("Post already processed. Skipping.")
            return
        if video_url:
            print(f"Video URL: {video_url}")

            # Derive audio URL from video URL
            match = re.search(r'https://v\.redd\.it/([^/]+)/DASH_\d+\.mp4', video_url)
            if match:
                reddit_id = match.group(1)
                audio_url = f'https://v.redd.it/{reddit_id}/HLS_AUDIO_128.aac'
                print(f"Audio URL: {audio_url}")
            else:
                print("Failed to derive audio URL.")
                return

            # Define file paths
            video_filename = f"{post.id}_video.mp4"
            audio_filename = f"{post.id}_audio.aac"
            output_filename = f"{post.id}_final.mp4"

            video_path = os.path.join(MEDIA_DIR, video_filename)
            audio_path = os.path.join(MEDIA_DIR, audio_filename)
            output_path = os.path.join(MEDIA_DIR, output_filename)

            # Download video
            if download_file(video_url, video_path):
                # Download audio
                if download_file(audio_url, audio_path):
                    # Merge video and audio
                    if merge_audio_video(video_path, audio_path, output_path):
                        print(f"Final video with audio saved as {output_filename}")

                        # Send to Telegram
                        caption = f"{title}\n`https://www.reddit.com{permalink}`"
                        if send_video_to_telegram(client, output_path, caption):
                            # Insert into database
                            db_handle.insert_url(permalink, video_url)
                            # Cleanup temporary files
                            cleanup_files(video_path, audio_path, output_path)
                        else:
                            print("Failed to send video to Telegram.")
                    else:
                        print("Failed to merge audio and video.")
                else:
                    print("Failed to download audio.")
            else:
                print("Failed to download video.")
    elif url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Check if the post has already been processed
        if db_handle.url_exists(permalink, url):
            print("Post already processed. Skipping.")
            return
        # Handle image posts
        image_url = url
        print(f"Image URL: {image_url}")

        # Define caption
        caption = f"{title}\n`https://www.reddit.com{permalink}`"

        # Send image to Telegram
        if send_photo_to_telegram(client, image_url, caption):
            # Insert into database
            db_handle.insert_url(permalink, image_url)
        else:
            print("Failed to send image to Telegram.")
    else:
        print("No supported media content found.")

    print('-' * 40)


def main():
    """
    Main function to connect to Telegram and process Reddit posts.
    """
    # Connect to Telegram
    try:
        client = TelegramClient('auto_forward_session_hot', api_id, api_hash)
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

    # Select subreddit
    subreddit = reddit.subreddit('asmongold')

    # Fetch the top 100 hot posts and process them
    for post in subreddit.new(limit=200):
        process_post(post, client)
    # Fetch the top 100 hot posts and process them
    for post in subreddit.now(limit=200):
        process_post(post, client)

    # Disconnect Telegram client
    client.disconnect()


if __name__ == "__main__":
    main()
