from dotenv import load_dotenv

from baseHandler import BaseHandler

load_dotenv()

directory = r"C:\Users\fueqq\Downloads\mattymatty417\LoveSongs4Peace"
user_name = directory.split('\\')[-1]


class TwitterUserHandler(BaseHandler):
    """
    Handler for fetching and processing Twitter user media.
    """
    def __init__(self, channel_id: int, db_name: str, telegram_session: str, user_id: str, count: int = 20):
        """
        Initializes the TwitterUserHandler with necessary parameters.

        Args:
            channel_id (int): The Telegram channel ID.
            db_name (str): The name of the database.
            user_id (str): The Twitter user ID to fetch media for.
            count (int, optional): Number of tweets to fetch. Defaults to 20.
        """
        super().__init__(channel_id, db_name, telegram_session)
        self.user_id = user_id
        self.count = count



    def fetch_and_send_media(self):
        import os

        # directory = r"C:\Users\fueqq\Downloads\UnzipHelper"
        continu = False
        try:
            # List all files and directories in the specified directory
            with os.scandir(directory) as entries:
                for entry in entries:
                    time_str = entry.name.split("_")[0]
                    if entry.is_file():
                        # if time_str == '1804191475783057861':
                        #     continu = True
                        # if not continu:
                        #     continue
                        print(f"File: https://x.com/{user_name}/status/{time_str} {entry.name}")
                        # caption = f"`https://x.com/{user_name}/status/{time_str}`"
                        caption = f"https://x.com/{user_name}/status/{time_str}"
                        file = f'{directory}/{entry.name}'
                        self.send_file_to_telegram(file, caption)
                    elif entry.is_dir():
                        print(f"Directory: {entry.name}")
        except FileNotFoundError:
            print(f"The directory '{directory}' does not exist.")
        except PermissionError:
            print(f"Permission denied to access '{directory}'.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def run(self):
        """
        Executes the media fetching and sending process.
        """
        self.fetch_and_send_media()
        self.disconnect_telegram()

db_name = 'twitter_watch'
# channel_id = 2311937905
# session = 'twitter_watch_session2'
channel_id = 2341112318
session = 'twitter_view_session'

handler = TwitterUserHandler(channel_id, db_name, session, user_name)
handler.run()

#1758867970976284710_1