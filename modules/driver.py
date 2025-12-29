from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(headless: bool = False) -> webdriver.Chrome:
    options = Options()
    
    if headless:
        options.add_argument("--headless")
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    options.add_argument("--blink-settings=imagesEnabled=true")
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 1,
        "profile.default_content_setting_values.notifications": 2
    })
    
    driver = webdriver.Chrome(options=options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver