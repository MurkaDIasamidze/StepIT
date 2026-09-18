import time
from functools import wraps

def handle_api_errors(retries=3, delay=1):
    """დეკორატორი API მოთხოვნის შეცდომების მართვისა და Retry ლოგიკისთვის."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        print(f"\n[შეცდომა] API-სთან კავშირი ვერ დამყარდა: {e}")
                        return None
                    time.sleep(delay)
        return wrapper
    return decorator