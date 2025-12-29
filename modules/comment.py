import time
from selenium.webdriver.common.by import By
from modules.utils import wait_fixed

class CommentPoster:
    def __init__(self):
        self.driver = None
    
    def post(self, text: str) -> bool:
        try:
            print("📝 Opening comment panel...")
            if not self._open_panel():
                return False
            
            print("📝 Writing text...")
            self._write_text(text)
            
            print("📝 Submitting...")
            if not self._submit():
                return False
            
            print("📝 Closing panel...")
            self._close_panel()
            
            print("✅ Comment posted")
            return True
        except Exception as e:
            print(f"❌ Comment error: {e}")
            return False
    
    def _open_panel(self):
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, ".reader-menu__item--comment")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", 
                button
            )
            time.sleep(2) 
            return True
        except Exception as e:
            print(f"Debug: Button click failed: {e}")
        
        try:
            icon = self.driver.find_element(By.CSS_SELECTOR, "i.icon-comment")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); arguments[0].closest('button').click();", 
                icon
            )
            time.sleep(2)
            return True
        except:
            pass
        
        print("❌ Comment button not found")
        return False
    
    def _write_text(self, text: str):
        # Spoiler
        try:
            spoilers = self.driver.find_elements(By.CSS_SELECTOR, ".comments__actions-btn--spoiler")
            for spoiler in spoilers:
                if spoiler.is_displayed():
                    self.driver.execute_script("arguments[0].click()", spoiler)
                    wait_fixed(0.5)
                    break
        except:
            pass
        
        # Textarea
        textareas = self.driver.find_elements(By.CSS_SELECTOR, "textarea")
        for ta in textareas:
            if ta.is_displayed():
                ta.clear()
                ta.send_keys(text)
                wait_fixed(1)
                return
        
        raise Exception("Textarea not found")
    
    def _submit(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".comments__send-btn")
        for btn in buttons:
            if btn.is_displayed() and 'отправить' in btn.text.lower():
                self.driver.execute_script("arguments[0].click()", btn)
                wait_fixed(2)
                return True
        
        # Backup по тексту
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if btn.is_displayed() and 'отправить' in btn.text.lower():
                self.driver.execute_script("arguments[0].click()", btn)
                wait_fixed(2)
                return True
        
        print("❌ Submit button not found")
        return False
    
    def _close_panel(self):
        selectors = [
            ".reader-comments__close",
            ".modal__close",
            "button[aria-label*='close']"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    if el.is_displayed():
                        self.driver.execute_script("arguments[0].click()", el)
                        wait_fixed(1)
                        return
            except:
                continue