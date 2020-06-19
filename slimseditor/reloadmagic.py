import functools

try:
    from reloadr import autoreload

except ImportError:
    def autoreload(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper