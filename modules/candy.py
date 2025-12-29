import time
from selenium.webdriver.common.by import By

class CandyHunter:
    def __init__(self):
        self.driver = None
        self.stats = None
    
    def check_all(self, after_scroll_time: int):
        try:
            self._check_balls(after_scroll_time)
            self._check_bags(after_scroll_time)
        except Exception as e:
            print(f"Candy check error: {e}")
    
    def _check_balls(self, after_scroll_time: int):
        balls = self.driver.find_elements(By.CSS_SELECTOR, "[class*='event-gift-ball']")
        for ball in balls:
            if 'event-gift-ball--collected' in ball.get_attribute('class'):
                continue
            
            self._click_js(ball)
            time.sleep(2)
            if self.stats:
                self.stats.record_candy("candy")
                print(f'Ball found timeout on {after_scroll_time} s')
                time.sleep(after_scroll_time)
            break
    
    def _check_bags(self, after_scroll_time: int):
        bags = self.driver.find_elements(By.CSS_SELECTOR, "[class*='event-bag']")
        for bag in bags:
            if not bag.is_displayed():
                continue
            
            for _ in range(5):
                self._click_js(bag)
                time.sleep(2)
            
            if self.stats:
                self.stats.record_candy("pumpkin")
                print(f'Bag found timeout on {after_scroll_time} s')
                time.sleep(after_scroll_time)
            break
    
    def _click_js(self, element):
        self.driver.execute_script("""
            var el = arguments[0];
            el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
            el.classList.add('event-gift-ball--collected');
        """, element)