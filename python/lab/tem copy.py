from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import json
from selenium.common.exceptions import TimeoutError

def intercept_network_requests(driver, timeout=60):
    """
    Intercepts network requests to capture the temporary email from temp-mail.org.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        logs = driver.get_log('performance')
        for entry in logs:
            try:
                message = json.loads(entry['message'])['message']
                if 'Network.responseReceived' in message['method']:
                    url = message.get('params', {}).get('response', {}).get('url', '')
                    if 'https://web2.temp-mail.org/messages' in url:
                        request_id = message['params']['requestId']
                        response = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        data = json.loads(response['body'])
                        if 'mailbox' in data:
                            return data['mailbox']
            except Exception as e:
                print(f"Error processing log entry: {e}")
        time.sleep(1)
    raise TimeoutError("Failed to retrieve email within the specified timeout.")

# Set up the WebDriver with proxy settings and enable performance logging
chrome_options = Options()
chrome_options.add_argument('--proxy-server=http://127.0.0.1:10809')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

# Enable performance logging
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# Use webdriver_manager to automatically download and manage the ChromeDriver
service = Service(ChromeDriverManager().install())

# Initialize the Chrome driver with the updated options
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navigate to temp-mail.org
    driver.get("https://temp-mail.org/en/")
    print("Navigated to temp-mail.org")

    # Wait for the email to load and print it
    email = intercept_network_requests(driver)
    print(f"Temporary email address: {email}")

    # Open a new tab and navigate to Twitter signup page
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://x.com/i/flow/login")
    print("Opened Twitter signup page in a new tab")

    # Switch back to the temp-mail tab if needed
    # driver.switch_to.window(driver.window_handles[0])

    # Proceed with the Twitter signup process
    # Wait for the signup button to be clickable and click it
    signup_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign up']"))
    )
    signup_button.click()
    print("Clicked on the signup button")

    # Wait for and click the "Create account" button
    create_account_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Create account']"))
    )
    create_account_button.click()
    print("Clicked on the Create account button")

    # Wait for and click the "Use email instead" button
    use_email_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Use email instead']"))
    )
    use_email_button.click()
    print("Clicked on the Use email instead button")

    # Wait for the email input field to be present
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Input the temporary email into the email field
    email_input.send_keys(email)
    print(f"Entered temporary email: {email}")

    ### Date of Birth Selection ###
    # Select date of birth using Select class with correct selectors and values
    # Selecting Month
    month_select_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "SELECTOR_1"))
    )
    month_select = Select(month_select_element)
    month_select.select_by_visible_text("January")  # Alternatively, select_by_value("1")
    print("Month selected successfully: January")

    # Selecting Day
    day_select_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "SELECTOR_2"))
    )
    day_select = Select(day_select_element)
    day_select.select_by_value("1")  # Select a valid day value
    print("Day selected successfully: 1")

    # Selecting Year
    year_select_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "SELECTOR_3"))
    )
    year_select = Select(year_select_element)
    year_select.select_by_value("2000")  # Ensure this value exists in the dropdown
    print("Year selected successfully: 2000")
    #######################################

    print("Date of birth set successfully")

    # Click the Next button
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
    )
    next_button.click()
    print("Next button clicked successfully")

    # Additional steps for Twitter signup can be added here

    # Wait for a moment to see the result
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
