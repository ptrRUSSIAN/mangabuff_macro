import time

class ScrollManager:
    def __init__(self):
        self.driver = None
        self.candy_hunter = None
        self.stats = None
        self.config = None
    
    def smooth_scroll(self, duration: int, after_scroll: int, mode: int = 1):
        if mode == 1:
            self._mode_1(duration, after_scroll)
        else:
            self._mode_2(duration, after_scroll)
    
    def _mode_1(self, duration: int, after_scroll: int):
        start = time.time()
        print(f'📜 Mode 1 scrolling for {duration}s')
        
        iteration = 0
        while time.time() - start < duration:
            iteration += 1
            cycle_start = time.time()
            
            # ВНИЗ
            self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
            time.sleep(.5)
            if self.candy_hunter:
                self.candy_hunter.check_all(after_scroll)
            
            # ВВЕРХ
            self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'})")
            time.sleep(0.5)
            if self.candy_hunter:
                self.candy_hunter.check_all(after_scroll)
            
            # ВНИХ еще раз
            self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
            time.sleep(0.5)
            if self.candy_hunter:
                self.candy_hunter.check_all(after_scroll)
            
            # Цикловая задержка (как в оригинале)
            cycle_elapsed = time.time() - cycle_start
            if cycle_elapsed < 5:
                time.sleep(5 - cycle_elapsed)
        print(f'🔍 Waiting 10 s...')
        end_time = time.time() + 10
        while time.time() < end_time:
            time.sleep(1)
            if self.candy_hunter:
                self.candy_hunter.check_all(after_scroll)
        print('✅ Scanning complete')
    
    def _mode_2(self, duration: int, after_scroll: int):
        start = time.time()
        print(f'📜 Mode 2 scrolling for {duration}s')
        
        while time.time() - start < duration:
            self.driver.execute_script("window.scrollBy({top: 300, behavior: 'smooth'})")
            time.sleep(0.5)
            if self.candy_hunter:
                self.candy_hunter.check_all(after_scroll)
        print(f'🔍 Waiting 10 s...')
        end_time = time.time() + 10
        while time.time() < end_time:
            time.sleep(1)
            if self.candy_hunter:
                self.candy_hunter.check_all(after_scroll)
        print('✅ Scanning complete')