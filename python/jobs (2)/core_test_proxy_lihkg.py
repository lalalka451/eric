import uuid

import requests



def fetch_data(url):
  """Fetches data from the given URL and returns the response content."""
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from {url}: {e}")
    return None


session_id = str(uuid.uuid4())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'X-Seek-Ec-Sessionid': session_id,
}


import uuid
import hashlib

# Define the URL
url = "https://lihkg.com/api_v2/thread/category?cat_id=5&page=1&count=60"

# Generate a random device ID
def generate_device_id():
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    # Convert the UUID to a string and encode it
    uuid_str = str(random_uuid).encode('utf-8')
    # Create a SHA1 hash of the UUID
    sha1_hash = hashlib.sha1(uuid_str).hexdigest()
    return sha1_hash

def test_proxy(proxy):
    try:

        # Define the headers
        headers = {
            "referer": "https://lihkg.com/thread/1/page/1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "X-Li-Device-Type": "browser",
            "X-Li-Device": generate_device_id(),
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
            "Priority": "u=1, i",
            "Connection": "keep-alive",
            # Add the cookie here if needed
            # "Cookie": "_ga=GA1.1.1408923090.1727350058; PHPSESSID=ok84r4f5f5b7gngjd5l93bg1kl; __cfruid=f0b00f51bb74f679e4c6201ba0a4a9a0bae30a34-1727595733; _cfuvid=M6wmXQ3AYfL2MtpmP2SuVD1RJtNc4wCRLMS5H2rC50Y-1727595733482-0.0.1.1-604800000; _ga_PPY9Z37CCJ=GS1.1.1727595735.3.1.1727595735.60.0.0; _ga_L8WS4GS6YR=GS1.1.1727595737.3.0.1727595737.0.0.0; __cf_bm=dgoxRaxD7_tSGwlplJ5yCOe8ix_lA8dvq_THUHiwkmw-1727597163-1.0.1.1-fTH0wx33FYvhA.ybsx3dvjVO6d6MOu6oIQ2jCzJ.6T4zEuuFUP.IjJv.CSeosN538ZMyGPId7dtKu1QewSBIlg; cf_clearance=ZQf3Ct7nrKOerXO6K0eT2_As1uDvYIybLgEzK.kgHR8-1727597165-1.2.1.1-OVtYGJB7VnZInLPErCwn1bV4_Ca_CmNo.m7.wVNtfiYQ7.B17ip6pCeGgpTOmmsCGVhfzte5x1soe17tY0vejTqJs.p7zBJCrwW1J_XdHuqgSihmR5yTi3B8Owqk0Pv4CTuO2Wsg2oKi3V.HntRiY08W_NNmi_2P7SnlST6JFzpD8VfUgAHfbgygWmVuQi0BgAdYp00emOFt4nOZe7LPzhoGCeUV9d8ZV1czDz5Rx7TBR3DtQVwzpY8jGK57brOL_skpAXfTJ7aEoCoxNlVOU.kKNhDFOHGrETuZDSmXC8arGOlzTEm6BM_6zI.SAdB4Gege6vRlZbSjyuEsEEUDG0x.tfG0B_Um8ET8Rkmd9YWNodn97rRq.AJT8OlUVmsi"
        }
        proxies = {
            # 'http': '127.0.0.1:6666'
            # 'http': '127.0.0.1:10809'
            'http': f'127.0.0.1:{proxy}'
            # 'http': random.choice(http_proxies) if http_proxies else '127.0.0.1:10809'
        }
        response = requests.get(url, headers=headers, proxies=proxies)

        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful!")
            return response.status_code == 200
        else:
            print(f"Request failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error testing proxy {proxy}: {e}")
        return False

def main():
  url = "https://imperialb.in/r/ywkbzmxe"
  data = fetch_data(url)
  # print(data)
  http_proxies = data.split("\n")
  # http_proxies = ["127.0.0.1:" + port for port in http_proxies]
  # test_proxy('127.0.0.1:10809')
  for proxy in http_proxies:
    print(proxy)
    if test_proxy(proxy):
      print(f"Proxy {proxy} is working")
    else:
      print(f"Proxy {proxy} is not working")


if __name__ == "__main__":
  main()
