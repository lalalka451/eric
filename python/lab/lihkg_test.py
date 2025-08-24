import random
import time
import requests
import uuid
import hashlib

# Define the URL
# url = "https://lihkg.com/api_v2/thread/latest?cat_id=1&page=1&count=60&type=now"
url = "https://lihkg.com/api_v2/thread/3794070/page/1?order=reply_time"
url = "https://lihkg.com/api_v2/thread/3794070/media?include_link=0"

# Generate a random device ID
def generate_device_id():
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    # Convert the UUID to a string and encode it
    uuid_str = str(random_uuid).encode('utf-8')
    # Create a SHA1 hash of the UUID
    sha1_hash = hashlib.sha1(uuid_str).hexdigest()
    return sha1_hash

# Define the headers

def get_proxy_uri():
    while True:
        proxy_uri = requests.get('http://192.168.1.14:5000/fetch_random').text
        if len(proxy_uri) == 0:
            print('暂时没有可用代理')
            time.sleep(5)  # Wait before trying again
            continue

        if not proxy_uri.startswith('http'):
            return proxy_uri

def get_proxy():
    proxy_uri = get_proxy_uri()
    print('获取到的代理是：' + proxy_uri)
    proxies = {proxy_uri.split(':')[0]: proxy_uri}
    # proxies = {'http':'127.0.0.1:10809'}
    # proxies = {}
    return proxies

#'url': '.*?'
# 4571037073
# Make the GET request


# while True:
headers = {
    "Host": "lihkg.com",
    "Sec-Ch-Ua-Platform": "Windows",
    "X-Li-Device-Type": "browser",
    "Sec-Ch-Ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Li-Device": "baa1c3ecc1e72b8bf63d9e9a6ddc5e4db3a3c0b0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "X-Li-Load-Time": "6.1713997",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://lihkg.com/thread/3795193/page/1",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
    "Priority": "u=1, i"

    # Add the cookie here if needed
    # "Cookie": "_ga=GA1.1.1408923090.1727350058; PHPSESSID=ok84r4f5f5b7gngjd5l93bg1kl; __cfruid=f0b00f51bb74f679e4c6201ba0a4a9a0bae30a34-1727595733; _cfuvid=M6wmXQ3AYfL2MtpmP2SuVD1RJtNc4wCRLMS5H2rC50Y-1727595733482-0.0.1.1-604800000; _ga_PPY9Z37CCJ=GS1.1.1727595735.3.1.1727595735.60.0.0; _ga_L8WS4GS6YR=GS1.1.1727595737.3.0.1727595737.0.0.0; __cf_bm=dgoxRaxD7_tSGwlplJ5yCOe8ix_lA8dvq_THUHiwkmw-1727597163-1.0.1.1-fTH0wx33FYvhA.ybsx3dvjVO6d6MOu6oIQ2jCzJ.6T4zEuuFUP.IjJv.CSeosN538ZMyGPId7dtKu1QewSBIlg; cf_clearance=ZQf3Ct7nrKOerXO6K0eT2_As1uDvYIybLgEzK.kgHR8-1727597165-1.2.1.1-OVtYGJB7VnZInLPErCwn1bV4_Ca_CmNo.m7.wVNtfiYQ7.B17ip6pCeGgpTOmmsCGVhfzte5x1soe17tY0vejTqJs.p7zBJCrwW1J_XdHuqgSihmR5yTi3B8Owqk0Pv4CTuO2Wsg2oKi3V.HntRiY08W_NNmi_2P7SnlST6JFzpD8VfUgAHfbgygWmVuQi0BgAdYp00emOFt4nOZe7LPzhoGCeUV9d8ZV1czDz5Rx7TBR3DtQVwzpY8jGK57brOL_skpAXfTJ7aEoCoxNlVOU.kKNhDFOHGrETuZDSmXC8arGOlzTEm6BM_6zI.SAdB4Gege6vRlZbSjyuEsEEUDG0x.tfG0B_Um8ET8Rkmd9YWNodn97rRq.AJT8OlUVmsi"
}
print(headers)
response = requests.get(url, headers=headers, proxies=get_proxy())

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    data = response.json()  # Get the response content as JSON
    print(data)  # Print or process the data as needed
    images = data['response']['images']
    if images:
        for image in images:
            print(f"Image URL: {image['url']}, {image['tag']}")
    else:
        print("No images found in this thread.")
else:
    print(f"Request failed with status code: {response.status_code}")
