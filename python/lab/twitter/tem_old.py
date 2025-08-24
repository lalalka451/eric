import json
import requests

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

url = "https://x.com/i/api/graphql/HJFjzBgCs16TqxewQOeLNg/HomeTimeline"

headers = {
    "Cookie": "night_mode=2; personalization_id=\"v1_jk8Mlc61eNWuk9or5hJP7g==\"; kdt=ZoKSTEV0UsygL0Pba7zO5Tl4Dj8XyGag5V7BQp7w; dnt=1; auth_multi=\"1167053222931914752:21cde1e5038945e5a23a103a8762d5dd2a9fbf77\"; auth_token=3638198c22563ddd181f6a98476a0050a18448c7; guest_id_ads=v1%3A172820473395861529; guest_id_marketing=v1%3A172820473395861529; lang=en; guest_id=v1%3A172820473395861529; twid=u%3D1842850005134254080; ct0=1222ad722c2e526e3f1bcfff9cc4d733ecb4f9fc7555fa1ca4afb4440faaeee5f48de4433189900c8a8af0eec59b98735d36a45cd8a464f7fa70492a1d5d71a0cd83463c441d257ce210a47f84773edd",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "X-Csrf-Token": "1222ad722c2e526e3f1bcfff9cc4d733ecb4f9fc7555fa1ca4afb4440faaeee5f48de4433189900c8a8af0eec59b98735d36a45cd8a464f7fa70492a1d5d71a0cd83463c441d257ce210a47f84773edd",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

payload = {
    "variables": {
        "count": 20,
        "includePromotedContent": True,
        "latestControlAvailable": True,
        "requestContext": "launch",
        "withCommunity": True,
        "seenTweetIds": ["1842336056022290584"]
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

response = requests.post(url, headers=headers, json=payload)
json_response = response.text
print(json_response)

tweets = parse_twitter_home_timeline(json_response)

for tweet in tweets:
    print(json.dumps(tweet, indent=2))  # Pretty print each tweet