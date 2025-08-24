import json
import re

import requests
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
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

# Create a directory to save media files
MEDIA_DIR = 'media'
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

db_handle = db_handler('twitter', 'media')
db_handle.create_database()
db_handle2 = db_handler('twitter_user_name', 'media')
db_handle2.create_database()

# 10 mb
def download_video_file(url, path, max_size=10*1024*1024):
    """
    Downloads a file from a URL and saves it to the specified path.
    If the content length exceeds max_size (default 10MB), the download is aborted.

    Parameters:
    - url (str): The URL of the file to download.
    - path (str): The local file path where the file will be saved.
    - max_size (int): Maximum allowed file size in bytes (default is 10MB).

    Returns:
    - bool: True if download succeeds, False otherwise.
    """
    try:
        # Initiate the GET request with streaming enabled
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes

        # Retrieve the Content-Length from headers
        content_length = response.headers.get('Content-Length')

        if content_length is not None:
            content_length = int(content_length)
            if content_length > max_size:
                print(f"Aborted: File size {content_length} bytes exceeds the 10MB limit.")
                return False
        else:
            print("Warning: Content-Length header is missing. Proceeding with download.")

        # Proceed to download the file in chunks
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)

        print(f"Downloaded successfully: {path}")
        return True

    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
channel_id = 2280520430

def parse_twitter_home_timeline(json_data):
    """Parses Twitter home timeline JSON and extracts tweet info."""
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        else:
            return []

        tweets = []
        instructions = data.get('data', {}).get('home', {}).get('home_timeline_urt', {}).get('instructions', [])

        for instruction in instructions:
            if instruction.get('type') == 'TimelineAddEntries':
                entries = instruction.get('entries', [])
                for entry in entries:
                    if entry.get('content', {}).get('entryType') == 'TimelineTimelineItem':
                         # Check if it's a Tweet, not a Community or other item type
                        if entry.get("content", {}).get("itemContent", {}).get("itemType") == "TimelineTweet":
                            item_content = entry['content']['itemContent']
                            tweet_results = item_content.get('tweet_results', {})  # Handle missing 'tweet_results'
                            if 'result' in tweet_results: #make sure there's a result before accessing it
                                tweet_data = tweet_results['result']

                                #Extract tweet
                                tweet = extract_tweet(tweet_data)
                                if tweet: #only add tweet if successfully extracted
                                    tweets.append(tweet)

        return tweets


    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON: {e}")
        return []


def extract_tweet(tweet_data):
    """Extract tweet from tweet_data"""
    tweet = {}
    try:
        tweet['tweet_id'] = tweet_data.get('rest_id')
        tweet['text'] = tweet_data.get('legacy', {}).get('full_text')
        tweet['created_at'] = tweet_data.get('legacy', {}).get('created_at')
        user = tweet_data.get('core', {}).get('user_results', {}).get('result', {})

        tweet['user_id'] = user.get('rest_id')
        tweet['username'] = user.get('legacy', {}).get('screen_name')
        tweet['name'] = user.get('legacy', {}).get('name')


        extended_entities = tweet_data.get('legacy', {}).get('extended_entities', {})
        media = extended_entities.get('media', [])

        tweet['images'] = [item.get('media_url_https') for item in media if item.get('type') == 'photo']
        tweet['videos'] = []
        tweet['video_thumb'] = None # Initialize video_thumb to None


        for item in media:
            if item.get('type') == 'video':
                variants = item.get('video_info', {}).get('variants', [])
                best_variant = max(variants, key=lambda x: x.get('bitrate', 0), default={})
                tweet['videos'].append(best_variant.get('url'))
                tweet['video_thumb'] = item.get('media_url_https')


        return tweet


    except (KeyError, AttributeError) as e:
        print("error extract data", e)


# Example usage with the provided API request
import requests
import json


# fail
headers = {
    "Cookie": "night_mode=2; kdt=ZoKSTEV0UsygL0Pba7zO5Tl4Dj8XyGag5V7BQp7w; g_state={\"i_l\":0}; dnt=1; guest_id=v1%3A172906336420847210; gt=1846451695322325253; _twitter_sess=BAh7BiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7AA%253D%253D--1164b91ac812d853b877e93ddb612b7471bebc74; auth_token=b3fe53777f9e005c489c34eec138631f419c5a3c; ct0=6717b1626fd03e43696941838b8eb6ecf355ce60aae7f7bc310f330d87430e7b09e2131482ddf0c94f9ab53f08066dffbd5e2c97d57e1d4d032e8c75a69c928b6ccd37c6991775f2bb08045dd6c946d5; lang=en; twid=u%3D1845291314038145024; att=1-yavOWSK4EC8JCMahDuiEUPttZGbE70BddLf3ezks",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "X-Csrf-Token": "6717b1626fd03e43696941838b8eb6ecf355ce60aae7f7bc310f330d87430e7b09e2131482ddf0c94f9ab53f08066dffbd5e2c97d57e1d4d032e8c75a69c928b6ccd37c6991775f2bb08045dd6c946d5",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",

}



