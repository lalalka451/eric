from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

# Set up the WebDriver with proxy settings
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://127.0.0.1:10809')
driver = webdriver.Chrome(options=chrome_options)  # 

try:
    # Navigate to the Twitter homepage
    driver.get("https://x.com/i/flow/login")

    # Wait for the signup button to be clickable and click it
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign up']"))
    )
    signup_button.click()
    print("Clicked on the signup button")

    try:
        # Wait for and click the "Create account" button
        create_account_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Create account']"))
        )
        create_account_button.click()
        print("Clicked on the Create account button")
    except:
        print('no use email button')

    try:
        # Wait for and click the "Use email instead" button
        use_email_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Use email instead']"))
        )
        use_email_button.click()
        print("Clicked on the Use email instead button")


    except Exception:
        print("no email input")

    # Wait for the email input field to be present
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Click on the email input to focus it
    email_input.click()

    # Input the value into the email field
    email_input.send_keys("hrthrts@outlook.com")

    # Print the current value of the input
    print("Current value of email input:", email_input.get_attribute("value"))
    # Wait a bit for any validation to occur

    # Check if the validation message exists
    try:
        validation_message = driver.find_element(By.XPATH, "//span[contains(@class, 'css-1jxf684')]")
        print("Validation message found:", validation_message.text)
    except:
        print("Validation message not found")

    names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Quinn", "Avery", "Charlie"]

    # Wait for and input the name
    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='name']"))
    )
    random_name = f"{random.choice(names)}{random.randint(0, 999)}"
    name_input.send_keys(random_name)
    print(f"Random name entered successfully: {random_name}")

    ### Updated Date of Birth Selection ###
    # Select date of birth using Select class with correct selectors and values
    # Selecting Month
    month_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "SELECTOR_1"))
    )
    month_select = Select(month_select_element)
    month_select.select_by_visible_text("January")  # Alternatively, select_by_value("1")
    print("Month selected successfully: January")

    # Selecting Day
    day_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "SELECTOR_2"))
    )
    day_select = Select(day_select_element)
    day_select.select_by_value("1")  # Select a valid day value
    print("Day selected successfully: 1")

    # Selecting Year
    year_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "SELECTOR_3"))
    )
    year_select = Select(year_select_element)
    year_select.select_by_value("2000")  # Ensure this value exists in the dropdown
    print("Year selected successfully: 2000")
    #######################################

    print("Date of birth set successfully")

    # Click the Next button
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
    )
    time.sleep(3)
    next_button.click()
    print("Next button clicked successfully")

    # Wait for a moment to see the result
    time.sleep(5000)

finally:
    # Close the browser
    driver.quit()
