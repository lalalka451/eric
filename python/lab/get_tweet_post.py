import requests
import json
from urllib.parse import urlencode

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
        "Referer": "https://x.com/elonmusk/status/1844613994709217467",
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
            # 'URL': url,  # Include the expanded URL
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
    instructions = json_data.get('data', {}).get('threaded_conversation_with_injections_v2', {}).get('instructions', [])

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

tweet_data = get_tweet_detail("1844252753763402157")
# print(tweet_data)
extracted_tweets = parse_twitter_json(tweet_data)
# Print tweets with media and video URLs
for tweet in extracted_tweets:
    # print(tweet)
    comment = tweet.get('Post Comment')
    media_urls = tweet.get('Media URLs')
    print(comment)
    print(media_urls)

