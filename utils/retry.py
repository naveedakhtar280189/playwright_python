import pytest
import logging

logger = logging.getLogger("retry")

def retry_on_failure(retries=2):
    """
    Decorator to retry a test on failure up to `retries` times.
    Use on individual test methods.
    """
    def decorator_retry(test_func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 2):  # +1 for original run
                try:
                    return test_func(*args, **kwargs)
                except AssertionError as e:
                    if attempt <= retries:
                        logger.warning(f"Retrying {test_func.__name__} (Attempt {attempt}/{retries + 1})")
                    else:
                        logger.error(f"{test_func.__name__} failed after {retries + 1} attempts")
                        raise
        return wrapper
    return decorator_retry

""" 
from retry import retry_on_failure

@retry_on_failure(retries=2)
def test_login():
    assert 1 == 2  # 

@pytest.mark.retry_count(3)
def test_checkout():
    assert False
    """
