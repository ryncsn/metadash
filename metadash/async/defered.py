"""
Some python/flask utils
"""
from config import ActiveConfig
from typing import Callable


def defered(fn: Callable) -> Callable:
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
    # TODO: Break recursion: A defered return a defered that returns a defered that r..(repeat)
    # TODO: use a defered class, so can set __getattr__ on defered, so we can have a defered loop.
    def op(*args, **kwargs):
        if ActiveConfig.DEFERED_ENABLE:
            entity = args[0]
            if not entity.uuid:
                raise RuntimeError("@defered can only be used with entity with valid uuid")
            raise NotImplementedError()
        else:
            return fn(*args, **kwargs)
    return op
