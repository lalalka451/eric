import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import sqlite3
import threading

def get_proxy_uri():
    while True:
        proxy_uri = requests.get('http://35.192.219.242:5000/fetch_random').text
        if len(proxy_uri) == 0:
            print('暂时没有可用代理')
            time.sleep(5)  # Wait before trying again
            continue

        if proxy_uri.startswith('socks4://') or proxy_uri.startswith('socks5://'):
            return proxy_uri

def get_proxy():
    proxy_uri = get_proxy_uri()
    proxies = {'http': proxy_uri, 'https': proxy_uri}
    print('获取到的代理是：' + str(proxies))
    return proxies, proxy_uri

def insert_successful_proxy(proxy_uri):
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS successful_proxies
                      (proxy_uri TEXT PRIMARY KEY, last_success TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('INSERT OR REPLACE INTO successful_proxies (proxy_uri) VALUES (?)', (proxy_uri,))
    conn.commit()
    conn.close()

def fetch_page(i):
    url = f'https://hk.jobsdb.com/jobs?page={i}'
    max_retries = 3
    for attempt in range(max_retries):
        try:
            proxies, proxy_uri = get_proxy()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, proxies=proxies, headers=headers, timeout=3)
            if response.status_code == 200:
                print(f'Successfully fetched page {i}')
                insert_successful_proxy(proxy_uri)
                return response.text
            else:
                print(f'Failed to fetch page {i}. Status code: {response.status_code}')
                # time.sleep(random.uniform(1, 3))  # Random delay between retries
        except Exception as e:
            print(f'Error fetching page {i}: {str(e)}')
            # time.sleep(random.uniform(1, 3))  # Random delay between retries
    print(f'Max retries reached for page {i}')
    return None

def count_proxies():
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM successful_proxies')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def add_proxies():
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_page, i) for i in range(1, 20)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                # Process the result here (e.g., parse HTML, extract data, etc.)
                pass
            # time.sleep(random.uniform(0.5, 1.5))  # Random delay between requests


            # Check if proxy count has reached 10
            if count_proxies() >= 10:
                print("Proxy count has reached 10. Switching back to maintenance mode.")
                return

def check_proxy(proxy_uri):
    try:
        proxies = {'http': proxy_uri, 'https': proxy_uri}
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False

def remove_invalid_proxy(proxy_uri):
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM successful_proxies WHERE proxy_uri = ?', (proxy_uri,))
    conn.commit()
    conn.close()

def maintenance_mode():
    print("Entering maintenance mode")
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT proxy_uri FROM successful_proxies')
    proxies = cursor.fetchall()
    conn.close()

    def validate_and_remove(proxy):
        proxy_uri = proxy[0]
        if check_proxy(proxy_uri):
            print(f"Proxy {proxy_uri} is still valid")
        else:
            print(f"Removing invalid proxy: {proxy_uri}")
            remove_invalid_proxy(proxy_uri)
        # time.sleep(random.uniform(0.5, 1.5))  # Random delay between checks

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(validate_and_remove, proxy) for proxy in proxies]
        for future in as_completed(futures):
            future.result()  # To raise any exceptions if occurred

    # After maintenance, check if proxy count has fallen below threshold
    if count_proxies() < 10:
        print("Proxy count has fallen below 10. Switching to add mode.")
        return False  # Indicate that we need to switch to add mode
    return True  # Indicate that maintenance is complete

def initialize_database():
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS successful_proxies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proxy_uri TEXT UNIQUE
    )
    ''')
    conn.commit()
    conn.close()

def main():
    initialize_database()

    def add_mode():
        while True:
            try:
                proxy_count = count_proxies()
                if proxy_count < 10:
                    print(f"Current proxy count: {proxy_count}. Running in add mode.")
                    add_proxies()
                # time.sleep(60)  # Wait for 1 minute before checking again
            except Exception as e:
                print(f"An error occurred in add mode: {e}")
                # time.sleep(30)  # Wait for 30 seconds before retrying

    def maintenance_mode_thread():
        while True:
            try:
                proxy_count = count_proxies()
                if proxy_count >= 10:
                    print(f"Current proxy count: {proxy_count}. Running in maintenance mode.")
                    maintenance_mode()
                # time.sleep(30)  # Wait for 5 minutes before next maintenance cycle
            except Exception as e:
                print(f"An error occurred in maintenance mode: {e}")
                # time.sleep(6)  # Wait for 1 minute before retrying

    add_thread = threading.Thread(target=add_mode)
    maintenance_thread = threading.Thread(target=maintenance_mode_thread)

    add_thread.start()
    maintenance_thread.start()

    add_thread.join()
    maintenance_thread.join()

if __name__ == "__main__":
    main()
