import json
import requests
from datetime import datetime


base_header = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
}

def request_followers(user_id, cursor=None, count=50):
    variables = {
        "userId": user_id,
        "count": count,
        "includePromotedContent": False
    }
    if cursor:
        variables["cursor"] = cursor

    features = {
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "tweetypie_unmention_optimization_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": False,
        "tweet_awards_web_tipping_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_media_download_video_enabled": False,
        "responsive_web_enhance_cards_enabled": False
    }

    url = f"https://twitter.com/i/api/graphql/OLcddmNLPVXGDgSdSVj0ow/Following"
    params = {
        "variables": json.dumps(variables),
        "features": json.dumps(features)
    }

    header_set = {
        "auth_token": "18fa9bfd558e65264f811dec9a4d8cf4c83309d3",
        "ct0": "40806c379e842c2df25b4e8bd47d43647825e80cfc47ada9525c27dc002011eb58d2bb0a8414c19592d2ee306fa61dcae2a4cfde30dd5fd98bc2e2fec1ebebe2dc1747c7aa1ee44b8237fd3829aa2c60"
    }
    headers = base_header.copy()
    headers.update({
        "Cookie": f"auth_token={header_set['auth_token']}; ct0={header_set['ct0']}",
        "X-Csrf-Token": header_set['ct0'],
    })


    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        followers = []
        next_cursor = None

        instructions = data['data']['user']['result']['timeline']['timeline']['instructions']
        for instruction in instructions:
            if instruction['type'] == 'TimelineAddEntries':
                for entry in instruction['entries']:
                    if 'user-' in entry['entryId']:
                        user_result = entry['content']['itemContent']['user_results']['result']
                        if not user_result:
                            print(f"user_results is empty: {entry}")
                            continue

                        legacy = user_result['legacy']
                        follower = {
                            "name": legacy['name'],
                            "user_name": legacy['screen_name'],
                            "user_id": user_result['rest_id'],
                            "can_dm": legacy['can_dm'],
                            "created_at": datetime.strptime(legacy['created_at'], '%a %b %d %H:%M:%S +0000 %Y').isoformat(),
                            "bio": legacy['description'],
                            "tweets_count": legacy['statuses_count'],
                            "followers_count": legacy['followers_count'],
                            "following_count": legacy['friends_count'],
                            "favourites_count": legacy['favourites_count'],
                            "location": legacy['location'],
                            "media_count": legacy['media_count'],
                            "profile_url": f"https://twitter.com/{legacy['screen_name']}",
                            "profile_banner_url": legacy.get('profile_banner_url'),
                            "avatar_url": legacy['profile_image_url_https'],
                            "verified": legacy['verified'],
                            "is_blue_verified": user_result['is_blue_verified']
                        }
                        followers.append(follower)
                    elif 'cursor-bottom-' in entry['entryId']:
                        next_cursor = entry['content']['value']

        print("exportedUserArray", followers)
        if next_cursor:
            cursor_parts = next_cursor.split("|")
            next_cursor = cursor_parts[0]
        return followers, next_cursor
    else:
        print(f"Error: {response.status_code}")
        return None, None

# Usage example:
followers, next_cursor = request_followers("shichuan5024")
print(f"Followers: {followers}")
print(f"Next cursor: {next_cursor}")
