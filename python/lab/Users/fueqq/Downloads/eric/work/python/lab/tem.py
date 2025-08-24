import requests
from bs4 import BeautifulSoup
from googlesearch import search
from transformers import pipeline
import sqlite3
import time
import random
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# Search for Masako Wakamiya's age
query = "Masako Wakamiya age"
urls = search(query, num_results=5)

# Initialize a summarization pipeline
summarizer = pipeline("summarization")

# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join([para.get_text() for para in paragraphs])
    except Exception as e:
        print(f"Failed to extract from {url}: {e}")
        return ""

# Extract and summarize text from each URL
for url in urls:
    text = extract_text_from_url(url)
    if text:
        summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
        print(f"Summary from {url}: {summary[0]['summary_text']}")

def maintenance_mode():
    print("Entering maintenance mode")
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT proxy_uri FROM successful_proxies')
    proxies = cursor.fetchall()
    conn.close()

    for proxy in proxies:
        proxy_uri = proxy[0]
        if not check_proxy(proxy_uri):
            print(f"Removing invalid proxy: {proxy_uri}")
            remove_invalid_proxy(proxy_uri)
        else:
            print(f"Proxy {proxy_uri} is still valid")
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between checks

        # Check if proxy count has fallen below 50
        if count_proxies() < 50:
            print("Proxy count has fallen below 50. Switching to add mode.")
            add_proxies()

def add_proxies():
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_page, i) for i in range(1, 100)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                # Process the result here (e.g., parse HTML, extract data, etc.)
                pass
            time.sleep(random.uniform(0.5, 1.5))  # Random delay between requests
            
            # Check if proxy count has reached 100
            if count_proxies() >= 100:
                print("Proxy count has reached 100. Switching back to maintenance mode.")
                return

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

def count_proxies():
    conn = sqlite3.connect('proxies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM successful_proxies')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def main():
    initialize_database()
    while True:
        try:
            proxy_count = count_proxies()
            if proxy_count < 100:
                print(f"Current proxy count: {proxy_count}. Running in add mode.")
                add_proxies()
            else:
                print(f"Current proxy count: {proxy_count}. Running in maintenance mode.")
                maintenance_mode()
            time.sleep(300)  # Wait for 5 minutes before next cycle
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait for 1 minute before retrying

if __name__ == "__main__":
    main()
