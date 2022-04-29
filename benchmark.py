import time
from functools import wraps


# Reference:
# https://qiita.com/hisatoshi/items/7354c76a4412dffc4fd7
def time_elapsed(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.time()
        result = func(*args, **kargs)
        elapsed = time.time() - start
        print('{:s} function took {:.3f} sec'.format(func.__name__, elapsed))
        return result

    return wrapper
