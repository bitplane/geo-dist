from functools import wraps
from time import time


def format_int(num):
    if num < 1000:
        return f"{num:.2f}"
    magnitude = 0
    while abs(num) >= 1000 and magnitude < 5:
        magnitude += 1
        num /= 1000
    return f"{num:.2f}{['', 'k', 'M', 'G', 'T'][magnitude]}"


def print_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = f(*args, **kwargs)
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"{f.__name__} took {elapsed_time:.6f} seconds")
        return result

    return wrapper
