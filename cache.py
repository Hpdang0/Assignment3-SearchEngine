class Cache():
    def __init__(self, size = 5):
        self._max_size = size
        self._queue = list()
    
    def append(self, element):
        if len(self._queue) >= self._max_size:
            self._queue.pop(0)
        self._queue.append(element)

    def __str__(self):
        return str(self._queue)

    def __repr__(self):
        return "Cache({})".format(self._max_size)

    def __iter__(self):
        self.current = -1
        return self

    def __next__(self):
        self.current += 1
        if self.current < len(self._queue):
            return self._queue[self.current]
        raise StopIteration