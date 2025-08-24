import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

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
        # time.sleep(3)
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




def get_user_by_screen_name(screen_name):
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

import requests
import json
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

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"


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

x_guest_token = get_x_guest_token()
# x_guest_token = str(1846380511582998872)

user_name = "michaelwong666"
# user_name = "https://x.com/1cedev_"
# Example usage
user_data = get_user_by_screen_name(user_name)
# print(user_data)
# Extract the user ID from the response
user_id = user_data['data']['user']['result']['rest_id']
print(f"Extracted user ID: {user_id}")


# Example usage
user_tweets = fetch_user_tweets(user_id)
print(json.dumps(user_tweets, indent=2))
tweets_with_media = parse_twitter_user_timeline(user_tweets)
print(tweets_with_media)





