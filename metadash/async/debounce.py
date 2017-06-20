"""
Some python/flask utils
"""
from threading import Timer
from config import ActiveConfig


def debounce(wait):
    """
    Debouncer, useful for statistic or other frequently updated,
    TODO: Use celery for this
    """
    def decorator(fn):
        # TODO: Corrently, it do nothing.
        def debounced(*args, **kwargs):
            def call_func():
                fn(*args, **kwargs)
            if ActiveConfig.DEBOUNCE_ENABLED:
                raise NotImplementedError()
            else:
                call_func()
        return debounced
    return decorator
