from datetime import datetime
from typing import List

class StatsCollector:
    def __init__(self):
        self.candy_times: List[datetime] = []
        self.candy_count: int = 0
        self.pumpkin_count: int = 0
        self.start_time: datetime = None
    
    def start(self):
        self.start_time = datetime.now()
    
    def record_candy(self, candy_type: str):
        now = datetime.now()
        self.candy_times.append(now)
        
        if candy_type == "pumpkin":
            self.pumpkin_count += 1
            self.candy_count += 3
            print(f"🎃 Pumpkin found! +3 candies (total: {self.candy_count})")
        else:
            self.candy_count += 1
            print(f"🍬 Candy found! (total: {self.candy_count})")
        
        if len(self.candy_times) % 5 == 0:
            self.print_stats()
    
    def print_stats(self):
        if len(self.candy_times) < 2:
            return
        
        total = (self.candy_times[-1] - self.candy_times[0]).total_seconds()
        avg = total / (len(self.candy_times) - 1)
        print(f"📊 Stats: {self.candy_count} candies ({self.pumpkin_count} pumpkins), avg: {avg:.1f}s")
    
    def print_final(self):
        end_time = datetime.now()
        
        print("\n" + "="*60)
        print("🎯 FINAL STATISTICS")
        print("="*60)
        
        if self.start_time:
            duration = (end_time - self.start_time).total_seconds()
            print(f"⏱️ Total time: {int(duration)}s")
        
        print(f"🍬 Candies: {self.candy_count - self.pumpkin_count * 3}")
        print(f"🎃 Pumpkins: {self.pumpkin_count}")
        print(f"💎 Total: {self.candy_count}")
        print("="*60)