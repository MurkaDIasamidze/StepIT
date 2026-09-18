"""
decorators.py
Reusable decorators used across the Joke / Quote Daily Collector app.
"""

import functools
import time


def retry(times=3, delay=1, exceptions=(Exception,)):
    """
    Retry a function call a number of times if it raises one of the
    given exceptions, waiting `delay` seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    print(f"[Retry {attempt}/{times}] {func.__name__} failed: {exc}")
                    if attempt < times:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def validate_non_empty(*param_names):
    """
    Ensure the given keyword/positional string arguments are not empty
    or whitespace-only. Raises ValueError otherwise.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for value in list(args) + list(kwargs.values()):
                if isinstance(value, str) and not value.strip():
                    raise ValueError(
                        f"Invalid input for '{func.__name__}': "
                        f"expected non-empty value for {param_names}."
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_result(func):
    """
    Simple in-memory cache keyed by the function's arguments.
    Useful for endpoints that rarely change (e.g. category list).
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            print(f"[Cache] Using cached result for {func.__name__}()")
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    wrapper.clear_cache = cache.clear
    return wrapper