import re
import urllib

import requests
from lxml import etree
from telethon.errors import RPCError

from rss_send import *
from dotenv import load_dotenv
import os

load_dotenv()

# Get values from environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

channel_id = 2262601777
db_handle = db_handler('reddit', 'media')
db_handle.create_database()


def fetch_asmongold_subreddit():
    url = "https://www.reddit.com/r/Asmongold/new"
    # url = "https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after=dDNfMWZ1cTFyNg%3D%3D&t=DAY&name=Asmongold&navigationSessionId=5bad3a53-73ee-4f21-9f09-2b02563eaf4b&feedLength=3"
    url = "https://www.reddit.com/svc/shreddit/community-more-posts/new/"
    params = {
        "after": "dDNfMWZ2MWg1cg==",
        "t": "DAY",
        "name": "Asmongold",
        "feedLength": "3"
    }
    headers = {
        "Host": "www.reddit.com",
        "Cookie": "edgebucket=EOtPTqFSH76GVaxOhr; csv=2; loid=000000000w65jk2iwe.2.1710424691805.Z0FBQUFBQm03M2V2eGJUR2lMYnI4VlBUc1BMeTM2NnRfOGZFWE9fTlhSQjYyNmxfU0NaYzBtMnRsSGk1Y2d4eUR4QXNLY0QwZHFobG1jeEdaUjhTWko4Q3VDalE4TEd2R01feVp6QVdIeU9vRUtuRS15N1dJcHNVM21MVGpZTzI4azExeDVJLTFVMWE; reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml93NjVqazJpd2UiLCJleHAiOjE3NDM0MDg1MjQuODkwNTU3LCJpYXQiOjE3Mjc3NzAxMjQuODkwNTU3LCJqdGkiOiJuMUtPN19YWm9yeV9XLWV0SVNUSElnN2VTSUhyYUEiLCJjaWQiOiJjb29raWUiLCJsY2EiOjE3MTA0MjQ2OTE4MDUsInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJ2MSI6IjkwNzU3NzY4NTAyMzE4LDIwMjQtMDktMjJUMDE6NDk6MzIsODFiOGZhNGNmNjgyNjk3YmIzNDY0YTljNDQ4NzY4MWUyNDBmYWNjZSIsImZsbyI6Mn0.tPOq4fALJL0r5SX4xGNtpVSWbTZ4w6lNXukhzJD0oM7hWE4MzaYW7QXFeDc9xdNi-gJlPhd_qFqSNGH9zG7PiFKrAiYBmJ9ttaGNu8RdywE2W8JObFx2rJOBdPFwS85P_JKQgdnyGYtr1f2DTDQc9QPaWuI6p9E6lfdrWSuE34Rv-agh-IyjtyzoxRSCcRV_k894lvHuY-FOAqHcJ84bIzRAWVPktmo7bEMZo-HWYvlt6OI4TRfj3_NUSPQM9UwMC6Llb2czrL1qxEPrIa-THbi15dEP8l_OgqfUBeuiUY3LydG3BAj2TH1DDDfQjXAKuskUu9P4Nhzaj4LIlU0D6Q; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzI3OTQ4NzU4Ljc2NjY1MywiaWF0IjoxNzI3ODYyMzU4Ljc2NjY1MywianRpIjoiVktOeGhrYzE3dDNHUWc3eHZlOVVKRnU3eHJGQk53IiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml93NjVqazJpd2UiLCJhaWQiOiJ0Ml93NjVqazJpd2UiLCJsY2EiOjE3MTA0MjQ2OTE4MDUsInNjcCI6ImVKeGtrZEdPdERBSWhkLWwxejdCX3lwX05odHNjWWFzTFFhb2szbjdEVm9jazcwN2NMNGlIUDhuS0lxRkxFMnVCS0drS1dFRld0T1VOaUx2NTh5OU9aRUZTeUZUUjg0M3l3b2thVXBQVW1ONXB5bFJ3V1prTGxmYXNVS0RCNllwVlM2WjIwS1BTNXZRM0kxRnowNk1xbHhXSHRUWW8zSnBiR01LMnhQanpjWnFReXF1eTZsTVlGa29uOFdMZnZ5Ry10WS1mN2JmaEhZd3JLZ0tEX1RPdUZ4d1lfSERGSGJfbnByMGJGMndxTDNYZzlRLTEtTjI3Yk5tb2RtNV9WelB2emFTY1RtRzVpZll2N3QtQ1IxNDVIbVpVUWN3WWcwX3lyQWo2X0N2T29ES0JRV01KWWhQSTVBcmwyX19KZGl1VGY4YXR5ZC0tR2JFVFdfNHJSbW81eExFb1VfajZ6Y0FBUF9fWERfZTR3IiwicmNpZCI6IlBia2NDYUthUEVhaGNudlRaVEd6ZDY1bHdGR1U4WlR1WVRHdGRxc2FVWTAiLCJmbG8iOjJ9.WzP3mZ0ualh2xJ9hC8STB50fdJyX-YdEERNRhM7bgNqAemUWm8E9luo3Dhha1fDOdKyIu7faO50tK9sd855dL61zeKhRCqdKB-xlwTW1z5yHvQO-wn9YGv6jBhifJL0ycvnd_AXbOXqVIdaPy-V4TpN1-DQ8BTMETutBHyo28ugrqFyp_xnyylXJ_BV38elqy6NjvAnzayhdWsy4D5kTKy82S1YOYYK7b1Ws6iXG4_S6T36CwDWtYQEdYjLpowDiHHALXfgja1b3e5-fykje0Eea2v9pieFLGWeQrMDKwKGcFXlavwfzhBPGHk30ZOUNdpqtX4BbvPXoRgEWvLYFBw; pc=xt; t2_w65jk2iwe_recentclicks3=t3_1fv1h5r%2Ct3_1fu52ww%2Ct3_1fux5ak%2Ct3_1fuzivn%2Ct3_1futyxn%2Ct3_1fuxzr3%2Ct3_15kwhgy%2Ct3_18mmfxb%2Ct3_1fu9bo0%2Ct3_1fuk3df;",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "text/vnd.reddit.partial+html, text/html;q=0.9",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Content-Type": "application/x-www-form-urlencoded",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.reddit.com/r/Asmongold/new/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }
    response = requests.get(url, params=params, headers=headers)

    print(response.text)
    tree = etree.HTML(response.text)
    img_xpath = f'/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/article/shreddit-post/div'
    url_xpath = f'/faceplate-partial/shreddit-feed/faceplate-batch/article/shreddit-post/a[2]'

    post_elements = tree.xpath(url_xpath)
    post_images = tree.xpath(img_xpath)

    for post_element in post_elements:
        print(post_element.get('href'))

    return response.text

def extract_post_info(html_content):
    tree = etree.HTML(html_content)
    url_xpath = f'/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/article/shreddit-post/a[1]'
    youtube_xpath = f'/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/article/shreddit-post'

    #subreddit
    #/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/article/shreddit-post/div/div[3]/shreddit-aspect-ratio/shreddit-media-lightbox-listener/div/img[2]

    img_xpath = f'/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/article/shreddit-post/div/shreddit-aspect-ratio/shreddit-media-lightbox-listener/div/img[2]'
    title_xpath = f'/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/article/shreddit-post/a/faceplate-screen-reader-content'

    post_elements = tree.xpath(url_xpath)
    post_images = tree.xpath(img_xpath)
    post_titles = tree.xpath(title_xpath)
    link_xpaths = tree.xpath(youtube_xpath)
    print(link_xpaths[0].get('content-href'))

    for post_element in post_elements:
        print(post_element.get('href'))

    post_info = []
    for c,v in enumerate(post_elements):
        post = post_elements[c].get('href')
        title = post_titles[c].text
        img = post_images[c].get('src') if c < len(post_images) else ''
        link = link_xpaths[c].get('content-href') if c < len(link_xpaths) else ''
    # for post, img, title,link in zip(post_elements, post_images, post_titles,link_xpaths):
        post_info.append({
            'url': post,
            'title': title,
            'img': img,
            'link': link
        })

    return post_info

from telethon.sync import TelegramClient


def do_it():
    html_content = fetch_asmongold_subreddit()
    # print(html_content)
    # post_info = extract_post_info(html_content)
    # client = TelegramClient('reddit_session', api_id, api_hash)
    #
    # try:
    #     client.connect()
    #     if not client.is_user_authorized():
    #         print("Client is not authorized. Please authorize the client.")
    #         # Handle authorization if necessary
    #         return
    # except RPCError as e:
    #     print(f"Failed to connect Telegram client: {e}")
    #     return

    # print(post_info)
    # if post_info:
    #     for index, post in enumerate(post_info, 1):
    #         # print(f"{index}. Title: {post['title']}")
    #         # print(f"   URL: {post['url']}")
    #         # print(f"   Image: {post['img']}")
    #         # print(f"   Image: {post['link']}")
    #         # print()
    #
    #         image_url = post['img']
    #         title = post['title']
    #         post_url = post['url']
    #         link = post['link']
    #         upload_success = False
    #         insert_url = ""
    #         if not db_handle.url_exists(post_url, image_url) and image_url:
    #             caption = f'{title}\n`https://www.reddit.com/{post_url}/`\n`{image_url}`'
    #             upload_success = send_photo_reddit(client, channel_id, image_url, caption)
    #             insert_url = image_url
    #         elif not db_handle.url_exists(post_url, link) and link.__contains__('youtu.be'):
    #             youtube_id = re.findall('be/(.*?)\?',link)[0]
    #             youtube_image_url = f'https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg'
    #             upload_success = False
    #             caption = f'{title}\n{link}\n`{youtube_image_url}`'
    #             upload_success = send_photo_reddit(client, channel_id, youtube_image_url, caption)
    #             insert_url = link
    #         if upload_success:
    #             print('Upload success', youtube_image_url, title)
    #             # Insert the URL into the database after successful upload
    #             db_handle.insert_url(post_url, insert_url)
    #         else:
    #             print(f"Upload failed for URL: {insert_url}. Not inserting into the database.")
    # else:
    #     print("No post information found")

do_it()
# print("\nTotal number of posts found:", len(post_info))
# print(html_content)
#
# print("\nAll Post Information:")
# print(post_info)
