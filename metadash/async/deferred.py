"""
Some python/flask utils
"""
from typing import Callable
from concurrent.futures import ThreadPoolExecutor


# In case of using socket io for dispatching deferred result:
# Using ThreadPoolExecutor and a thread shared variable for single worker shoule be fine
# As the client requesting the deferred resource and the client waiting for the required
# resource is handled by the same thread
# clients = {}
executor = ThreadPoolExecutor(2)


def runner_wrapper(fn: Callable, cb):
    result = fn()
    cb(result)
    return result


def deferred(fn: Callable) -> Callable:
    """
    Return "loading..." when called, and queue actuall operation,
    will push actual result using a connection when it's ready.

    Could apply this on any *function*, a model's function property or a
    extending class's __get__ or things like that, as long as their first
    arguement have a uuid attribute, which should be just like it using
    with EntityModel or providing and extending model.
    When applied to a property with @propery, have to apply before @property
    If not, it can track which the return value belongs to.
    """
    # TODO: Break recursion: A deferred return a deferred that returns a deferred that r..(repeat)
    # TODO: use a deferred class, so can set __getattr__ on deferred, so we can have a deferred loop.
    def op(*args, **kwargs):
        entity = args[0]
        if not entity.uuid:
            raise RuntimeError("@deferred can only be used with entity with valid uuid")
        future = executor.submit(fn, *args, **kwargs)
        return future
    return op