other_headers = [
    # @tatafa112157
    {
        "auth_token": "984d40ba28798a4008ee6972f543cf49d4be88e8",
        "ct0": "d1ea7ac110c79812a538957cc4c6bfec0435672a2cf1caa2fd2a37ab9fcae02fb62a79e6e70266ce81761ad7ac7e13ba699308f906b2597388f4f87ae0fd88473b937519f9ed005bd519ad5936823c97",
    },
    # @HerekSilbe96611
    {
        "auth_token": "34cb6f16c9e36fd2b78a188ea3097d01be1d050a",
        "ct0": "497ab9a3deee698d1af8ce0309fa134c1945801027b2c9c9295a30e94288e0809a08fc522e5b960670f8fadd524bc463b4166aab8730c6152976b93df5aae4f8000d2f62a2c82d8d8304cb524e4d4b8d",
    },
    # eric21516693724
    # tatafa2234@gmail.com
    {
        "auth_token": "984d40ba28798a4008ee6972f543cf49d4be88e8",
        "ct0": "d1ea7ac110c79812a538957cc4c6bfec0435672a2cf1caa2fd2a37ab9fcae02fb62a79e6e70266ce81761ad7ac7e13ba699308f906b2597388f4f87ae0fd88473b937519f9ed005bd519ad5936823c97",
    },
    # ffsaf261920
    # rqwrwqrwq2@outlook.com
    {
        "auth_token": "34cb6f16c9e36fd2b78a188ea3097d01be1d050a",
        "ct0": "497ab9a3deee698d1af8ce0309fa134c1945801027b2c9c9295a30e94288e0809a08fc522e5b960670f8fadd524bc463b4166aab8730c6152976b93df5aae4f8000d2f62a2c82d8d8304cb524e4d4b8d",
    },
    # ffsaf261920
    # rqwrwqrwq2@outlook.com
    {
        "auth_token": "eb03c1e5aa93b597f2ab9a7fb75f3616db014ed4",
        "ct0": "0a19aa7d34a436b9630fc46b6a385cf40efb512bdb614d537b888be5682d4264cba73454d4b62ff5dad579f8f217387d5c1dd08ded473407d70ae3deeb3881cfaed883ce93c3920c1a0871cc9353e740",
    },
    # @deswfqw89664
    # rwqtawrw@outlook.com
    {
        "auth_token": "43c51f3e94de8c428e3447242d51afa8d01b0fd6",
        "ct0": "cd62332d167e71fdb893049e487bfc3a49f3ae7d76867af3870755e90ad90cd59ee397f30a5b577a7b5e37f72ae5630b9f9065623b93d3b619fde7b497fa4bec1cca0d81c34797d9488571e597ba65df",
    },

    # @rdudu268799
    # fueqq23fdas@outlook.com
    {
        "auth_token": "eacd53188877239ca8dea73c4f33424c397dcf48",
        "ct0": "8fb5ac453d0d212e9d002d13f3a8189c8d6b352f8ac0dac7c6b09a5e31cb59ac859b68dba5c8b34f6e88e68efa1eb79b8af2f7bc00900dec3c91152c9fbe5952b0eef5a38dd68a6f7c3d22d47f5846bc",
    },
    #@dsafww190922
    {
        "auth_token": "1c422d26cf2913bcadb439ba5382aef5114b9346",
        "ct0": "b23f9e8f125ab32b74a2c6857fde7f8def9e3055b60fa06727e2688a883b73000ce38ea28fb4d83bc6bea57f653df7d34812c2a9c8bb2688a7b90663c1cfa27186fccfc97b2801db8ebd38b61b591b2f",
    },
]



