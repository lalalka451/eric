import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
b = webdriver.Chrome(options=chrome_options)

b.get('https://boards.4chan.org/a/')

# Get the header cookie
cookies = b.get_cookies()
header_cookie = next((cookie for cookie in cookies if cookie['name'] == '4chan_header'), None)

if header_cookie:
    print(f"Header cookie: {header_cookie['value']}")
else:
    print("Header cookie not found")

time.sleep(20)
b.quit()