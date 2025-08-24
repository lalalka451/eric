import requests
import time
import schedule
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from rss_send import *
from dotenv import load_dotenv
import os

load_dotenv()

db_handle = db_handler('4chan', 'media')
db_handle.create_database()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

channel_id = 2352398795
session_name = '4chan_session'


def fetch_4chan_thread(thread_id):
    url = f"https://boards.4chan.org/a/thread/{thread_id}"
    headers = {
        "Host": "boards.4chan.org",
        "Cookie": "cf_clearance=0bFOho.45mB6cc8o3N9AC4KbqFQ.sn_qpmwSw3ZeI4c-1728221883-1.2.1.1-xS7fH.v7tTsgeOOpUlpZ_Q7np9R9FRTrVUhJE6E8CXXew.t6lGIxGW_FbNAV2IHwmrHM8zLw2QDvY90uHbpYm7KpaIXxCOVGyoeliVukqBXrwwyTvEyWOcUa07HUybl8kSz9OExCGTbPnIsbRvkdDEraMjKcJbhIDu2znD9GGBaFRZH9CUKRe0se.4uTeVnmz1akPAQ7aKLNKdMLen4zTtjjP26jd1J9WEtwzBO_lLFQcqIHlNUG3N3ZU99PFchQZKKpdfsniVs1LFFb0i3rY6bC7p5f.rDx11rxBgmXQ6P9r_Q1QX5vsm9XUPIYqv6kXQcliAmlSXqJG9_NzcJ.h1ZQ3Su5VHasESKTclAMGusAm5.AsIBM1Iy8HOTz.uE9ZdZ7gzlXf2bJc6MH.oMb0P2C.1W5l0tuFypRq3HEd0whEdcu.YMh5CVLPdTRuNtL; _ga=GA1.3.605155716.1728221889; _gid=GA1.3.45787778.1728221889",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Full-Version": '"129.0.6668.90"',
        "Sec-Ch-Ua-Arch": '"x86"',
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
        "Sec-Ch-Ua-Model": '""',
        "Sec-Ch-Ua-Bitness": '"64"',
        "Sec-Ch-Ua-Full-Version-List": '"Google Chrome";v="129.0.6668.90", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.90"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "If-None-Match": '"67029288-128f1"',
        "If-Modified-Since": "Sun, 06 Oct 2024 13:37:12 GMT",
        "Priority": "u=0, i",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch thread. Status code: {response.status_code}"

# Example usage
thread_id = "271768899"
thread_content = fetch_4chan_thread(thread_id)
import re
import os


def get_title_list(html_content):
    # This function should be implemented to extract titles from HTML content
    # For now, we'll return an empty list as a placeholder
    return []

def get_valid_filename(name):
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    return s

def download_thread_images(thread_content, board, thread_id, workpath, with_counter=False, use_title=False):
    regex = r'(\/\/i(?:s|)\d*\.(?:4cdn|4chan)\.org\/\w+\/(\d+\.(?:jpg|png|gif|webm|pdf)))'
    regex_result = list(set(re.findall(regex, thread_content)))
    regex_result = sorted(regex_result, key=lambda tup: tup[1])
    regex_result_len = len(regex_result)
    regex_result_cnt = 1

    # directory = os.path.join(workpath, 'downloads', board, thread_id)
    directory = os.path.join(workpath, 'media')
    if not os.path.exists(directory):
        os.makedirs(directory)

    if use_title:
        all_titles = get_title_list(thread_content)

    for enum_index, enum_tuple in enumerate(regex_result):
        link, img = enum_tuple

        if use_title:
            img = all_titles[enum_index]
            img_path = os.path.join(directory, get_valid_filename(img))
        else:
            img_path = os.path.join(directory, img)

        if not os.path.exists(img_path):
            # link = 'https:' + link

            output_text = f"{board}/{thread_id}/{img}"
            if with_counter:
                output_text = f"[{str(regex_result_cnt).rjust(len(str(regex_result_len)))}/{regex_result_len}] {output_text}"

            import requests

            link = 'https://i.4cdn.org/a/'+img
            print(output_text)
            response = requests.get(link)
            data = response.content
            print(link,img)
            with open(img_path, 'wb') as f:
                f.write(data)

            regex_result_cnt += 1

# Example usage
board = 'a'  # Replace with the actual board name
workpath = '.'  # Replace with the desired working directory
download_thread_images(thread_content, board, thread_id, workpath, with_counter=True, use_title=False)


# print(thread_content)

