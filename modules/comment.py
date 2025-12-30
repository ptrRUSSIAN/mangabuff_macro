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
        # First selector attempt
        try:
            button = self.driver.find_element(By.CSS_SELECTOR, ".reader-menu__item--comment")
            print(f"🔍 Selector '.reader-menu__item--comment' found element")
            if button.is_displayed():
                print(f"✅ Opening comment panel with first selector...")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", 
                    button
                )
                time.sleep(2) 
                return True
            else:
                print(f"⏸️ Element found but not visible: .reader-menu__item--comment")
        except Exception as e:
            print(f"❌ Selenium error with selector '.reader-menu__item--comment': {e}")
            print(f"   Error type: {type(e).__name__}")
        
        # Second selector attempt
        try:
            icon = self.driver.find_element(By.CSS_SELECTOR, "i.icon-comment")
            print(f"🔍 Selector 'i.icon-comment' found element")
            if icon.is_displayed():
                print(f"✅ Opening comment panel with second selector...")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'}); arguments[0].closest('button').click();", 
                    icon
                )
                time.sleep(2)
                return True
            else:
                print(f"⏸️ Element found but not visible: i.icon-comment")
        except Exception as e:
            print(f"❌ Selenium error with selector 'i.icon-comment': {e}")
            print(f"   Error type: {type(e).__name__}")
        
        print("❌ Comment button not found")
        return False
    
    def _write_text(self, text: str):
        # Spoiler
        try:
            spoilers = self.driver.find_elements(By.CSS_SELECTOR, ".comments__actions-btn--spoiler")
            print(f"🔍 Selector '.comments__actions-btn--spoiler' found {len(spoilers)} elements")
            for spoiler in spoilers:
                if spoiler.is_displayed():
                    print(f"✅ Clicking spoiler button...")
                    self.driver.execute_script("arguments[0].click()", spoiler)
                    wait_fixed(0.5)
                    break
                else:
                    print(f"⏸️ Spoiler element found but not visible")
        except Exception as e:
            print(f"❌ Selenium error with spoiler selector: {e}")
            print(f"   Error type: {type(e).__name__}")
        
        # Textarea
        textareas = self.driver.find_elements(By.CSS_SELECTOR, "textarea")
        print(f"🔍 Selector 'textarea' found {len(textareas)} elements")
        for ta in textareas:
            if ta.is_displayed():
                print(f"✅ Writing comment text...")
                ta.clear()
                ta.send_keys(text)
                wait_fixed(1)
                return
            else:
                print(f"⏸️ Textarea found but not visible")
        
        raise Exception("Textarea not found")
    
    def _submit(self):
        # First selector attempt
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".comments__send-btn")
        print(f"🔍 Selector '.comments__send-btn' found {len(buttons)} elements")
        for btn in buttons:
            if btn.is_displayed() and 'отправить' in btn.text.lower():
                print(f"✅ Clicking submit button with first selector...")
                self.driver.execute_script("arguments[0].click()", btn)
                wait_fixed(2)
                return True
            elif btn.is_displayed():
                print(f"⏸️ Submit button found but text doesn't contain 'отправить': {btn.text}")
        
        # Backup по тексту
        print("🔍 Trying backup selector: button tags")
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if btn.is_displayed() and 'отправить' in btn.text.lower():
                print(f"✅ Clicking submit button with backup selector...")
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
                print(f"🔍 Selector '{selector}' found {len(elements)} elements")
                for el in elements:
                    if el.is_displayed():
                        print(f"✅ Closing panel with selector: {selector}")
                        self.driver.execute_script("arguments[0].click()", el)
                        wait_fixed(1)
                        return
                    else:
                        print(f"⏸️ Element found but not visible: {selector}")
            except Exception as e:
                print(f"❌ Selenium error with selector '{selector}': {e}")
                print(f"   Error type: {type(e).__name__}")
                continue
