import requests
import json
import urllib.parse

import schedule

from baseHandler import BaseHandler
from dotenv import load_dotenv
import os




channel_id = 2238825797
db_name = 'twitter_chinese'

def parse_twitter_user_timeline(data):
    """
    Extracts tweets that contain media (images or videos) from the provided JSON data.

    Args:
        data (dict): JSON data from the Twitter API response.

    Returns:
        list: A list of dictionaries, each containing the `tweet_id`, `text`, and a list of `media_urls`.
    """
    tweets_with_media = []

    try:
        instructions = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    except KeyError:
        print("Unexpected data format. Please check the JSON structure.")
        return tweets_with_media

    for instruction in instructions:
        if instruction.get('type') == 'TimelineAddEntries':
            entries = instruction.get('entries', [])
            for entry in entries:
                content = entry.get('content', {})
                if content.get('entryType') == 'TimelineTimelineModule':
                    items = content.get('items', [])
                    for item in items:
                        tweet_content = item.get('item', {}).get('itemContent', {})
                        if tweet_content.get('itemType') == 'TimelineTweet':
                            tweet = tweet_content.get('tweet_results', {}).get('result', {})
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



def get_user_media(user_id, count=20):
    url = "https://x.com/i/api/graphql/HaouMjBviBKKTYZGV_9qtg/UserMedia"

    variables = {
        "userId": user_id,
        "count": count,
        "includePromotedContent": False,
        "withClientEventToken": False,
        "withBirdwatchNotes": False,
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

    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"

    # eric21516693724
    # tatafa2234@gmail.com

    headers = {
        "Host": "x.com",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Cookie": "guest_id=v1%3A172878714057722438; night_mode=2; guest_id_marketing=v1%3A172878714057722438; guest_id_ads=v1%3A172878714057722438; gt=1845293134869299409; kdt=rnpMLaA6LkRZksdVx5uZzGxtxsENwEATgbKQwfsW; auth_token=0443facd794e40536627216f639f29e750f312e6; ct0=5dcd73d51b7edb427b5301afe3b884d6e3af65c7179f8bc7bdbf27d01af4cc1e93e25070834778c0301019d64044d9e011568fa3b9a06e708da0ca4881079a0ce76193411f48f0787d6c9d0f7c073d2e; att=1-FzEaj86RW1740fchSqaTb7OV1Q1VK9mVEiN5w8oS; lang=en; twid=u%3D1845291314038145024; personalization_id=\"v1_PfPTJuiE2eVI76eMxWMFxQ==\"",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Content-Type": "application/json",
        "X-Csrf-Token": "5dcd73d51b7edb427b5301afe3b884d6e3af65c7179f8bc7bdbf27d01af4cc1e93e25070834778c0301019d64044d9e011568fa3b9a06e708da0ca4881079a0ce76193411f48f0787d6c9d0f7c073d2e",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-Client-Uuid": "4b0a8e8a-be8b-479c-a136-215dad269f5f",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "X-Twitter-Client-Language": "en",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Twitter-Active-User": "yes",
        "X-Client-Transaction-Id": "ILvBUmxfKWelOXoMpp14MAGSFy2gSMDIZVZSqeoJwQARX5m4nhBUd8kXhJgKh6TsH1XwmyIX7oBh5KsOAgxnkr5YXMcFIw",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://x.com/OLgirl_Akina",
        # not working in arm64
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }

    response = requests.get(full_url, headers=headers)

    print(response.json())
    # parse_twitter_user_timeline(response.json())


    if response.status_code == 200:
        try:
            tweets = parse_twitter_user_timeline(response.json())
        except:
            print(response)
            print(response.text)
            return None
        return tweets
    else:
        return None


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
        tweets_data = get_user_media(self.user_id, self.count)
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
                if self.db_handle.url_exists(tweet_id,media_url):
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
    url = "https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery"
    params = {
        "variables": f'{{"screen_name":"{screen_name}"}}'
    }
    headers = {
        "Host": "x.com",
        "Cookie": "guest_id=v1%3A172878714057722438; night_mode=2; guest_id_marketing=v1%3A172878714057722438; guest_id_ads=v1%3A172878714057722438; gt=1845293134869299409; kdt=rnpMLaA6LkRZksdVx5uZzGxtxsENwEATgbKQwfsW; auth_token=0443facd794e40536627216f639f29e750f312e6; ct0=5dcd73d51b7edb427b5301afe3b884d6e3af65c7179f8bc7bdbf27d01af4cc1e93e25070834778c0301019d64044d9e011568fa3b9a06e708da0ca4881079a0ce76193411f48f0787d6c9d0f7c073d2e; att=1-FzEaj86RW1740fchSqaTb7OV1Q1VK9mVEiN5w8oS; lang=en; twid=u%3D1845291314038145024; personalization_id=\"v1_PfPTJuiE2eVI76eMxWMFxQ==\"",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "X-Csrf-Token": "5dcd73d51b7edb427b5301afe3b884d6e3af65c7179f8bc7bdbf27d01af4cc1e93e25070834778c0301019d64044d9e011568fa3b9a06e708da0ca4881079a0ce76193411f48f0787d6c9d0f7c073d2e",
        "X-Client-Uuid": "4b0a8e8a-be8b-479c-a136-215dad269f5f",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "X-Twitter-Client-Language": "en",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Twitter-Active-User": "yes",
        "X-Client-Transaction-Id": "ILvBUmxfKWelOXoMpp14MAGSFy2gSMDIZVZSqeoJwQARX5m4nhBUd8kXhJgKh6TsH1XwmyIX7oBh5KsOAgxnkr5YXMcFIw",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://x.com/{screen_name}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Priority": "u=1, i"
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()



if __name__ == "__main__":
    load_dotenv()

    channel_id = 2484441083
    db_name = 'twitter_chinese'
    session = 'twitter_chinese_session'

    twitter_users = [
    "FreiheitYu",
    "nateleex",
    "yuxiyou",
    "xushiwei",
    "skywind3000",
    "vikingmute",
    "waylybaye",
    "dotey",
    "manateelazycat",
    "middlefeng",
    "DLKFZWilliam",
    "javayhu",
    "nextify2024",
    "xiongchun007",
    "yihong0618",
    "yihui_indie",
    "goocarlos",
    "ruanyf",
    "appinn",
    "turingou",
    "Linmiv",
    "chenbimo",
    "feltanimalworld",
    "mrbear1024",
    "xiaopeng163",
    "AgileQuery",
    "tison1096",
    "RyanMfer",
    "zhugezifang",
    "haoel",
    "huihoo",
    "knowledgefxg",
    "hixiaoji",
    "bnu_chenshuo",
    "gefei55",
    "wshuyi",
    "felixding",
    "huangzworks",
    "zhufengme",
    "marchliu",
    "glow1n",
    "li_wujie",
    "yosei8964",
    "seclink",
    "kuizuo",
    "harryworld",
    "CoooolXyh",
    "DIGITALYCHEE",
    "davidchen2024",
    "taro_dict",
    "ihower",
    "ethanhuang13",
    "PeterTW777",
    "hwwaanng",
    "MapleShadow",
    "lexrus",
    "arui_kisi",
    "Bitturing",
    "ccbikai",
    "weijunext",
    "pingchn",
    "leafwind",
    "fetalkpodcast",
    "hhmy27",
    "indigo11",
    "decohack",
    "geekplux",
    "henices",
    "lyc_zh",
    "JourneymanChina",
    "huangyun_122",
    "vista8",
    "lewangdev",
    "thinkingjimmy",
    "shengxj1",
    "meathill1",
    "ailiangzi",
    "dingyi",
    "hal__lee",
    "shao__meng",
    "CZXNew",
    "henuwangkai",
    "YosefBlockchain",
    "cesihai1",
    "qloog",
    "johnny____11",
    "nishuang",
    "DashHuang",
    "robbinfan",
    "turingbook",
    "mujiang",
    "csdncto",
    "zhuangbiaowei",
    "buaaxhm",
    "nmdfzf404",
    "AndyRoamer",
    "wsygc",
    "monk_robot",
    "daniu1719",
    "remixdesigner",
    "imtigerchew",
    "ikennylin",
    "balconychy",
    "catmangox",
    "oran_ge",
    "river_leaves",
    "HiTw93",
    "trojantale",
    "9yearfish",
    "leoxoocanada",
    "i5ting",
    "blankwebdev",
    "boo_hz",
    "tonyzhu1984",
    "hongming731",
    "benshandebiao",
    "tinyfool",
    "whiteboardxcom",
    "CurtisChengC",
    "cui_xiaorui",
    "hsin747",
    "StarKnight",
    "easychen",
    "AndrewBBoo",
    "dev_afei",
    "pekingmuge",
    "ginhoor",
    "oulvhai",
    "Tumeng05",
    "anqirocks",
    "austinit",
    "hzlzh",
    "cellinlab",
    "richriverspirit",
    "sailfishcc1",
    "hi_an_orange",
    "fengbuyou",
    "ilovek8s",
    "evanlong_zh",
    "xinbaocode",
    "Amztion",
    "hagerhu",
    "liseami1",
    "container202",
    "oschina",
    "junyu",
    "DigitalNomadLC",
    "_kaichen",
    "taoshenga19",
    "shamzaaz1",
    "spacewander_lzx",
    "CarsonYangk8s",
    "Piglei",
    "ThonsChang",
    "435hz",
    "MooenyChu",
    "chenboos5",
    "greylihui",
    "foxshuo",
    "Ninsbay",
    "sekay2016",
    "layla8964",
    "kenshinji",
    "michaelwong666",
    "jessieinorge",
    "CaminoTexas",
    "no13bus",
    "USAHS1",
    "neverrainmyself",
    "tuturetom",
    "jyrnan",
    "NodYoung",
    "cellier_",
    "Aviva",
    "Gorden_Sun",
    "7733Bianca",
    "horsezhanbin",
    "iamluokai",
    "youtubedubbing",
    "Yangyixxxx",
    "op7418",
    "OwenYoungZh",
    "imxiaohu",
    "kasong2048",
    "arvin17x",
    "likefeiwu",
    "houjoe1",
    "readyfor2025",
    "choicky",
    "linroid",
    "real_kai42",
    "cholf5",
    "siantgirl",
    "lvxinxin",
    "__oQuery",
    "_justineo",
    "chaosflutt28952",
    "AnwFM",
    "JohnnyBi577370",
    "yan5xu",
    "VKoooooon",
    "belliedmonkey",
    "Huanghanzhilian",
    "pupilcc",
    "wangeguo",
    "frank_8848",
    "1024_zip",
    "zolplay",
    "nanshanjukr",
    "haohailong",
    "le0zh0u",
    "jinjinledaofm",
    "x_canoe",
    "sspai_com",
    "coolXiao",
    "jike_collection",
    "liruifengv",
    "whileGreatHair",
    "FinoGeng",
    "CMGS1988",
    "zuozizhen",
    "fuxiaohei",
    "randyloop",
    "Lakr233",
    "alswl",
    "HzaoHzao",
    "geekbb",
    "JinsFavorites",
    "leeoxiang",
    "nexmoe",
    "SaitoWu",
    "HongyuanCao",
    "huangjinbo",
    "CeoSpaceY",
    "9hills",
    "mundane799699",
    "luobogooooo",
    "OpenQiang",
    "qilong87",
    "ftium4",
    "CNBorn",
    "gametofuofl",
    "sh_awai",
    "strrlthedev",
    "freesisx",
    "baoshu88",
    "santiagoyoungus",
    "raycat2021",
    "mike_d1213",
    "liuren",
    "onenewbite",
    "thecalicastle",
    "Himalaya_bear1",
    "jason5ng32",
    "Beichen",
    "ifanr",
    "erchenlu1",
    "realliaohaibo",
    "oIUnIfxxuuNRpIA",
    "Yintinusa",
    "FinanceYF5",
    "0xluffy_eth",
    "HeySophiaHong",
    "Trillion5205189",
    "CoderJeffLee",
    "minizz1949",
    "juransir",
    "gidot",
    "lemon_hx",
    "imsingee",
    "HotmailfromSH",
    "WildCat_zh",
    "beihuo",
    "haveafreeheart",
    "wong2_x",
    "fkysly",
    "plusyip",
    "alanblogsooo",
    "nianyi_778",
    "ovst36099",
    "_KleinHe_",
    "lumaoyangmao",
    "ShouChen_",
    "wwek",
    "edwardzsky2017",
    "fxxkol",
    "ruiyanghim",
    "waiwen3",
    "gasikaramada",
    "marvin102465536",
    "tianlan",
    "wulujia",
    "quentin_hsu",
    "lgywrite",
    "FlashSnail",
    "nuannuan_share",
    "sitinme",
    "boy94288021",
    "liuyi0922",
    "kevinzhow",
    "DIYgod",
    "zoeyzhou1103",
    "caizhenghai",
    "DinChao",
    "KidyLee",
    "YunYouJun",
    "jesselaunz",
    "xds2000",
    "baiwusanyu",
    "laobaishare",
    "wanerfu",
    "Caijingtianxia",
    "iskyzh",
    "zty0826",
    "gong_cn",
    "zhongerxin",
    "Li_miao_wen",
    "ouranswers_",
    "yfractal",
    "Jiaxi_Cui",
    "iWillDev",
    "JJH_Chi",
    "leiyatsaan",
    "Raymond_Hou_",
    "eryidebiji",
    "Gruff1561002",
    "lvloomystery",
    "noobnooc",
    "lcayu",
    "xieisabug",
    "jrenc2002",
    "GoJun315",
    "suaihk",
    "_wissx",
    "lincolnstark5",
    "kiwiflysky",
    "KumaTea0",
    "__RedForest",
    "ivyliner",
    "oldj",
    "Hawstein",
    "joyqi",
    "_sluke_",
    "sunshineg",
    "pythonhunter__",
    "adaaaamwen",
    "tufucheung",
    "iamcheyan",
    "rickywang233",
    "shmily7",
    "EZFIX_",
    "dream_qiang",
    "wanghao8080",
    "jameszz343698",
    "patrici00662047",
    "bestlacklock",
    "FeigelC35583",
    "fyfyfm",
    "silosrc",
    "expatlevi",
    "modaotool",
    "recatm",
    "abskoop",
    "shuziyimin",
    "sunbelife"

    "vista8",
    "dotey",
    "op7418",
    "xicilion",
    "WaytoAGI",
    "hanqing_me",
    "jesselaunz",
    "lewangx",
    "JefferyTatsuya",
    "FinanceYF5",
    "thinkingjimmy",
    "oran_ge",
    "99aico",
    "XDash",
    "GlocalTerapy",
    "fuxiangPro",
    "Gorden_Sun",
    "indigo11",



    ]
    twitter_users = list(set(twitter_users))
    

    def main():

        for twitter_user in twitter_users:
            result = fetch_profile_spotlights(twitter_user)
            try:
                rest_id = result['data']['user_result_by_screen_name']['result']['rest_id']
                print(f'User: {twitter_user}, rest_id: {rest_id}')
            except KeyError:
                print(f'Error: Unable to fetch rest_id for user {twitter_user}. Skipping...')
                continue
            USER_ID = rest_id
            handler = TwitterUserHandler(channel_id=channel_id, db_name=db_name, telegram_session=session,
                                         user_id=USER_ID)
            handler.run()
    main()
    schedule.every(4).hours.do(main)
    while True:
        schedule.run_pending()

        