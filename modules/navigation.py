import time
from selenium.webdriver.common.by import By

class Navigator:
    def __init__(self):
        self.driver = None
        
    def next_page(self) -> bool:
        selectors = [
            "a.navigate-button i.icon-new-arrow-next",
            "a.navigate-button[rel='next']",
            ".reader-pagination__next",
            ".navigate-button--next"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"🔍 Selector '{selector}' found {len(elements)} elements")
                
                for element in elements:
                    if element.is_displayed():
                        print(f"✅ Found visible element with selector: {selector}")
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", element)
                        time.sleep(1)
                        
                        if selector.startswith("a.navigate-button i.icon"):
                            click_target = self.driver.execute_script("return arguments[0].closest('a');", element)
                        else:
                            click_target = element
                        
                        if click_target:
                            print("🖱️ Clicking next page button...")
                            self.driver.execute_script("arguments[0].click();", click_target)
                            time.sleep(3)
                            return True
                    else:
                        print(f"⏸️ Element found but not visible: {selector}")
            except Exception as e:
                print(f"❌ Selenium error with selector '{selector}': {e}")
                print(f"   Error type: {type(e).__name__}")
                continue
        
        return False
    
    def update_config_url(self, new_url: str):
        try:
            with open('config.py', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                if 'start_url: str =' in line:
                    start_quote = line.find("'")
                    end_quote = line.rfind("'")
                    if start_quote != -1 and end_quote != -1:
                        lines[i] = line[:start_quote+1] + new_url + line[end_quote:]
                    break
            
            with open('config.py', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"✅ Config updated: {new_url}")
            return True
            
        except Exception as e:
            print(f"❌ Config update error: {e}")
            return False