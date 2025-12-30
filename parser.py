import time
import signal
import sys
from config import ParserConfig
from modules.auth import AuthManager
from modules.scrolling import ScrollManager
from modules.candy import CandyHunter
from modules.comment import CommentPoster
from modules.mine import MineWorker
from modules.navigation import Navigator
from modules.stats import StatsCollector
from modules.utils import wait_fixed

class MangaParser:
    def __init__(self, config: ParserConfig, headless: bool = False):
        self.config = config
        self.driver = None
        self.stats = StatsCollector()
        
        # Менеджеры
        self.auth = AuthManager(headless)
        self.candy_hunter = CandyHunter()
        self.scroller = ScrollManager()
        self.commenter = CommentPoster()
        self.mine_worker = MineWorker()
        self.nav = Navigator()
        
        self.mine_done = False
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        print("\n\n⚠️ INTERRUPTING...")
        self.stats.print_final()
        self.cleanup()
        sys.exit(0)
    
    def _bind_managers(self):
        for manager in [self.nav, self.scroller, self.candy_hunter,
                        self.commenter, self.mine_worker]:
            manager.driver = self.driver
            manager.config = self.config
            manager.stats = self.stats
        
        self.scroller.candy_hunter = self.candy_hunter
        self.nav.config = self.config
    
    def setup(self):
        print("🚀 Setting up driver...")
        self.driver = self.auth.setup_driver()
        print("🍪 Loading cookies...")
        self.auth.load_cookies(self.driver)
        self._bind_managers()
        self.stats.start()
        print("✅ Setup complete")
    
    def cleanup(self):
        if self.driver:
            print("🚪 Closing browser...")
            self.driver.quit()
    
    def login_only(self):
        self.setup()
        print("👤 Please login in the browser...")
        input("Press Enter after login...")
        self.auth.save_cookies(self.driver)
    
    def _navigate_with_cooldown(self, url: str, cooldown: int = 5):
        print(f'🌐 Navigating: {url}')
        self.driver.get(url)
        wait_fixed(cooldown)
    
    def _refresh_with_cooldown(self, cooldown: int = 3):
        print('🔄 Refreshing page')
        self.driver.refresh()
        wait_fixed(cooldown)
        
    def parse_manga(self):
        try:
            self.setup()
            current_day = 0
            current_url = self.config.start_url
            
            while True:
                now = time.localtime().tm_mday
                if now != current_day:
                    if current_day != 0:
                        print("🔄 Day changed! Resetting counters...")
                        current_day = now
                        self.mine_done = False
                        self.config.comments_ready = 0
                
                print(f"\n{'='*60}")
                print(f"📖 Processing: {current_url}")
                print(f"📊 Stats: {self.stats.candy_count} candies, {self.stats.pumpkin_count} pumpkins")
                print(f"{'='*60}")

                self._navigate_with_cooldown(current_url, 5)
                
                # Комментарии
                if self.config.comment_on and self.config.comments_ready < self.config.comments_need:
                    print(f"📝 Posting comment ({self.config.comments_ready + 1}/{self.config.comments_need})")
                    self._refresh_with_cooldown(3)
                    self.commenter.post(self.config.comment_text)
                    self.config.comments_ready += 1
                
                # Шахта
                elif self.config.mine_needed and not self.mine_done:
                    print("⛏️ Processing mine...")
                    self.mine_done = self.mine_worker.work()
                
                # Скроллинг
                print(f"📜 Starting scroll (mode {self.config.scroll_mode})")
                self.scroller.smooth_scroll(
                    self.config.scroll_time,
                    self.config.after_found_time,
                    self.config.scroll_mode
                )
                
                # Следующая страница
                print("➡️ Looking for next page...")
                if not self.nav.next_page():
                    print("❌ No next page found")
                    break
                
                new_url = self.driver.current_url
                if new_url != current_url:
                    self.nav.update_config_url(new_url)
                    current_url = new_url
                
                wait_fixed(3)
        except KeyboardInterrupt:
            print("\n\n⚠️ Program interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"❌ Critical error: {e}")
        finally:
            self.stats.print_final()