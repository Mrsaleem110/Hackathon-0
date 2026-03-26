"""
X (Twitter) Post Automation - Simplified version
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def post_to_x(tweet_text):
    """Post a tweet to X using Selenium"""

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Opening X.com...")
        driver.get("https://x.com/home")

        time.sleep(5)

        # Check if logged in
        try:
            # Look for the compose button or tweet area
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))
            )
            print("Already logged in!")
        except:
            print("Please log in manually in the browser window...")
            print("Waiting for login (120 seconds)...")
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))
            )
            print("Login detected!")

        time.sleep(2)

        # Click on tweet area
        print("Clicking tweet area...")
        tweet_area = driver.find_element(By.XPATH, "//div[@data-testid='tweetTextarea_0']")
        tweet_area.click()

        time.sleep(1)

        # Type tweet
        print("Typing tweet...")
        tweet_area.send_keys(tweet_text)

        time.sleep(1)

        # Find and click post button
        print("Posting...")
        post_button = driver.find_element(By.XPATH, "//button[@data-testid='Tweet_Button_Base']")
        post_button.click()

        print("Tweet posted!")
        time.sleep(3)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    tweet_text = "Agentic Sphere: AI Employee Vault\nMulti-channel detection, intelligent planning, autonomous execution. The future of work is here."
    post_to_x(tweet_text)
