import json
import re

import requests
import requests
from bs4 import BeautifulSoup
import html
import time
import schedule
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from rss_send import *
from dotenv import load_dotenv
import os
from telegram_template import send_photo_to_telegram, send_video_to_telegram, cleanup_files

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
# Create a directory to save media files
MEDIA_DIR = 'media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

headers = {
    'Host': 'www.instagram.com',
    'Cookie': 'mid=ZvTgtwALAAGAdMJE3UPzr71FkujN; ig_nrcb=1; wd=1536x695; dpr=1.25; ig_did=0AB246CC-F033-444C-B009-9C639E0E73BA; datr=N-H0ZjbMqRDWKgaSHTKKqDI-; ps_l=1; ps_n=1; fbm_124024574287414=base_domain=.instagram.com; shbid="18186\05458366020763\0541759297096:01f7e6353492cb601003fe87faef874ec9b61a1deb713cd61d5a75d0a268afe4d0b09f55"; shbts="1727761096\05458366020763\0541759297096:01f7fbcef44f8857860073dacb372f1266927d49ffa539f21de7b30ffeeb85f160de1bda"; ds_user_id=69858613900; csrftoken=7sYx2E50pGjacByxmvEDck27Dh78Avxg; sessionid=69858613900%3AW9QkBR41afl3D4%3A2%3AAYe_NdsshHYLLJNxioH0j0m19m633cI6XhCT5uVXxA; fbsr_124024574287414=Jgx3BpejPwnr7dTrdhLy6QavYJldNGVXqJ0z3XlJ4JM.eyJ1c2VyX2lkIjoiNjE1NjY0NzU0NzcxNjYiLCJjb2RlIjoiQVFCZDd5X1FwMFlPdTRGM3BGaklEbUR0R1VhSlJwZU5CNDBfamp6NlJJOFV1V3VjeFFnd2pQLVBGSzd4ZnJ2WkVzeTJjVjFBTERGT2o0Q0JGeDl4dnQxRVZFbGFNY25IWkVCWWticl9qWGxGeGg5X0k0RVYzTnBwN054Y2VoXzBPNDQzcDJnZF8ybzJoMVJkS1dzekV3a0VJemdiZkNDM19tVF9GcnJRYjRQb1NBX2J2NU9lQlJ5TWlra1JNYlRXeTlIdF9ZLThYcXBWek5PWXlRVDJSUXlrOUhxOGQxWjktQmxrSmhnc2oxTkpBak9rVXJxWC0xZF9wdDNhdWtETHY0ZXIyLXU1MTk3WDlnYlYzTFk3bzdObTQ3dURzQVJIaUN4ZDVSM2xwSld4bld4VzViUmotcjVVVFFtbEwzM2VsVlVkSy1SYmR2Y1RfQWlVbUZIUEpJa0EiLCJvYXV0aF90b2tlbiI6IkVBQUJ3ekxpeG5qWUJPNDZWUHhjQVVMWkNzWkIxdlpDcjVsOTAyN3FqMG9zNVJ2UUpGTjFQdVhxWkJ2UktVOFpCSkI3RTlQMWxSdm1xWkM0anl0R28xSW1IdjV1MkdmOTI3OGZENUN0WFlUV0lRem5GZXcybWdIcDZiZmx3R3NNMWozV09wdnphWkNZZElMbnM4WkF6c1pCQVVKdFhjRWNHT0VaQkhyY0hMZTB3UTl2cm9UdVpDWkJhZVhxTkVFUnVpdFpCMndaQUR3Y0hPNXo3eGxDcllaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzI4MzAwNzI0fQ; fbsr_124024574287414=Jgx3BpejPwnr7dTrdhLy6QavYJldNGVXqJ0z3XlJ4JM.eyJ1c2VyX2lkIjoiNjE1NjY0NzU0NzcxNjYiLCJjb2RlIjoiQVFCZDd5X1FwMFlPdTRGM3BGaklEbUR0R1VhSlJwZU5CNDBfamp6NlJJOFV1V3VjeFFnd2pQLVBGSzd4ZnJ2WkVzeTJjVjFBTERGT2o0Q0JGeDl4dnQxRVZFbGFNY25IWkVCWWticl9qWGxGeGg5X0k0RVYzTnBwN054Y2VoXzBPNDQzcDJnZF8ybzJoMVJkS1dzekV3a0VJemdiZkNDM19tVF9GcnJRYjRQb1NBX2J2NU9lQlJ5TWlra1JNYlRXeTlIdF9ZLThYcXBWek5PWXlRVDJSUXlrOUhxOGQxWjktQmxrSmhnc2oxTkpBak9rVXJxWC0xZF9wdDNhdWtETHY0ZXIyLXU1MTk3WDlnYlYzTFk3bzdObTQ3dURzQVJIaUN4ZDVSM2xwSld4bld4VzViUmotcjVVVFFtbEwzM2VsVlVkSy1SYmR2Y1RfQWlVbUZIUEpJa0EiLCJvYXV0aF90b2tlbiI6IkVBQUJ3ekxpeG5qWUJPNDZWUHhjQVVMWkNzWkIxdlpDcjVsOTAyN3FqMG9zNVJ2UUpGTjFQdVhxWkJ2UktVOFpCSkI3RTlQMWxSdm1xWkM0anl0R28xSW1IdjV1MkdmOTI3OGZENUN0WFlUV0lRem5GZXcybWdIcDZiZmx3R3NNMWozV09wdnphWkNZZElMbnM4WkF6c1pCQVVKdFhjRWNHT0VaQkhyY0hMZTB3UTl2cm9UdVpDWkJhZVhxTkVFUnVpdFpCMndaQUR3Y0hPNXo3eGxDcllaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzI4MzAwNzI0fQ; rur="EAG\05469858613900\0541759836763:01f7f8ec14a31853e591d388da27c5bf4187674250fa7aa3259209ab9bbff13b2f563873"',
    'Content-Length': '75',
    'Sec-Ch-Ua-Full-Version-List': '"Google Chrome";v="129.0.6668.90", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.90"',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Ch-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'Sec-Ch-Ua-Model': '""',
    'Sec-Ch-Ua-Mobile': '?0',
    'X-Ig-App-Id': '936619743392459',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Instagram-Ajax': '1017106274',
    'X-Csrftoken': '7sYx2E50pGjacByxmvEDck27Dh78Avxg',
    'X-Asbd-Id': '129477',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Sec-Ch-Prefers-Color-Scheme': 'dark',
    'X-Ig-Www-Claim': 'hmac.AR1HtUoeR7Pag-vTp_hCJfETwEV7hDCqeiQ1_L5rFhlgWUxn',
    'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
    'Origin': 'https://www.instagram.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.instagram.com/explore/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5',
    'Priority': 'u=1, i'
}

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def sanitize_comment(text):
    unescaped_text = html.unescape(text)
    clean_text = remove_html_tags(unescaped_text)
    return clean_text


