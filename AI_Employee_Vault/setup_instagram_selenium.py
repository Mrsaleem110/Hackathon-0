"""
Instagram Setup with Selenium - Direct login and session management
"""

import os
import json
import time
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import set_key
import pickle

# Fix Unicode encoding on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
INSTAGRAM_USERNAME = "m.saleem_ai_engineer"
INSTAGRAM_PASSWORD = "$@!eem1234"
SESSION_PATH = Path(__file__).parent / '.instagram_session'
ENV_PATH = Path(__file__).parent / '.env'


def setup_chrome_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login_to_instagram(driver, username, password):
    """Login to Instagram"""
    print(f"\n🔐 Logging in to Instagram as {username}...")

    try:
        # Go to Instagram
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        # Enter username
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_input.clear()
        username_input.send_keys(username)
        print("✅ Username entered")

        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)
        print("✅ Password entered")

        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='button']")
        login_button.click()
        print("⏳ Logging in...")

        # Wait for login to complete
        time.sleep(5)

        # Check if login was successful
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/')]"))
            )
            print("✅ Login successful!")
            return True
        except:
            print("❌ Login failed - check credentials")
            return False

    except Exception as e:
        print(f"❌ Error during login: {e}")
        return False


def handle_2fa(driver):
    """Handle 2FA if prompted"""
    try:
        # Check if 2FA prompt appears
        time.sleep(2)
        if "two_factor" in driver.current_url or "challenge" in driver.current_url:
            print("\n⚠️  2FA detected!")
            print("📱 Please complete 2FA in the browser window")
            print("⏳ Waiting for 2FA completion (60 seconds)...")

            # Wait for user to complete 2FA
            for i in range(60):
                time.sleep(1)
                if "two_factor" not in driver.current_url and "challenge" not in driver.current_url:
                    print("✅ 2FA completed!")
                    return True

            print("❌ 2FA timeout")
            return False
    except:
        pass

    return True


def get_account_info(driver):
    """Get Instagram account information"""
    try:
        print("\n📊 Fetching account information...")

        # Go to profile
        driver.get("https://www.instagram.com/accounts/edit/")
        time.sleep(3)

        # Try to get username from page
        try:
            username_elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@value]"))
            )
            username = username_elem.get_attribute("value")
            print(f"✅ Username: @{username}")
        except:
            username = INSTAGRAM_USERNAME

        # Get user ID from API
        driver.get(f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}/")
        time.sleep(2)

        try:
            page_source = driver.page_source
            if "user" in page_source:
                print(f"✅ Account info retrieved")
                return {
                    "username": username,
                    "account_id": username  # Will be updated with real ID
                }
        except:
            pass

        return {
            "username": username,
            "account_id": username
        }

    except Exception as e:
        print(f"❌ Error getting account info: {e}")
        return None


def save_session(driver):
    """Save browser session cookies"""
    try:
        print("\n💾 Saving session...")
        SESSION_PATH.mkdir(exist_ok=True)

        # Save cookies
        cookies = driver.get_cookies()
        with open(SESSION_PATH / 'cookies.pkl', 'wb') as f:
            pickle.dump(cookies, f)

        print(f"✅ Session saved to {SESSION_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error saving session: {e}")
        return False


def save_credentials(username, account_id):
    """Save credentials to .env"""
    try:
        print("\n🔑 Saving credentials to .env...")

        set_key(ENV_PATH, 'INSTAGRAM_USERNAME', username)
        set_key(ENV_PATH, 'INSTAGRAM_ACCOUNT_ID', account_id)
        set_key(ENV_PATH, 'INSTAGRAM_SESSION_PATH', str(SESSION_PATH))

        print("✅ Credentials saved")
        return True
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False


def setup_instagram():
    """Main Instagram setup flow"""
    print("\n" + "=" * 60)
    print("INSTAGRAM SETUP WITH SELENIUM")
    print("=" * 60)

    driver = None
    try:
        # Setup driver
        print("\n🚀 Starting Chrome browser...")
        driver = setup_chrome_driver()

        # Login
        if not login_to_instagram(driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD):
            return False

        # Handle 2FA if needed
        if not handle_2fa(driver):
            return False

        # Get account info
        account_info = get_account_info(driver)
        if not account_info:
            return False

        # Save session
        if not save_session(driver):
            return False

        # Save credentials
        if not save_credentials(account_info['username'], account_info['account_id']):
            return False

        print("\n" + "=" * 60)
        print("✅ INSTAGRAM SETUP COMPLETE!")
        print("=" * 60)
        print(f"\n📱 Account: @{account_info['username']}")
        print(f"📁 Session saved: {SESSION_PATH}")
        print(f"🔑 Credentials saved to .env")
        print("\nYou can now use Instagram features!")
        print("=" * 60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False

    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()


if __name__ == '__main__':
    setup_instagram()