def get_tweet_detail(tweet_id):
    base_url = "https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail"

    variables = {
        "focalTweetId": tweet_id,
        "with_rux_injections": False,
        "rankingMode": "Relevance",
        "includePromotedContent": True,
        "withCommunity": True,
        "withQuickPromoteEligibilityTweetFields": True,
        "withBirdwatchNotes": True,
        "withVoice": True
    }

    features = {
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_enhance_cards_enabled": False
    }

    field_toggles = {
        "withArticleRichContentState": True,
        "withArticlePlainText": False,
        "withGrokAnalyze": False,
        "withDisallowedReplyControls": False
    }

    params = {
        "variables": json.dumps(variables),
        "features": json.dumps(features),
        "fieldToggles": json.dumps(field_toggles)
    }

    url = f"{base_url}?{urlencode(params)}"

    headers = {
        "Cookie": "guest_id=v1%3A172863372811688527; night_mode=2; guest_id_marketing=v1%3A172863372811688527; guest_id_ads=v1%3A172863372811688527; personalization_id=\"v1_UiYpJQE0fF5AS9+CO7bCUg==\"; gt=1844649678610251785; kdt=Q1nmbJaOf1sUH65qFVhpkRKe412NV0TUomNDVjx3; auth_token=be8fb704baf6c6b524b65855b544394c224fc7fa; ct0=3e3cc34e7d4b7c3521967ce95536c1fb0864cc654af43f93e14e45611d54d89410281a7891665003dfc615eff45c23d650bb2cc016954e029ba3e144e3f02e34f8ae421ad20946c6d769228f3ad06941; att=1-5bYqulV75itqPFF1qkQjPL3x9rCnsHPKELYPkOQU; twid=u%3D1842850005134254080; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; lang=en",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "X-Csrf-Token": "3e3cc34e7d4b7c3521967ce95536c1fb0864cc654af43f93e14e45611d54d89410281a7891665003dfc615eff45c23d650bb2cc016954e029ba3e144e3f02e34f8ae421ad20946c6d769228f3ad06941",
        "X-Client-Uuid": "330af735-6b27-4b00-b12e-46f3cca08423",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "X-Twitter-Client-Language": "en",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Twitter-Active-User": "no",
        "X-Client-Transaction-Id": "kbZRLPCtcdbzJqXohrMXMetGoy2pn3jVnf1N2o4mgR2B/CdhtTdpanH+GOPD23b8brIaKJMRdSjQHihAYWyp1C8fvfUYkg",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://x.com/elonmusk/status/"+tweet_id,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def extract_tweet_info(tweet):
    """
    Extracts relevant information from a single tweet object.
    """
    tweet_id = tweet.get('rest_id', '')

    # Extract user information
    user_info = tweet.get('core', {}).get('user_results', {}).get('result', {})
    user_id = user_info.get('rest_id', '')
    user_name = user_info.get('legacy', {}).get('screen_name', '')

    # Extract post text
    post_text = tweet.get('legacy', {}).get('full_text', '')

    # Extract URLs
    urls = tweet.get('legacy', {}).get('entities', {}).get('urls', [])
    url = urls[0]['expanded_url'] if urls else ''

    # Extract Media URLs (Images and Videos)
    media = tweet.get('legacy', {}).get('extended_entities', {}).get('media', [])
    media_urls = []
    if media:
        for m in media:
            if m.get('type') == 'photo':
                media_urls.append(m.get('media_url_https', ''))
            elif m.get('type') == 'video':
                variants = m.get('video_info', {}).get('variants', [])
                # Get the highest bitrate video URL (or the first if bitrate isn't available)
                best_variant = max(variants, key=lambda x: x.get('bitrate', 0))
                media_urls.append(best_variant.get('url', ''))

    # Check if the tweet is a reply
    in_reply_to = tweet.get('legacy', {}).get('in_reply_to_user_id_str', '')
    post_comment = ''
    comment_media_urls = []

    if in_reply_to:
        post_comment = post_text
        comment_media_urls = media_urls

    # Only include tweets that have media
    if media_urls:
        return {
            # 'Tweet ID': tweet_id,
            # 'User ID': user_id,
            # 'User Name': user_name,
            # 'Post Text': post_text,
            'Post Comment': post_comment,
            'URL': url,  # Include the expanded URL
            'Media URLs': media_urls,
            # 'Comment Media URLs': '; '.join(comment_media_urls)
        }
    else:
        return None  # Return None if no media is found


def parse_twitter_json(json_data):
    """
    Parses the Twitter JSON data and extracts tweets information, including replies.
    """
    tweets_data = []

    # Navigate through the JSON structure
    instructions = json_data.get('data', {}).get('threaded_conversation_with_injections_v2', {}).get(
        'instructions', [])

    for instruction in instructions:
        if instruction.get('type') != 'TimelineAddEntries':
            continue  # Skip if not adding entries

        entries = instruction.get('entries', [])
        for entry in entries:
            content = entry.get('content', {})
            if not content:
                continue  # Skip if no content

            entry_type = content.get('entryType', '')

            if entry_type == 'TimelineTimelineItem':
                item_content = content.get('itemContent', {})
                if not item_content:
                    continue  # Skip if no itemContent

                item_type = item_content.get('itemType', '')
                if item_type != 'TimelineTweet':
                    continue  # Process only tweets

                tweet = item_content.get('tweet_results', {}).get('result', {})
                if not tweet:
                    continue  # Skip if no tweet data

                tweet_info = extract_tweet_info(tweet)
                if tweet_info:  # Only append if tweet_info is not None
                    tweets_data.append(tweet_info)

            elif entry_type == 'TimelineTimelineModule':
                items = content.get('items', [])
                for item in items:
                    item_content = item.get('item', {}).get('itemContent', {})
                    if not item_content:
                        continue  # Skip if no itemContent

                    item_type = item_content.get('itemType', '')
                    if item_type != 'TimelineTweet':
                        continue  # Process only tweets

                    tweet = item_content.get('tweet_results', {}).get('result', {})
                    if not tweet:
                        continue  # Skip if no tweet data

                    tweet_info = extract_tweet_info(tweet)
                    if tweet_info:  # Only append if tweet_info is not None
                        tweets_data.append(tweet_info)

    return tweets_data



other_headers_index = 0

def get_headers():
    base_header = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    }
    header_set = other_headers[other_headers_index]
    headers = base_header.copy()
    headers.update({
        "Cookie": f"auth_token={header_set['auth_token']}; ct0={header_set['ct0']}",
        "X-Csrf-Token": header_set['ct0']
    })
    return headers

