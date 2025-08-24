import json
import time

from lihkg_send import *

import random


load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Define multiple categories
categories = [
    {'name': 'water', 'id': 1, 'chat_id': 2400257786},
    {'name': 'anime', 'id': 8, 'chat_id': 2400438813},
    {'name': 'news', 'id': 5, 'chat_id': 2405192502},
    #love
    {'name': 'news', 'id': 30, 'chat_id': 2405192502},
    #work
    {'name': 'news', 'id': 14, 'chat_id': 2405192502},

    #interest
    #travel
    {'name': 'interest', 'id': 17, 'chat_id': 2417674433},
    #sport
    {'name': 'interest', 'id': 6, 'chat_id': 2417674433},
    #music
    {'name': 'interest', 'id': 21, 'chat_id': 2417674433},

    # {'name': 'love', 'id': 30, 'chat_id': 2417674433},
    # {'name': 'work', 'id': 14, 'chat_id': 2280520430},
]
order = [
    'new',
    'hot'
    'now',
]


# Add this function to get a list of proxies
def fetch_proxies():
    url = "https://imperialb.in/r/ywkbzmxe"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return [f"127.0.0.1:{port}" for port in response.text.split("\n") if port.strip()]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching proxies: {e}")
        return []


# Global list to store proxies
proxies_list = fetch_proxies()
current_proxy_index = 0


def get_next_proxy():
    global current_proxy_index
    if not proxies_list:
        return None
    proxy = proxies_list[current_proxy_index]
    current_proxy_index = (current_proxy_index + 1) % len(proxies_list)
    return {'http': '127.0.0.1:10809'}
    return {'http': proxy}


