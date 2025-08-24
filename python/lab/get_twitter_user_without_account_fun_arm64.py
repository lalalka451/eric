import requests
import json
import urllib.parse

import schedule

from baseHandler import BaseHandler
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

channel_id = 2339485461
db_name = 'twitter_fun'
x_guest_token = str(12345678)


def get_x_guest_token():
    # Set up Chrome options (optional: for headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify the path to chromedriver
    service = Service('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)


    try:
        # Navigate to the specified URL
        driver.get("https://x.com/patrici00662047")

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)

        # Get all cookies
        cookies = driver.get_cookies()
        print(cookies)
        print(cookies[0]['value'])
        guest_token = cookies[0]['value']

        if guest_token:
            print(f"X-Guest-Token: {guest_token}")
            return guest_token
        else:
            print("X-Guest-Token not found in cookies")
            return None
    finally:
        driver.quit()

def refresh_guest_token():
    global x_guest_token
    x_guest_token = get_x_guest_token()


def parse_twitter_user_timeline(user_tweets):
    tweets_with_media = []

    # Navigate to the instructions containing tweet entries
    instructions = user_tweets.get('data', {}).get('user', {}).get('result', {}) \
        .get('timeline_v2', {}).get('timeline', {}).get('instructions', [])

    for instruction in instructions:
        if instruction.get('type') == 'TimelineAddEntries':
            entries = instruction.get('entries', [])
            for entry in entries:
                content = entry.get('content', {})
                item_content = content.get('itemContent', {})

                if item_content.get('itemType') == 'TimelineTweet':
                    tweet = item_content.get('tweet_results', {}).get('result', {})
                    legacy = tweet.get('legacy', {})
                    tweet_id = legacy.get('id_str')
                    text = legacy.get('full_text', '')

                    # Initialize media URLs list
                    media_urls = []

                    # Check for extended_entities and media
                    extended_entities = legacy.get('extended_entities', {})
                    media = extended_entities.get('media', [])

                    for m in media:
                        media_type = m.get('type')
                        if media_type == 'photo':
                            media_url = m.get('media_url_https')
                            if media_url:
                                media_urls.append(media_url)
                        elif media_type in ['video', 'animated_gif']:
                            variants = m.get('video_info', {}).get('variants', [])
                            # Select the MP4 variant with the highest bitrate
                            mp4_variants = [v for v in variants if v.get('content_type') == 'video/mp4']
                            if mp4_variants:
                                # Sort by bitrate descending and select the highest
                                mp4_variants.sort(key=lambda x: x.get('bitrate', 0), reverse=True)
                                media_url = mp4_variants[0].get('url')
                                if media_url:
                                    media_urls.append(media_url)

                    if media_urls:
                        tweets_with_media.append({
                            'tweet_id': tweet_id,
                            'text': text,
                            'media_urls': media_urls
                        })

    return tweets_with_media


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
        tweet['video_thumb'] = None  # Initialize video_thumb to None

        for item in media:
            if item.get('type') == 'video':
                variants = item.get('video_info', {}).get('variants', [])
                best_variant = max(variants, key=lambda x: x.get('bitrate', 0), default={})
                tweet['videos'].append(best_variant.get('url'))
                tweet['video_thumb'] = item.get('media_url_https')

        return tweet

    except (KeyError, AttributeError) as e:
        print("Error extracting data:", e)
        return None  # Return None if extraction fails


import random
import string
import time

def generate_random_cookie():
    # Helper function to generate random alphanumeric string
    def random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Generate random timestamp (within a reasonable range)
    timestamp = int(time.time() * 1000000) + random.randint(-1000000, 1000000)

    # Generate random 19-digit number for gt
    gt = ''.join(random.choices(string.digits, k=19))

    # Generate random base64-encoded string for personalization_id
    personalization_id = random_string(22)

    cookie = f"night_mode=2; kdt={random_string(30)}; dnt=1; att=1-{random_string(30)}; " \
             f"guest_id=v1%3A{timestamp}; guest_id_marketing=v1%3A{timestamp}; " \
             f"guest_id_ads=v1%3A{timestamp}; gt={gt}; " \
             f'personalization_id="v1_{personalization_id}=="'

    return cookie


