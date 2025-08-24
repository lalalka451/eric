from telethon.sync import TelegramClient
from telethon.errors import RPCError
from dotenv import load_dotenv
import os

load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = ""


# Create a directory to save media files
MEDIA_DIR = 'tikkok/media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)



from PIL import Image

def is_valid_image(path):
    try:
        with Image.open(path) as img:
            img.verify()  # Verify that it's an image
        return True
    except (IOError, SyntaxError) as e:
        print(f"Invalid image file: {path}, Error: {e}")
        return False


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
    image_url_name = image_url.split('aweme_comment&l=')[1]
    image_filename = re.sub(r'[<>:"/\\|?*]', '', image_url_name)+'.jpg'
    image_path = os.path.join(MEDIA_DIR, image_filename)

    # Download the image
    if download_file(image_url, image_path):
        if not is_valid_image(image_path):
            print(f"Image validation failed: {image_path}")
            os.remove(image_path)
            return False
        try:
            with open(image_path, 'rb') as f:
                client.send_file(channel_id, f, caption=caption, file_name=image_filename)
            print(f"Sent to Telegram: {image_path}")
            os.remove(image_path)
            print(f"Deleted temporary image: {image_path}")
            return True
        except RPCError as e:
            print(f"Failed to send image to Telegram: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    else:
        print(f"Failed to download image: {image_url}")
        return False




def get_image(id, title, video_url):
    global channel_id
    url = "https://www.douyin.com/aweme/v1/web/comment/list/"
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "aweme_id": id,
        "cursor": "0",
        "count": "20",
        "item_type": "0",
        "insert_ids": "",
        "whale_cut_token": "",
        "cut_version": "1",
        "rcFT": "",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "en-US",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "129.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "129.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "12",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "0",
        "webid": "7419221520197813775",
        "msToken": "qTJtRAGOEY7184CoixyXI6wb9IQhmkVQDFNnYapgFvrxeqApfSZ0YEWs7X5cmUcOSfA6A7w9MVga2sn77tzkDxTi4SNCTZnaFqWmLuoIUkdv9musBPP7z83Ibh9sKPDoyFtMisRYBuHJ6TWf_3O0sTNqd0NYqxu74FXvi2cD5BvQ",
        "a_bogus": "QysVD7WjY2AfFd%2Ft8CmoyA5UZwxlNTuySliOWrIPyOzgYhFcyuPworCtrouJITlrsRBwiF5HIxaMbjVbFzXsZ9CpomZDum46MU%2F9VU0L%2FqwgGt4%2FLrguSg4FKwMF0OvNlA9SiI8R1s0x2fxRnrVLAB2GC5Fo5bfgbqp9p2SyJDCW3PyT99QfC-vWwXE%3D",
        "verifyFp": "verify_m1ww0lc1_WErDEBN7_LQz7_4lSd_8z1p_FpKULeDa7GS0",
        "fp": "verify_m1ww0lc1_WErDEBN7_LQz7_4lSd_8z1p_FpKULeDa7GS0"
    }
    headers = {
        "Host": "www.douyin.com",
        "Cookie": "passport_csrf_token=ce2899cf0db8e28f536a916926058827; passport_csrf_token_default=ce2899cf0db8e28f536a916926058827; bd_ticket_guard_client_web_domain=2; ttwid=1%7CMC21H_Mb9j8lH93LOkm_gOyxE3cU7HtZXKUpG1phEbM%7C1727422146%7C04dc408bf8b9f8b55a761b8633aab797cb5128184e74ffa59b4e6cdd87296117; __ac_signature=_02B4Z6wo00f01B5u1FgAAIDCGcTh.Cl0YAAeTtDAAGCgd4; UIFID_TEMP=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457b8f515a834c0ecc82c067d8fdd1324eb4a99188a749a44932052656d06410109c01a81f2c385f9b9b6b4206b6608e709a; douyin.com; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; hevc_supported=true; dy_swidth=1536; dy_sheight=864; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; strategyABtestKey=%221728177082.495%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; csrf_session_id=83c6a7ca445e31b3a1ff0364a03034fd; s_v_web_id=verify_m1ww0lc1_WErDEBN7_LQz7_4lSd_8z1p_FpKULeDa7GS0; xgplayer_user_id=698235855467; fpk1=U2FsdGVkX1++wLBFbf601U9z1ywdiNB0SSlbBqwSPlw+vrWb6reDbn2f11P1XXDyn/2OeBAbVMKZLMtE+WotAA==; fpk2=16453d6e2683b8800ded2a27c7f595d9; xg_device_score=7.802204888412783; UIFID=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457b8f515a834c0ecc82c067d8fdd1324eb4c72f64efa21a94d2ae050846e3eb429c598d53baad272932c8eaa3caa0a1dba103b639401e91c7628eb6c4afecdce9f5bd7398c5a047b9d24c07f360eb315b21cff795b8749ef8c6ed8ddf6a859afabfcaa988995721fa1fb45bb451767ec21c462afdf5c924d2bde65f61cee949818d; WallpaperGuide=%7B%22showTime%22%3A1728179415811%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; __ac_nonce=06701f11a003a7b1a9a65; n_mh=irBzyV0OuesE-LvbiK2AKUGQ9n8jO5mZ-mXHcPoPPAI; toutiao_sso_user=5174394313ffee8b8b00011809d680b8; toutiao_sso_user_ss=5174394313ffee8b8b00011809d680b8; passport_auth_status=25087fac42d958f101760ff3181b7d79%2C; passport_auth_status_ss=25087fac42d958f101760ff3181b7d79%2C; is_staff_user=false; SelfTabRedDotControl=%5B%5D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAnosb7IbnjdIciThilRveH9Gw8nMIBwM4eav286PjdqyYdtRuJtNG5RuPJ5f6eUn9%2F1728230400000%2F0%2F1728180523540%2F0%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=767d87166269e7abc7350c72ea491549; __security_server_data_status=1; publish_badge_show_info=%220%2C0%2C0%2C1728180529085%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAnosb7IbnjdIciThilRveH9Gw8nMIBwM4eav286PjdqyYdtRuJtNG5RuPJ5f6eUn9%2F1728230400000%2F0%2F1728180850981%2F0%22; my_rd=2; store-region=cn-hk; store-region-src=uid; sso_uid_tt=8ed59e1a4f56948506f8878202c22aba; sso_uid_tt_ss=8ed59e1a4f56948506f8878202c22aba; sid_ucp_sso_v1=1.0.0-KGMzNjgwZTJlYTA2YjY0ODhjYTdlNjA0YTI2NWE2YjI3ZTlkNDAyNGYKCRD65Ie4BhjvMRoCbHEiIDUxNzQzOTQzMTNmZmVlOGI4YjAwMDExODA5ZDY4MGI4; ssid_ucp_sso_v1=1.0.0-KGMzNjgwZTJlYTA2YjY0ODhjYTdlNjA0YTI2NWE2YjI3ZTlkNDAyNGYKCRD65Ie4BhjvMRoCbHEiIDUxNzQzOTQzMTNmZmVlOGI4YjAwMDExODA5ZDY4MGI4; sid_guard=b755863ed8e1722e9f61407f33363362%7C1728180858%7C21600%7CSun%2C+06-Oct-2024+08%3A14%3A18+GMT; uid_tt=93904a238516c74418884073ae75b72b; uid_tt_ss=93904a238516c74418884073ae75b72b; sid_tt=b755863ed8e1722e9f61407f33363362; sessionid=b755863ed8e1722e9f61407f33363362; sessionid_ss=b755863ed8e1722e9f61407f33363362; sid_ucp_v1=1.0.0-KDA1YmZiZGNlODAxYTExZWNmNjc3NjdmYTMxMjY4YmJlNzIzZmM0MGMKCBD65Ie4BhgNGgJscSIgYjc1NTg2M2VkOGUxNzIyZTlmNjE0MDdmMzMzNjMzNjI; ssid_ucp_v1=1.0.0-KDA1YmZiZGNlODAxYTExZWNmNjc3NjdmYTMxMjY4YmJlNzIzZmM0MGMKCBD65Ie4BhgNGgJscSIgYjc1NTg2M2VkOGUxNzIyZTlmNjE0MDdmMzMzNjMzNjI; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTU5jWGhnQmFXYlBuaWxXL1A5RE9tRm82NEh4WWozU0l2b3ZQejNqRWVJWldUWGFyN2VkNmYwVDZFdmJBU0dZMEdZbnE2dHhzazFHQU41QzU2YnFsUmc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; biz_trace_id=7cee3339; odin_tt=4f313cf84e205d15934f6b2ca0533efac640df3407a77e511daf045c59d25cfb4a1c0b823a76152f95b02236d50700b36cd11d2dfff648941d6bee9b9ad1b0a73a8c35a4579549e95a46f2b6529bb893; download_guide=%223%2F20241006%2F0%22; pwa2=%220%7C0%7C3%7C0%22; IsDouyinActive=true",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.douyin.com/discover?modal_id="+id,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }

    retry = 5
    for attempt in range(retry):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            if attempt == retry - 1:
                raise
            print(f"Request failed. Retrying... (Attempt {attempt + 1}/{retry})")
            time.sleep(1)

    if response.status_code == 200:
        try:
            comments_data = response.json()

            # Assuming comments are in a list under a specific key, e.g., 'comments'
            # comments = comments_data.get('comments', [])

            # Function to extract only the highest resolution image URLs
            def get_highest_resolution_image_urls(comments_data):
                avatar_urls = []
                cover_urls = []
                comment_image_urls = []
                sticker_urls = []

                for comment in comments_data.get('comments', []):
                    # Extract only the 'avatar_larger' from the user field
                    user = comment.get('user', {})
                    avatar_larger = user.get('avatar_larger', {})
                    avatar_urls.extend(avatar_larger.get('url_list', []))

                    # # Extract only the first 'cover_url' assuming it's the highest resolution
                    # cover_list = user.get('cover_url', [])
                    # if cover_list:
                    #     first_cover = cover_list[0]
                    #     cover_urls.extend(first_cover.get('url_list', []))
                    #
                    # # Extract only the 'origin_url' from image_list
                    # image_list = comment.get('image_list', [])
                    # if image_list:
                    #     for image in image_list:
                    #         origin_url_obj = image.get('origin_url', {})
                    #         print('ewqeqw', )
                    #         a = [origin_url_obj.get('url_list', [])[0]]
                    #         comment_image_urls.extend(a)

                    # Extract only the 'animate_url' from sticker if available, else 'static_url'
                    sticker = comment.get('sticker', {})
                    if sticker:
                        animate_url_obj = sticker.get('animate_url', {})
                        static_url_obj = sticker.get('static_url', {})
                        if animate_url_obj.get('url_list'):
                            a = [animate_url_obj.get('url_list', [])[0]]
                            sticker_urls.extend(a)
                        elif static_url_obj.get('url_list'):
                            a = [static_url_obj.get('url_list', [])[0]]
                            sticker_urls.extend(a)

                # Remove duplicates by converting to sets
                avatar_urls = list(set(avatar_urls))
                cover_urls = list(set(cover_urls))
                comment_image_urls = list(set(comment_image_urls))
                sticker_urls = list(set(sticker_urls))

                return avatar_urls, cover_urls, comment_image_urls, sticker_urls

            # Extract image URLs
            avatar_urls, cover_urls, comment_image_urls, sticker_urls = get_highest_resolution_image_urls(comments_data)

            # # Display the results
            # if avatar_urls:
            #     print("Avatar Image URLs:")
            #     for url in avatar_urls:
            #         print(url)
            # else:
            #     print("No Avatar URLs found.")

            # if cover_urls:
            #     print("\nCover Image URLs:")
            #     for url in cover_urls:
            #         print(url)
            # else:
            #     print("\nNo Cover URLs found.")

            if comment_image_urls:
                print("\nComment Image URLs:")
                for url in comment_image_urls:
                    print('process:',url)
            else:
                print("\nNo Comment Image URLs found.")


            if sticker_urls:
                print("\nSticker URLs:")
                for url in sticker_urls:
                    print(url)
            else:
                print("\nNo Sticker URLs found.")

            if comment_image_urls:
                channel_id = 2238825797
                for url in comment_image_urls:
                    print(url)
                    caption = f'{title}\n`{video_url}`'
                    send_photo_to_telegram(client,url,caption)


            if sticker_urls:
                channel_id = 2484441083

                for url in sticker_urls:
                    print('process:',url)
                    caption = f'{title}\n`{video_url}`'
                    send_photo_to_telegram(client,url,caption)
        except ValueError:
            print("Error decoding JSON response.")
    else:
        print(f"Request failed with status code: {response.status_code}")
import json
import time

import requests
from bs4 import BeautifulSoup
import html
import re



def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def sanitize_comment(text):
    unescaped_text = html.unescape(text)
    clean_text = remove_html_tags(unescaped_text)
    return clean_text



def fetch_discover_page():
    url = "https://www.douyin.com/aweme/v1/web/module/feed/"

    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "module_id": "3003101",
        "count": "20",
        "filterGids": "",
        "presented_ids": "",
        "refresh_index": "25",
        "refer_id": "",
        "refer_type": "10",
        "awemePcRecRawData": '{"is_client":false}',
        "Seo-Flag": "0",
        "install_time": "1727422146",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "update_version_code": "170400",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1536",
        "screen_height": "864",
        "browser_language": "en-US",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "129.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "129.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "12",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "0",
        "webid": "7419221520197813775",
        "msToken": "iV89AIFWCmHjfnuurbPwS3Xr2OW7lJnFvEYes4Y0YVrRVbYnaF4ZhJ6Kv1CM1WzvRm3uLuiiJ4lba4VASD78i6W_Opzf0wKeOhfofU2utj3VKaPeyWCJXx6nD4Wrnt7wEP26D57NBp-TBKqtGR0CyVtqEl3w_IOeIFtHanx6WPKf",
        "a_bogus": "x74fhqULdx5ccdMtuKDxyfnlRADlNsWygBTKWFqPtNFabwMaOWNhdacAJxuEWz-v08pwiKBH6xe/TEdbFtU0Ze3kqmpDu0USF4/IVW8L/qqgGUG/gqguS8Wzqw0C0QkNlQCRi10R1sMN2VnRVN58AQpGH5zHQ5EgWqp5p2G9rDC8pPgTVo2SCcwAPXL=",
        "verifyFp": "verify_m1ww0lc1_WErDEBN7_LQz7_4lSd_8z1p_FpKULeDa7GS0",
        "fp": "verify_m1ww0lc1_WErDEBN7_LQz7_4lSd_8z1p_FpKULeDa7GS0"
    }

    headers = {
        "Host": "www.douyin.com",
        "Cookie": "passport_csrf_token=ce2899cf0db8e28f536a916926058827; passport_csrf_token_default=ce2899cf0db8e28f536a916926058827; bd_ticket_guard_client_web_domain=2; ttwid=1%7CMC21H_Mb9j8lH93LOkm_gOyxE3cU7HtZXKUpG1phEbM%7C1727422146%7C04dc408bf8b9f8b55a761b8633aab797cb5128184e74ffa59b4e6cdd87296117; UIFID_TEMP=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457b8f515a834c0ecc82c067d8fdd1324eb4a99188a749a44932052656d06410109c01a81f2c385f9b9b6b4206b6608e709a; douyin.com; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; hevc_supported=true; dy_swidth=1536; dy_sheight=864; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; strategyABtestKey=%221728177082.495%22; csrf_session_id=83c6a7ca445e31b3a1ff0364a03034fd; s_v_web_id=verify_m1ww0lc1_WErDEBN7_LQz7_4lSd_8z1p_FpKULeDa7GS0; xgplayer_user_id=698235855467; fpk1=U2FsdGVkX1++wLBFbf601U9z1ywdiNB0SSlbBqwSPlw+vrWb6reDbn2f11P1XXDyn/2OeBAbVMKZLMtE+WotAA==; fpk2=16453d6e2683b8800ded2a27c7f595d9; xg_device_score=7.802204888412783; UIFID=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457b8f515a834c0ecc82c067d8fdd1324eb4c72f64efa21a94d2ae050846e3eb429c598d53baad272932c8eaa3caa0a1dba103b639401e91c7628eb6c4afecdce9f5bd7398c5a047b9d24c07f360eb315b21cff795b8749ef8c6ed8ddf6a859afabfcaa988995721fa1fb45bb451767ec21c462afdf5c924d2bde65f61cee949818d; WallpaperGuide=%7B%22showTime%22%3A1728179415811%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A10%2C%22cursor2%22%3A2%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; n_mh=irBzyV0OuesE-LvbiK2AKUGQ9n8jO5mZ-mXHcPoPPAI; passport_auth_status=25087fac42d958f101760ff3181b7d79%2C; passport_auth_status_ss=25087fac42d958f101760ff3181b7d79%2C; is_staff_user=false; SelfTabRedDotControl=%5B%5D; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAnosb7IbnjdIciThilRveH9Gw8nMIBwM4eav286PjdqyYdtRuJtNG5RuPJ5f6eUn9%2F1728230400000%2F0%2F1728180523540%2F0%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=767d87166269e7abc7350c72ea491549; __security_server_data_status=1; publish_badge_show_info=%220%2C0%2C0%2C1728180529085%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAnosb7IbnjdIciThilRveH9Gw8nMIBwM4eav286PjdqyYdtRuJtNG5RuPJ5f6eUn9%2F1728230400000%2F0%2F1728180850981%2F0%22; my_rd=2; store-region=cn-hk; store-region-src=uid; sid_guard=b755863ed8e1722e9f61407f33363362%7C1728180858%7C21600%7CSun%2C+06-Oct-2024+08%3A14%3A18+GMT; uid_tt=93904a238516c74418884073ae75b72b; uid_tt_ss=93904a238516c74418884073ae75b72b; sid_tt=b755863ed8e1722e9f61407f33363362; sessionid=b755863ed8e1722e9f61407f33363362; sessionid_ss=b755863ed8e1722e9f61407f33363362; sid_ucp_v1=1.0.0-KDA1YmZiZGNlODAxYTExZWNmNjc3NjdmYTMxMjY4YmJlNzIzZmM0MGMKCBD65Ie4BhgNGgJscSIgYjc1NTg2M2VkOGUxNzIyZTlmNjE0MDdmMzMzNjMzNjI; ssid_ucp_v1=1.0.0-KDA1YmZiZGNlODAxYTExZWNmNjc3NjdmYTMxMjY4YmJlNzIzZmM0MGMKCBD65Ie4BhgNGgJscSIgYjc1NTg2M2VkOGUxNzIyZTlmNjE0MDdmMzMzNjMzNjI; odin_tt=4f313cf84e205d15934f6b2ca0533efac640df3407a77e511daf045c59d25cfb4a1c0b823a76152f95b02236d50700b36cd11d2dfff648941d6bee9b9ad1b0a73a8c35a4579549e95a46f2b6529bb893; download_guide=%223%2F20241006%2F0%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; xgplayer_device_id=55353321124; __ac_signature=_02B4Z6wo00f01b8F4cgAAIDDuK.Ubu1XWY2.JeVAAAjE57; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; _waftokenid=eyJ2Ijp7ImEiOiJYSWVpSDh1QlpQZk1yanc2YW5BanJ3TG5Wc3ByUVpEbmdJOUFoNXdHMVZrPSIsImIiOjE3MjgxODczNjEsImMiOiJ0QW1JTklpcGhWRVpKYStQUXRTYkg3MytHbnZjdnM1NktJUlpnSE1xL1A0PSJ9LCJzIjoiaTNvUFZsVVhHcm0zYURjcEs5bkdVZzFQZkFwL1BWSnpBMnV2NjF4cC9BYz0ifQ; IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTU5jWGhnQmFXYlBuaWxXL1A5RE9tRm82NEh4WWozU0l2b3ZQejNqRWVJWldUWGFyN2VkNmYwVDZFdmJBU0dZMEdZbnE2dHhzazFHQU41QzU2YnFsUmc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; biz_trace_id=35f13486",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "X-Secsdk-Csrf-Token": "0001000000015d96e3a9dd7d1f3f4efcadf8cbb517376a6edaed4d5fdf9c18f41df1b9857e9817fbc1408dc7efe3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Origin": "https://www.douyin.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.douyin.com/discover",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }

    try:
        response = requests.post(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching the discover page: {e}")
        return None



def sanitize_text(text):
    """
    Unescape HTML entities and remove HTML tags.
    """
    unescaped_text = html.unescape(text)
    clean_text = remove_html_tags(unescaped_text)
    return clean_text


def main():
    global client
    try:
        client = TelegramClient('justforfun_session2', api_id, api_hash)
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

    html_content = fetch_discover_page()
    if html_content:
        # print(str(html_content))
        meta_data = re.findall(r'aweme_id":"(\d+)","desc":"(.*?)"', str(html_content))
        # print(meta_data)
        for data in meta_data:
            video_url = 'https://www.douyin.com/video/'+data[0]
            id = data[0]
            title = data[1]
            print(video_url,title)
            get_image(id, title, video_url)
            # process_thread(video_url,title)
    else:
        print("Failed to fetch discover page")

    # Disconnect Telegram client
    client.disconnect()

if __name__ == "__main__":
    while True:
        main()
