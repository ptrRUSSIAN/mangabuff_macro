import json
import os
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from modules.driver import create_driver
from modules.utils import wait_fixed

class AuthManager:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.cookies_file = "manga_cookies.json"
    
    def setup_driver(self) -> WebDriver:
        return create_driver(self.headless)
    
    def save_cookies(self, driver: WebDriver):
        cookies = driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Saved {len(cookies)} cookies")
    
    def load_cookies(self, driver: WebDriver):
        if not os.path.exists(self.cookies_file):
            print("⚠️ Cookie file not found, starting fresh")
            return
        
        try:
            print('🍪 Loading cookies...')
            
            driver.get("https://mangabuff.ru")
            
            wait_fixed(3)
            
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    try:
                        if 'domain' in cookie:
                            del cookie['domain']
                        driver.add_cookie(cookie)
                    except Exception as e:
                        pass 
            
            wait_fixed(2)
            driver.refresh()
            wait_fixed(1)
            
            print('✅ Cookies loaded')
            
        except Exception as e:
            print(f'⚠️ Cookie loading issue: {e}')