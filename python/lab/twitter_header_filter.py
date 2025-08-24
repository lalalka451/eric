text = """POST /i/api/graphql/E6AtJXVPtK7nIHAntKc5fA/HomeTimeline HTTP/2
Host: x.com
Cookie: guest_id=v1%3A172863391111633982; night_mode=2; guest_id_marketing=v1%3A172863391111633982; guest_id_ads=v1%3A172863391111633982; gt=1844650445513556275; g_state={"i_l":0}; kdt=rurt4fx9yqSL6Q512DbSeQzCUWwx82ACXYPSzeyk; auth_token=34cb6f16c9e36fd2b78a188ea3097d01be1d050a; ct0=497ab9a3deee698d1af8ce0309fa134c1945801027b2c9c9295a30e94288e0809a08fc522e5b960670f8fadd524bc463b4166aab8730c6152976b93df5aae4f8000d2f62a2c82d8d8304cb524e4d4b8d; lang=en; twid=u%3D1844650618021167104; personalization_id="v1_+As2LtQS2IZnru2BMh5dVg=="
Content-Length: 1408
Sec-Ch-Ua-Platform: "Windows"
Authorization: Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
X-Csrf-Token: 497ab9a3deee698d1af8ce0309fa134c1945801027b2c9c9295a30e94288e0809a08fc522e5b960670f8fadd524bc463b4166aab8730c6152976b93df5aae4f8000d2f62a2c82d8d8304cb524e4d4b8d
Sec-Ch-Ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
X-Twitter-Client-Language: en
Sec-Ch-Ua-Mobile: ?0
X-Twitter-Active-User: yes
X-Client-Transaction-Id: 9+tY6cObY6c7a+sB6cNFupxRXD26NZcQC0qe/uiQdPCoMp2pY4wMnlRuxjNnQYpozE53TvVr2PqUwFqcj6LixGieP89r9A
X-Twitter-Auth-Type: OAuth2Session
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: https://x.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://x.com/home
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Priority: u=1, i

{"variables":{"count":20,"includePromotedContent":true,"latestControlAvailable":true,"requestContext":"launch","withCommunity":true,"seenTweetIds":["1844376559979045128","1844550057242263591"]},"features":{"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false},"queryId":"E6AtJXVPtK7nIHAntKc5fA"}"""



import re

def filter_twitter_headers(text):
    # Find the Cookie header
    cookie_match = re.search(r'Cookie: (.+)', text)
    cookie = cookie_match.group(1) if cookie_match else ''

    # Find the Authorization header
    auth_match = re.search(r'Authorization: (.+)', text)
    authorization = auth_match.group(1) if auth_match else ''

    # Find the X-Csrf-Token header
    csrf_match = re.search(r'X-Csrf-Token: (.+)', text)
    csrf_token = csrf_match.group(1) if csrf_match else ''

    # Find the User-Agent header
    ua_match = re.search(r'User-Agent: (.+)', text)
    user_agent = ua_match.group(1) if ua_match else ''
    # Handle special cases in the Cookie header
    cookie = re.sub(r'g_state=\{[^}]+\}', 'g_state={"i_l":0}', cookie)
    cookie = re.sub(r'dnt=[^;]+', 'dnt=1', cookie)
    cookie = re.sub(r'lang=[^;]+', 'lang=en', cookie)
    
    # Replace double quotes with single quotes in the Cookie value
    cookie = cookie.replace('"', "'")

    return {
        "Cookie": cookie,
        "Authorization": authorization,
        "X-Csrf-Token": csrf_token,
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }

# Example usage:
filtered_headers = filter_twitter_headers(text)
print("Twitter Headers:")
print("{")
for key, value in filtered_headers.items():
    if key == "Cookie":
        print(f'    "{key}": "{value}",')
    else:
        print(f'    "{key}": "{value}",')
print("}")