client = ""
cursor = ""



def do_it():
    global client, other_headers_index, cursor
    try:
        client = TelegramClient('twitter_session', api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            print("Telegram client is not authorized. Please authorize the client.")
            return

    except Exception as e:
        print(f"Failed to connect Telegram client: {e}")
        return

    url = "https://x.com/i/api/graphql/HJFjzBgCs16TqxewQOeLNg/HomeTimeline"

    payload = {
        "variables": {
            "count": 40,
            "cursor": cursor,
            "includePromotedContent": True,
            "latestControlAvailable": True,
            "requestContext": "ptr",
            "withCommunity": True,
        },

        "features": {
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        },
        "queryId": "HJFjzBgCs16TqxewQOeLNg"
    }

    print("Sending request to Twitter API...")
    response = requests.post(url, headers=headers, json=payload)
    json_response = response.text
    print(f"Received response from Twitter API. Status code: {response.status_code}")

    def format_tweet_caption(tweet):
        """Formats tweet text and adds tweet URL."""
        tweet_url = f"https://x.com/{tweet['username']}/status/{tweet['tweet_id']}"
        caption = f"{tweet['text']}\n`{tweet_url}`"
        return caption

    def format_tweet_caption_comment(tweet,comment):
        """Formats tweet text and adds tweet URL."""
        tweet_url = f"https://x.com/{tweet['username']}/status/{tweet['tweet_id']}"
        caption = f"{comment}\n`{tweet_url}`"
        return caption

    print("Parsing Twitter home timeline...")
    tweets = parse_twitter_home_timeline(json_response)
    print(f"Found {len(tweets)} tweets")

    while len(tweets) == 0:
        print("Sending request to Twitter API with other account... ",other_headers_index)
        response = requests.post(url, headers=get_headers(), json=payload)
        json_response = response.text
        print(f"Received response from Twitter API. Status code: {response.status_code}")
        print("Parsing Twitter home timeline...")
        tweets = parse_twitter_home_timeline(json_response)
        print(f"Found {len(tweets)} tweets")
        other_headers_index += 1
        if other_headers_index >= len(other_headers):
            other_headers_index = 0
    next_cursor = re.findall(r'cursor-bottom.*?":".*?"value":"(.*?)","cursorType":"Bottom',json_response)
    if next_cursor:
        cursor = next_cursor[0]
        print("next cursor", cursor)
    for tweet in tweets:
        user_name = tweet['username']
        if not db_handle2.thread_id_exists(user_name):
            db_handle2.insert_url(user_name, '')
            print(f"insert into db {user_name}:")
        caption = format_tweet_caption(tweet)
        print(f"\nProcessing tweet {tweet['tweet_id']}:")
        print(f"Caption: {caption}")

        if not db_handle.thread_id_exists(tweet['tweet_id']):
            print("Tweet not found in database. Processing...")
            if tweet['images'] or tweet['videos']:
                for image_url in tweet['images']:
                    print(f"Sending image: {image_url}")
                    if send_photo_to_telegram(client, image_url, caption):
                        print(f"Successfully sent image for tweet {tweet['tweet_id']}")
                        db_handle.insert_url(tweet['tweet_id'], '')
                    else:
                        print(f"Failed to send image for tweet {tweet['tweet_id']}")

                for video_url in tweet['videos']:
                    print(f"Processing video: {video_url}")
                    video_filename = f"video_{tweet['tweet_id']}.mp4"
                    video_path = os.path.join(MEDIA_DIR, video_filename)
                    if download_video_file(video_url, video_path):
                        print(f"Successfully downloaded video for tweet {tweet['tweet_id']}")
                        if send_video_to_telegram(client, video_path, caption):
                            print(f"Successfully sent video for tweet {tweet['tweet_id']}")
                            db_handle.insert_url(tweet['tweet_id'], '')
                        else:
                            print(f"Failed to send video for tweet {tweet['tweet_id']}")
                        cleanup_files(video_path)
                    else:
                        print(f"Failed to download video: {video_url}")


                print(f"Fetching tweet details for tweet ID: {tweet['tweet_id']}")
                tweet_datas = get_tweet_detail(tweet['tweet_id'])
                if not tweet_datas:
                    print(f"No tweet details found for tweet ID: {tweet['tweet_id']}. Skipping.")
                    continue

                extracted_tweets = parse_twitter_json(tweet_datas)
                print(f"Found {len(extracted_tweets)} tweet details for tweet ID: {tweet['tweet_id']}")
                tweet_comment_old = ""
                for index, tweet_data in enumerate(extracted_tweets, 1):
                    print(f"Processing tweet detail {index} of {len(extracted_tweets)}")
                    tweet_comment = tweet_data.get('Post Comment')
                    if not tweet_comment_old:
                        tweet_comment_old = tweet_comment
                    media_urls = tweet_data.get('Media URLs')
                    print(f"Number of media URLs: {len(media_urls)}")
                    if not tweet_comment:
                        print('repeated content',tweet_comment)
                        continue
                    if tweet_comment == tweet_comment_old:
                        print('repeated content old',tweet_comment)
                        continue
                    else:
                        tweet_comment_old = tweet_comment
                    caption = format_tweet_caption_comment(tweet, tweet_comment)
                    if media_urls:
                        print(f"Found {len(media_urls)} media URLs for this tweet detail")
                        for media_url in media_urls:
                            if media_url.endswith('.jpg'):
                                print(f"Sending image: {media_url}")
                                if send_photo_to_telegram(client, media_url, caption):
                                    print(f"Successfully sent image for tweet comment")
                                    # db_handle.insert_url(tweet['tweet_id'], '')
                                else:
                                    print(f"Failed to send image for tweet comment")
                            elif media_url.endswith('.mp4'):
                                print(f"Processing video: {media_url}")
                                video_filename = f"video_comment_{tweet['tweet_id']}.mp4"
                                video_path = os.path.join(MEDIA_DIR, video_filename)
                                if download_video_file(media_url, video_path):
                                    print(f"Successfully downloaded video for tweet comment")
                                    if send_video_to_telegram(client, video_path, caption):
                                        print(f"Successfully sent video for tweet comment")
                                        # db_handle.insert_url(tweet['tweet_id'], '')
                                    else:
                                        print(f"Failed to send video for tweet comment")
                                    cleanup_files(video_path)
                                else:
                                    print(f"Failed to download video: {media_url}")
                            else:
                                print(f"Unsupported media type: {media_url}")
                    else:
                        print("Tweet comment has no media. Skipping.")

            else:
                print("Tweet has no media. Skipping.")
        else:
            print(f"Tweet {tweet['tweet_id']} already exists in database. Skipping.")

print("Starting main loop...")
while True:
    print("Running do_it() function...")
    do_it()
    print("Disconnecting Telegram client...")
    client.disconnect()
    print("Waiting before next iteration...")
    time.sleep(60)  # Wait for 60 seconds before the next iteration

