# base_handler.py

from abc import ABC, abstractmethod
import os
import requests
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from rss_send import db_handler


load_dotenv()

class BaseHandler(ABC):
    """
    Abstract base class for media handlers.
    """

    def __init__(self, channel_id: int, db_name: str, telegram_session: str):
        """
        Initializes the handler with channel ID, database name, Telegram API credentials.

        Args:
            channel_id (int): The Telegram channel ID.
            db_name (str): The name of the database.
            api_id (str): Telegram API ID.
            api_hash (str): Telegram API Hash.
        """
        self.channel_id = channel_id
        self.db_name = db_name
        self.telegram_session = telegram_session
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        self.api_id = api_id
        self.api_hash = api_hash
        self.media_dir = 'media'
        if not os.path.exists(self.media_dir):
            os.makedirs(self.media_dir)
        self.db_handle = db_handler(self.db_name, 'media')
        self.db_handle.create_database()
        self.client = self.connect_telegram()



    def connect_telegram(self):
        """
        Connects to the Telegram client.

        Returns:
            TelegramClient: An instance of the connected Telegram client.
        """
        print('connect_telegram:',self.telegram_session)
        try:
            client = TelegramClient(self.telegram_session, self.api_id, self.api_hash)
            client.connect()
            if not client.is_user_authorized():
                print("Telegram client is not authorized. Please authorize the client.")
                return None
            return client
        except Exception as e:
            print(f"Failed to connect Telegram client: {e}")
            return None

    def disconnect_telegram(self):
        """
        Disconnects the Telegram client.
        """
        if self.client:
            self.client.disconnect()
            print("Disconnected Telegram client.")

    def send_photo_to_telegram(self, photo_url: str, caption: str, headers: dict = None) -> bool:
        """
        Downloads a photo from a URL and sends it to Telegram.

        Args:
            photo_url (str): The URL of the photo to download.
            caption (str): The caption for the photo.
            headers (dict, optional): HTTP headers for the download request.

        Returns:
            bool: True if the photo was sent successfully, False otherwise.
        """
        try:
            response = requests.get(photo_url, headers=headers, stream=True)
            response.raise_for_status()
            photo_path = os.path.join(self.media_dir, os.path.basename(photo_url))
            with open(photo_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            with self.client:
                self.client.send_file(self.channel_id, photo_path, caption=caption)
            print(f"Sent photo: {photo_url}")
            self.cleanup_files(photo_path)
            return True
        except requests.RequestException as e:
            print(f"Failed to download photo {photo_url}: {e}")
            return False
        except RPCError as e:
            print(f"Failed to send photo to Telegram: {e}")
            return False

    def send_video_to_telegram(self, video_url: str, caption: str, headers: dict = None) -> bool:
        """
        Downloads a video from a URL and sends it to Telegram.

        Args:
            video_url (str): The URL of the video to download.
            caption (str): The caption for the video.
            headers (dict, optional): HTTP headers for the download request.

        Returns:
            bool: True if the video was sent successfully, False otherwise.
        """
        try:
            response = requests.get(video_url, headers=headers, stream=True)
            response.raise_for_status()
            if video_url.__contains__('tag'):
                video_url = video_url.split('?')[0]
            video_path = os.path.join(self.media_dir, os.path.basename(video_url))
            with open(video_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            with self.client:
                self.client.send_file(self.channel_id, video_path, caption=caption)
            print(f"Sent video: {video_url}")
            self.cleanup_files(video_path)
            return True
        except requests.RequestException as e:
            print(f"Failed to download video {video_url}: {e}")
            return False
        except RPCError as e:
            print(f"Failed to send video to Telegram: {e}")
            return False

    def send_file_to_telegram(self, file: str, caption: str) -> bool:
        self.client.send_file(self.channel_id, file, caption=caption)
        print(f"Sent video: {file}")


    def download_file(self, url: str, path: str, headers: dict = None) -> bool:
        """
        Downloads a file from a URL and saves it to the specified path.

        Args:
            url (str): The URL of the file to download.
            path (str): The local file path where the file will be saved.
            headers (dict, optional): HTTP headers for the download request.

        Returns:
            bool: True if download succeeds, False otherwise.
        """
        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded file: {path}")
            return True
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
            return False

    def download_video_file(self, url: str, path: str, headers: dict = None, max_size: int = 10 * 1024 * 1024) -> bool:
        """
        Downloads a video file from a URL with a size limit.

        Args:
            url (str): The URL of the video to download.
            path (str): The local file path where the video will be saved.
            headers (dict, optional): HTTP headers for the download request.
            max_size (int, optional): Maximum allowed file size in bytes (default is 10MB).

        Returns:
            bool: True if download succeeds and within size limit, False otherwise.
        """
        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > max_size:
                print(f"Aborted: File size {content_length} bytes exceeds the {max_size} bytes limit.")
                return False

            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Downloaded video file: {path}")
            return True
        except requests.RequestException as e:
            print(f"Failed to download video {url}: {e}")
            return False

    def cleanup_files(self, path: str):
        """
        Removes the specified file from the local filesystem.

        Args:
            path (str): The path of the file to remove.
        """
        try:
            os.remove(path)
            print(f"Cleaned up file: {path}")
        except OSError as e:
            print(f"Failed to delete file {path}: {e}")