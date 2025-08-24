import cloudscraper
import time
import schedule
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from rss_send import *
from dotenv import load_dotenv
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from lxml import etree
from urllib.parse import urlparse, urljoin

load_dotenv()

db_handle = db_handler('4chan', 'media')
db_handle.create_database()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

channel_id = 2352398795
session_name = '4chan_session2'

# Create a directory to save media files
MEDIA_DIR = 'media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)
category = 'a'

def fetch_4chan_thread(driver, thread_id):
    url = f"https://boards.4chan.org/{category}/thread/{thread_id}"
    try:
        driver.get(url)
        # Wait until the thread content is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.post"))
        )
        return driver.page_source
    except Exception as e:
        return f"Failed to fetch thread. Error: {e}"

def download_file(driver, url, save_path):
    """
    Initiates a download via Selenium by navigating to the file URL.
    The WebDriver is configured to download files automatically to MEDIA_DIR.
    """
    try:
        # Extract the filename from the URL
        filename = os.path.basename(urlparse(url).path)
        expected_path = os.path.join(os.path.abspath(MEDIA_DIR), filename)

        # Navigate to the image URL to trigger the download
        driver.get(url)

        # Wait for the download to start by checking for the existence of the expected file
        wait_time = 0
        download_timeout = 30  # seconds
        while wait_time < download_timeout:
            if os.path.exists(expected_path):
                # Additional check to ensure the file has fully downloaded
                if not expected_path.endswith('.crdownload'):
                    print(f"Image downloaded successfully: {expected_path}")
                    return True
            time.sleep(1)
            wait_time += 1

        print(f"Failed to download image within {download_timeout} seconds: {url}")
        return False

    except Exception as e:
        print(f"Failed to download image. Error: {e}")
        return False

def send_photo_to_telegram(driver, client, image_url, caption):
    """
    Sends an image from a URL to the specified Telegram chat.
    Downloads the image using Selenium before sending.
    """
    try:
        image_filename = os.path.basename(urlparse(image_url).path)
        image_path = os.path.join(os.path.abspath(MEDIA_DIR), image_filename)

        # Download the image using Selenium
        if download_file(driver, image_url, image_path):
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

def get_title_list(html_content):
    # This function should be implemented to extract titles from HTML content
    # For now, we'll return an empty list as a placeholder
    return []

def get_valid_filename(name):
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    return s

def download_thread_images(driver,client, thread_content, board, thread_id, workpath, with_counter=False, use_title=False):
    regex = r'(\/\/i(?:s|)\d*\.(?:4cdn|4chan)\.org\/\w+\/(\d+\.(?:jpg|png|gif|webm|pdf)))'
    regex_result = list(set(re.findall(regex, thread_content)))
    regex_result = sorted(regex_result, key=lambda tup: tup[1])
    regex_result_len = len(regex_result)
    regex_result_cnt = 1

    directory = os.path.join(workpath, 'media')
    if not os.path.exists(directory):
        os.makedirs(directory)

    if use_title:
        all_titles = get_title_list(thread_content)

    for enum_index, enum_tuple in enumerate(regex_result):
        link, img = enum_tuple
        if db_handle.url_exists(thread_id, img):
            continue
        if use_title:
            img = all_titles[enum_index]
            img_path = os.path.join(directory, get_valid_filename(img))
        else:
            img_path = os.path.join(directory, img)

        if not os.path.exists(img_path):
            output_text = f"{board}/{thread_id}/{img}"
            if with_counter:
                output_text = f"{board}/{thread_id}/{img} [{str(regex_result_cnt).rjust(len(str(regex_result_len)))}/{regex_result_len}] {output_text}"
            print(output_text)

            link = f'https://i.4cdn.org/{category}/' + img
            caption = f"`https://boards.4chan.org/{category}/thread/{thread_id}`"
            if send_photo_to_telegram(driver, client, link, caption):
                db_handle.insert_url(thread_id, img)
            regex_result_cnt += 1

def do_it():
    global category
    try:
        client = TelegramClient(session_name, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print("Telegram client is not authorized. Please authorize the client.")
            # Handle authorization if necessary
            return
    except Exception as e:
        print(f"Failed to connect Telegram client: {e}")
        return

    # Define download preferences
    download_prefs = {
        "download.default_directory": os.path.abspath(MEDIA_DIR),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode if desired
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    # Uncomment the next line if you need to use a proxy
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:10809')
    chrome_options.add_experimental_option("prefs", download_prefs)

    driver = webdriver.Chrome(options=chrome_options)

    # Inside your main loop where you process threads
    for c in ['int', 'g', 'v', 'tv', 'biz']:
        category = c
        for page in range(1, 2):
            if page == 1:
                url = f'https://boards.4chan.org/{category}/'
            else:
                url = f'https://boards.4chan.org/{category}/{page}'
            print('pageurl:', url)

            # Navigate to the 4chan board page
            driver.get(url)

            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Get the page source
            page_source = driver.page_source

            # Print the page source (optional)
            print(page_source)

            # Parse the HTML content
            html = etree.HTML(page_source)

            # Find all thread links using XPath
            thread_links = html.xpath('/html/body/form[2]/div[1]/div/div/div[2]/blockquote/a')

            print("Thread links:")
            unique_threads = set()
            for link in thread_links:
                thread_url = urljoin(url, link.get('href'))
                parsed_url = urlparse(thread_url)
                thread_path = parsed_url.path
                if thread_path not in unique_threads:
                    unique_threads.add(thread_path)
                    post_url = f"https://boards.4chan.org{thread_path}"
                    thread_id = re.findall('\d+', thread_path)[0]
                    print('post_url:', thread_id, post_url)
                    # Fetch thread content using Selenium
                    thread_content = fetch_4chan_thread(driver, thread_id)

                    # Download images from the thread
                    board = category  # Updated to use current category
                    workpath = '.'  # Replace with the desired working directory
                    download_thread_images(driver,client, thread_content, board, thread_id, workpath, with_counter=True, use_title=False)

    # Quit the driver and disconnect the client
    driver.quit()
    client.disconnect()

do_it()