def make_api_request(url, headers, max_retries=5, retry_delay=2):
    global proxies_list
    for attempt in range(max_retries):
        try:
            proxy = get_next_proxy()
            if proxy is None:
                print("No proxies available. Using direct connection.")
                response = requests.get(url, headers=headers, timeout=5)
            else:
                response = requests.get(url, headers=headers, proxies={}, timeout=5)
            time.sleep(1)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                print(f"Too Many Requests error. Switching proxy and retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print(f"HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Failed to make API request: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(retry_delay)
            else:
                return None
    return None


def process_thread(client, category, thread_id, thread_title):
    MEDIA_URL = f"https://lihkg.com/api_v2/thread/{thread_id}/media?include_link=0"
    headers = get_page_headers()


    print(f"Processing Thread ID: {thread_id}, Title: {thread_title}")

    response_text = make_api_request(MEDIA_URL, headers)
    if response_text is None:
        return

    # Clean the response text and extract URLs
    clean_text = response_text.replace("\\", "")
    media_urls = re.findall('"url":"(.*?)"', clean_text)
    print(f"Extracted {len(media_urls)} media URLs for thread {thread_id}.")

    if not media_urls:
        print(f"No media URLs found for thread {thread_id}.")
        insert_url(category['name'], thread_id, '0')
        return

    # Get the destination chat entity
    try:
        # No need to get_entity since we're using chat_id directly
        chat = category['chat_id']
        print(f"Destination chat for category '{category['name']}': {chat}")
    except Exception as e:
        print(f"Failed to get destination chat '{category['chat_id']}': {e}")
        return
    data = json.loads(response_text)
    images = data['response']['images']
    if images:
        for image in images:
            url = image['url']
            tag = image['tag']
            if not url_exists(category['name'], thread_id, url):
                upload_success = False
                print(f"Image URL: {image['url']}, {image['tag']}")
                if tag == 'img':
                    if url.__contains__('.gif'):
                        upload_success = send_gif(client, chat, url, thread_title, thread_id)
                    else:
                        upload_success = send_photo(client, chat, url, thread_title, thread_id)
                # elif tag == 'youtube':
                #     upload_success = send_message(client, chat, url, thread_title, thread_id)
                elif tag == 'youtube':
                    print('youtube:', url)
                    # upload_success = send_message(client, chat, url, thread_title, thread_id)
                    try:
                        # youtube_id = re.findall('be/(.*?)\?', url)[0]
                        youtube_id = url.split('.be/')[1]
                    except:
                        # 'https://www.youtube.com/watch?v=UZo1ST0K_iQ'
                        try:
                            youtube_id = re.findall('\?v=(.*)', url)[0]
                        except:
                            try:
                                youtube_id = re.findall('/v/(.*?)\?', url)[0]
                            except:
                                continue
                    youtube_image_url = f'https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg'
                    print('youtube_image_url:', youtube_image_url)
                    upload_success = False
                    caption = f'{thread_title}\n`https://lihkg.com/thread/{thread_id}/`\n\n{url}'
                    upload_success = send_youtube_photo(client, chat, youtube_image_url, caption)
                else:
                    print(f"Unrecognized media type for URL: {url}")
                if upload_success:
                    # Insert the URL into the database after successful upload
                    insert_url(category['name'], thread_id, url)
                else:
                    print(f"Upload failed for URL: {url}. Not inserting into the database.")
    # # Iterate over each URL and send appropriately
    # for url in media_urls:
    #     if not url_exists(category['name'], thread_id, url):
    #         upload_success = False  # Initialize upload success flag
    #         # url = 'https://na.cx/i/3LkwM3w.webp'
    #         if is_image(url):
    #             upload_success = send_photo(client, chat, url, thread_title, thread_id)
    #         elif is_gif(url):
    #             upload_success = send_gif(client, chat, url, thread_title, thread_id)
    #         elif is_youtube(url) or is_video(url):
    #             upload_success = send_message(client, chat, url, thread_title, thread_id)
    #         else:
    #             print(f"Unrecognized media type for URL: {url}")
    #         if upload_success:
    #             # Insert the URL into the database after successful upload
    #             insert_url(category['name'], thread_id, url)
    #         else:
    #             print(f"Upload failed for URL: {url}. Not inserting into the database.")
    #     else:
    #         print(f"URL already processed: {url}")

def get_page_headers():
    headers = {
        "Host": "lihkg.com",
        "Sec-Ch-Ua-Platform": "Windows",
        "X-Li-Device-Type": "browser",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Li-Device": "baa1c3ecc1e72b8bf63d9e9a6ddc5e4db3a3c0b0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "X-Li-Load-Time": "5.2369263",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://lihkg.com/category/1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }
    return headers

def process_category(category, client, page, order,type):
    category_name = category['name']
    category_id = category['id']
    chat_id = category['chat_id']

    print(f"Starting processing for category: {category_name} (ID: {category_id})")

    # Create the database for this category
    create_database(category_name)

    # Define the URL to fetch threads for this category

    if category['name'] == 'water':
        if order == "":
            threads_url = f"https://lihkg.com/api_v2/thread/latest?cat_id={category_id}&page={page}&count=60&type={type}"
        elif type == "":
            threads_url = f"https://lihkg.com/api_v2/thread/latest?cat_id={category_id}&page={page}&count=60&type=now&order={order}"
    else:
        if order == "":
            threads_url = f"https://lihkg.com/api_v2/thread/category?cat_id={category_id}&page={page}&count=60&type={type}"
        elif type == "":
            threads_url = f"https://lihkg.com/api_v2/thread/category?cat_id={category_id}&page={page}&count=60&type=now&order={order}"
    print('threads_url:', threads_url)
    headers = get_headers()

    response_text = make_api_request(threads_url, headers)
    if response_text is None:
        return



    print(response_text)
    # Extract thread IDs and titles using regex
    thread_data = re.findall(r'"thread_id":\s*(\d+),"cat_id":(\d+),.*?"title":\s*"(.*?)"', response_text, re.DOTALL)
    print(f"Found {len(thread_data)} threads in category '{category_name}'.")

    # Initialize the Telegram client
    try:
        client.start()
        print(f"Telegram client started for category '{category_name}'.")
    except RPCError as e:
        print(f"Failed to start Telegram client for category '{category_name}': {e}")
        return

    # Process each thread in the category
    for thread_id, cat_id, thread_title in thread_data:
        if thread_title.endswith("\\"):
            thread_title = thread_title[:-1]  # Remove the trailing backslash

        try:
            thread_title = thread_title.replace('\/', '')
            print(f"unencode title: {thread_title}")
            thread_title = codecs.decode(thread_title, 'unicode_escape')
            thread_title = thread_title.encode('utf-16', 'surrogatepass').decode('utf-16')
        except UnicodeEncodeError:
            thread_title = "[Unprintable characters]"
        thread_title = thread_title.replace('\/', '')

        print('debug123', category['name'], thread_id, cat_id)
        if (category['name'] == 'water' and int(cat_id) in [8, 17, 6, 21]):
            print('others in water:',thread_id,thread_title,cat_id)
            continue
        if category['name'] == 'anime' and int(cat_id) != 8:
            print('not anime:',thread_id,thread_title,cat_id)
            continue
        if category['name'] == 'news' and int(cat_id) != 5:
            print('not news:',thread_id,thread_title,cat_id)
            continue
        if category['name'] == 'love' and int(cat_id) != 30:
            print('not love:',thread_id,thread_title,cat_id)
            continue
        if category['name'] == 'work' and int(cat_id) != 14:
            print('not work:',thread_id,thread_title,cat_id)
            continue
        # if thread_Id_exists(category_name,thread_id):
        #     print("thread_id exists:", thread_id)
        #     continue
        process_thread(client, category, thread_id, thread_title)

    # Disconnect the client after processing
    client.disconnect()
    print(f"Telegram client disconnected for category '{category_name}'.")

def main():
    global proxies_list
    # Fetch proxies before starting the main loop
    proxies_list = fetch_proxies()
    if not proxies_list:
        print("No proxies available. The script will use direct connections.")

    # Initialize a single Telegram client
    client = TelegramClient('lihkg_session', api_id, api_hash)
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
        # for i in range(1, 3):
        process_category(category, client, 1, "hot", "")
        process_category(category, client, 2, "hot", "")
        process_category(category, client, 1, "","now")
        process_category(category, client, 2, "","now")
        process_category(category, client, 3, "","now")

    # Disconnect the client after all categories are processed
    client.disconnect()
    print("Telegram client disconnected after processing all categories.")


# ------------------------ Entry Point ------------------------

if __name__ == "__main__":
    while True:
        main()
