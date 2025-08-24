import json
import time

import requests
from bs4 import BeautifulSoup
import html
import re

from selenium.common import TimeoutException


def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def sanitize_comment(text):
    unescaped_text = html.unescape(text)
    clean_text = remove_html_tags(unescaped_text)
    return clean_text

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_discover_page():
    url = "https://www.douyin.com/discover"

    chrome_options = Options()
    # Removed the headless mode to show the window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for the body to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 1. Attempt to locate and click the login panel
        try:
            login_panel_xpath = "//*[@id='login-pannel']/div/div/div[2]"
            login_pannel_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, login_panel_xpath))
            )
            login_pannel_element.click()
            print("Login panel clicked.")
        except TimeoutException:
            print("Login panel not found or not clickable.")

        # Optional: Wait for any post-click actions (e.g., login form) to load
        time.sleep(1)  # Adjust as necessary

        # 2. Attempt to locate and click the navigation element
        try:
            navigation_element_xpath = "//*[@id='douyin-navigation']/div/div[2]/div/div[1]/div/div/div[1]/div/div/a"
            navigation_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, navigation_element_xpath))
            )
            navigation_element.click()
            print("Navigation element clicked.")
        except TimeoutException:
            print("Navigation element not found or not clickable.")

        # Optional: Wait for any post-click actions
        time.sleep(5)  # Adjust as necessary
        # Optional: Wait for any post-click actions (e.g., login form) to load

        # Get the page source
        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f"Error fetching the discover page: {e}")
        return None
    finally:
        if 'driver' in locals():
            # time.sleep(5)
            driver.quit()

def extract_aweme_data(html_content):
    meta_data = re.findall(r'awemeId\\":\\"(\d+)\\".*?"desc\\":\\"(.*?)\\",',html_content)
    aweme_data_list = [{"awemeId": video_id, "title": title} for video_id, title in meta_data]
    return aweme_data_list


def sanitize_text(text):
    """
    Unescape HTML entities and remove HTML tags.
    """
    unescaped_text = html.unescape(text)
    clean_text = remove_html_tags(unescaped_text)
    return clean_text


def find_aweme_entries(data):
    """
    Recursively search for dictionaries containing `awemeId` and `desc`.
    """
    aweme_entries = []
    if isinstance(data, dict):
        if "awemeId" in data and "desc" in data:
            aweme_id = data["awemeId"]
            title = sanitize_text(data["desc"])
            aweme_entries.append({
                "awemeId": aweme_id,
                "title": title
            })
        for key, value in data.items():
            aweme_entries.extend(find_aweme_entries(value))
    elif isinstance(data, list):
        for item in data:
            aweme_entries.extend(find_aweme_entries(item))
    return aweme_entries

def main():
    html_content = fetch_discover_page()
    if html_content:
        print(html_content)
        aweme_data = extract_aweme_data(html_content)
        if aweme_data:
            print(f"Found {len(aweme_data)} aweme entries:")
            for idx, entry in enumerate(aweme_data, start=1):
                print(entry)
        else:
            print("No awemeId and titles found on the discover page.")
    else:
        print("Failed to fetch discover page")

if __name__ == "__main__":
    main()
