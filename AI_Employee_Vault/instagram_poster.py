"""
Instagram Poster - Post to Instagram using Selenium session
"""

import os
import time
import pickle
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', 'm.saleem_ai_engineer')
SESSION_PATH = Path(os.getenv('INSTAGRAM_SESSION_PATH', '.instagram_session'))
ENV_PATH = Path(__file__).parent / '.env'


def setup_chrome_driver():
    """Setup Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def load_session(driver):
    """Load saved session cookies"""
    try:
        print("📁 Loading saved session...")
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        cookies_file = SESSION_PATH / 'cookies.pkl'
        if not cookies_file.exists():
            print("❌ Session file not found")
            return False

        with open(cookies_file, 'rb') as f:
            cookies = pickle.load(f)

        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                pass

        # Refresh to apply cookies
        driver.refresh()
        time.sleep(3)

        print("✅ Session loaded")
        return True

    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return False


def is_logged_in(driver):
    """Check if user is logged in"""
    try:
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        # Check for profile link
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/accounts/edit/')]"))
        )
        print("✅ Logged in successfully")
        return True
    except:
        print("❌ Not logged in")
        return False


def download_image(image_url, save_path):
    """Download image from URL"""
    try:
        print(f"📥 Downloading image from {image_url}...")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ Image saved to {save_path}")
        return True
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return False


def post_to_instagram(driver, caption, image_path=None, image_url=None):
    """Post to Instagram"""
    try:
        print("\n📱 Starting Instagram post...")

        # Download image if URL provided
        if image_url and not image_path:
            image_path = Path(__file__).parent / 'temp_instagram_image.jpg'
            if not download_image(image_url, image_path):
                return False

        # Go to Instagram home
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        # Click create button
        print("🔍 Looking for create button...")
        create_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/create/')]"))
        )
        create_button.click()
        print("✅ Create button clicked")

        time.sleep(2)

        # Select image if provided
        if image_path:
            print(f"📸 Uploading image: {image_path}")

            # Find file input
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(str(image_path.absolute()))
            print("✅ Image uploaded")

            time.sleep(3)

            # Click Next
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
            print("✅ Clicked Next")

            time.sleep(2)

            # Click Next again (filters page)
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
            print("✅ Clicked Next (filters)")

            time.sleep(2)

        # Add caption
        print(f"✍️  Adding caption: {caption[:50]}...")
        caption_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption...']"))
        )
        caption_input.click()
        caption_input.send_keys(caption)
        print("✅ Caption added")

        time.sleep(1)

        # Click Share button
        print("📤 Posting...")
        share_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Share')]"))
        )
        share_button.click()

        # Wait for post to complete
        time.sleep(5)

        print("✅ Post shared successfully!")
        return True

    except Exception as e:
        print(f"❌ Error posting: {e}")
        return False


def post_instagram(caption, image_path=None, image_url=None):
    """Main function to post to Instagram"""
    print("\n" + "=" * 60)
    print("INSTAGRAM POSTER")
    print("=" * 60)

    driver = None
    try:
        # Setup driver
        print("\n🚀 Starting Chrome browser...")
        driver = setup_chrome_driver()

        # Load session
        if not load_session(driver):
            print("❌ Failed to load session")
            return False

        # Check if logged in
        if not is_logged_in(driver):
            print("❌ Not logged in")
            return False

        # Post
        if not post_to_instagram(driver, caption, image_path, image_url):
            return False

        print("\n" + "=" * 60)
        print("✅ POST COMPLETE!")
        print("=" * 60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()


if __name__ == '__main__':
    # Example usage
    caption = "🚀 AI Employee Vault - Automating business workflows!\n\n#AI #Automation #Business"
    image_url = "https://via.placeholder.com/1080x1080?text=AI+Employee+Vault"

    post_instagram(caption, image_url=image_url)
