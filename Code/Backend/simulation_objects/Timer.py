import time
from functools import wraps

def functimer_perturn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        runtime = end-start
        totaltime = runtime * 22000
        if totaltime > 1:
            print(f"{func.__name__} would add {totaltime} seconds")
        #print(f"Finished {func.__name__} in {end - start:.4f} seconds.")
        return result
    return wrapper

def functimer_once(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        runtime = end-start
        print(f"{func.__name__} took {runtime} seconds ({runtime/60} minutes)")
        #print(f"Finished {func.__name__} in {end - start:.4f} seconds.")
        return result
    return wrapper