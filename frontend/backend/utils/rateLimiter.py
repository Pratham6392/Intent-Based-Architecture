import time
from collections import deque

class RateLimiter:
    def __init__(self, requests_per_second=10):
        self.requests_per_second = requests_per_second
        self.requests = deque()
        
    def allow_request(self) -> bool:
        current_time = time.time()
        
        # Remove requests older than 1 second
        while self.requests and current_time - self.requests[0] >= 1:
            self.requests.popleft()
            
        # Check if we're under the rate limit
        if len(self.requests) < self.requests_per_second:
            self.requests.append(current_time)
            return True
            
        return False