def fetch_user_tweets(user_id, count=20):
    global x_guest_token
    url = "https://api.x.com/graphql/Tg82Ez_kxVaJf7OPbUdbCg/UserTweets"

    variables = {
        "userId": user_id,
        "count": count,
        "includePromotedContent": True,
        "withQuickPromoteEligibilityTweetFields": True,
        "withVoice": True,
        "withV2Timeline": True
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
        "withArticlePlainText": False
    }

    params = {
        "variables": json.dumps(variables),
        "features": json.dumps(features),
        "fieldToggles": json.dumps(field_toggles)
    }

    headers = {
        "Host": "api.x.com",
        "Cookie": generate_random_cookie(),
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "X-Guest-Token": x_guest_token,
        "X-Twitter-Client-Language": "en",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Twitter-Active-User": "yes",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://x.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://x.com/",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }

    response = requests.get(url, params=params, headers=headers)

    return response

def get_user_media(user_id, count=20):
    global x_guest_token
    response = fetch_user_tweets(user_id)

    # if response.status_code == 200:
    #     try:
    tweets = parse_twitter_user_timeline(response.json())
    print(tweets)
        # except:
        #     print(response)
        #     print(response.text)
        #     return None
    return tweets
    # elif response.status_code == 429:
    #     x_guest_token = refresh_guest_token()
    #     response = fetch_user_tweets(user_id)
    #     print(response)
    #     print(response.text)
    #     tweets = parse_twitter_user_timeline(response.json())
    #     print('parse_twitter_user_timeline',len(tweets))
    # else:
    #     return None


def format_tweet_caption(tweet):
    """Formats tweet text and adds tweet URL."""
    tweet_url = f"https://x.com/123/status/{tweet['tweet_id']}"
    caption = f"{tweet['text']}\n`{tweet_url}`"
    return caption


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
        """
        Fetches media from the specified Twitter user and sends it to Telegram.
        """
        tweets_data = None
        for i in range(3):
            try:
                tweets_data = get_user_media(self.user_id, self.count)
                break
            except Exception as e:
                print(f'Error: tweets_data. Skipping...')
                refresh_guest_token()
                continue
        if not tweets_data:
            print("No tweets data fetched.")
            return
        for tweet in tweets_data:
            print(tweet)
            tweet_id = tweet.get('tweet_id')
            media_urls = tweet.get('media_urls', [])

            if not media_urls:
                print(f"No media found in tweet {tweet_id}. Skipping.")
                continue

            # Use the format_tweet_caption function to create the caption
            caption = format_tweet_caption(tweet)
            for media_url in media_urls:
                if self.db_handle.url_exists(tweet_id, media_url):
                    print(f"Media {media_url} already exists in tweet {tweet_id}. Skipping.")
                    continue
                if media_url.endswith(('.jpg', '.png', '.gif')):
                    success = self.send_photo_to_telegram(media_url, caption)
                    if success:
                        self.db_handle.insert_url(tweet_id, media_url)
                        print(f"Photo from tweet {tweet_id} sent successfully.")
                    else:
                        print(f"Failed to send photo from tweet {tweet_id}.")
                elif media_url.endswith('.mp4'):
                    success = self.send_video_to_telegram(media_url, caption)
                    if success:
                        self.db_handle.insert_url(tweet_id, media_url)
                        print(f"Video from tweet {tweet_id} sent successfully.")
                    else:
                        print(f"Failed to send video from tweet {tweet_id}.")
                else:
                    print(f"Unsupported media type for URL: {media_url}")

    def run(self):
        """
        Executes the media fetching and sending process.
        """
        self.fetch_and_send_media()
        self.disconnect_telegram()


import requests


def fetch_profile_spotlights(screen_name):
    global x_guest_token
    url = "https://api.x.com/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName"

    params = {
        "variables": f'{{"screen_name":"{screen_name}"}}',
        "features": '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        "fieldToggles": '{"withAuxiliaryUserLabels":false}'
    }

    headers = {
        "Host": "api.x.com",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "X-Guest-Token": x_guest_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()


if __name__ == "__main__":
    load_dotenv()

    channel_id = 2339485461
    db_name = 'twitter_fun'
    session = 'twitter_fun_session'

    twitter_users = [
       'hsn8086',
        'UnzipHelper',

    ]
    twitter_users = list(set(twitter_users))


    def main():

        for twitter_user in twitter_users:
            for i in range(3):
                try:
                    result = fetch_profile_spotlights(twitter_user)
                    rest_id = result['data']['user']['result']['rest_id']
                    print(f'User: {twitter_user}, rest_id: {rest_id}')
                    break
                except Exception as e:
                    print(f'Error: Unable to fetch rest_id for user {twitter_user}. Skipping...')
                    refresh_guest_token()
                    continue
            USER_ID = rest_id
            handler = TwitterUserHandler(channel_id=channel_id, db_name=db_name, telegram_session=session,
                                         user_id=USER_ID)
            handler.run()


    main()
    schedule.every(1).hours.do(main)
    while True:
        schedule.run_pending()

