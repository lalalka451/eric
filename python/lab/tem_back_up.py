from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.support.ui import Select

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

    # Wait for and click the "Create account" button
    create_account_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Create account']"))
    )
    create_account_button.click()
    print("Clicked on the Create account button")


    # Wait for and click the "Use email instead" button
    use_email_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Use email instead']"))
    )
    use_email_button.click()
    print("Clicked on the Use email instead button")

    # Wait for the email input field to be present
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Click on the email input to focus it
    email_input.click()

    # Input the value '1' into the email field
    email_input.send_keys("1")

    # Print the current value of the input
    print("Current value of email input:", email_input.get_attribute("value"))

    # Wait a bit for any validation to occur
    time.sleep(22)

    # Check if the validation message exists
    try:
        validation_message = driver.find_element(By.XPATH, "//span[contains(@class, 'css-1jxf684')]")
        print("Validation message found:", validation_message.text)
    except:
        print("Validation message not found")


    #
    # # Input email
    # email_input = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.NAME, "email"))
    # )
    # email_input.send_keys("novelof391@scarden.com")
    # print("Email entered successfully")
    #
    # Select date of birth
    month_select = driver.find_element(By.XPATH, "//select[@aria-label='Month']")
    month_select.send_keys("January")
    day_select = driver.find_element(By.XPATH, "//select[@aria-label='Day']")
    day_select.send_keys("1")
    year_select = driver.find_element(By.XPATH, "//select[@aria-label='Year']")
    year_select.send_keys("2000")
    print("Date of birth set successfully")

    # # Generate and input random name
    # names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Quinn", "Avery", "Charlie"]
    # random_name = f"{random.choice(names)}{random.randint(0, 999)}"
    # name_input = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.NAME, "name"))
    # )
    # name_input.send_keys(random_name)
    # print(f"Random name entered successfully: {random_name}")
    #
    # # Re-enter name after a short delay
    # time.sleep(1)
    # name_input.clear()
    # name_input.send_keys(random_name)
    # print("Random name re-entered after 1 second")
    #
    # # Click the Next button
    # next_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
    # )
    # next_button.click()
    # print("Next button clicked successfully")

    # Wait for and input the name
    name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='name']"))
    )
    random_name = f"{random.choice(names)}{random.randint(0, 999)}"
    name_input.send_keys(random_name)
    print(f"Random name entered successfully: {random_name}")

    # Select date of birth using Select class
    month_select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Month']"))
    ))
    month_select.select_by_visible_text("January")

    day_select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Day']"))
    ))
    day_select.select_by_value("1")

    year_select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Year']"))
    ))
    year_select.select_by_value("2000")

    print("Date of birth set successfully")

    # Click the Next button
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
    )
    next_button.click()
    print("Next button clicked successfully")

    # Wait for a moment to see the result
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
