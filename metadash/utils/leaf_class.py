"""
Consider class inherits like a tree, follow helper help you
to iterate through its leaf
"""


def all_leaf(cls):
    subs = cls.__subclasses__()
    return sum([all_leaf(cls) for cls in subs], []) if subs else [cls]


def all_leaf_class(cls):
    if cls.__subclasses__():
        return all_leaf(cls)
    return []
