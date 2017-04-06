"""
Some python/flask utils
"""
from threading import Timer

def debounce(wait):
    """
    Decouncer, useful for statistic or other frequently updated
    data, which the later one will override former one.
    """
    def decorator(fn):
        # TODO: Corrently, it do nothing.
        def debounced(*args, **kwargs):
            def call_func():
                fn(*args, **kwargs)
            # TODO: use celery?
            call_func()
        return debounced
    return decorator
