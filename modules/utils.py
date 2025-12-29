import time

def wait_fixed(seconds: float = 5.0):
    if seconds > 0:
        time.sleep(seconds)

def retry_on_timeout(func, max_attempts: int = 3, delay: int = 5):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1 and ("timed out" in str(e) or "TimeoutException" in str(e)):
                time.sleep(delay)
                continue
            raise
    return None