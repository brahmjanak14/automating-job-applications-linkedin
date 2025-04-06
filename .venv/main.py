from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials
ACCOUNT_EMAIL = os.getenv('ACCOUNT_EMAIL')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')
PHONE = os.getenv('PHONE')

# Set up Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=chrome_options)

# Open LinkedIn job search
browser.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom")

time.sleep(3)

# Click Sign In Button
try:
    sign_in_button = browser.find_element(By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
    sign_in_button.click()
    time.sleep(3)
except NoSuchElementException:
    print("Sign-in button not found. Proceeding...")

# Sign in Linkdin
time.sleep(5)
email_input = browser.find_element(by = By.ID, value="base-sign-in-modal_session_key")
email_input.send_keys(ACCOUNT_EMAIL)
password_input = browser.find_element(by = By.ID, value="base-sign-in-modal_session_password")
password_input.send_keys(ACCOUNT_PASSWORD)
password_input.send_keys(Keys.ENTER)


# Wait for page to load
time.sleep(5)
input("Solve Captcha and Press Enter to Continue...")

# Function to close application pop-up
def abort_application():
    try:
        close_button = browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Dismiss')]")
        close_button.click()
        time.sleep(2)

        discard_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Discard')]")
        discard_button.click()
    except NoSuchElementException:
        print("Close or Discard button not found.")

# Get all job listings
time.sleep(5)
job_listings = browser.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

print(f"Found {len(job_listings)} jobs.")

# Loop through each job
for job in job_listings:
    try:
        print("\nOpening job listing...")
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", job)
        time.sleep(1)
        job.click()
        time.sleep(2)

        # Click Apply Button
        try:
            apply_button = browser.find_element(By.CSS_SELECTOR, ".jobs-apply-button")
            apply_button.click()
            time.sleep(3)

            # Fill Phone Number if required
            try:
                phone_input = browser.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
                if phone_input.get_attribute("value") == "":
                    phone_input.send_keys(PHONE)
            except NoSuchElementException:
                print("Phone input not found. Skipping...")

            # Check Submit Button
            submit_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "footer button"))
            )

            button_text = submit_button.text.lower()

            # Skip multi-step applications
            if "next" in button_text or "continue" in button_text:
                abort_application()
                print("❌ Complex application detected, skipping...")
            else:
                # Click Submit Button
                print("✅ Submitting application...")
                submit_button.click()
                time.sleep(2)

                # Close the success popup
                try:
                    close_button = browser.find_element(By.XPATH, "//button[contains(@aria-label, 'Dismiss')]")
                    browser.execute_script("arguments[0].click();", close_button)
                except NoSuchElementException:
                    print("No close button found.")

        except NoSuchElementException:
            print("No Easy Apply button found, skipping job.")

    except ElementClickInterceptedException:
        print("Element not clickable, skipping job.")

# Close browser
print("All jobs processed!")
browser.quit()
