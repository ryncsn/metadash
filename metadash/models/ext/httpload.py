import requests


class ChunkLoader(object):
    """
    A Helper to lazy load data, and save memory when iterating through
    a huge list from paginified http api.

    Special case is when __len__ is called, the default implement is
    raise AttributeError.
    """
    #TODO: weakref to reduce mem use
    def __init__(self, data="data", method="GET", chunk=100,
                 requester=None, breaker=None, length_key=None):

        self._page = 0
        self._list = []
        self._stop = False
        self._data = False
        self.length_key = length_key or 'count'
        self.chunk = chunk

        if method == "GET":
            self.requester = requester or (lambda *args, **kws: requests.get(*args, **kws).json())
        elif method == "POST":
            self.requester = requester or (lambda *args, **kws: requests.post(*args, **kws).json())

        self.breaker = breaker or (lambda res: not res[data])

    def _load(self, position=0):
        while position >= len(self._list) and not self._stop:
            res = self.requester(url=self.url, chunk=self.chunk, page=self._page)
            data = res[self.data]
            if self.breaker(data):
                break

        raise IndexError()

    def __getitem__(self, index):

        self._list(index)
        return self._nonlazy[index]

    def __delitem__(self, index):
        self._delazify(index)
        del self._nonlazy[index]

    def __iter__(self):
        yield from self._list
        for value in self._lazy:
            self._nonlazy.append(value)
            yield value
