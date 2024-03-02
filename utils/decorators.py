import time
import logging

logger = logging.getLogger('console')

def calculate_time_process(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} Time process was {execution_time} seconds.")
        return result
    return wrapper