channel_id = 2484441083



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


def send_photo_to_telegram(client, image_url, caption):
    """
    Sends an image from a URL to the specified Telegram chat.
    Downloads the image before sending.
    """
    try:
        # Generate a valid filename by removing invalid characters and truncating if necessary
        image_filename = ''.join(c for c in os.path.basename(image_url) if c.isalnum() or c in '._- ')
        image_filename = image_filename[:103]  # Truncate to maximum allowed filename length
        # If the filename is empty after sanitization, use a default name
        # if not image_filename:
        #     image_filename = 'instagram_image.jpg'
        image_path = os.path.join(MEDIA_DIR, image_filename+'.jpg')

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
def main():
    global channel_id, db_handle
    """
    Main function to connect to Telegram and process Reddit posts.
    """
    # Connect to Telegram
    try:
        client = TelegramClient('instagram_session', api_id, api_hash)
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

    url = 'https://www.instagram.com/api/v1/discover/ayml/'
    data = {
        'max_id': '[]',
        'max_number_to_display': '30',
        'module': 'discover_people',
        'paginate': 'true'
    }

    response = requests.post(url, headers=headers, data=data)
    t = response.text.replace('\\u0026', '&')
    image_urls = re.findall(r'"image_versions2":\{"candidates":\[\{".*?"url":"(.*?)"', t)
    video_urls = re.findall(r'"video_versions":\[\{".*?"url":"(.*?)"', t)

    for image_url in image_urls:
        print(image_url)
        send_photo_to_telegram(client,image_url,"")
    for video_url in video_urls:
        print(video_url)
        send_photo_to_telegram(client,image_url,"")
        video_filename = f"video.mp4"
        video_path = os.path.join(MEDIA_DIR, video_filename)
        if download_file(video_url, video_path):
            if send_video_to_telegram(client, video_path, ""):
                cleanup_files(video_path)

    # Disconnect Telegram client
    client.disconnect()
main()
# ig_contents = re.findall(r'"response":"(.*?"ok\\"\})',response.text)
# ig_contents = re.findall(r'"(https:\\/\\/instagram.fhkg1-1.fna.fbcdn.*?)"',response.text)
# for ig_content in ig_contents:
#     print(ig_content.replace('\\', ''))
# # Save the response text to tem.txt
# with open('tem.txt', 'w', encoding='utf-8') as file:
#     file.write(response.text.replace('\\u0026','&'))
#
# print("Response text has been saved to tem.txt")



