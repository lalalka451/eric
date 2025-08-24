import requests
import json
import time
import random

def get_bilibili_video_detail(aid):
    url = "https://api.bilibili.com/x/player/wbi/v2"
    
    # Generate random values for dynamic parameters
    cid = str(random.randint(26000000000, 26999999999))
    w_rid = ''.join(random.choices('0123456789abcdef', k=32))
    wts = str(int(time.time()))
    
    params = {
        "aid": aid,
        "cid": cid,
        "isGaiaAvoided": "true",
        "web_location": 1315873,
        "w_rid": w_rid,
        "wts": wts
    }
    headers = {
        "Host": "api.bilibili.com",
        "Cookie": "buvid3=B6C236E4-1712-1360-FEBA-2F6E0FD676FE25334infoc; b_nut=1726971825; _uuid=954B7E71-3229-9869-1235-E31DDF314D8C26133infoc; enable_web_push=DISABLE; CURRENT_FNVAL=4048; DedeUserID=29193955; DedeUserID__ckMd5=d0ebc9048b739d48; header_theme_version=CLOSE; rpdid=|(JlJYmRkmJm0J'u~kYmmYk~l; fingerprint=c1cd70686aff79039c496ea00f41f88c; buvid_fp_plain=undefined; CURRENT_QUALITY=80; buvid4=2271D7AE-FAA0-FF99-55BA-0D9A549F2D0726805-024092202-kRDUpJB%2BJtJG9dqCKb2MAg%3D%3D; buvid_fp=c1cd70686aff79039c496ea00f41f88c; home_feed_column=5; browser_resolution=1536-695; SESSDATA=bdba71c0%2C1744080552%2C8c0f1%2Aa2CjDEwVPrWfWqaO7QykiPWWegPUg4xVeWUJcXDfPzEbkYub_xkgFLqqP3LCEtua-QsAASVml5VnlKTTNhQ1FsNllwWTNmdTRDVDVOa1RMR0draVpvLWhpYUowVldSb2RDN01YNDFoY1pvaFF6SFF0LWZXVFY1SG5xRmN5OFFsaVNNSldYeExxSGV3IIEC; bili_jct=9385beb0a5eab83df84b19898694798c; sid=5a8rjjjl; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg4OTkyNjAsImlhdCI6MTcyODY0MDAwMCwicGx0IjotMX0.uO4q1YIBes5q_eRfBZ-N7rJFOGVXNuzjaAraP_BbZbE; bili_ticket_expires=1728899200; b_lsid=3F3D4261_1927BB9F347; bp_t_offset_29193955=987049098836180992",
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Origin": "https://www.bilibili.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.bilibili.com/?spm_id_from=..0.0",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

# Example usage
video_detail = get_bilibili_video_detail("113286926305899")
if video_detail:
    print(json.dumps(video_detail, ensure_ascii=False, indent=2))
else:
    print("Failed to retrieve video detail")