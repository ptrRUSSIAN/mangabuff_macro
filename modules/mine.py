import time
from selenium.webdriver.common.by import By
from modules.utils import wait_fixed

class MineWorker:
    def __init__(self):
        self.driver = None
        self.config = None
    
    def work(self) -> bool:
        try:
            print("⛏️ Processing mine...")
            current_url = self.driver.current_url
            
            profile = self.driver.find_element(By.CSS_SELECTOR, ".header-profile")
            self.driver.execute_script("arguments[0].click()", profile)
            wait_fixed(2)
            
            mine_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='/mine']")
            self.driver.execute_script("arguments[0].click()", mine_link)
            wait_fixed(3)
            hit_log = True
            while True:
                hits = self._get_hits(hit_log)
                hit_log = False
                if hits <= 0:
                    break
                
                self._click()
                wait_fixed(0.3)
            
            print("✅ Mine completed")
            self.driver.get(current_url)
            wait_fixed(3)
            return True
        except Exception as e:
            print(f"Mine error: {e}")
            return False
    
    def _get_hits(self, hit_log) -> int:
        try:
            hits = int(self.driver.find_element(By.CSS_SELECTOR, ".main-mine__game-hits-left").text)
            if hit_log:
                print(f'Need to do {hits} hits')
            return hits
        except:
            return 0
    
    def _click(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".main-mine__game-tap").click()
        except:
            pass