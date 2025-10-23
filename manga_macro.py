import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
from config import start_url, scroll_time, comment_on, comment_text, comments_need,comments_ready,mine_needed, after_scroll_time, scroll_mode
from datetime import datetime

class MangaParser:
    def __init__(self, headless=False):
        self.chrome_options = Options()
        
        if headless:
            self.chrome_options.add_argument("--headless")
        
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        self.chrome_options.add_argument("--blink-settings=imagesEnabled=true")
        self.chrome_options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 1,
            "profile.default_content_setting_values.notifications": 2
        })
        self.chrome_options.set_capability("pageLoadStrategy", "none")  
        
        self.driver = None
        self.cookies_file = "manga_cookies.json"
        self.comments_count = comments_ready
        self.max_comments_per_session = comments_need
        
        self.candy_times = []
        self.candy_count = 0
        self.pumpkin_count = 0

    def update_config_url(self, new_url):
        try:
            with open('config.py', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                if line.startswith('start_url ='):
                    lines[i] = f"start_url = '{new_url}'\n"
                    break
            
            with open('config.py', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"✅ Конфиг обновлен: {new_url}")
        except Exception as e:
            print(f"❌ Ошибка обновления конфига: {e}")

    def setup_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.set_page_load_timeout(1)
        self.driver.set_script_timeout(10)
        self.load_cookies()

    def save_cookies(self): 
        if self.driver:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f)
        print('Куки файлы сохранены')

    def retry_on_timeout(self, func, max_attempts=3, delay=5, func_name=""):
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if "timed out" in str(e) or "Read timed out" in str(e) or "TimeoutException" in str(e):
                    print(f"⚠️ Таймаут {func_name} (попытка {attempt + 1}/{max_attempts}): {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        continue
                else:
                    raise e
        print(f"❌ Пропускаем {func_name} после {max_attempts} неудачных попыток")
        return None

    def load_cookies(self):
        print('Выгружаю куки фйлы...')
        if os.path.exists(self.cookies_file):
            try:
                self.driver.get("https://mangabuff.ru")
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                time.sleep(2)
            except Exception as e:
                print(f"Error loading cookies: {e}")
        print('Куки файлы загружены')

    def wait_fixed_cooldown(self, seconds=5):
        print(f'Жду {seconds} секунд фиксированного кулдауна')
        time.sleep(seconds)
        print('Кулдаун завершен')

    def navigate_with_cooldown(self, url, cooldown=5):
        try:
            print(f'Перехожу по URL: {url}')
            self.driver.set_page_load_timeout(2)
            self.driver.get(url)
        except Exception as e:
            print(f'Игнорируем таймаут загрузки: {e}')
        finally:
            self.wait_fixed_cooldown(cooldown)

    def refresh_with_cooldown(self, cooldown=3):
        try:
            print('Обновляю страницу')
            self.driver.set_page_load_timeout(cooldown)
            self.driver.refresh()
        except Exception as e:
            print(f'Игнорируем таймаут обновления: {e}')
        finally:
            self.wait_fixed_cooldown(cooldown)

    def smooth_scroll(self, duration=30, after_scroll_time=15, mode=1):
        if mode == 1:
            start_time = time.time()
            
            print(f'Скролю страницу {duration} секунд')
            
            while time.time() - start_time < duration:
                cycle_start = time.time()
                
                self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
                time.sleep(0.5)
                self.enhanced_check_buttons()
                
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
                time.sleep(0.5)
                self.enhanced_check_buttons()
                
                self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
                time.sleep(0.5)
                self.enhanced_check_buttons()
                
                cycle_elapsed = time.time() - cycle_start
                if cycle_elapsed < 5:
                    time.sleep(5 - cycle_elapsed)
            
            print(f'Страница доскролена, проверяю конфеты {after_scroll_time} секунд')
            
            final_check_start = time.time()
            while time.time() - final_check_start < after_scroll_time:
                time.sleep(1)
                self.enhanced_check_buttons()
            
            print(f'Наличие конфеты проверено')

        elif mode == 2:

            start_time = time.time()
            viewport_height = self.driver.execute_script("return window.innerHeight")
            step_time = 2.0

            scroll_iteration = 0
            print(f'Скролю страницу {duration} секунд')
            while time.time() - start_time < duration:
                scroll_iteration += 1

                current_position = self.driver.execute_script("return window.pageYOffset;")
                current_total_height = self.driver.execute_script("return document.body.scrollHeight")
                remaining_height = current_total_height - current_position - viewport_height

                if remaining_height <= 0:
                    break

                time_elapsed = time.time() - start_time
                time_left = duration - time_elapsed

                if time_left <= 0:
                    break

                current_pixels_per_second = remaining_height / time_left if time_left > 0 else remaining_height
                scroll_down_distance = current_pixels_per_second * step_time
                scroll_down_distance = max(100, min(scroll_down_distance, 800))

                if scroll_down_distance > 0:
                    self.driver.execute_script(f"""
                        window.scrollBy({{
                            top: {scroll_down_distance},
                            left: 0,
                            behavior: 'smooth'
                        }});
                    """)
                    time.sleep(1)
            print(f'Страница доскролена, проверяю конфеты {after_scroll_time} секунд')
            while time.time() - start_time < duration + after_scroll_time:
                time.sleep(1)
                self.enhanced_check_buttons()
            print(f'Наличие конфеты проверено')

    def record_candy_found(self, candy_type="candy"):
        current_time = datetime.now()
        self.candy_times.append(current_time)
        
        if candy_type == "pumpkin":
            self.pumpkin_count += 1
            self.candy_count += 3
            print(f"🎃 Найдена тыква! +3 конфеты (всего конфет: {self.candy_count})")
        else:
            self.candy_count += 1
            print(f"🍬 Найдена конфета! (всего конфет: {self.candy_count})")
        
        if len(self.candy_times) > 1:
            self.print_candy_statistics()

    def print_candy_statistics(self):
        if len(self.candy_times) < 2:
            return
            
        total_seconds = 0
        for i in range(1, len(self.candy_times)):
            time_diff = (self.candy_times[i] - self.candy_times[i-1]).total_seconds()
            total_seconds += time_diff
        
        avg_time = total_seconds / (len(self.candy_times) - 1)
        print(f"📊 Статистика: найдено {self.candy_count} конфет ({self.pumpkin_count} тыкв), среднее время между конфетами: {avg_time:.1f} сек")

    def enhanced_check_buttons(self):
        self.check_event_ball_buttons()
        self.check_event_bag_buttons()
    
    def check_event_ball_buttons(self):
        try:
            selectors = [
                "[class*='event-gift-ball']",
                "div[class*='event-gift-ball']"
            ]
            
            candy_found = False
            for selector in selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        try:
                            class_name = button.get_attribute('class')
                            if 'event-gift-ball--collected' in class_name:
                                continue
                                
                            self.driver.execute_script("""
                                var element = arguments[0];
                                element.style.display = 'block';
                                element.style.visibility = 'visible';
                                element.style.opacity = '1';
                                element.style.pointerEvents = 'auto';
                            """, button)
                            
                            script = """
                            var element = arguments[0];
                            
                            function triggerEvent(element, eventType) {
                                var event = new MouseEvent(eventType, {
                                    'view': window,
                                    'bubbles': true,
                                    'cancelable': true,
                                    'clientX': element.getBoundingClientRect().left + element.offsetWidth / 2,
                                    'clientY': element.getBoundingClientRect().top + element.offsetHeight / 2,
                                    'button': 0,
                                    'buttons': 1
                                });
                                element.dispatchEvent(event);
                            }
                            
                            triggerEvent(element, 'mouseover');
                            triggerEvent(element, 'mousedown');
                            triggerEvent(element, 'mouseup');
                            triggerEvent(element, 'click');
                            
                            if (window.jQuery) {
                                var $elem = jQuery(element);
                                if ($elem) {
                                    $elem.trigger('mouseenter');
                                    $elem.trigger('mousedown');
                                    $elem.trigger('mouseup');
                                    $elem.trigger('click');
                                }
                            }
                            
                            return 'Event triggered';
                            """
                            
                            self.driver.execute_script(script, button)
                            time.sleep(2)
                            
                            if not candy_found:
                                self.record_candy_found("candy")
                                candy_found = True
                            
                        except Exception as e:
                            pass
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print("ball error")
            pass

    def check_event_bag_buttons(self):
        try:
            selectors = [
                "[class*='event-bag']",
                "div[class*='event-bag']",
                ".event-bag"
            ]
            
            candy_found = False
            for selector in selectors:
                try:
                    bags = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for bag in bags:
                        try:
                            class_name = bag.get_attribute('class')
                            is_displayed = bag.is_displayed()
                            
                            for click_count in range(10):
                                try:
                                    script = """
                                    var element = arguments[0];
                                    var clickCount = arguments[1];
                                    
                                    var event = new MouseEvent('click', {
                                        view: window,
                                        bubbles: true,
                                        cancelable: true,
                                        clientX: element.getBoundingClientRect().left + element.offsetWidth / 2,
                                        clientY: element.getBoundingClientRect().top + element.offsetHeight / 2,
                                        button: 0
                                    });
                                    
                                    element.dispatchEvent(event);
                                    
                                    if (window.jQuery) {
                                        jQuery(element).trigger('click');
                                    }
                                    
                                    return 'Click ' + clickCount + ' triggered';
                                    """
                                    
                                    self.driver.execute_script(script, bag, click_count + 1)
                                    time.sleep(0.3)
                                    
                                    if not candy_found:
                                        self.record_candy_found("candy")
                                        candy_found = True
                                    
                                except Exception as e:
                                    pass
                            
                            time.sleep(2)
                            break
                            
                        except Exception as e:
                            pass
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print('bag error')
            pass

    def check_pumpkin_on_event_page(self):
        try:
            pumpkin_selectors = [
                "[class*='pumpkin']",
                "[class*='halloween']",
                ".event-game__item"
            ]
            
            for selector in pumpkin_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return True
            return False
        except:
            return False

    def post_comment(self, comment_text="спаисбо за главу"):
        if self.comments_count >= self.max_comments_per_session:
            print('Написано достаточно комментариев')
            return False

        try:
            print(f'Пишу комментарий "{comment_text}"')
            time.sleep(3)
            self.refresh_with_cooldown(3)
            comment_button_selectors = [
                ".reader-menu__item--comment",
                "[class*='comment']",
                ".reader-menu__item i.icon-comment"
            ]
            
            comment_button = None
            for selector in comment_button_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            comment_button = element
                            break
                    if comment_button:
                        break
                except:
                    continue
            
            if not comment_button:
                print("Не найдена кнопка комментариев")
                return False
                
            self.driver.execute_script("arguments[0].click();", comment_button)
            time.sleep(3)
                        
            spoiler_selectors = [
                ".comments__actions-btn--spoiler",
                "[class*='spoiler']",
                "button[title*='спойлер']"
            ]
            
            spoiler_button = None
            for selector in spoiler_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            spoiler_button = element
                            break
                    if spoiler_button:
                        break
                except:
                    continue
            
            if spoiler_button:
                self.driver.execute_script("arguments[0].click();", spoiler_button)
                time.sleep(1)
            
            textarea_selectors = [
                ".comments__send-form textarea",
                "textarea[placeholder*='комментарий']",
                "textarea.comments__textarea"
            ]
            
            comment_textarea = None
            for selector in textarea_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            comment_textarea = element
                            break
                    if comment_textarea:
                        break
                except:
                    continue
            
            if not comment_textarea:
                print("Не найдено поле для комментария")
                return False
                
            comment_textarea.clear()
            comment_textarea.send_keys(comment_text)
            time.sleep(1)
            
            send_selectors = [
                ".comments__send-btn",
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Отправить')"
            ]
            
            send_button = None
            for selector in send_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and "отправить" in element.text.lower():
                            send_button = element
                            break
                    if send_button:
                        break
                except:
                    continue
            
            if send_button:
                self.driver.execute_script("arguments[0].click();", send_button)
                time.sleep(2)
            
            close_selectors = [
                ".reader-comments__close",
                ".modal__close",
                "button[aria-label*='close']",
                "button:contains('Закрыть')"
            ]
            
            close_button = None
            for selector in close_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            close_button = element
                            break
                    if close_button:
                        break
                except:
                    continue
            
            if close_button:
                self.driver.execute_script("arguments[0].click();", close_button)
            
            self.comments_count += 1
            print(f"✅ Комментарий написан ({self.comments_count}/{self.max_comments_per_session})")
            time.sleep(2)
            return True

        except Exception as e:
            print(f'comment_error: {e}')
            return False


    def go_to_mine(self):
        try:
            print('Отправляюсь в шахту')
            current_url = self.driver.current_url
            
            profile_selectors = [
                ".header-profile.dropdown__trigger",
                ".user-avatar",
                "[class*='profile']",
                "[class*='dropdown']"
            ]
            
            profile_button = None
            for selector in profile_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            profile_button = element
                            break
                    if profile_button:
                        break
                except:
                    continue
            
            if not profile_button:
                print("Не найдена кнопка профиля")
                return False
                
            self.driver.execute_script("arguments[0].click();", profile_button)
            time.sleep(2)
            
            mine_selectors = [
                "a[href='/mine']",
                "a[href*='mine']",
                "a:contains('Шахта')",
                "a:contains('шахта')"
            ]
            
            mine_link = None
            for selector in mine_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and ("шахт" in element.text.lower() or "mine" in element.text.lower()):
                            mine_link = element
                            break
                    if mine_link:
                        break
                except:
                    continue
            
            if not mine_link:
                print("Не найдена ссылка на шахту")
                return False
                
            self.driver.execute_script("arguments[0].click();", mine_link)
            time.sleep(3)
            
            if "mine" not in self.driver.current_url:
                print("Не удалось перейти на страницу шахты")
                return False
            
            hits_left = self.check_mine_hits()
            print(f'Нужно вскопать еще {hits_left} раз')
            
            while hits_left > 0:
                success = self.click_mine_button()
                if success:
                    hits_left -= 1
                time.sleep(0.5)
                
                if hits_left % 5 == 0:
                    hits_left = self.check_mine_hits()

            print('Шахта вскопана')
            
            self.navigate_with_cooldown(current_url, 3)
            return True

        except Exception as e:
            print(f'mine error: {e}')
            return False

    def click_mine_button(self):
        try:
            mine_button = self.driver.find_element(By.CSS_SELECTOR, ".main-mine__game-tap")
            mine_button.click()
            time.sleep(0.1)  
            return True
        except:
            return False

    def check_mine_hits(self):
        try:
            hits_element = self.driver.find_element(By.CSS_SELECTOR, ".main-mine__game-hits-left")
            hits_text = hits_element.text.strip()
            return int(hits_text)
        except:
            return 0

    def go_to_next_page(self):
        try:
            print('Перелистываю страницу')
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.navigate-button i.icon-new-arrow-next"))
            )
            
            link = next_button.find_element(By.XPATH, "./..")
            link.click()
            print('Страница перевернута')
            return True
                
        except Exception as e:
            print('next page error')
            return False

    def quick_scroll_to_bottom(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            return True
        except:
            return False

    def parse_manga(self, start_url, scroll_duration=30, comment_text="спаисбо за главу", after_scroll_time=15, scroll_mode=1):
        try:
            self.setup_driver()
            current_url = start_url
            mine_flag = False
            
            current_day = datetime.now().day
            day_changed = False

            while True:
                now = datetime.now()
                if now.day != current_day:
                    print("🔄 Обнаружена смена дня! Сбрасываем счетчики...")
                    current_day = now.day
                    mine_flag = False 
                    self.comments_count = 0  
                    day_changed = True

                cycle_start_time = datetime.now()
                print(f"Начало цикла - {cycle_start_time}")
                print(f"📊 Всего найдено конфет: {self.candy_count}")

                if day_changed:
                    print("🎉 Счетчики сброшены для нового дня!")
                    day_changed = False
                
                self.navigate_with_cooldown(current_url, 5)
                
                if self.comments_count < self.max_comments_per_session and comment_on:
                    self.refresh_with_cooldown(3)
                    self.post_comment(comment_text)

                elif not mine_flag and mine_needed:   
                    mine_result = self.go_to_mine()
                    if mine_result is not None:
                        mine_flag = mine_result

                self.retry_on_timeout(
                    lambda: self.smooth_scroll(scroll_duration, after_scroll_time, mode=scroll_mode),
                    func_name="скроллинг страницы"
                )

                next_page_success = False
                a = 3
                for attempt in range(a):
                    self.quick_scroll_to_bottom()
                    self.enhanced_check_buttons()
                    
                    next_result = self.retry_on_timeout(
                        lambda: self.go_to_next_page(),
                        func_name="переход на следующую страницу"
                    )
                    time.sleep(5)
                    if next_result:
                        self.refresh_with_cooldown(3)
                        next_page_success = True
                        break
                    print(f"Не удалось открыть следующую страницу, попытка {attempt + 1}/{a}")
                    time.sleep(2)

                if not next_page_success:
                    break

                new_url = self.driver.current_url
                if new_url != current_url:
                    self.update_config_url(new_url)
                    current_url = new_url

                self.wait_fixed_cooldown(3)
                
        except Exception as e:
            print(f"Критическая ошибка: {e}")
        finally:
            if self.candy_count > 0:
                print(f"🎯 ФИНАЛЬНАЯ СТАТИСТИКА: найдено {self.candy_count} конфет ({self.pumpkin_count} тыкв)")
                if len(self.candy_times) > 1:
                    total_seconds = (self.candy_times[-1] - self.candy_times[0]).total_seconds()
                    avg_time = total_seconds / (len(self.candy_times) - 1)
                    print(f"📊 Среднее время между конфетами: {avg_time:.1f} сек")
            exit

    def login_only(self):
        self.setup_driver()
        self.driver.get("https://mangabuff.ru")
        input("Press Enter after login...")
        self.save_cookies()
        self.driver.quit()

def main():

    print("1 - Login only")
    print("2 - Full parsing")
    
    choice = input("Enter mode (1 or 2): ").strip()
    
    parser = MangaParser(headless=False)
    
    if choice == "1":
        parser.login_only()
    elif choice == "2":
        START_URL = start_url
        SCROLL_DURATION = scroll_time
        COMMENT_TEXT = comment_text
        
        parser.parse_manga(
            start_url=START_URL,
            scroll_duration=SCROLL_DURATION,
            comment_text=COMMENT_TEXT,
            after_scroll_time=after_scroll_time,
            scroll_mode=scroll_mode
        )
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
